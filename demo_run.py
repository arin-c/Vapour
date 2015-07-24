import os, sys, pygame,levelEditor,player

pygame.init()
screen_width, screen_height = 500,500
screen = pygame.display.set_mode((screen_width,screen_height))
lEditor = levelEditor.LevelEditor(screen)
player = player.Player(50,50,screen)
quit = False

while(not quit):
    pygame.time.Clock().tick(30)

    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                quit = True
        if(e.type == pygame.QUIT):
            quit = True
    
    lEditor.update()
    screen.fill(0)
    lEditor.draw()
    player.draw()
    pygame.display.flip()
lEditor.getLevel().save('2sweg.txt')
