import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 20
BALL_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")

# Initialize ball position and speed
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce the ball off the edges
    if ball_x + BALL_RADIUS > WIDTH or ball_x - BALL_RADIUS < 0:
        ball_speed_x = -ball_speed_x
    if ball_y + BALL_RADIUS > HEIGHT or ball_y - BALL_RADIUS < 0:
        ball_speed_y = -ball_speed_y

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the ball
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.delay(30)

