#!/usr/bin/env python3
# ec.py
# KRY Project 2 - Find private key to PUBLIC key
# Michal Ormos (xormos00)
# xormos00@stud.fit.vutbr.cz
# April 2019

import sys

FP = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
A = -0x3
B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
P = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
PUBLIC = (0x52910a011565810be90d03a299cb55851bab33236b7459b21db82b9f5c1874fe,
0xe3d03339f660528d511c2b1865bcdfd105490ffc4c597233dd2b2504ca42a562)

"""
calculateInverseElement
"""
def calculateInverseElement(element):
    return pow(element, FP-2, FP)

"""
ECSumTwoPoints    
    - sum of two point on elyptical curve
"""
def ECSumTwoPoints(pointA, pointB):
    (xp,yp) = pointA
    (xq,yq) = pointB
    l = ((yq - yp) * calculateInverseElement(xq - xp)) % FP
    xr = (l * l - xp - xq) % FP
    yr = (l * (xp - xr) - yp) % FP
    return (xr,yr)

"""
ECMultiplyPoint
"""
def ECMultiplyPoint(point):
    (xp,yp) = point
    l = ((3 * xp * xp + A) * calculateInverseElement(2 * yp)) % FP
    xr = (l * l - 2 * xp) % FP
    yr = (l * (xp - xr) - yp) % FP
    return (xr,yr)

"""
findPrivateKey
"""
def findPrivateKey():
    if(P == PUBLIC):
        return 1
    i = 2
    i_times_P = ECMultiplyPoint(P)

    if(i_times_P == PUBLIC):
        return i

    while i_times_P != PUBLIC and i<100:
        i = i + 1
        i_times_P = ECSumTwoPoints(P, i_times_P)
    return i

"""
Main
    - process arguments from Makefile
    - parse input to desired Tuple and convert to int
"""
if __name__ == '__main__':
    try:
        PUBLIC_KEY = sys.argv[1]
        first_key = PUBLIC_KEY.split(',')[0]
        first_key = (first_key[1:])
        second_key = PUBLIC_KEY.split(',')[1]
        second_key = (second_key[:-1])        
        PUBLIC = (int(first_key), int(second_key))
    except:
        pass    
    print(findPrivateKey())
