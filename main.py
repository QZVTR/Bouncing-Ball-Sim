import pygame
import pygame_gui
from Ball import Ball
import random
import argparse
from collections import defaultdict


def main(spawnNewBall):
    pygame.init()

    background_colour = (255, 255, 255)
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Bouncing Balls")

    screenWidth = 600
    screenHeight = 600

    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((600, 600))

    gravitySlider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
        relative_rect=pygame.Rect((150, 10), (300, 25)),
        start_value=9.81,
        value_range=(0.0, 20.0),
        manager=manager,
    )

    pygame.font.init()
    font = pygame.font.Font(None, 36)

    running = True
    balls = []
    gridSize = 50

    def randomColour():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    while running:
        time_delta = clock.tick(60) / 1000.0

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
                    gravity=gravitySlider.get_current_value(),
                )
                balls.append(newBall)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    for ball in balls:
                        ball.velocity[1] -= 10
                if event.key == pygame.K_DOWN:
                    for ball in balls:
                        ball.velocity[1] += 10
                if event.key == pygame.K_LEFT:
                    for ball in balls:
                        ball.velocity[0] -= 10
                if event.key == pygame.K_RIGHT:
                    for ball in balls:
                        ball.velocity[0] += 10
                if event.key == pygame.K_SPACE:
                    for ball in balls:
                        ball.velocity[0] += random.randint(-150, 150)
                        #ball.velocity[0] -= random.randint(1, 15)
                        ball.velocity[1] += random.randint(-150, 150)
                        #ball.velocity[1] -= random.randint(1, 15)
                if event.key == pygame.K_r:
                    balls.clear()

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(background_colour)

        grid = defaultdict(list)
        for ball in balls:
            gridX = int(ball.x // gridSize)
            gridY = int(ball.y // gridSize)
            grid[(gridX, gridY)].append(ball)

        # Update gravity for all balls
        currentGravity = gravitySlider.get_current_value()
        for ball in balls:
            ball.gravity = currentGravity

        """
        # Update all balls
        for ball in balls:
            ball.applyGravity()
            ball.checkCollisionWall(screenWidth, screenHeight)
            ball.move()

        # Handle collisions between balls
        newBalls = []
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if balls[i].checkCollision(balls[j]):
                    newBall = balls[i].handleCollision(balls[j])
                    if newBall:
                        newBalls.append(newBall)

        # Add newly spawned balls to the list
        balls.extend(newBalls)
        """

        newBalls = []
        for ball in balls:
            ball.applyGravity()
            ball.checkCollisionWall(screenWidth, screenHeight)
            ball.move()

            gridX = int(ball.x // gridSize)
            gridY = int(ball.y // gridSize)

            # Check for collisions with balls in the same or adjacent grid cells
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    adjacentCell = (gridX + dx, gridY + dy)
                    for otherBall in grid[adjacentCell]:
                        if ball != otherBall and ball.checkCollision(otherBall):
                            newBall = ball.handleCollision(otherBall)
                            if newBall:
                                newBalls.append(newBall)

        # Add newly spawned balls to the list
        balls.extend(newBalls)

        # Draw all balls
        for ball in balls:
            ball.draw(screen)

        # Display FPS
        fps = clock.get_fps()
        fpsText = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
        screen.blit(fpsText, (10, 10))

        gravityText = font.render(
            f"Gravity: {gravitySlider.get_current_value():.2f}m/s", True, (0, 0, 0)
        )
        screen.blit(gravityText, (10, 50))

        # Draw the UI
        manager.draw_ui(screen)

        # Update the display
        pygame.display.flip()

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

    spawnNewBall = args.spawn_new_ball == "True"
    main(spawnNewBall)
