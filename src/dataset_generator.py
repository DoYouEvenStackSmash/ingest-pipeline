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

default_params = {
  "amplitude": [
    0.1
  ],
  "defocus": [
    0.0
  ],
  "b_factor": [
    1.0
  ],
  "img_dims": [
    2.0,
    1.0
  ],
  "num_pixels": [
    128.0
  ],
  "pixel_width": [
    0.3
  ],
  "sigma": [
    1.0
  ],
  "elecwavel": [
    0.019866
  ],
  "snr": [
    1.0
  ],
  "experiment_parameters": [
    25.0,
    25.5
  ],
  "seed": [
    28.0,
    28.5
  ],
  "structures": [
    31.0,
    31.5
  ],
  "coordinates": [
    34.0,
    34.5
  ]
}

def generate_tensor_pairs(num_points, dims):
    torch.manual_seed(50)
    tensors_list = [[torch.rand(dims),torch.tensor(1)] for _ in range(num_points)]
    return tensors_list

def generate_datumT(tensor_pairs):
  datumT_arr = []
  for mat1,mat2 in tensor_pairs:
    matT_val = [mat_to_matrixT(mat1), mat_to_matrixT(mat2)]
    datumT_val = matrixT_pair_to_datumT(matT_val)
    datumT_arr.append(datumT_val)
    
  return datumT_arr

def serialize_datumT(paramsT, datumT_list, output):
    dst = DataSetT()
    dst.params = paramsT
    dst.data = datumT_list
    
    builder = flatbuffers.Builder(1024)
    sb = DataSetT.Pack(dst, builder)
    sb = builder.Finish(sb)

    f = open(output, "wb")
    f.write(builder.Output())
    f.close()
  
def main():
    parser = argparse.ArgumentParser(description="Generate tensors with random values.")

    parser.add_argument(
        "-n",
        "--num_points",
        type=int,
        default=100,
        help="Number of data points to generate (default: 100)",
    )

    parser.add_argument(
        "-d",
        "--dims",
        nargs="+",
        type=int,
        default=[2, 1],
        help="Dimensions of data as a list, e.g., -d 2 1 (default: [2, 1])",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.fbs",
        help="Output filename for the generated tensors (default: output.txt)",
    )
    args = parser.parse_args()

    
    dst = DataSetT()
    
    num_points = args.num_points
    default_params["img_dims"] = args.dims
    toup = lambda a : ''.join([a.split("_")[0],''.join([f'{i[0].upper()}{i[1:]}' for i in a.split("_")[1:]])])
    po = ParametersT()
    for k, v in default_params.items():
      setattr(po,toup(k),v)
    
    dims = tuple(args.dims)
    tensors_list = generate_tensor_pairs(num_points, dims)
    datumT_list = generate_datumT(tensors_list)
    
    serialize_datumT(po,datumT_list, args.output)
    
    
    
if __name__ == '__main__':
  main()