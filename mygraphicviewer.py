import os
#from tkinter import *
#from tkinter import filedialog
from customtkinter import *

window = CTk()

def drawTile(pixels):
    twoBitColorsList = ["00", "01", "10", "11"]
    colors = ["black", "#555555", "#888888", "white"]
    #tileWin = CTk()
    #tileWin = "Tile Viewer"
    #w = 0
    #h = 0
    #tileBlockSize = 30
    #w_max = 8*tileBlockSize#width*tileBlockSize
    #h_max = 8*tileBlockSize
    #tileCanvas = CTkCanvas(tileWin, height=h_max, width=w_max)
    #for p in pixels:
    #    tileCanvas.create_rectangle(w,h,w+tileBlockSize,h+tileBlockSize, fill=colors[twoBitColorsList.index(p)])
    #    w += tileBlockSize
    #    if h >= h_max:
    #        break
    #    if w >= w_max:
    #        w = 0
    #        h += tileBlockSize
    #tileCanvas.pack()
    #tileWin.mainloop()


def canvasDelete():
    global width
    canvas.create_rectangle(0,0,512,width, fill="black")
    
def bytesToBinStr(b):
    s = ""
    for x in b:
        s_ = bin(x)[2:]
        while len(s_) != 8:
            s_ = "0" + s_
        s = s + s_
    return s
    
def drawFromPos(event):
    global file
    draw(file)
    
