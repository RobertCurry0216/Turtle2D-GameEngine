from turtle import *


def intersect(v1, v2, v3, v4, overlap_as_intersect=False):
    """ find the intersection point between 2 lines 
    [v1, v2] = line 1
    [v3, v4] = line 2 """

    def is_zero(a):
        zero = 1 ** (-10)
        return abs(a) < zero

    p = v1
    p2 = v2
    q = v3
    q2 = v4
    r = p2 - p
    s = q2 - q
    rxs = r.cross(s)
    qpxr = (q - p).cross(r)

    # If r x s = 0 and (q - p) x r = 0, then the two lines are collinear.
    if is_zero(rxs) and is_zero(qpxr):
        if overlap_as_intersect:
            # 1. If either  0 <= (q - p) * r <= r * r or 0 <= (p - q) * s <= * s
            # then the two lines are overlapping,
            if (0 <= q - p * r <= r * r) or (0 <= p - q * s <= s * s):
                return True
        # 2. If neither 0 <= (q - p) * r = r * r nor 0 <= (p - q) * s <= s * s
        return False
    # 3. If r x s = 0 and (q - p) x r != 0, then the two lines are parallel and non-intersecting.
    if is_zero(rxs) and not is_zero(qpxr):
        return False

    t = (q - p).cross(s) / rxs
    u = (q - p).cross(r) / rxs

    # 4. If r x s != 0 and 0 <= t <= 1 and 0 <= u <= 1
    # the two line segments meet at the point p + t r = q + u s.
    if not is_zero(rxs) and (0 <= t <= 1) and (0 <= u <= 1):
        return p + (r * t)
    # 5. Otherwise, the two line segments are not parallel but do not intersect.
    return False


class Vector:
    """
    basic unit for 2d vector graphics
    has basic math functionality, ie +, -, *
    """

    def __init__(self, x, y):
        self._coords = [x, y]

    @property
    def x(self):
        return self._coords[0]

    @x.setter
    def x(self, x):
        self._coords[0] = x

    @property
    def y(self):
        return self._coords[1]

    @y.setter
    def y(self, y):
        self._coords[1] = y

    def get(self):
        return self._coords

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, ', '.join(str(a) for a in self._coords))

    def __add__(self, other):
        values = (a + b for a, b in zip(self._coords, other.get()))
        return self.__class__(*values)

    def __sub__(self, other):
        values = (a - b for a, b in zip(self._coords, other.get()))
        return self.__class__(*values)

    def __mul__(self, other):
        if type(other) == Vector:
            values = (a * b for a, b in zip(self._coords, other.get()))
        else:
            values = (a * other for a in self._coords)
        return self.__class__(*values)

    def __eq__(self, other):
        zero = 1 ** (-10)
        return all(abs(a - b) <= zero for a, b in zip(self.get(), other.get()))

    def __getitem__(self, item):
        return self._coords[item]

    def cross(self, other):
        return (self.x * other.y) - (self.y * other.x)

    def dot(self, other):
        return sum(a*b for a, b in zip(self, other.get())) 


class Polygon(Turtle):
    """ Basic unit for drawing shapes """
    def __init__(self, 
                outline, 
                starting_point=Vector(0,0), 
                colour=(255,255,255)):
        super().__init__()
        self._outline = outline
        self._location = starting_point
        self.color = colour
        self.width = 1

    def __repr__(self):
        return f'{self.__class__.__name__}({self._outline}, {self._location}, {self._colour}, {self._closed})'

    def draw(self, solid=False):
        """ Draws the polygon to the screen"""
        self.clear()
        self.pu()
        self.goto(self._outline[0].x, self._outline[0].y)
        self.pd()
        for p in self._outline:
            x, y = p + self._location
            self.goto(x, y)
        self.pu()


class Outline:
    """ class defining the outline of a shape """
    def __init__(self, *points, closed=True):
        self._points = [Vector(x, y) for x, y in points]
        if closed:
            self._points.append(self._points[0])
        
    def __getitem__(self, item):
        return self._points[item]

    def __setitem__(self, item, value):
        self._points[item] = Vector(value[0], value[1])



if __name__ == '__main__':
    wn = Screen()
    wn.setup(800, 800)
    wn.screensize(800, 800)
    wn.bgcolor(0,0,0)
    wn.tracer(0)
    wn.title('Turtle2D Engine')

    o = Outline((-10,-10),(10,10), (0,0))
    a = Polygon(o, Vector(0, 0))

    while True:
        a.draw()
        wn.update()
