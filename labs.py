from tkinter import *
from math import sqrt,pow
import numpy as np
from json import load, dump
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename


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

def save_draw():
    
    file_name = asksaveasfilename(
            title = "Выберите файл, сэр.",
    )
    if file_name:
        
        dump(lines, open(file_name, 'w'), indent = 2)
    

def load_draw():
    global lines
    file_name = askopenfilename(
        title = "Выберите файл, сэр.",
    )
    
    if file_name:
    
        for line in lines:
            canvas.delete(line['line'])
    
        lines = load(open(file_name))
    
        for line in lines:
            x1 = line['x1']
            y1 = line['y1']
            x2 = line['x2']
            y2 = line['y2']
            color = line['color']
            line['line'] = canvas.create_line(x1, y1, x2, y2, fill=color ,width=2)
        
        update_labels()


def del_selected_line(event):
    global lines
    global canvas
    
    line_to_del = None
    
    for line in lines:
        x1, y1, x2, y2 = canvas.coords(line['line'])
    
        r1 = sqrt(pow(x1 - event.x,2) + pow(y1 - event.y,2))
        r2 = sqrt(pow(x2 - event.x,2) + pow(y2 - event.y,2))
    
        if r1 < 20 or r2 < 20:
            line_to_del = line
    
    if line_to_del != None:
        n = lines.index(line_to_del)
        canvas.delete(lines.pop(n)['line'])
        update_labels()
    