def draw(file):
    global canvas
    global startOffset
    global width
    global state
    global wayToDraw
    bpp = wayToDraw.get()
    match bpp:
        case "2bpp":
            tileMode = True
            startOffset = int(offsetEntry.get())
            width = int(widthEntry.get())-3
            canvas.configure(width=width)
            canvasDelete()
            h = 0
            w = 0
            h_max = 512
            w_max = width
            bitToColor = {"00": "#000000",
                          "1": "#444444",
                          "10": "#888888",
                          "11": "#FFFFFF"}
            field = file[int(startOffset):int(startOffset)+h_max*(w_max//2)]
            for b in field:
                b = bin(b)[2:]
                while len(b) != 8:
                    b = "0"+b
                pixels = [b[0:2], b[2:4], b[4:6], b[6:8]]
                twoBitColorsList = ["00", "01", "10", "11"]
                colors = ["black", "#555555", "#888888", "white"]
                for p in pixels:
                    canvas.create_line(w,h,w+1,h, fill=colors[twoBitColorsList.index(p)])
                    w += 1
                if h >= h_max:
                    break
                if w >= w_max:
                    w = 0
                    h += 1
                    
        case "2bpp NES":
            tileMode = True
            startOffset = int(offsetEntry.get())
            width = int(widthEntry.get())
            canvas.configure(width=width)
            canvasDelete()
            h = 0
            w = 0
            h_max = 512
            w_max = width
            field = file[int(startOffset):int(startOffset)+h_max*(w_max//2)]
            
            for tile in range(0, len(field), 16):
                tileFirstHalf = bytesToBinStr(field[tile:tile+8])
                tileSecondHalf = bytesToBinStr(field[tile+8:tile+16])
                pixels = []
                
                for i in range(len(tileFirstHalf)):
                    pixels.append(tileFirstHalf[i]+tileSecondHalf[i])
                twoBitColorsList = ["00", "01", "10", "11"]
                colors = ["black", "#555555", "#888888", "white"]
                w_max = width
                drawTile(pixels)
                for p in pixels:
                    canvas.create_line(w,h,w+1,h, fill=colors[twoBitColorsList.index(p)])
                    w += 1
                    if h >= h_max:
                        break
                    if w % 8 == 0:
                        w = w - 8
                        h += 1
                        if h % 8 == 0:
                            w = w + 8
                            h = h - 8
                            if w >= w_max:
                                w = 0
                                h = h + 8
                
        case "4bpp":
            tileMode = False
            startOffset = int(offsetEntry.get())
            width = int(widthEntry.get())-2
            canvas.configure(width=width)
            canvasDelete()
            h = 0
            w = 0
            h_max = 512
            w_max = width
            field = file[int(startOffset):int(startOffset)+h_max*(w_max//2)]
            for b in field:
                b = hex(b)[2:]
                b_ = b[-1]
                b = b[0]
                color = "#"+(b_*6)
                color2 = "#"+(b*6)
                #print(color)
                #print(color2)
                canvas.create_line(w,h,w+1,h, fill=color)
                canvas.create_line(w+1,h,w+2,h, fill=color2)
                if h >= h_max:
                    break
                if w >= w_max:
                    w = 0
                    h += 1
                else:
                    w += 2
        case "8bpp":
            tileMode = False
            startOffset = int(offsetEntry.get())
            width = int(widthEntry.get())-1
            canvas.configure(width=width)
            canvasDelete()
            h = 0
            w = 0
            h_max = 512
            w_max = width
            
            field = file[int(startOffset):int(startOffset)+h_max*w_max]
            for b in field:
                    b = hex(b)[2:]
                    color = "#"+b+b+b
                    
                    canvas.create_line(w,h,w+1,h, fill=color)
                    if h == h_max:
                        break
                    if w == w_max:
                        w = 0
                        h += 1
                    else:
                        w += 1

                        
        case "32bppRGBA":
            tileMode = False
            startOffset = int(offsetEntry.get())
            width = int(widthEntry.get())-1
            canvas.configure(width=width)
            canvasDelete()
            h = 0
            w = 0
            h_max = 512
            w_max = width
            field = file[int(startOffset):int(startOffset)+h_max*(w_max*4)]
            for b in range(0, len(field), 4):
                
                r = field[b]
                g = field[b+1]
                a = field[b+3]
                b = field[b+2]
                
                a = a / 255
                r = int(r * a)
                g = int(g * a)
                b = int(b * a)
                
                r = hex(r)[2:]
                g = hex(g)[2:]
                b = hex(b)[2:]
                
                while len(r) < 2: r = "0"+r
                while len(g) < 2: g = "0"+g
                while len(b) < 2: b = "0"+b
                
                color = "#"+r+g+b
                
                canvas.create_line(w,h,w+1,h, fill=color)
                if h == h_max:
                    break
                if w == w_max:
                    w = 0
                    h += 1
                else:
                    w += 1
                    
        case _: print("error")
    
def displayMousePos(event):
    global mouseLabel
    global width
    offsetstr = str(((event.y-1)*width)+event.x)
    mouseLabel.configure(text=f"Mouse: x={event.x}, y={event.y}\nOffset={offsetstr}", justify=LEFT, width=30)

def newFile():
    global canvas
    global startOffset
    global file
    path = filedialog.askopenfilename()
    if not os.path.isfile(path):
        return 1
    filename = path.split("/")[-1]
    print(filename)
    with open(path, 'rb') as file:
        file = file.read()
        draw(file)

CTkLabel(window, text="Initial offset: ").grid(row=0, column=1)
CTkLabel(window, text="Width: ").grid(row=1, column=1)
CTkLabel(window, text="Tile size [width, height]: ").grid(row=2, column=1)

startOffset = 0
offsetEntry = CTkEntry(window)
offsetEntry.insert(0, str(startOffset))

width = 256
widthEntry = CTkEntry(window)
widthEntry.insert(0, str(width))

tileWEntry = CTkEntry(window)
tileWEntry.insert(0, str(8))

tileHEntry = CTkEntry(window)
tileHEntry.insert(0, str(8))

openButton = CTkButton(window, text="Open file", command=newFile).grid(row=0, column=3)
cleanButton = CTkButton(window, text="Clean canvas", command=canvasDelete).grid(row=1, column=3)

mouseLabel = CTkLabel(window, text=f"Click to display \nmouse position.", justify=LEFT, width=20)

canvas = CTkCanvas(window, height=512, width=512)
canvas.create_rectangle(0,0,512,512, fill="black")
canvas.bind('<Button-1>', displayMousePos)

offsetEntry.bind('<Return>', drawFromPos)
offsetEntry.grid(row=0, column=2)

widthEntry.bind('<Return>', drawFromPos)
widthEntry.grid(row=1, column=2)

tileWEntry.grid(row=2, column=2)
tileHEntry.grid(row=2, column=3)

canvas.grid(row=5,column=0, columnspan=4)
mouseLabel.grid(row=6, column=0)

CTkLabel(window, text="Choose a draw method:").grid(row=6, column=2,sticky=SE)

wayToDrawList = ["2bpp", "2bpp NES", "4bpp", "8bpp", "32bppRGBA"]
wayToDraw = CTkComboBox(window, values=wayToDrawList)
wayToDraw.grid(row=6, column=3, sticky=SE)
wayToDraw.set("8bpp")

window.title(f"RawGraphicViewer")
window.resizable(height=False, width=False)
window.mainloop()
