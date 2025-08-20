#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Given coordinates for points A and B and a pair of constraining points P1 and P2, this script constructs a trapezium
ABCD with internal angles ∠A = ∠B = 3*pi/4, and ∠C = ∠D = pi/4, respectively.

Created on Tue Aug 19 23:50:47 2025

@author: dash-dot
"""

import numpy
import matplotlib.pyplot as plt
import sys


def project_a_onto_b(a: numpy.array, b: numpy.array) -> numpy.array:
    """Calculates the projection of vector a onto b."""
    return (a.dot(b) / b.dot(b)) * b

def rotate_vector(vector: numpy.array, angle: float) -> numpy.array:
    rotation_matrix = numpy.array([[numpy.cos(angle), -numpy.sin(angle)],
                                   [numpy.sin(angle),  numpy.cos(angle)]])
    # Numpy and other modules perform matrix multiplication using the '@' operator
    return rotation_matrix @ vector

def main(args):
    xA = float(args[0])
    yA = float(args[1])
    xB = float(args[2])
    yB = float(args[3])
    xP1 = float(args[4])
    yP1 = float(args[5])
    xP2 = float(args[6])
    yP2 = float(args[7])
    
    # Define the position vectors rA, rB, rP1 and rP2 for points A, B, P1 and P2, respectively
    rA = numpy.array([xA, yA])
    rB = numpy.array([xB, yB])
    rP1 = numpy.array([xP1, yP1])
    rP2 = numpy.array([xP2, yP2])

    # Rudimentary error handling/avoidance: rotate all vectors by an arbitrary angle to avoid singularities
    rA = rotate_vector(rA, numpy.exp(1))
    rB = rotate_vector(rB, numpy.exp(1))
    rP1 = rotate_vector(rP1, numpy.exp(1))
    rP2 = rotate_vector(rP2, numpy.exp(1))

    rAB = rB - rA
    rAP1 = rP1 - rA
    rAP2 = rP2 - rA

    # Now compute the orthogonal vectors pointing between the parallel lines
    d1 = rAP1 - project_a_onto_b(rAP1, rAB)
    d2 = rAP2 - project_a_onto_b(rAP2, rAB)
    # Select the longer of the two vectors (a vector dotted with itself is its norm squared)
    if d1.dot(d1) > d2.dot(d2):
        rP = rP1
        d = d1
    else:
        rP = rP2
        d = d2
    # Use the 2-argument arctangent to compute the correct angle in the interval (-pi, pi]
    angle = numpy.arctan2(d[1], d[0])
    # Slope when the subtended angle is 3*pi/4
    mA = (1 + numpy.tan(angle)) / (1 - numpy.tan(angle))
    # The non-parallel sides of the trapezium are mutually orthogonal, and so:
    mB = -1 / mA
    mAB = (rB[1] - rA[1]) / (rB[0] - rA[0])
    # Solve for point D, which should (normally) be adjacent to A
    xD = (rP[1] - rA[1] + mA*rA[0] - mAB*rP[0]) / (mA - mAB)
    yD = mAB*(xD - rP[0]) + rP[1]
    rD = numpy.array([xD, yD])
    # Solve for point C, which should (normally) be adjacent to B
    xC = (rP[1] - rB[1] + mB*rB[0] - mAB*rP[0]) / (mB - mAB)
    yC = mAB*(xC - rP[0]) + rP[1]
    rC = numpy.array([xC, yC])
    
    # Now rotate items back into place before plotting
    rC = rotate_vector(rC, -numpy.exp(1))
    rD = rotate_vector(rD, -numpy.exp(1))
    
    print('\nSpecifications:')
    print(f'Point A:  ({xA}, {yA}), point B:  ({xB}, {yB})')
    print(f'Point P1: ({xP1}, {yP1}), point P2: ({xP2}, {yP2})\n')
    print(f'Point C is: ({rC[0]}, {rC[1]}).')
    print(f'Point D is: ({rD[0]}, {rD[1]}).')
    plt.plot([xA, xB], [yA, yB], 'ko-', linewidth=2)
    plt.plot([rC[0], rD[0]], [rC[1], rD[1]], 'ro-', linewidth=2)
    plt.plot([xA, rD[0]], [yA, rD[1]], 'g-', linewidth=2)
    plt.plot([xB, rC[0]], [yB, rC[1]], 'g-', linewidth=2)
    plt.plot([xP1, xP2], [yP1, yP2], 'ko--', linewidth=2)
    # Equal scaling of the axes is critical for depicting the angles correctly without distortion!
    plt.axis('equal')
    plt.show()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 8:
        print("\nIncorrect number of arguments. 8 values expected, all separated by spaces.\n")
        print('Usage:\n    python construct_trapezium.py xA yA xB yB xP1 yP1 xP2 yP2')
        print(__doc__)
        sys.exit()
    else:
        main(args)