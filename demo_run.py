import os, sys, pygame,levelEditor,camera,player

pygame.init()
screen_width, screen_height = 500,500
cam = camera.Camera(screen_width,screen_height)
screen = pygame.display.set_mode((screen_width,screen_height))
lEditor = levelEditor.LevelEditor(screen,cam)
currentLevel = lEditor.getLevel()
player = player.Player(100,50,cam,screen,"images/Player/")
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
            elif(e.key == pygame.K_g):
                lEditor.grid = not(lEditor.grid)
        if(e.type == pygame.QUIT):
            return True
    key = pygame.key.get_pressed()
    if(key[pygame.K_LEFT]):
        player.move("LEFT")
    elif(key[pygame.K_RIGHT]):
        player.move("RIGHT")
    return False
backgroundSurface = pygame.surface.Surface((currentLevel.width,currentLevel.height))
if(hasattr(currentLevel,'background')):
    backgroundSurface.blit(currentLevel.background,(0,0))

while(not quit):
    pygame.time.Clock().tick(45)
    quit = handleEvents()
    lEditor.update()
    player.update()
    cam.centre(player)
    screen.fill(0)
    screen.blit(backgroundSurface,(0,0))
    lEditor.draw()
    player.draw()
    pygame.display.flip()
currentLevel.save('2sweg.txt')
