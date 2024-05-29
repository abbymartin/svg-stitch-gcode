from svgpathtools import Path, Line, svg2paths, disvg, wsvg

paths, attributes = svg2paths('test.svg')
p = paths[0]

num_segs = 10
offset_dist = -10

nls = []

#change to make all segments equal LINEAR distance apart?
for curve in p:
    for i in range(num_segs):
        loc = i/num_segs
        offset_vector = offset_dist * curve.normal(loc)
        nl = Line(curve.point(loc), curve.point(loc) + offset_vector)
        nls.append(nl)
    connect_the_dots = [Line(nls[k].end, nls[k+1].end) for k in range(len(nls)-1)]
    if p.isclosed():
        connect_the_dots.append(Line(nls[-1].end, nls[0].end))
    offset_path = Path(*connect_the_dots)    
    print(offset_path)
    disvg([p, offset_path])

