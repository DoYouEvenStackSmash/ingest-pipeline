#!/usr/bin/python3
import flatbuffers
import sys
import argparse
import torch

sys.path.append("./converters")
sys.path.append("./generators")
sys.path.append("../")
from DataModel.Atom import Atom, AtomT
from DataModel.Structure import Structure, StructureT
from DataModel.Quaternion import Quaternion, QuaternionT
from DataModel.P import P, PT
from DataModel.AtomicModel import *
from DataModel.Parameters import Parameters, ParametersT

from DataModel.DataClass import DataClass
from DataModel.Datum import Datum, DatumT
from DataModel.Matrix import Matrix, MatrixT
from DataModel.Domain import Domain
from DataModel.DataType import DataType
from DataModel.DataSet import DataSet, DataSetT
from filegroup import *
from transform_generator import *
from ctf_generator import *
from image_generator import *
from dataloader import Dataloader as dl
import matplotlib.pyplot as plt

def get_stats(buf):
  """Get status of flatbuffer dataset

  Args:
      buf (_type_): _description_
  """
  stats_dict = {"num_elems": 0, "elem_types": {"m1": None, "m2": None}}
  ds = DataSet.GetRootAsDataSet(buf,0)
  
  stats_dict["num_elems"] = ds.DataLength()
  
  check_type = lambda matrix: None if matrix == None else matrix.DataType()
  get_type = lambda datum: [check_type(datum.M1()),check_type(datum.M2())]
  stats_dict["elem_type"]["m1"],stats_dict["elem_type"]["m2"] = get_type(ds.Data(0))
  
  return stats_dict 
  

def extract_datum(dataset_buf):
  """Helper function for extracting the list of datum from the dataset buf

  Args:
      dataset_buf (flatbuffer): bytearray contining the dataset

  Returns:
      list of data bytearrays
  """
  return [dataset_buf.Data(j) for j in range(dataset_buf.DataLength())]

def extract_params(dataset_buf):
  """Helper function for extracting params

  Args:
      dataset_buf (flatbuffer): bytearray contining the dataset

  Returns:
      Parameters bytearray
  """
  return dataset_buf.Params()

def extract_image_dims(params_buf):
  """Extractor for image dimensions as a numpy array

  Args:
      params_buf (flatbuffer): bytearray containing parameters

  Returns:
      numpy array containing [x,y,...] dimensions
  """
  return params_buf.ImgDimsAsNumpy()

def assemble_matrix(matrix_buf,dims):
  """Helper function for building a matrix tensor from a matrix buf

  Args:
      matrix_buf (list of flatbuffers): list of Matrix bytearrays

  Returns:
      torch tensor: a torch tensor of shape (TODO shape)
  """
  get_complex_pixels = lambda rp, ip: rp + 1j * ip
  return torch.tensor(
        np.array(
            [
                get_complex_pixels(
                    matrix_buf.RealPixelsAsNumpy(), matrix_buf.ImagPixelsAsNumpy()
                ).reshape((dims[0], dims[1]))
            ]
        )
    )
  
def extract_matrices_from_buf(datum_buf, dims):
  """Helper function for extracting matrices from a datum buffer

  Args:
      datum_buf (list of flatbuffers): list of bytearrays of Datum objecs

  Returns:
      [tensor, tensor]: pair of tensors of type=complex 
  """
  mat1 = assemble_matrix(datum_buf.M1(), dims)
  mat2 = torch.tensor(1) if datum_buf.M2() == None else assemble_matrix(datum_buf.M2(),dims)
  return [mat1,mat2]

def extract_matrices_from_datumT(datumT):
  """Helper function for extracting matrices from a datumT

  Args:
      datumT (DatumT): DatumT object

  Returns:
      [tensor, tensor]: pair of tensors of type=complex 
  """
  shape = [int(i) for i in datumT.m1.shape]
  print(shape)
  mat1 = datumT.m1
  mat2 = torch.tensor(1) if datumT.m2 == None else datumT.m2
  return [mat1,mat2]
  
def lift_datum_buf_to_datumT(datum_buf,params_buf):
  """helper function for lifting the datum buffer into objects

  Args:
      datum_buf (flatbuffer): a list of Datum flatbuffers

  Returns:
      datum_list (list of DatumT): a list of DatumT objects
  """
  dims = [int(i) for i in extract_image_dims(params_buf)]
  datum_list = []
  for datum_idx, datum in enumerate(datum_buf):
    data_t = DatumT()
    data_t.m1,data_t.m2 = extract_matrices_from_buf(datum,dims)
    datum_list.append(data_t)
  return datum_list

def apply_d1m2_to_d2m1(D1,D2):
  """Function for in-situ modulation of D2.m1 tensor

  Args:
      D1 (DatumT): DatumT acting as a modifier
      D2 (DatumT): DatumT to be modified

  Returns:
      tensor: result of multiply_matrices
  """
  return multiply_matrices([D2.m1,D1.m2])

def multiply_matrices(mat_pair):
  """helper function for multiplying matrices in the synthesis fashion

  Args:
      mat_pair (list of tensors): a pair of tensors

  Returns:
      tensor: element-wise product of the pair of tensors
  """
  if not len(mat_pair[1].shape):
    return mat_pair[0] * mat_pair[1]
  return torch.matmul(mat_pair[0], mat_pair[1])
  
def complex_tensor_to_components(complex_tensor):
  """Turns a complex tensor into two arrays of serializable floats

  Args:
      complex_tensor (_type_): a tensor containing complex numbers

  Returns:
      realPixels, imagPixels: list of torch tensors which can be added to yield complex
      numbers in rectangular form
  """
  realPixels = None
  imagPixels = None
  complex_tensor = complex_tensor.reshape(-1, 1)
  realPixels = [torch.real(val) for val in complex_tensor]
  if type(complex_tensor[0]) == complex:
      imagPixels = [torch.imag(val) for val in complex_tensor]
  else:
      imagPixels = [torch.zeros(1) for _ in complex_tensor]
  
  return realPixels, imagPixels
      
def mat_to_matrixT(mat, datatype=0,dataspace=0):
  """ Create a MatrixT object from a torch tensor

  Args:
      mat_pair (list of torch tensors containing complex numbers): _description_
  """
  
  if torch.equal(mat,torch.tensor(1)):
    return None

  mT = MatrixT()
  mT.realPixels, mT.imagPixels = complex_tensor_to_components(mat)
  mT.dataType = datatype
  mT.dataSpace = dataspace
  return mT

def matrixT_pair_to_datumT(mat_pair):
  """Create a DatumT object from a pair of MatrixT objects

  Args:
      mat_pair (list of matrixT objects): _description_

  Returns:
      DatumT: DatumT object
  """
  dt = DatumT()
  dt.m1 = mat_pair[0]
  dt.m2 = mat_pair[1]
  return dt
