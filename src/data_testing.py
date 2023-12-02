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


from datum_helpers import *
# flatbuffer
exp_fb = dl.load_flatbuffer("exp.bin")
# dataset buffer
exp_buf = DataSet.GetRootAsDataSet(exp_fb,0)

### option 1: datum_buf->datum-[lift]->mats
# list of datum_buf
datum_buf = extract_datum(exp_buf)
# param_buf
param_buf = extract_params(exp_buf)
# numpy array of image dimensions
dims = extract_image_dims(param_buf)
# list of pairs of torch tensors with dimensions according to dims
mats = [extract_matrices_from_buf(datum_buf[j], [int(i) for i in dims]) for j in range(len(datum_buf))]


### option 2: datum_buf-[lift]->datumT->mats
datumT_list = lift_datum_buf_to_datumT(datum_buf, param_buf)
matsT = [extract_matrices_from_datumT(datumT_list[j]) for j in range(len(datumT_list))]

for i,m in enumerate(matsT):
  print(f"{mats[i]}\t\n{m}")

### at this point mats == matsT

datum_arr = []
for m in mats:
  # construct matrixT objects from torch tensors
  matrixT1 = mat_to_matrixT(m[0])
  matrixT2 = mat_to_matrixT(m[1])
  
  # construct datumT object from pair of matrixT objects
  datumT = matrixT_pair_to_datumT([matrixT1, matrixT2])
  
  datum_arr.append(datumT)

# for d in datum_arr:
#   print(d.m1)
#   print(d.m2)
  
