#C:\Python32\python.exe "$(FULL_CURRENT_PATH)" "$(CURRENT_DIRECTORY)" "$(NAME_PART)"
import tkinter as tk
import sys,demo_run
resX, resY = 225, 325
mainWindow = tk.Tk()
m1 = resX*.05
m2 = resY*.3
bWidth = resX-m1*2
bHeight = resY*.1
quit = True

def play():
    demo_run.start()
def level():
    demo_run.start(True)
def quit():
    global quit
    quit = False
mainWindow.geometry(str(resX)+'x'+str(resY))
mainWindow.wm_title('Vapour Lancher')

bImage = tk.PhotoImage('Art\\Logo.png')
backLabel = tk.Label(mainWindow, image=bImage)
playButton = tk.Button(mainWindow, text='Play', command=play)
levelButton = tk.Button(mainWindow, text='Level Editor', command=level)
quitButton = tk.Button(mainWindow, text='Quit', command=quit)

backLabel.place(x=0, y=0, width=resX, height=resY)
playButton.place(x=m1, y=m2, width=bWidth, height=bHeight)
levelButton.place(x=m1, y=m2*1.5, width=bWidth, height=bHeight)
quitButton.place(x=m1, y=m2*2, width=bWidth, height=bHeight)

while quit:
    mainWindow.update()
