import pygame
from Ball import Ball
import random
import argparse


def main(spawnNewBall):
    pygame.init()

    background_colour = (255, 255, 255)
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Bouncing Balls")

    screenWidth = 600
    screenHeight = 600

    clock = pygame.time.Clock()

    pygame.font.init()
    font = pygame.font.Font(None, 36)

    running = True
    balls = []

    def randomColour():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                newBall = Ball(
                    id=len(balls),
                    mass=1.0,
                    angle=0,
                    colour=randomColour(),
                    hasGravity=True,
                    canCollide=True,
                    checkCollisions=False,
                    fixed=False,
                    x=x,
                    y=y,
                    z=0,
                    spawnNewBall=spawnNewBall,
                    velocity=[0.0, 0.0],
                )
                balls.append(newBall)

        # Clear the screen
        screen.fill(background_colour)

        # Update all balls
        for ball in balls:
            ball.applyGravity()
            ball.checkCollisionWall(screenWidth, screenHeight)
            ball.move()

        # Handle collisions between balls
        new_balls = []
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if balls[i].checkCollision(balls[j]):
                    new_ball = balls[i].handleCollision(balls[j])
                    if new_ball:
                        new_balls.append(new_ball)

        # Add newly spawned balls to the list
        balls.extend(new_balls)

        # Draw all balls
        for ball in balls:
            ball.draw(screen)

        # Display FPS and Gravity
        fps = clock.get_fps()
        gravity = (
            balls[0].velocity[1] if balls else 0
        )  # Example: using the first ball's gravity

        fpsText = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
        # gravityText = font.render(f"Gravity: {gravity:.2f}", True, (0, 0, 0))

        screen.blit(fpsText, (10, 10))
        # screen.blit(gravityText, (10, 50))

        # Update the display
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the ball simulation.")
    parser.add_argument(
        "spawn_new_ball",
        type=str,
        choices=["True", "False"],
        help="Whether to spawn a new ball upon collision ('True' or 'False').",
    )
    args = parser.parse_args()

    # Convert the argument to boolean
    spawnNewBall = args.spawn_new_ball == "True"

    main(spawnNewBall)
