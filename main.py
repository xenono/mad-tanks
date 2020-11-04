import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Tanks")
background = pygame.image.load("assets/background.jpg").convert_alpha()

running = True
while running:

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # Closes the window when pressing X on upper taskbar
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
