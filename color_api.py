from ctypes import *
import ctypes
from ctypes import wintypes

dll = ctypes.CDLL("magnification.dll")


def SetWarmth(warmval):
    class MAGCOLOREFFECT(ctypes.Structure):
        _fields_ = [("colormatrix", (wintypes.FLOAT*5)*5)]

    one = ctypes.c_float
    zero = ctypes.c_float
    g_val = ctypes.c_float
    b_val = ctypes.c_float

    g_val = 0.6+(warmval/100)*0.4
    b_val = (warmval)/100

    one = 1.0
    zero = 0.0

    g_MagEffectCustom = MAGCOLOREFFECT()

    for i in range(0, 4):
        for j in range(0, 4):
            g_MagEffectCustom.colormatrix[i][j] = zero

    g_MagEffectCustom.colormatrix[0][0] = one
    g_MagEffectCustom.colormatrix[1][1] = g_val
    g_MagEffectCustom.colormatrix[2][2] = b_val
    g_MagEffectCustom.colormatrix[3][3] = one
    g_MagEffectCustom.colormatrix[4][4] = one

    dll.MagInitialize()

    dll.MagSetFullscreenColorEffect(g_MagEffectCustom)


def Reset():
    dll.MagUninitialize()
