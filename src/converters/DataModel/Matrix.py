# automatically generated by the FlatBuffers compiler, do not modify

# namespace: DataModel

import flatbuffers
from flatbuffers.compat import import_numpy

np = import_numpy()


# could be an image or a filter
class Matrix(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAsMatrix(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Matrix()
        x.Init(buf, n + offset)
        return x

    # Matrix
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # content of the matrix
    # Matrix
    def RealPixels(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(
                flatbuffers.number_types.Float32Flags,
                a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4),
            )
        return 0

    # Matrix
    def RealPixelsAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Float32Flags, o)
        return 0

    # Matrix
    def RealPixelsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Matrix
    def RealPixelsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # Matrix
    def ImagPixels(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(
                flatbuffers.number_types.Float32Flags,
                a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4),
            )
        return 0

    # Matrix
    def ImagPixelsAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Float32Flags, o)
        return 0

    # Matrix
    def ImagPixelsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Matrix
    def ImagPixelsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # auxiliary in case of image
    # Matrix
    def OrientationId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # peek whether the data is an image or a filter
    # Matrix
    def DataType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # peek whether the data is in real space or frequency space
    # Matrix
    def DataSpace(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # auxiliary in case of image
    # Matrix
    def ParentStructure(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0


def MatrixStart(builder):
    builder.StartObject(6)


def MatrixAddRealPixels(builder, realPixels):
    builder.PrependUOffsetTRelativeSlot(
        0, flatbuffers.number_types.UOffsetTFlags.py_type(realPixels), 0
    )


def MatrixStartRealPixelsVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)


def MatrixAddImagPixels(builder, imagPixels):
    builder.PrependUOffsetTRelativeSlot(
        1, flatbuffers.number_types.UOffsetTFlags.py_type(imagPixels), 0
    )


def MatrixStartImagPixelsVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)


def MatrixAddOrientationId(builder, orientationId):
    builder.PrependInt32Slot(2, orientationId, 0)


def MatrixAddDataType(builder, dataType):
    builder.PrependInt8Slot(3, dataType, 0)


def MatrixAddDataSpace(builder, dataSpace):
    builder.PrependInt8Slot(4, dataSpace, 0)


def MatrixAddParentStructure(builder, parentStructure):
    builder.PrependInt32Slot(5, parentStructure, 0)


def MatrixEnd(builder):
    return builder.EndObject()


try:
    from typing import List
except:
    pass


class MatrixT(object):
    # MatrixT
    def __init__(self):
        self.realPixels = None  # type: List[float]
        self.imagPixels = None  # type: List[float]
        self.orientationId = 0  # type: int
        self.dataType = 0  # type: int
        self.dataSpace = 0  # type: int
        self.parentStructure = 0  # type: int

    @classmethod
    def InitFromBuf(cls, buf, pos):
        matrix = Matrix()
        matrix.Init(buf, pos)
        return cls.InitFromObj(matrix)

    @classmethod
    def InitFromObj(cls, matrix):
        x = MatrixT()
        x._UnPack(matrix)
        return x

    # MatrixT
    def _UnPack(self, matrix):
        if matrix is None:
            return
        if not matrix.RealPixelsIsNone():
            if np is None:
                self.realPixels = []
                for i in range(matrix.RealPixelsLength()):
                    self.realPixels.append(matrix.RealPixels(i))
            else:
                self.realPixels = matrix.RealPixelsAsNumpy()
        if not matrix.ImagPixelsIsNone():
            if np is None:
                self.imagPixels = []
                for i in range(matrix.ImagPixelsLength()):
                    self.imagPixels.append(matrix.ImagPixels(i))
            else:
                self.imagPixels = matrix.ImagPixelsAsNumpy()
        self.orientationId = matrix.OrientationId()
        self.dataType = matrix.DataType()
        self.dataSpace = matrix.DataSpace()
        self.parentStructure = matrix.ParentStructure()

    # MatrixT
    def Pack(self, builder):
        if self.realPixels is not None:
            if np is not None and type(self.realPixels) is np.ndarray:
                realPixels = builder.CreateNumpyVector(self.realPixels)
            else:
                MatrixStartRealPixelsVector(builder, len(self.realPixels))
                for i in reversed(range(len(self.realPixels))):
                    builder.PrependFloat32(self.realPixels[i])
                realPixels = builder.EndVector(len(self.realPixels))
        if self.imagPixels is not None:
            if np is not None and type(self.imagPixels) is np.ndarray:
                imagPixels = builder.CreateNumpyVector(self.imagPixels)
            else:
                MatrixStartImagPixelsVector(builder, len(self.imagPixels))
                for i in reversed(range(len(self.imagPixels))):
                    builder.PrependFloat32(self.imagPixels[i])
                imagPixels = builder.EndVector(len(self.imagPixels))
        MatrixStart(builder)
        if self.realPixels is not None:
            MatrixAddRealPixels(builder, realPixels)
        if self.imagPixels is not None:
            MatrixAddImagPixels(builder, imagPixels)
        MatrixAddOrientationId(builder, self.orientationId)
        MatrixAddDataType(builder, self.dataType)
        MatrixAddDataSpace(builder, self.dataSpace)
        MatrixAddParentStructure(builder, self.parentStructure)
        matrix = MatrixEnd(builder)
        return matrix
