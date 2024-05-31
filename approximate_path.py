#converts svg path to line segments of equal lengths (within given tolerance)

from svgpathtools import svg2paths, disvg
import math

paths, attributes = svg2paths('test.svg')
p = paths[0]
points = []


def find_next_point(path, start, low, high, seg_len, tolerance):
    start_point = path.point(start)
    mid_point = (low + high)/2
    test_point = path.point(mid_point)
    linear_dist = math.sqrt(math.pow(start_point.real - test_point.real, 2) + math.pow(start_point.imag - test_point.imag, 2))
    error = abs(seg_len - linear_dist)/linear_dist
    print("error", error)

    if error <= tolerance:
        points.append(test_point) #accept point
        if mid_point <= 0.95: 
            find_next_point(path, mid_point, mid_point, 1, seg_len, tolerance) #find next point
    
    else: #binary search
        if linear_dist > seg_len:
            find_next_point(path, start, start, mid_point, seg_len, tolerance) #try closer point
        else:
            if 1-mid_point > 0.01:
                find_next_point(path, start, mid_point, high, seg_len, tolerance) #try further point
        

for curve in p:
    points.append(curve.point(0))
    find_next_point(curve, 0, 0, 1, 5, 0.01)

disvg(p, nodes=points)

