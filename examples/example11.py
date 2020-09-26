## yapCAD boolean operations geometry example

print("example11.py -- yapCAD boolean operations demonstration")
print("""
In this example, we create yapCAD Polygon() geometry generators and
perform boolean operations on them to create combined profiles.

This demo also allows you to choose the rendering back-end from the
command line""")

from yapcad.geom import *
from yapcad.poly import *
from yapcad.combine import *

import math
import random

def geometry():
    p1 = Polygon()
    p1.addArc(arc(point(-5,5),3.0))

    p2 = makeRoundRect(7,6,1)
    p3 = makeRoundRect(7,6,1,point(-10.0,-10.0))
    b = Boolean('union',[p1,p2])

    p4 = Polygon()
    p5 = Polygon()

    x = point(10,-10)
    r = 5
    d=2
    for i in range(8):
        ang = (pi2/8)*i
        p = p4
        if i%2 ==0:
            p = p5
        p.addArc(arc(add(x, point(math.cos(ang)*r,
                                  math.sin(ang)*r)),d))

    b2 = Boolean('union',[p4,p5])
        
    return [p1.geom(),p2.geom(),b.geom(),b2.geom()]
    #return [p1.geom(),p2.geom(),b.geom()]

def testAndDraw(dd):
    dd.set_linecolor('red')

    gl = geometry()

    g1 = gl[0]
    g2 = gl[1]
    g3 = gl[2]
    g4 = gl[3]

#    dd.draw(g1)
#    dd.draw(g2)

    dd.set_linecolor('aqua')

    dd.draw(g3)

    dd.set_linecolor('white')
    for i in range(len(g4)):
        dd.set_linecolor(i%7+1)
        dd.draw(g4[i])
    
    dd.display()
    
if __name__ == "__main__":
    import sys
    renderOgl = False
    filename="example11-out"
    oglarg= ("pyglet","opengl","OpenGL")
    dxfarg= ("ezdxf","dxf","DXF")
    if len(sys.argv) > 1:
        if sys.argv[1] in oglarg:
            renderOgl=True
        elif sys.argv[1] in dxfarg:
            renderOgl=False
        else:
            print("syntax: $ python3 {} <rendertype> [filename]".format(sys.argv[0]))
            print("    where <rendertype> is one of {} for OpenGL".format(oglarg))
            print("    or one of {} for DXF".format(dxfarg))
            print("    For DXF, you can optionally specify [filename].dxf as the output file")
            quit()
    if len(sys.argv) > 2 and renderOgl==False:
        filename = sys.argv[2]+".dxf"
    dd = []
    if renderOgl:
        print("OpenGL rendering selected")
        from yapcad.pyglet_drawable import *
        dd=pygletDraw()
    else:
        print("DXF rendering selected")
        from yapcad.ezdxf_drawable import *
        #set up DXF rendering
        dd=ezdxfDraw()
        dd.saveas(filename)
    print("rendering...")
    testAndDraw(dd)
    print("done")