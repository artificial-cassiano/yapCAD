## simple object-oriented framework for drawable objects

from geom import *

## Generic drawing functions -- assumed to use current coordinate
## transform and drawing pen (color, line weight, etc.)
 
## function to draw an arc -- wrapper around whatever renderer is used
## p is center in current coordinate system, r is radius, start is
## starting angle in degrees (0.0 is 12 o'clock) proceeding
## counter-clockwise (90.0 is 9 o'clock). angles less than 0 are
## clipped to 0, angles greater than 360.0 are clipped to 360.0.

class Drawable:
    """simple base class for all drawable geometry"""

    ## utility functions for drawing
    ## -----------------------------
    
    ## pure virtual functions -- override for specific rendering
    ## system
    def draw_arc(self,p,r,start,end):
        print("pure virtual draw_arc called: {}, {}, {}, {}".format(p,r,start,end)) 
        return

    def draw_line(self,p1,p2):
        print("pure virtual draw_line called: {}, {}".format(p1,p2))
        return

    ## non-virtual utility drawing functions 
    def draw_circle(self,p,r):
        self.draw_arc(p,r,0.0,360.0)
        return

    ## utility function to draw an "x", centered on point p inside square of
    ## dimension d
    def draw_x(self,p,d):
        hd=d/2
        p1=add(p,[-hd,-hd,0])
        p2=add(p,[hd,hd,0])
        p3=add(p,[-hd,hd,0])
        p4=add(p,[hd,-hd,0])
        self.draw_line(p1,p2)
        self.draw_line(p3,p4)
        return;


    def __repr__(self):
        return 'an abstract, generic drawable object'

    def str(self):
        return self.__repr__()
    
    def print(self):
        print(self.str())

    def draw(self):
        print('abstract draw function called')

    ## function to return a coordinate (point) given a parameter u,
    ## such that 0 <= u <=1 will map to the range of the
    ## drawable. Values of u outside the 0 to 1 range may result in
    ## samples that lie on the unbounded function.
    def sample(self,u):
        return [0.0,0.0]
    
    ## return center of object in object-coordinate space
    def center(self):
        return [0.0,0.0]

    ## return bounding box in object-coordinate space
    def bounding(self):
        return [ [-epsilon,-epsilon],[epsilon,epsilon] ]

    ## sample-based bounding box utilty function, default takes 10 samples
    def __sample_bounding(self,samples=10):
        first=True

        minx = 0.0
        maxx = 0.0
        miny = 0.0
        maxy = 0.0
        
        for i in range(samples):
            u=i/(samples-1)
            p=self.sample(u)
            if first or p[0] < minx:
                minx = p[0]
            if first or p[0] > maxx:
                maxx = p[0]
            if first or p[1] < miny:
                miny = p[1]
            if first or p[1] > maxy:
                maxy = p[1]
            first=False

        return [[minx,miny],[maxx,maxy]]
    
    ## test for a point: inside or outside? 
    def is_inside(self,p):
        return False
    
class Point(Drawable):
    """ a drawable point class """
    def __init__(self,p,drawtype='x'):
        self.p = p
        self.drawtype=drawtype

    def __repr__(self):
        return 'Point({},{})'.format(self.p,self.drawtype)

    def draw(self):
        if self.drawtype == 'x' or self.drawtype == 'xo':
            self.draw_x(self.p,0.2)

        if self.drawtype == 'o' or self.drawtype == 'xo':
            self.draw_circle(self.p,0.1)

    def sample(self,u):
        return self.p
    
    def center(self):
        return self.p

    def bounding(self):
        return [ add(self.p,[-epsilon,-epsilon,0]),
                 add(self.p,[epsilon,epsilon,0]) ]

    ## this is tricky -- technically a point has no interior volume,
    ## but the point of this test (hah) is to allow two numerically
    ## coincident points to test as inside each other.  Think of this
    ## as a point equality test in floating-point space
    def is_inside(self,p):
        return dist(self.p,p) < epsilon
     

