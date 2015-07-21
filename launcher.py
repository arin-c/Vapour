#C:\Python32\python.exe "$(FULL_CURRENT_PATH)" "$(CURRENT_DIRECTORY)" "$(NAME_PART)"
import tkinter as tk
resX, resY = 225, 325
mainWindow = tk.Tk()
m1 = resX*.05
m2 = resY*.3
bWidth = resX-m1*2
bHeight = resY*.1
def play():
    pass
mainWindow.geometry(str(resX)+'x'+str(resY))
mainWindow.wm_title('Vapour Lancher')

playButton = tk.Button(mainWindow, command=play)
levelButton = tk.Button(mainWindow, command=play)
quitButton = tk.Button(mainWindow, command=play)

playButton.place(x=m1, y=m2, width=bWidth, height=bHeight)
levelButton.place(x=m1, y=m2*1.5, width=bWidth, height=bHeight)
quitButton.place(x=m1, y=m2*2, width=bWidth, height=bHeight)

while True:
    mainWindow.update()
