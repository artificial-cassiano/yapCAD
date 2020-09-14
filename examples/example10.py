## yapCAD 3D geometry example

print("example10.py -- yapCAD inside-outside testing demonstration")
print("""
In this example, we create different types of yapCAD geometry and
randomly gemerate test ponts.  Test points that fall inside are
rendered as aqua crosses, points that fall outside are rendered as red
crosses.

This demo also allows you to choose the rendering back-end from the
command line""")

from yapcad.geom import *
import random

def randomPoints(bbox,numpoints):
    points = []
    minx = bbox[0][0]
    maxx = bbox[1][0]
    miny = bbox[0][1]
    maxy = bbox[1][1]
    rangex = maxx-minx
    rangey = maxy-miny
    for i in range(numpoints):
        points.append(point(random.random()*rangex+minx,
                            random.random()*rangey+miny))
    return points

def pointInBox(bbox,r):
    minx = bbox[0][0]+r
    maxx = bbox[1][0]-r
    miny = bbox[0][1]+r
    maxy = bbox[1][1]-r
    rangex = maxx-minx
    rangey = maxy-miny
    x = point(random.random()*rangex+minx,
              random.random()*rangey+miny)
    return x


def randomArc(bbox,minr=0.0,maxr=10.0,circle=False):
    radr = maxr-minr
    r = random.random()*radr+minr
    start = 0
    end = 360
    if not circle:
        start = random.random()*360.0
        end = start + random.random()*360.0

    x = pointInBox(bbox,r)
    return arc(x,r,start,end)

def randomPoly(bbox,numpoints=10,minr = 1.0,maxr = 10.0):
    angles = []
    rads = []
    ang = 0.0
    rr = maxr-minr
    for i in range(numpoints):
        a = random.random()
        angles.append(ang)
        ang = ang + a
        # print("a: ",a," ang: ",ang)
        rads.append(random.random()*rr+minr)

    sf = pi2/ang

    points = []
    x = pointInBox(bbox,maxr)
    
    for i in range(numpoints):
        p = [cos(angles[i]*sf)*rads[i],
             sin(angles[i]*sf)*rads[i],0,1]
        points.append(add(p,x))

    return points + [ points[0] ]

def randomGeometry(bbox, numarcs, numcircles, numpolys):
    geom=[]
    for i in range(numarcs):
        geom.append(randomArc(bbox,minr = 5,maxr=10))

    for i in range(numcircles):
        geom.append(randomArc(bbox,minr = 3, maxr=10,circle=True))

    for i in range(numpolys):
        geom.append(randomPoly(bbox,numpoints=round(random.random()*7+3),
                               maxr =10))
    return geom

def drawGeom(dd,geom):
    for g in geom:
        if isarc(g) and not iscircle(g):
            ## draw the piza slice
            dd.draw(g)
            dd.draw(line(sample(g,1.0),
                         g[0]))
            dd.draw(line(g[0],
                         sample(g,0.0)))
        else:
            dd.draw(g)

def testPoints(points,geom):
    inpts=[]
    outpts=[]

    for p in points:
        ins = False
        for g in geom:
            if inside(g,p):
                inpts.append(p)
                ins = True
                continue
        if not ins:
            outpts.append(p)
    return inpts, outpts

def testAndDraw(dd):
    dd.set_linecolor('white')

    ## this is the bounding box for our test area
    bbox = line([-60,-60,0,1],[60,60,0,1])

    ## make 2,000 points
    tps = randomPoints(bbox,2000)

    ## make 20 random arcs, 20 random circles, and 20 random polys.
    glist = randomGeometry(bbox,20,20,20)

    ## test the list of points, sort in to inside points and outside
    ## points
    inpts,outpts = testPoints(tps,glist)

    ## draw the test geometry -- we are using a special draw function
    ## that will render arcs as "pizza slices."
    drawGeom(dd,glist)

    ## Draw the points.
    dd.polystyle='points'

    dd.set_linecolor('aqua')
    dd.pointstyle = 'x'
    dd.draw(inpts)

    dd.set_linecolor('red')
    dd.pointstyle = 'x'
    dd.draw(outpts)
    dd.display()
    
if __name__ == "__main__":
    import sys
    renderOgl = False
    filename="example10-out"
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