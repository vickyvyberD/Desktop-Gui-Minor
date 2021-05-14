from tkinter import *
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageGrab
from os import path
import win32gui
import cnt2 as c
from tkinter.colorchooser import askcolor


class MainApplication(tk.Frame):
    currx, curry = 0, 0

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.top = tk.Frame(self.parent, width=600, height=400, )
        self.top.pack(side=tk.TOP)

        self.bottom = tk.Frame(self.parent, width=600, height=400, )
        self.bottom.pack(side=tk.BOTTOM,fill = tk.BOTH)

        self.topleft = tk.Frame(self.top, width=600, height=600,)
        self.topleft.pack(side=tk.LEFT, fill=tk.X)

        self.topright = tk.Frame(self.top, width=200, height=400,)
        self.topright.pack(side=tk.RIGHT)

        self.bottomright = tk.Frame(self.bottom, width=200, height=200,)
        self.bottomright.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self.topleft, background='white', height=170, width=500)
        self.canvas.bind('<Button-1>', self.locate_point)
        self.canvas.bind('<B1-Motion>', self.draw_line)
        self.canvas.grid(padx=20, pady=20, row=0, column=0)
        # save postscipt image 
        
        self.theme = 'blue'
        self.button_theme ='light' + self.theme
        self.save_button = tk.Button(self.topright, text="Save", font=('Cambria'),command=self.save, padx=20,)
        self.save_button.grid(padx=15, pady=15, row=0, column=0)

        self.clear_button = tk.Button(self.topright, text='Clear', font=('Cambria'),command=self.clear, padx=20,)
        self.clear_button.grid(padx=15, pady=15, row=1, column=0)

        self.browser_button = tk.Button(self.topright, text="Browse",font=('Cambria'),command = self.file_browse , padx = 20,)
        self.browser_button.grid(padx=15,pady=15,row=2,column = 0 )

        self.color_button = Button(self.topright, text = "Button_Theme",font=('Cambria'), command = self.choose_color,padx = 20,) 
        self.color_button.grid(padx=15,pady=15,row=3,column=0) 
        
        self.entire_color_button = Button(self.topright, text = "Theme",font=('Cambria'), command = self.choose_color2,padx = 20,) 
        self.entire_color_button.grid(padx=15,pady=15,row=4,column=0)
  
         
        
        # output frame
        self.bottomleft = tk.LabelFrame(self.bottom, width=400, height=200)
         
        self.bottomleft.pack(side=tk.LEFT, fill=tk.X)

        self.label = tk.Label(self.bottomleft,text=' '*8,font = ('Consolas',30))
        self.label.grid(row=0,column=1,padx = 5,pady=5)

        # output frame end

        self.proceed_button = tk.Button(self.bottomright, text="Predict",font=('Cambria'), command=self.run, padx=20)
        self.proceed_button.grid(padx=20, pady=20, row=0, column=0)

        self.abort_button = tk.Button(self.bottomright, text="Abort",font=('Cambria'),fg = 'red', command=close_window, padx=20)
        self.abort_button.grid(padx=20, pady=20, row=1, column=0)

        
        # self.img = None 
        self.file_img = None
    
    def choose_color(self): 
  
            # variable to store hexadecimal code of color 
            color_code = askcolor()[1]  
            self.button_theme = color_code  

            self.save_button.config(bg=self.button_theme)  
            self.browser_button.config(bg=self.button_theme) 
            self.clear_button.config(bg=self.button_theme)    
    def choose_color2(self): 
  
            # variable to store hexadecimal code of color 
            color_code = askcolor()[1]  
            self.theme = color_code  
            self.top.config(background=self.theme)
            self.bottom.config(background=self.theme)
            self.topleft.config(background=self.theme)
            self.bottomleft.config(background=self.theme)
            self.topright.config(background=self.theme)
            self.bottomright.config(background=self.theme)
    def locate_point(self, event):
        MainApplication.currx = event.x
        MainApplication.curry = event.y

    def draw_line(self, event):
        self.canvas.create_line(MainApplication.currx, MainApplication.curry, event.x, event.y,width=3)
        
        MainApplication.currx = event.x
        MainApplication.curry = event.y


    def save(self):
        
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        im = ImageGrab.grab(rect)  
        #self.canvas.postscript(file = 'temp' + '.eps') 
        # use PIL to convert to PNG 
        #im = Image.open("temp.eps")
        im.save("temp.png",lossless=True)
        
    def clear(self):
        self.canvas.delete("all")


    def run(self):
        #image grab method
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        im = ImageGrab.grab(rect)

        #save method
        if (self.file_img == None ) :
            img='temp.png'
        else : 
            img = self.file_img 
            self.file_img = None 
        val = c.run(img)+' = '+str(eval(c.run(img)))
        self.label.configure(text = val, font =('Cambria',20,'bold'))

    

    def file_browse(self):
        img_file = tkinter.filedialog.askopenfile()
        self.file_img  = img_file.name 
    
    def abort(self):
        self.destroy()

def close_window():
    root.destroy()        

if __name__ == "__main__":
    root = tk.Tk()
    root.title('RECOGNITION APPLICATION')
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
