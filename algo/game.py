import tkinter as tk
from tkinter import *
from tkinter import messagebox
import cv2
import numpy as np
'''top = Tk()

C = Canvas(top, bg="grey", height=500, width=1000)
filename = PhotoImage(file = "gameboard.png")
background_label = Label(top, image=filename)
background_label.place(x=0, y=0)

C.pack()
top.mainloop()'''

'''img = cv2.imread('gameboard.png', 0)

width,height = img.shape
for col in range(width):
    for row in range(height):
        if img[col][row] <127:
            img[col][row] = 255

backtorgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
for col in range(width):
    for row in range(height):
        if np.array_equal([255,255,255], backtorgb[col][row]):
            backtorgb[col][row] = [46,244,41]


img2 = np.zeros((500,500, 3), dtype = "uint8")
img_3 = cv2.addWeighted(img2,0.5,backtorgb,0.5,0)
cv2.imwrite('board_overlay.png',img_3)'''



#print(board)
