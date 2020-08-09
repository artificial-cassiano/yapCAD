## generalized matrix transformation operations for 3D homogeneous
## coordinates in yapCAD

from geom import *

## a matrix is represented as a list of four four vectors. In a
## matrix, vectors represent rows unless the transpose property is
## true.  Because vectors are represented as lists (not as instances
## of a class with meta-info) we assume that operations like Mx imply
## a column vector and that xM imply a row vector.

## There are two classes defined here: Matrix and MatrixStack.  Matrix
## is a relatively lightweight class that provides foundation
## matrix-matrix and matrix-vector operations.  MatrixStack is a class
## that captures a series of transformations and their inverses.  Note
## that inverses are generally determined analytically through
## composition, though we don't dismiss the possibility of a numeric
## inversion.

class Matrix:
    """4x4 transformation matrix class for transforming homogemenous 3D coordinates"""

    def __init__(self,a=False,trans=False):
        self.m = [[1,0,0,0],
                  [0,1,0,0],
                  [0,0,1,0],
                  [0,0,0,1]]
        self.trans=False
        
        if isinstance(a,Matrix):
            for i in range(4):
                self.setrow(i,a.getrow(i))
                
        elif isinstance(a,(tuple,list)):
            if len(a) == 4:
                r1 =a[0]
                r2 =a[1]
                r3 =a[2]
                r4 =a[3]
                if len(r1) == len(r2) == len(r3) == len(r4) == 4:
                    for i in range(4):
                        for j in range(4):
                            x =a[i][j]
                            if (not isinstance(x,bool)) and isinstance(x,(int,float)):
                                self.m[i][j]=x
            elif len(a)==16:
                for i in range(4):
                    for j in range(4):
                        ind=i*4+j
                        x = a[ind]
                        if (not isinstance(x,bool)) and isinstance(x,(int,float)):
                            self.m[i][j]=x
        self.trans=trans
                            
    def __repr__(self):
        return "Matrix({},{},{},{},{})".format(self.m[0],self.m[1],
                                               self.m[2],self.m[3],self.trans)

    #return value indexed by i,j
    def get(self,i,j):
        if self.trans:
            return self.m[j][i]
        else:
            return self.m[i][j]

    #set value indexed by i,j
    def set(self,i,j,x):
        if isgoodnum(x):
            if self.trans:
                self.m[j][i]=x
            else:
                self.m[i][j]=x

    def getrow(self,i):
        if self.trans:
            return [self.m[0][i],
                    self.m[1][i],
                    self.m[2][i],
                    self.m[3][i]]
        else:
            return self.m[i]
        
    def getcol(self,j):
        if not self.trans:
            return [self.m[0][j],
                    self.m[1][j],
                    self.m[2][j],
                    self.m[3][j]]
        else:
            return self.m[j]

    def setrow(self,i,x):
        if not isvect(x):
            return False
        if self.trans:
            self.m[0][i] = x[0]
            self.m[1][i] = x[1]
            self.m[2][i] = x[2]
            self.m[3][i] = x[3]
        else:
            self.m[i] = x
        
    def setcol(self,j,x):
        if not isvect(x):
            return False
        if not self.trans:
            self.m[0][j] = x[0]
            self.m[1][j] = x[1]
            self.m[2][j] = x[2]
            self.m[3][j] = x[3]
        else:
            self.m[j] = x
        

    # matrix multiply.  If x is a matrix, compute MX.  If X is a
    # vector, compute Mx. If x is a scalar, compute xM. If x isn't any
    # of these, return False.  Respects transpose flag.
    
    def mul(self,x):
        if isinstance(x,Matrix):
            result = Matrix()
            for i in range(4):
                for j in range(4):
                    result.set(i,j,
                               dot4(self.getrow(i),x.getcol(j)))
            return result
        elif isvect(x):
            result = vect()
            for i in range(4):
                result[i]=dot4(self.getrow(i),x)
            return result
        elif isgoodnum(x):
            result = Matrix()
            for i in range(4):
                result.setrow(i,scale4(self.getrow(i),x))
            return result
        
        return False
    

## check to see if we have been invoked on the command line
## if so, run some tests
if __name__ == "__main__":
    foo = Matrix([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
    fooT = Matrix(foo,True)
    bar = Matrix([[1,0,0,1],[0,1,0,1],[0,0,1,1],[0,0,0,1]])
    baz = vect(1,2,3)
    I = Matrix()
    a = 10.0
    print("foo: {}".format(foo))
    print("fooT: {}".format(fooT))
    print("bar: {}".format(bar))
    print("baz: {}".format(baz))
    print("I: {}".format(I))
    print("a: {}".format(a))
    print("I.mul(bar): {}".format(I.mul(bar)))
    print("I.mul(foo): {}".format(I.mul(foo)))
    print("I.mul(fooT): {}".format(I.mul(fooT)))
    print("fooT.mul(I): {}".format(fooT.mul(I)))
    print("I.mul(I): {}".format(I.mul(I)))
    print("foo.mul(bar): {}".format(foo.mul(bar)))
    print("foo.mul(baz): {}".format(foo.mul(baz)))
    print("foo.ml(a): {}".format(foo.mul(a)))
    print("I.mul(baz): {}".format(I.mul(baz)))
    print("homo(foo.mul(baz)): {}".format(homo(foo.mul(baz))))
    
    