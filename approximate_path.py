#converts svgpath to line segments of equal lengths (within given tolerance)

from svgpathtools import svg2paths, disvg
import math

paths, attributes = svg2paths('test.svg')
p = paths[0]
points = []


def calc_distance(a, b):
    return math.sqrt(math.pow(a.real - b.real, 2) + math.pow(a.imag - b.imag, 2))

#fix infinite loop - don't allow segment length too small?
#offset 0 for no offset
def find_next_point(path, start_point, low, high, offset, seg_len, tolerance):
    mid_point = (low + high)/2 #how far along path to test

    test_point = path.point(mid_point) + offset * path.normal(mid_point)

    #calculate error
    linear_dist = calc_distance(start_point, test_point)
    error = abs(seg_len - linear_dist)

    print("error", error)

    if error <= tolerance:
        points.append(test_point) #accept point
        if mid_point <= 0.99: 
            find_next_point(path, path.point(mid_point) + offset * path.normal(mid_point), mid_point, 1, offset, seg_len, tolerance) #find next point
    
    else: #binary search
        if linear_dist > seg_len and mid_point > 0.001:
            find_next_point(path, start_point, low, mid_point, offset, seg_len, tolerance) #try closer point
        elif 1-mid_point > 0.001:
            find_next_point(path, start_point, mid_point, high, offset, seg_len, tolerance) #try further point


#fills with concentric paths
def fill_shape(path, num_layers, seg_len, tolerance):
    for i in range(num_layers):
        points.append(path.point(0) - seg_len*i * p.normal(0))
        find_next_point(path, path.point(0) + -seg_len*i * p.normal(0), 0, 1, -seg_len*i, seg_len, tolerance)


fill_shape(p, 13, 4, 0.05)

disvg(p, nodes=points)
print(points)


