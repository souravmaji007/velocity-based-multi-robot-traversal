from config import *


class MovingObstacle:

    def __init__(self, x, y, dx, dy, size):

        self.x = x
        self.y = y

        self.dx = dx
        self.dy = dy

        self.size = size


    def move(self):

        self.x += self.dx
        self.y += self.dy


        # WALL BOUNCE

        if self.x <= 0 or self.x >= WIDTH:
            self.dx *= -1

        if self.y <= 0 or self.y >= HEIGHT:
            self.dy *= -1