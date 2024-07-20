import pygame
import math
import random


class Ball:
    def __init__(
        self,
        id,
        mass,
        angle,
        colour,
        hasGravity,
        canCollide,
        checkCollisions,
        fixed,
        x,
        y,
        z,
        spawnNewBall,
        velocity,
    ):
        self.id = id
        self.mass = mass
        self.angle = angle
        self.colour = colour
        self.defaultColour = colour
        self.hasGravity = hasGravity
        self.checkCollisions = checkCollisions
        self.canCollide = canCollide
        self.fixed = fixed
        self.velocity = velocity
        self.angularVelocity = 0.0
        self.thrusts = []
        self.torques = []
        self.x = x
        self.y = y
        self.z = z
        self.previousDistances = {}
        self.parent = None
        self.dampingFactor = 0.9
        self.radius = 20
        self.spawnNewBall = spawnNewBall

    def getForces(self):
        return None

    def reset(self):
        self.thrusts = []
        self.torques = []

    def updatePos(self, newX, newY):
        self.x = newX
        self.y = newY

    def applyGravity(self):
        gravityConstant = 9.81 / 60
        if self.hasGravity:
            self.velocity[1] += gravityConstant

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def printCoordinates(self):
        print(f"x:{self.x}, y:{self.y}")

    def checkCollisionWall(self, screenWidth, screenHeight):
        # Check for collision with the top or bottom borders
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.velocity[1] = abs(self.velocity[1]) * self.dampingFactor
        elif self.y + self.radius >= screenHeight:
            self.y = screenHeight - self.radius
            self.velocity[1] = -abs(self.velocity[1]) * self.dampingFactor

        # Check for collision with the left or right borders
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.velocity[0] = abs(self.velocity[0]) * self.dampingFactor
        elif self.x + self.radius >= screenWidth:
            self.x = screenWidth - self.radius
            self.velocity[0] = -abs(self.velocity[0]) * self.dampingFactor

    def checkCollision(self, other):
        d = math.sqrt((other.y - self.y) ** 2 + (other.x - self.x) ** 2)
        # dsqrd = ((other.y - self.y) * (other.y - self.y)) + (
        #    (other.x - self.x) * (other.x - self.x)
        # )
        # dsqrd < (other.radius * self.radius)
        return d < (other.radius + self.radius)

    def handleCollision(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            distance = 1  # Prevent division by zero

        nx = dx / distance
        ny = dy / distance

        dvx = other.velocity[0] - self.velocity[0]
        dvy = other.velocity[1] - self.velocity[1]

        dot = dvx * nx + dvy * ny

        if dot > 0:
            return None

        coefficientOfRestitution = 0.8
        impulse = (2 * dot) / (self.mass + other.mass) * coefficientOfRestitution
        self.velocity[0] += impulse * other.mass * nx
        self.velocity[1] += impulse * other.mass * ny
        other.velocity[0] -= impulse * self.mass * nx
        other.velocity[1] -= impulse * self.mass * ny

        if self.spawnNewBall:
            newBallX = self.x
            newBallY = self.y
            newBallVelocity = [self.velocity[0], self.velocity[1]]
            return Ball(
                id=random.randint(100000, 100000000),
                mass=1.0,
                angle=0,
                colour=self.randomColour(),
                hasGravity=True,
                canCollide=True,
                checkCollisions=False,
                fixed=False,
                x=newBallX,
                y=newBallY,
                z=0,
                spawnNewBall=False,  # New balls won't spawn further balls
                velocity=newBallVelocity,
            )
        return None

    def randomColour(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius)

