import pygame

print('Setup Start')
pygame.init()
window = pygame.display.set_mode(size=( 720, 720))
print('Setup End')

print('Loop Start')
while True:
    # Check for all events
    for event in pygame.event.get():
        # If the event is the quit event, exit the loop
        if event.type == pygame.QUIT:
            print('Quitting...')
            pygame.quit() #Close Window
            quit() #Exit Program