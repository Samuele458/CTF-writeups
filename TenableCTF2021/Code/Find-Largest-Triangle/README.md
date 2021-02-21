# Find Largest Triangle
Challenge description:
> Below is some starter code that reads in 3D points (x,y,z) from stdin
> and calls **FindLargestTriangleArea**. You just need to impliment the
> "**FindLargestTriangleArea**" function. This function should find the
> largest triangle area (2D) you can make using any three points. The
> function simply takes a list of 3D points and returns the area of the
> largest triangle found. The code then prints that result **rounded to
> the nearest whole number**.
> ```
> # points is a list of 3D points
> # ie: [[2, 9, -15], [0, 33, -20], ...] def FindLargestTriangleArea(points):   # return largest area
> 
> # Reading space delimited points from stdin
> # and building list of 3D points points_data = raw_input() points = [] for point in points_data.split(' '):   point_xyz = point.split(',')  
> points.append([int(point_xyz[0]), int(point_xyz[1]),
> int(point_xyz[2])])
> 
> # Compute Largest Triangle and Print Area rounded to nearest whole number area = FindLargestTriangleArea(points) print int(round(area))
> 
> ```
> 
> stdin example:
> 
> ```
> -21,59,-93 -4,91,-2 1,61,2, 0,44,1
> ```
> 
> stdout example:
> 
> ``` 
> 2241
> ```


## Solution
```
$  python2 script.py
-21,59,-93 -4,91,-2 1,61,2, 0,44,1
2241
```

### How to solve the problem

In order to solve this problem, we have just to:

- group the points three by three (combinations)
- define a function for calculating distance between two points, so for calculating sides of triangles.
- define a function for calculating the area of a triangle
- calculate the area of every possible triangle, and return the max value

