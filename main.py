from turtle2D import *
from random import uniform


class Asteroid(Player):
    def __init__(self, 
                size, 
                starting_point=Vector(0,0), 
                colour='white'):
        o = Polygon(12, size)
        for i, p in enumerate(o):
            o[i] = p * uniform(0.5, 1.1)
        o.close()
        super().__init__(o, starting_point, colour)


if __name__ == '__main__':
    game = Game(600, 800)
    Asteroid(75)
    game.game_loop()