def start(editingMode=False):
    import os, sys, pygame,levelEditor,level,camera,player

    def handleEvents():
        for e in pygame.event.get():
            if(e.type == pygame.KEYDOWN):
                if(e.key == pygame.K_ESCAPE):
                    return True
                if(e.key == pygame.K_UP):
                    pc.move("JUMP")
                if(e.key == pygame.K_g):
                    if(editingMode):
                        lEditor.grid = not(lEditor.grid)
                if(e.key == pygame.K_SPACE):
                    pc.attack()
            if(e.type == pygame.QUIT):
                return True
        key = pygame.key.get_pressed()
        if(key[pygame.K_LEFT]):
            pc.move("LEFT")
        elif(key[pygame.K_RIGHT]):
            pc.move("RIGHT")
        elif(not key[pygame.K_SPACE]):
            pc.currentState = "STILL"
        if(editingMode):
            if(key[pygame.K_e]):
                lEditor.blockRotation+=5
            elif(key[pygame.K_q]):
                lEditor.blockRotation-=5
        return False

    pygame.init()
    screen_width, screen_height = 500,500
    cam = camera.Camera(screen_width,screen_height)
    screen = pygame.display.set_mode((screen_width,screen_height))
    if(editingMode):
        lEditor = levelEditor.LevelEditor(screen,cam)
        currentLevel = lEditor.getLevel()
    else:
        currentLevel = level.Level("testLevel.txt",2000,2000,cam,screen)
        currentLevel.setBackground(pygame.image.load("images/sky.png"))
    pc = player.Player(100,50,cam,screen,"images/Player/")
    pc.setLevel(currentLevel)
    pygame.display.set_caption("Vapour")
    quit = False
    backgroundSurface = pygame.surface.Surface((currentLevel.width,currentLevel.height))
    clock = pygame.time.Clock()
    if(hasattr(currentLevel,'background')):
        backgroundSurface.blit(currentLevel.background,(0,0))
    while(not quit):
        clock.tick(30)
        quit = handleEvents()
        if(editingMode):
            lEditor.update()
        pc.update()
        cam.centre(pc)
        screen.fill(0)
        screen.blit(backgroundSurface,(0,0))
        if(editingMode):
            lEditor.draw()
        else:
            currentLevel.draw()
        pc.draw()
        pygame.display.flip()
    currentLevel.save('2sweg.txt')
    pygame.quit()

if(__name__ == "__main__"):
    start(True) #true = level editing mode enabled
