# **yapCAD**
yet another procedural CAD and computational geometry system written in python 3

![**yapCAD** image](images/example6-out.png)

## **yapCAD** goals

The purpose of **yapCAD** is to support 2D and 3D computational geometry and procedural CAD projects in python3.  **yapCAD** is designed to support multiple rendering back-ends, such that a relatively small amount of code is necessary to add support for a 2D or 3D cad or drawing file format.  At present, **yapCAD** supports the AutoCad DXF file format for creating two-dimensional drawings and OpenGL for creating interactive 2D and 3D renderings. 

The foundations of **yapCAD** are grounded in decades of the author's experience with graphics system programming, 3D CAD and simulation. **yapCAD** has an underlying framework and architecture designed to support sohpisticated computational geometry and procedural CAD applications.  At the same time, the design of **yapCAD** should make easy stuff relatively easy, and the more advanced stuff possible. 

The initial implementation of **yapCAD** provides DXF file creation support through the awesome [ezdxf](https://github.com/mozman/ezdxf) package, and interactive OpenGL visualization using the amazing [pyglet](https://github.com/pyglet/pyglet) package.

## **yapCAD** examples

(for a more complete list, see the [examples folder](./examples/))

It's pretty easy to make a DXF drawing with **yapCAD**.  Here is an example:

	from yapcad.ezdxf_drawable import *
	from yapcad.geom import *

	#set up DXF rendering
	dd=ezdxfDraw()
    dd.saveas("example1-out")

    ## make dxf-renderable geometry

    # make a point located at 10,10 in the x-y plane, rendered as a small
    # red cross and circle
	dd.pointstyle = 'xo' # also valid are 'x' or 'o'
	dd.set_linecolor(1) # set color to red (DXF index color 1)
    dd.draw(point(10,10))

    # make a line segment between the points -5,10 and 10,-5 in the x-y plane
	# and draw it in white
	
	dd.set_linecolor('white') # set color by name
    dd.draw(line(point(-5,10),
		         point(10,-5)))

    # make an arc with a center at 0,3 with a radius of 3, from 45 degrees
    # to 135 degrees, and draw it in aqua
	
	dd.set_linecolor([0,255,255]) # RGB tripple, corresponds to 'aqua'
    dd.draw(arc(point(0,3),3,45,135))

    # write out the geometry as example1-out.dxf
	dd.display()

The **yapCAD** system isn't just about rendering, of course, it's about computational geometry.  For example, if you want to calculate the intersection of lines and arcs in a plane, we have you covered:

	from yapcad.geom import *

    # define some points
    a = point(5,0)
    b = point(0,5)
    c = point(-3,0)
    d = point(10,10)

    # make a couple of lines
    l1 = line(a,b)
    l2 = line(c,d)

    # define a semicircular arc centerd at 2.5, 2,5 with a radius of 2.5
    # extending from 90 degress to 135 degrees

    arc1=arc(point(2.5,2.5),2.5,90.0,270.0)

    # calculate the intersection of lines l1 and l2
    int0 = intersectXY(l1,l2)

    # calculate the intersection of the line l1 and the arc arc1
    int1 = intersectXY(l1,arc1)

    print("intersection of l1 and l2:",vstr(int0))
    print("intersection of l1 and arc1:",vstr(int1))
	
And there are lots more [examples](examples/README.md) available to
demonstrate the various computational geometry and rendering
capabilities of **yapCAD**, including 3D geometry and OpenGL rendering.

## **yapCAD** geometry

**yapCAD** distinguishes between "pure" geometric elements, such as lines,
arcs, ***etc.***, and drawn representations of those things, which
might have attributes like line color, line weight, drawing layer,
***etc.*** This distinction is important, because the pure geometry
exists independent of these attributes, which are themselves
rendering-system dependent.

More importantly, for every geometric element you decide to draw,
there will typcialy be many more &mdash; perhaps dozens &mdash; that
should not be in the final rendering.  By separating these two
elements &mdash; computation and rendering &mdash; **yapCAD** makes them
both more intentional and reduces the likelyhood of certain type of
drawing-quality issues, such as redundant or spurious drawing
elements, that can cause confusion problems for computer-aided
manufacturing (CAM).

For example, you might construct a finished drawing that includes a
drill patern that consists of circles (drill holes with centers) that
follow a complex, geometrically constrained patern.  This patern is
itself the result of numerous computational geometry operations,
perhaps driven by parameters relating to the size and shape of other
parts. 

In a program like Autodesk's Fusion360, you would typically use
construction lines and constraints to create the underliying geometric
pattern.  These additional construction elements would have to be
removed in order to make a clean DXF export of your drawing.  On more
than one occasion **yapCAD**'s author has created headaches by failing to
remove some of these elements, confusing CAM technicians, causing
delays, and sometimes resulting in expensive part fabrication errors.

Thus, **yapCAD** allows you to work freely with computational geometry
without cluttering up your drawing page, since you specifically decide
what to draw.  It also means you can do computational geometry in
**yapCAD** without ever invoking a rendering system, which can be useful
when incorporating these geometry operations as part of a larger
computational system, such as a tool-path generator. 

As a rule, in **yapCAD** pure geonetry representations capture only the
minimum necessary to perform computational geometry, and the rest gets
dealt with by the rendering system, which are subclasses of `Drawable`
that actually make images, CAD drawings, ***etc.***

### vector representation in **yapCAD**
For the sake of uniformity, all **yapCAD** vectors are stored as
projective geometry 4-vectors. (see discussion in **architecture**,
below) However, most of the time you
will work with them as though they are 3-vectors or 2-vectors.

It woud be annoying to have to specify the redundant coordinates you
aren't using every time you specify a vector, so **yapCAD** provides you
with the `vect` function.  It fills in defaults for the z and w
parameters you may not want to specify.  ***e.g.***

    >>> from geom import *
    >>> vect(10,4)
    [10, 4, 0, 1]
	>>> add(vect(10,4),vect(10,9))  ## add operates in 3-space
    [20, 13, 0, 1.0]
	
Of course, you can specify all three (or even four) coordinates using
`vect`. 

Since it gets ugly to look at a bunch of [x, y, z, w] lists that all
end in `0, 1]` when you are doing 2D stuff, **yapCAD** provides a
convenience function `vstr` that intelligently converts **yapCAD** vectors
(and lists that contain vectors, such as lines, triangles, and
polygons) to strings, assuming that as long as z = 0 and w = 1, you
don't need to see those coordinates.

    >>> from geom import *
    >>> a = sub(vect(10,4),vect(10,9)) ## subtract a couple of vectors 
    >>> a
    [0, -5, 0, 1.0]
    >>> print(vstr(a)) ## pretty printing, elide the z and w coordinates
    >>> [0, -5]

### pure geometry
Pure geometric elements in **yapCAD** form the basis for computational
geometry operations.  Pure geometry can also be drawn, of course
&mdash; see **drawable geometry** below.

In general, **yapCAD** pure geometry supports the operations of parametric
sampling, intersection calculation, "unsampling" (going from a point
on the figure to the sampling parameter that would produce it), and
bounding box calculation.  **yapCAD** geometry is based on projective or
homogeneous coordinates, thus supporting generalized affine
transformations;  See the discussion in **architecture**, below.

Pure geometry includes (among other elements) vectors, points, lines,
and multi-segment polylines.  A vector is a list of exactly four
numbers, each of which is a float or integer.  A point is a vector
that lies in a w > 0 hyperplane; Points are used to represent
coordinates in **yapCAD** geometry.  A line is a list of two points, and a
polyline is a list of 3 or more points. 

Pure geometry also includes arcs.  An arc is a list of a point and a
vector, followed optionally by another point. The first list element
is the center of the arc, the second is a vector in the w=-1
hyperplane whose first three elements are the scalar parameters 
`[r, s, e]`: the radius, the start angle in degrees, and the end angle
in degrees.  The third element (if it exists) is the normal for the
plane of the arc, which is assumed to be `[0, 0, 1]` (the x-y plane)
if it is not specified.

Simple multi-vertex polylines are represented by lists of points.  If
the last point is the same as the first, the polyline figure is
closed.  Closed coplanar polylines may be interpreted as polygons.
Like other elements of pure geometry, polylines are subject to
sampling.

Pure geometry also includes instances of the `Polyline` and `Polygon`
class.  Instances of these classes are used for representing
multi-figure drawing elements in an XY plane with C0 continuity.  They
differ from the point-list-based `poly()` representation in that the
elements of a `Polyline` or `Polygon` can include lines and arcs as
well as points.  These elements need not be contiguous, as successive
elements will be computationally joined by straight lines.  `Polygons`
are special in that they are always closed, and that full circle
elements are interpreted as "rounded corners," with the actual span of
the arc calculated after tangent lines are drawn.

Pure geometry also includes geometry lists, which is to say a list of
zero or more elements of **yapCAD** pure geometry.  Many **yapCAD**
computational geometry functions return either geometry elements or
geometry lists.


### drawable geometry

The idea is that you will do your computational geometry with "pure"
geometry, and then generate rendered previews or output with one or
more `Drawable` instances.

In **yapCAD**, geometry is rendered with instances of subclasses of
`Drawable`, which at present include `ezdxfDrawable`, a class for
producing DXF renderinsgs using the awesome `ezdxf` package, and
`pygletDrawable`, a class for interactive 2D and 3D OpenGL rendering.

To setup a drawing environment, you create an instance of the
`Drawable` base class corresponding to the rendering system you want
to use.

To draw, create the pure geometry and then pass that to the drawbles's
`draw()` method.  To display or write out the results you will invoke
the `display` method of the drawable instance.

#### supported rendering systems

DXF rendering using `ezdxf` and interactive OpenGL rendering using
`pyglet` are currently supported, and the design of **yapCAD** makes
it easy to support other rendering backends.

## **yapCAD** architecture

Under the hood, **yapCAD** is using [projective
coordiates](https://en.wikipedia.org/wiki/Homogeneous_coordinates),
sometimes called homogeneous coordinates, to represent points as 3D
coodinates in the w=1 hyperplane. If that sounds complicated, its
because it is. :P But it does allow for a wide range of geometry
operations, specifically [affine
transforms](https://www.cs.utexas.edu/users/fussell/courses/cs384g-fall2011/lectures/lecture07-Affine.pdf)
to be represented as composable transformation matricies. The benefits
of this conceptual complexity is an architectual elegance and
generality.

Support for affine transforms is at present rudamentary, but once a
proper matrix transform stack is implemented it will allow for the
seamless implementation and relatively easy use of a wide range of
transformation and projection operations.

What does that buy you? It means that under the hood, **yapCAD** uses the
same type of geometry engine that advanced CAD and GPU-based rendering
systems use, and should allow for a wide range of computational
geomety systems, possibly hardware-accelerated, to be built on top of
it.

The good news is that you don't need to know about homogeneous
coordinates, affine transforms, etc., to use **yapCAD**.  And most of the
time you can pretend that your vectors are just two-dimensional if
everything you are doing happens to lie in the x-y plane.

So, if you want to do simple 2D drawings, we have you covered.  If you
want to buid a GPU-accelerated constructive solid geometry system, you
can do that, too.
