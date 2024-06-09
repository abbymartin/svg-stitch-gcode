#converts svgpath_seg to line segments of equal lengths (within given tolerance)

from svgpathtools import svg2paths, disvg
import math

paths, attributes = svg2paths('test.svg')
p = paths[0]
points = []

#can get stuck in infinite loop
#make it work better with multi-curvepath_segs
#fill in shape!

def calc_distance(a, b):
    return math.sqrt(math.pow(a.real - b.real, 2) + math.pow(a.imag - b.imag, 2))

def find_next_point(path, curve_index, start_point, low, high, seg_len, tolerance):
    path_seg = path[curve_index]
    mid_point = (low + high)/2 #how far along path to test
    test_point = path_seg.point(mid_point)

    #calculate error
    linear_dist = calc_distance(start_point, test_point)
    error = abs(seg_len - linear_dist)/linear_dist

    print("error", error)

    if error <= tolerance:
        points.append(test_point) #accept point
        if mid_point <= 0.99: 
            find_next_point(path, curve_index, path_seg.point(mid_point), mid_point, 1, seg_len, tolerance) #find next point
        elif len(path) > curve_index + 1: #try next curve in path
                find_next_point(path, curve_index + 1, start_point, 0, 1, seg_len, tolerance)
    
    else: #binary search
        if linear_dist > seg_len:
            find_next_point(path, curve_index, start_point, low, mid_point, seg_len, tolerance) #try closer point
        else:
            if 1-mid_point > 0.01: #check if distance at end point is far enough
                find_next_point(path, curve_index, start_point, mid_point, high, seg_len, tolerance) #try further point
            elif len(path) > curve_index + 1: #try next curve in path
                find_next_point(path, curve_index + 1, start_point, 0, 1, seg_len, tolerance)
        

find_next_point(p, 0, p[0].point(0), 0, 1, 5, 0.08)
disvg(p, nodes=points)