def mouse_click(event):
    global mouse_clicked
    global lines
    global canvas
    global selected_line
    
    if mouse_clicked == 0:
        
        n = 0
    
        for line in lines:
            x1, y1, x2, y2 = canvas.coords(line['line'])
        
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
                selected_line['color'] = canvas.itemconfig(line['line'])['fill'][4]
                selected_line['n'] = n
                canvas.itemconfig(line['line'],fill="red",width=3)
                break
            n += 1
                
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
            
            canvas.coords(line['line'],x1,y1,x2,y2)
            lines[selected_line['n']] = {
                    'line': line['line'], 
                    'x1': x1, 
                    'y1': y1, 
                    'x2': x2, 
                    'y2': y2, 
                    'color': selected_line['color']
                    }
            update_labels()
            
            selected_line['line'] = None
            
            canvas.itemconfig(line['line'],fill=selected_line['color'],width=2)
            
        
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
        
    x1, y1, x2, y2 = 100, 100, 250, 200
    
    line = canvas.create_line(x1, y1, x2, y2, fill=color ,width=2)    
    lines += [{'line': line, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': color}]
    update_labels()

    
def del_line():  
    try:
        canvas.delete(lines.pop()['line'])
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
            x1, y1, x2, y2 = canvas.coords(line['line'])
            sx1, sy1, sx2, sy2 = x1 - 250, 200 - y1, x2 - 250, 200 - y2
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
            x1, y1, x2, y2 = canvas.coords(line['line'])
            x = (x1 + x2)/2
            y = (y1 + y2)/2
            sx1, sy1, sx2, sy2 = x1 - 250, 200 - y1, x2 - 250, 200 - y2
            s = '(x - %s)/%s = (y - %s)/%s'%(sx1,sx2 - sx1, sy1, sy2 - sy1)
            f = canvas.create_text(x, y, text=s, justify=CENTER)
            funcs += [f]
        
def create_window():
    global canvas 
    root = Tk()
    root.title(u'Графический редактор к вашим услугам, сэр.')
    
    root["bg"] = "#ebff9c"
    
    root.geometry('975x700+200+10')
    
    btn_nl=Button(root,text='Прямая, появись!',width=15,height=1,bg='#aad400',
                   fg='black',font='arial 14', command=new_line).place(x=15, y=10)
    
    btn_dl=Button(root,text='Прямая, сгинь!',width=15,height=1,bg='#ff5555',
                   fg='black',font='arial 14', command=del_line).place(x=322, y=10)
    
    btn_sc=Button(root,text='Координаты,\nявитесь!',width=15,height=2,bg='#ffcf55',
                   fg='black',font='arial 14', command=show_coordinates).place(x=15, y=465)
    
    btn_sf=Button(root,text='Уравнение,\nя выбираю тебя!',width=15,height=2,bg='#ffb355',
                   fg='black',font='arial 14', command=show_functions).place(x=15, y=530)
    
    btn_save=Button(root,text='Сохранитесь,\nглупцы!',width=15,height=2,bg='#55ff91',
                   fg='black',font='arial 14', command=save_draw).place(x=322, y=465)
    
    btn_load=Button(root,text='Сказано -\nзагружено.',width=15,height=2,bg='#00d491',
                   fg='black',font='arial 14', command=load_draw).place(x=322, y=530)
    
    btn_T=Button(root,text='Смещение',width=14,height=1,bg='#FFE261',
                   fg='black',font='arial 14', command=load_draw).place(x=520, y=55)
    
    btn_R=Button(root,text='Вращение',width=14,height=1,bg='#FFE261',
                   fg='black',font='arial 14', command=load_draw).place(x=520, y=95)
    
    btn_S=Button(root,text='Масштабирование',width=14,height=1,bg='#FFE261',
                   fg='black',font='arial 14', command=load_draw).place(x=520, y=135)
    
    btn_M=Button(root,text='Зеркалирование',width=14,height=1,bg='#FFE261',
                   fg='black',font='arial 14', command=load_draw).place(x=520, y=175)
    
    btn_P=Button(root,text='Проецирование',width=14,height=1,bg='#FFE261',
                   fg='black',font='arial 14', command=load_draw).place(x=520, y=215)
    
    btn_do=Button(root,text='Выполнить',width=14,height=1,bg='#FF9E61',
                   fg='black',font='arial 14', command=load_draw).place(x=520, y=320)
    
    poetry = "Для создания прямой, нажмите 'Прямая, появись!'.\nДля удаления последней созданной прямой, нажмите 'Прямая, сгинь!'. Для удаления конкретной прямой, нажмите на ее конец ср.кнопкой мыши.\nДля передвижения конца прямой, нажмите на интересующий Вас конец и щелкните на желаемое место.\nДля появления координат прямых, нажмите 'Координаты, явитесь!'.\nДля появления уравнений, нажмите 'Уравнение, я выбираю тебя!'.\nДля сохранения и загрузки файла, нажмите на 'Сохранитесь, глупцы!' и 'Сказано - загружено.' соответственно.\nПриятного пользования!"
    label2 = Label(text=poetry,bg='#e5ff80', justify=LEFT).place(x=15, y=595)
    
    M = [
            [DoubleVar(),DoubleVar(),DoubleVar()],
            [DoubleVar(),DoubleVar(),DoubleVar()],
            [DoubleVar(),DoubleVar(),DoubleVar()]
        ]
    
    message_entry00 = Entry(textvariable=M[0][0],width=5)
    message_entry00.place(x=545, y=265, anchor="c")
    
    message_entry01 = Entry(textvariable=M[0][1],width=5)
    message_entry01.place(x=590, y=265, anchor="c")
    
    message_entry02 = Entry(textvariable=M[0][2],width=5)
    message_entry02.place(x=635, y=265, anchor="c")
    
    message_entry10 = Entry(textvariable=M[1][0],width=5)
    message_entry10.place(x=545, y=285, anchor="c")
    
    message_entry11 = Entry(textvariable=M[1][1],width=5)
    message_entry11.place(x=590, y=285, anchor="c")
    
    message_entry12 = Entry(textvariable=M[1][2],width=5)
    message_entry12.place(x=635, y=285, anchor="c")
    
    message_entry20 = Entry(textvariable=M[2][0],width=5)
    message_entry20.place(x=545, y=305, anchor="c")
    
    message_entry21 = Entry(textvariable=M[2][1],width=5)
    message_entry21.place(x=590, y=305, anchor="c")
    
    message_entry22 = Entry(textvariable=M[2][2],width=5)
    message_entry22.place(x=635, y=305, anchor="c")

    
    canvas = Canvas(root,bg='#f3ffc5')
    canvas.place(x=15, y=55, width=500, height=400)
    canvas.bind("<Button-1>" ,mouse_click)
    canvas.bind("<Button-2>" ,del_selected_line)

    canvas.create_line(250,0, 250,400, fill="#aad400")    
    canvas.create_line(0,200, 500,200, fill="#aad400")    

    for x in np.linspace(-250,250,11):
        canvas.create_line(x + 250, 195, x + 250, 205, fill="#aad400") 
        canvas.create_text(x + 250, 215, text = str(x), justify=CENTER, fill="#aad400")
        
    for y in np.linspace(-200,200,11):
        if y != 0:
            canvas.create_line(245, 200 - y, 255, 200 - y, fill="#aad400") 
            canvas.create_text(280, 200 - y, text = str(y), fill="#aad400")

    
    return root
    
    
if __name__ == '__main__':
    root = create_window()
    root.mainloop()