import math
from itertools import combinations 

def distance( p1, p2 ):
    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2 )

def area( A, B, C ):
    AB = distance(A,B)
    BC = distance(B,C)
    AC = distance(A,C)
    p = ( AB + BC + AC ) / 2
    return math.sqrt( p * (p-AB) * (p-AC) * (p-BC))


# points is a list of 3D points
# ie: [[2, 9, -15], [0, 33, -20], ...]
def FindLargestTriangleArea(points):
    triangles = combinations( points, 3 )
    areas = []
    for triangle in triangles:
        areas.append(area(triangle[0],triangle[1],triangle[2]))
    return max(areas)
  # return largest area

# Reading space delimited points from stdin
# and building list of 3D points
points_data = raw_input()
points = []
for point in points_data.split(' '):
  point_xyz = point.split(',')
  points.append([int(point_xyz[0]), int(point_xyz[1]), int(point_xyz[2])])

# Compute Largest Triangle and Print Area rounded to nearest whole number
area = FindLargestTriangleArea(points)

print int(round(area))
