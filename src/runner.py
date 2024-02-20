#!/usr/bin/python3
import flatbuffers
import sys
import argparse
import torch
#!/usr/bin/python3
import flatbuffers
import sys
import argparse
import torch

sys.path.append("./converters")
sys.path.append("./generators")
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
from DataGenerator import _hidden_dataset_unpacker,_hidden_matrix1_unpacker,build_data_set

sys.path.append("./res")
from inspector import *

def concatenator(filenames):
    dsarr = [_hidden_dataset_unpacker(filenames[0])]
    imarr = []
    imarr.extend([_hidden_matrix1_unpacker(f) for f in filenames])
    params = ParametersT.InitFromObj(dsarr[0].Params())
    ds_t = build_data_set(imarr, params,2,0)
    builder = flatbuffers.Builder(1024)
    sb = DataSetT.Pack(ds_t, builder)
    builder.Finish(sb)
    sb = builder.Output()
    f = open(f"conc_synt_dataset.fbs", "wb")
    f.write(sb)
    f.close()

concatenator([
  f"images_{i}.fbs" for i in range(2)
])