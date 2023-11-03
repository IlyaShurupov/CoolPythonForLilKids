# this is statments that we need to use some libraries for window drawing and system utils
# google "python modules" "importing python modules" "popular python modules"
import pygame
import sys

# our ball variables
windowHeight = 600
windowWidth = 800

ballRadius = 20
ballPosX = windowWidth // 2
ballPosY = windowHeight // 2
ballSpeedX = 5
ballSpeedY = 5

# inititalize window using library
# tell pygame that we want to start using it
# u can google what for pygame is needed
pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Bouncing Ball")


# Main game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update ball position
    ballPosX += ballSpeedX
    ballPosY += ballSpeedY

    # Bounce the ball off the edges
    if ballPosX + ballRadius > windowWidth or ballPosX - ballRadius < 0:
        ballSpeedX = -ballSpeedX
    if ballPosY + ballRadius > windowHeight or ballPosY - ballRadius < 0:
        ballSpeedY = -ballSpeedY

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the ball
    pygame.draw.circle(screen, (255, 0, 0), (ballPosX, ballPosY), ballRadius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.delay(30)

