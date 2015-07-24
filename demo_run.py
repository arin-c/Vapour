import os, sys, pygame,levelEditor,player

pygame.init()
screen_width, screen_height = 500,500
screen = pygame.display.set_mode((screen_width,screen_height))
lEditor = levelEditor.LevelEditor(screen)
player = player.Player(100,50,screen)
player.setLevel(lEditor.getLevel())
pygame.display.set_caption("Vapour")
quit = False

def handleEvents():
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                return True
            elif(e.key == pygame.K_UP):
                player.move("JUMP")
        if(e.type == pygame.QUIT):
            return True
    key = pygame.key.get_pressed()
    if(key[pygame.K_LEFT]):
        player.move("LEFT")
    elif(key[pygame.K_RIGHT]):
        player.move("RIGHT")
    return False

while(not quit):
    pygame.time.Clock().tick(30)
    quit = handleEvents()
    lEditor.update()
    player.update()
    screen.fill(0)
    lEditor.draw()
    player.draw()
    pygame.display.flip()
lEditor.getLevel().save('2sweg.txt')
