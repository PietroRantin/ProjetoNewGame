import pygame as pg

# ctr + alt + l (formatar pep8)

print('Start Setup')
pg.init()
tela = pg.display.set_mode(size=(640, 480))
print('End Setup')

print('Start Loop')
while True:
    # Check for all events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()  # Close Window
            quit()  # End Pygame