class Line(Drawable):
    """ a drawable line segment """
    def __init__(self,p1,p2):
        self.p1=p1
        self.p2=p2

    def __repr__(self):
        return 'Line({},{})'.format(self.p1,self.p2)

    def draw(self):
        self.draw_line(self.p1,self.p2)

    def sample(self,u):
        p = 1.0-u
        return add(scale(self.p1,p),scale(self.p2,u))
                   
    def center(self):
        return scale(add(self.p1,self.p2),0.5)

    def bounding(self):
        minx = min(self.p1[0],self.p2[0])
        maxx = max(self.p1[0],self.p2[0])
        miny = min(self.p1[1],self.p2[1])
        maxy = max(self.p1[1],self.p2[1])
        return [ [minx,miny],[maxx,maxy]]

    ## this is tricky -- lines have no volume, but a point on a line
    ## should be considered 'inside' the line.  Test for zero distance
    ## from point to line segment.
    def is_inside(self,p):
        d = linePointDist([self.p1,self.p2],p)
        return d < epsilon
    
    
class Arc(Drawable):
    """ a drawble arc, or full circle"""
    def __init__(self,p,r,start,end):
        self.p=p
        self.r=r
        self.start= start % 360.0 ## make start positive in 0-360
        self.end=end % 360.0 ## make end positive in 0-360

        ## if end less than start, "wrap" end into next cycle
        if self.end <= self.start:
            self.end = self.end+360.0
            
    def __repr__(self):
        return 'Arc({},{},{},{})'.format(self.p,self.r,
                                         self.start,self.end)

    def draw(self):
        self.draw_arc(self.p,self.r,self.start,self.end)

    def sample(self,u):
        angle = ((self.end-self.start)*u+self.start)
        radians = angle*pi2/360.0
        q = scale([cos(radians),sin(radians)],self.r)
        return add(self.p,q)
        
    def center(self):
        return self.p

    def bounding(self):
        return [add(self.p,[-self.r,-self.r]),
                add(self.p,[self.r,self.r])]

    ## treat this arc as a pie wedge for the purposes of inside testing
    def is_inside(self,p):
        if dist(self.p,p) >= r:
            return false
        p2 = sub(p,self.p)
        ang = (atan2(p2[0],p2[1]) % pi2)*360.0/pi2
        return ang >= self.start and ang <= self.end
    

## check to see if we have been invoked on the command line
## if so, run some tests
if __name__ == "__main__":
    print("testing for drawable.py")
    print("-----------------------")
    print("instantiating drawables...")
    print("instantiating Point")
    print("point=Point([10,10])")
    point=Point([10,10],"xo")
    print("instantiating Line")
    line=Line([-5,10],[10,-5])
    print("line=Line([-5,-5],[10,10])")
    print("instantiating Arc")
    print("arc=Arc([0,3],3,45,135)")
    arc=Arc([0,3],3,45,135)
    print("print tests")
    point.print()
    line.print()
    arc.print()
    print("draw tests")
    point.draw()
    line.draw()
    arc.draw()
    print("center tests")
    print("{}: center {}".format(point,point.center()))
    print("{}: center {}".format(line,line.center()))
    print("{}: center {}".format(arc,arc.center()))
    print("bouding tests")
    print("{}: bounding {}".format(point,point.bounding()))
    print("{}: bounding {}".format(line,line.bounding()))
    print("{}: bounding {}".format(arc,arc.bounding()))
    print("sample test")
    print("drawing 4 samples from line")
    line.draw()
    for i in range(4):
        u = i/3
        p = line.sample(u)
        pnt = Point(p,"o")
        pnt.draw()
    print("drawing 8 samples from arc")
    arc.draw()
    for i in range(8):
        u = i/7
        p = arc.sample(u)
        pnt = Point(p,"o")
        pnt.draw()
    
