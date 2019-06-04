from turtle import Turtle, Screen
from math import sin, cos, pi
from time import time, sleep


def intersect(v1, v2, v3, v4, overlap_as_intersect=False):
    """ find the intersection point between 2 lines 
    [v1, v2] = line 1
    [v3, v4] = line 2 
       v1    v4
        \   /
         \ /
          x  
         / \
        /   \
      v3      v2
    """

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

    def rotate(self, theta):
        # theta -= (pi/2)
        a = cos(theta)
        b = sin(theta)
        m = [
            [a,b],
            [-b,a],
        ]
        x = (self.x * m[0][0]) + (self.y * m[1][0])
        y = (self.x * m[0][1]) + (self.y * m[1][1])
        return Vector(x, y)


class Player(Turtle):
    """ Basic unit for drawing shapes """
    def __init__(self, 
                outline, 
                starting_point=Vector(0,0), 
                colour='white'):
        super().__init__()
        self._outline = outline
        self._location = starting_point
        self._rotation = 0
        self._size = 0
        self.color(colour)
        self.width(1)
        self.pu()
        self.ht()

        Game.players.append(self)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._outline}, {self._location}, {self._colour})'

    def draw(self, solid=False):
        """ Draws the player to the screen"""
        self.clear()
        self.pu()
        start = self._location + self._outline[0].rotate(self._rotation)
        self.goto(start.x, start.y)
        self.pd()
        for p in self._outline[1:]:
            point = p.rotate(self._rotation) + self._location
            x, y = point
            self.goto(x, y)
        self.pu()

    def update(self, time_delta=None):
        self._rotation += time_delta
        self.draw()

    def screenloop(self):
        sw = Game.screenwidth + self._size * 2
        sh = Game.screenheight + self._size * 2

        if self._location.x < -sw/2:
            self._location.x += sw
        elif self._location.x > sw/2:
            self._location.x -= sw
        if self._location.y < -sh/2:
            self._location.y += sh
        elif self._location.y > sh/2:
            self._location.y -= sh

    def collision(self, other):
        for p1, p2 in zip(self._outline, self._outline[1:]):
            p1 = p1.rotate(self._rotation) + self._location
            p2 = p2.rotate(self._rotation) + self._location
            for o1, o2 in zip(other._outline, other._outline[1:]):
                o1 = o1.rotate(other._rotation) + other._location
                o2 = o2.rotate(other._rotation) + other._location
                if intersect(p1,p2,o1,o2):
                    return True
        return False

    def die(self):
        Game.players.remove(self)
        self.clear()


class Outline(list):
    """ class defining the outline of a shape """
    def __init__(self, *points, closed=False):
        super().__init__([Vector(x, y) for x, y in points])
        if closed:
            self.close()
        
    def close(self, extend=False):
        if self[0] != self[-1]:
            if extend:
                self.append(self[0])
            else:
                self[-1] = self[0]
    
    def scale(self, num):
        for i, v in enumerate(self):
            self[i] = v * num


def Polygon(sides, radius):
    step = (2*pi) / sides
    points = []
    for i in range(sides):
        x = radius * cos(i * step)
        y = radius * sin(i * step)
        points.append(Vector(x, y))
    outline = Outline(*points)
    outline.close(True)
    return outline


class Game:
    players = []
    screenwidth = 0
    screenheight = 0
    _time = 0
    _wn = None

    @classmethod
    def setup(cls, height, width, bg=(0,0,0), title='Turtle2D Engine'):
        cls._wn = Screen()
        cls._wn.setup(width + 20, height + 20)
        cls._wn.screensize(width, height)
        cls._wn.bgcolor(bg)
        cls._wn.tracer(0)
        cls._wn.title(title)
        cls._time = None
        cls.screenwidth = width
        cls.screenheight = height
        cls._wn.listen()

    @classmethod
    def game_loop(cls):
        """ Calls the update function on all players passing in the time delta since the last frame """
        while True:
            if cls._time:
                t = time()
                td = t - cls._time
                cls._time = t
                for player in cls.players:
                    player.update(td)
            else:
                cls._time = time()
            cls._wn.update()


if __name__ == '__main__':
    Game.setup(600, 800)
    Player(Polygon(12, 100), Vector(0, 0))
    Player(Polygon(4, 75), Vector(0, -100))
    Game.game_loop()

