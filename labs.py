from tkinter import *
from math import sqrt,pow
import numpy as np
from json import load, dump

root = None
canvas = None
mouse_clicked = 0
lines = []
coords = []
funcs = []
selected_line = {
    'line': None, 
    'end': 0,
    'x1,y1': [],
    'x2,y2': [],
}
coords_visible = 0
funcs_visible = 0

colors = load(open('colors.json'))
last_color = 0

def del_selected_line(event):
    global lines
    global canvas
    
    line_to_del = None
    
    for line in lines:
        x1, y1, x2, y2 = canvas.coords(line)
    
        r1 = sqrt(pow(x1 - event.x,2) + pow(y1 - event.y,2))
        r2 = sqrt(pow(x2 - event.x,2) + pow(y2 - event.y,2))
    
        if r1 < 20 or r2 < 20:
            line_to_del = line
    
    if line_to_del != None:
        n = lines.index(line_to_del)
        canvas.delete(lines.pop(n))
        update_labels()
    
def mouse_click(event):
    global mouse_clicked
    global lines
    global canvas
    global selected_line
    
    if mouse_clicked == 0:
    
        for line in lines:
            x1, y1, x2, y2 = canvas.coords(line)
        
            r1 = sqrt(pow(x1 - event.x,2) + pow(y1 - event.y,2))
            r2 = sqrt(pow(x2 - event.x,2) + pow(y2 - event.y,2))
        
            if r1 < 10:
                selected_line['line'] = line
                selected_line['end'] = 0
                selected_line['x2,y2'] = [x2,y2]
                mouse_clicked = 1
            if r2 < 10:
                selected_line['line'] = line
                selected_line['end'] = 1
                selected_line['x1,y1'] = [x1,y1]
                mouse_clicked = 1
            if  mouse_clicked:
                selected_line['color'] = canvas.itemconfig(line)['fill'][4]
                canvas.itemconfig(line,fill="red",width=3)
                break
                
    else:
        mouse_clicked = 0
        line = selected_line['line']
        if line != None:
            
            if selected_line['end'] == 0:
                x1, y1 = event.x, event.y  
                x2, y2 = selected_line['x2,y2']
                
            if selected_line['end'] == 1:
                x2, y2 = event.x, event.y
                x1, y1 = selected_line['x1,y1']
            
            canvas.coords(line,x1,y1,x2,y2)
            update_labels()
            
            selected_line['line'] = None
            
            canvas.itemconfig(line,fill=selected_line['color'],width=2)
            
        
def update_labels():
    show_coordinates()
    show_coordinates()
    show_functions()
    show_functions()

def new_line():   
    global canvas
    global lines
    global last_color
    
    try:
        color = colors[last_color]
        last_color += 1
        
    except IndexError:
        last_color = 0
        color = colors[last_color]
    
    line = canvas.create_line(50,50,200,200,fill=color ,width=2)    
    lines += [line]
    update_labels()

    
def del_line():  
    try:
        canvas.delete(lines.pop())
    except IndexError:
        pass
    update_labels()

    
def show_coordinates():
    global coords_visible
    global canvas
    global coords
    
    if coords_visible:
        coords_visible = 0
        try:
            while 1:
                canvas.delete(coords.pop())
        except IndexError:
            pass
            
    else:
        coords_visible = 1
        for line in lines:
            x1, y1, x2, y2 = canvas.coords(line)
            sx1, sy1, sx2, sy2 = x1 - 235, 165 - y1, x2 - 235, 165 - y2
            A = canvas.create_text(x1, y1, text="(%s,%s)"%(sx1,sy1), justify=CENTER)
            B = canvas.create_text(x2, y2, text="(%s,%s)"%(sx2,sy2), justify=CENTER)
            coords += [A]
            coords += [B]
    
def show_functions():
    global funcs_visible
    global canvas
    global funcs
    
    if funcs_visible:
        funcs_visible = 0
        try:
            while 1:
                canvas.delete(funcs.pop())
        except IndexError:
            pass        
    else:
        funcs_visible = 1
        for line in lines:
            x1, y1, x2, y2 = canvas.coords(line)
            x = (x1 + x2)/2
            y = (y1 + y2)/2
            sx1, sy1, sx2, sy2 = x1 - 235, 165 - y1, x2 - 235, 165 - y2
            s = '(x - %s)/%s = (y - %s)/%s'%(sx1,sx2 - sx1, sy1, sy2 - sy1)
            f = canvas.create_text(x, y, text=s, justify=CENTER)
            funcs += [f]
        
def create_window():
    global canvas 
    root = Tk()
    root.title(u'Графический редактор к вашим услугам, сэр.')
    
    root["bg"] = "#e5ff80"
    
    root.geometry('500x500+300+100')
    
    btn_nl=Button(root,text='Прямая, появись!',width=15,height=1,bg='#aad400',
                   fg='black',font='arial 14', command=new_line).place(x=10, y=5)
    btn_dl=Button(root,text='Прямая, сгинь!',width=15,height=1,bg='#ff5555',
                   fg='black',font='arial 14', command=del_line).place(x=295, y=5)
    btn_sc=Button(root,text='Координаты, явитесь!',width=23,height=1,bg='#ffcf55',
                   fg='black',font='arial 14', command=show_coordinates).place(x=10, y=400)
    btn_sf=Button(root,text='Уравнение, я выбираю тебя!',width=23,height=1,bg='#ffb355',
                   fg='black',font='arial 14', command=show_functions).place(x=10, y=450)
    
    canvas = Canvas(root,bg='#f3ffc5')
    canvas.place(x=15, y=55, width=470, height=330)
    canvas.bind("<Button-1>" ,mouse_click)
    canvas.bind("<Button-2>" ,del_selected_line)

    canvas.create_line(235,0, 235,330, fill="#aad400")    
    canvas.create_line(0,165, 470,165, fill="#aad400")    

    for x in np.linspace(-230,230,11):
        canvas.create_line(x + 235, 160, x + 235, 170, fill="#aad400") 
        canvas.create_text(x + 235, 175, text = str(x), justify=CENTER, fill="#aad400")
        
    for y in np.linspace(-160,160,11):
        if y != 0:
            canvas.create_line(230, 165 - y, 240, 165 - y, fill="#aad400") 
            canvas.create_text(260, 165 - y, text = str(y), fill="#aad400")

    
    return root
    
    
if __name__ == '__main__':
    root = create_window()
    root.mainloop()