from turtle2D import *
from random import uniform, randint
import math


class Asteroid(Player):
    SIZE = (25, 35, 50, 75, 100)

    def __init__(self, 
                size, 
                starting_point=None, 
                colour='white'):
        o = Polygon(12, Asteroid.SIZE[size])
        for i, p in enumerate(o):
            o[i] = p * uniform(0.5, 1.1)
        o.close()
        if not starting_point:
            width = Game.screenwidth + 2 * Asteroid.SIZE[size]
            height = Game.screenheight + 2 * Asteroid.SIZE[size]
            if randint(0,1):
                x = uniform(0, width) - width/2
                y = -height/2
            else:
                x = -width/2
                y = uniform(0, height) - height/2
            starting_point = Vector(x, y)
        super().__init__(o, starting_point, colour)
        self._level = size
        self._size = Asteroid.SIZE[size]
        self._speed = uniform(50, 150)
        self._direction = uniform(0, math.pi*2)
        self._rotation_speed = uniform(-2,2)
        self.dx = math.cos(self._direction) * self._speed
        self.dy = math.sin(self._direction) * self._speed

    def update(self, time_delta):
        dx = self.dx * time_delta
        dy = self.dy * time_delta
        self._location += Vector(dx, dy)
        self._rotation += time_delta * self._rotation_speed
        self.screenloop()
        self.draw()

    def die(self):
        if self._level > 0:
            Asteroid(self._level - 1, starting_point=self._location)
            Asteroid(self._level - 1, starting_point=self._location)
        super().die()


class Spaceship(Player):
    def __init__(self):
        o = Outline((0,0), (1,1), (0, -2), (-1,1), (0,0))
        o.scale(10)
        super().__init__(o)
        self._rotation = 0
        self._frame_rotation = 0
        self.dx = 0
        self.dy = 0
        self._move = False
        
        # movement vars
        self._turn_speed = 5
        self._movement_speed = 400
        
        # key bindings
        Game._wn.onkeypress(self._turn_left_pressed, 'Left')
        Game._wn.onkeyrelease(self._turn_left_released, 'Left')
        Game._wn.onkeypress(self._turn_right_pressed, 'Right')
        Game._wn.onkeyrelease(self._turn_right_released, 'Right')
        Game._wn.onkeypress(self._turn_forward_pressed, 'Up')
        Game._wn.onkeyrelease(self._turn_forward_released, 'Up')
        Game._wn.onkeypress(self.shoot, 'space')
        

    # turning
    def _turn_left_pressed(self):
        self._frame_rotation = self._turn_speed
    def _turn_left_released(self):
        self._frame_rotation = 0
    def _turn_right_pressed(self):
        self._frame_rotation = self._turn_speed * -1
    def _turn_right_released(self):
        self._frame_rotation = 0

    #movement
    def _turn_forward_pressed(self):
        self._move = True
    def _turn_forward_released(self):
        self._move = False

    def shoot(self):
        Bullet(self._location, self._rotation - (math.pi/2))

    def check_colision(self):
        for asteroid in Game.players:
            if not isinstance(asteroid, Asteroid):
                continue
            if self.collision(asteroid):
                self._location = Vector(-1000000000, -100000000)
                self.die()
                break

    def update(self, time_delta):
        # turning
        self._rotation += self._frame_rotation * time_delta

        #movement
        if self._move:
            self.dx += self._movement_speed * math.sin(self._rotation) * time_delta
            self.dy += self._movement_speed * -math.cos(self._rotation) * time_delta
        x = self.dx * time_delta
        y = self.dy * time_delta
        self._location += Vector(x, y)
        self.screenloop()
        self.draw()
        self.check_colision()


class Bullet(Player):
    def __init__(self, starting_point, direction):
        o = Outline((0,0), (1,0))
        o.scale(10)
        super().__init__(o, starting_point)
        self._direction = direction
        self._rotation = direction
        self._speed = 400
        self._life = 1
        self.dx = math.cos(self._direction) * self._speed
        self.dy = math.sin(self._direction) * self._speed

    def check_colision(self):
        for asteroid in Game.players:
            if not isinstance(asteroid, Asteroid):
                continue
            x, y = self._location
            ax, ay = asteroid._location
            if math.sqrt((x-ax)**2 + (y-ay)**2) < asteroid._size:
                asteroid.die()
                return True
        return False

    def update(self, time_delta):
        dx = self.dx * time_delta
        dy = self.dy * time_delta
        self._location += Vector(dx, dy)
        self.screenloop()
        self.draw()
        self._life -= time_delta
        if self._life <= 0 or self.check_colision():
            self.die()


if __name__ == '__main__':
    Game.setup(600, 800)
    for i in range(5):
        Asteroid(i)
    Spaceship()
    Game.game_loop()