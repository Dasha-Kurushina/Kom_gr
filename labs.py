from tkinter import *
from math import sqrt,pow
import numpy as np
from json import load, dump
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk  


root = None
canvas = None
img_cnv = None
img_mov = None
img_mir = None
img_pro = None
img_rot = None
img_scl = None
img_lab = None
mouse_clicked = 0
lines = []
coords = []
funcs = []
selected_line = {
    'line': None, 
    'end': -1,
    'x1,y1': [],
    'x2,y2': [],
}
selected_lines = []
coords_visible = 0
funcs_visible = 0
f_xy = lambda matr, x, y: (x, y)

matr = []

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

def display_image(image):
    global img_lab
    global root
    
    try:
        img_lab.destroy()
    except AttributeError:
        pass
    
    img_lab = Label(root, image=image, bg='#ebff9c')
    img_lab.place(x= 520, y=450, width=400, height=101)


def read_matr(matr):
    a, b, p = matr[0][0].get(), matr[0][1].get(), matr[0][2].get() 
    c, d, q = matr[1][0].get(), matr[1][1].get(), matr[1][2].get()
    e, f, s = matr[2][0].get(), matr[2][1].get(), matr[2][2].get()
    return a, b, c, d, e, f, p, q, s
       
def смещение():
    def f_mov(matr, x, y):
        a, b, c, d, e, f, p, q, s = read_matr(matr)
        x1 = x + e
        y1 = y + f
        return x1, y1  
    
    global f_xy
    global img_mov


    matr[0][0].set(1), matr[0][1].set(0), matr[0][2].set(0) 
    matr[1][0].set(0), matr[1][1].set(1), matr[1][2].set(0)
    matr[2][0].set(50),matr[2][1].set(40), matr[2][2].set(1)
    f_xy = f_mov
    
    display_image(img_mov)
    

def масштабирование():
    def f_scl(matr, x, y):
        a, b, c, d, e, f, p, q, s = read_matr(matr)
        x1 = a * x
        y1 = d * y
        return x1, y1
    
    global f_xy
    global img_scl
    
    matr[0][0].set(0.5), matr[0][1].set(0), matr[0][2].set(0) 
    matr[1][0].set(0), matr[1][1].set(0.4), matr[1][2].set(0)
    matr[2][0].set(0),matr[2][1].set(0), matr[2][2].set(1)
    f_xy = f_scl
    
    display_image(img_scl)


def зеркалирование():    
    def f_mir(matr, x, y):
        a, b, c, d, e, f, p, q, s = read_matr(matr)
        x1 = a * x + c * y + e
        y1 = b * x + d * y + f
#        z1 = p * x + q * y + s
#        x1 *= z1
#        y1 *= z1
        return x1, y1  
    
    global img_mir
    
    global f_xy
    matr[0][0].set(-1), matr[0][1].set(0), matr[0][2].set(0) 
    matr[1][0].set(0), matr[1][1].set(1), matr[1][2].set(0)
    matr[2][0].set(0),matr[2][1].set(0), matr[2][2].set(1)
    f_xy = f_mir
    
    display_image(img_mir)


def вращение():
    def f_rot(matr, x, y):
        a, b, c, d, e, f, p, q, s = read_matr(matr)
        a, b, c, d = radians(a), radians(b), radians(c), radians(d)
        x1 = x * cos(a) - y * sin(c)
        y1 = x * sin(b) + y * cos(d)

        return x1, y1  
    
    global img_rot
    
    global f_xy
    matr[0][0].set(30), matr[0][1].set(30), matr[0][2].set(0) 
    matr[1][0].set(30), matr[1][1].set(30), matr[1][2].set(0)
    matr[2][0].set(0),  matr[2][1].set(0),  matr[2][2].set(1)
    f_xy = f_rot
    
    display_image(img_rot)


def проецирование():
    def f_pro(matr, x, y):
        a, b, c, d, e, f, p, q, s = read_matr(matr)
        x1 = x / (p * x + q * y + 1)
        y1 = y / (p * x + q * y + 1)
        return x1, y1
    
    global img_pro
    
    global f_xy
    matr[0][0].set(1), matr[0][1].set(0), matr[0][2].set(20) 
    matr[1][0].set(0), matr[1][1].set(1), matr[1][2].set(30)
    matr[2][0].set(0),  matr[2][1].set(0),  matr[2][2].set(1)
    f_xy = f_pro
    
    display_image(img_pro)

        
def transform():
    for line in canvas.find_withtag("selected"):        
        coords = canvas.coords(line)
        coords_new = []
        a, b, p = matr[0][0].get(), matr[0][1].get(), matr[0][2].get() 
        c, d, q = matr[1][0].get(), matr[1][1].get(), matr[1][2].get()
        e, f, s = matr[2][0].get(),-matr[2][1].get(), matr[2][2].get()
        for i in range(len(coords) // 2):        
            x, y = coords[i * 2] - 250, 200 - coords[i * 2 + 1]       
            x1,y1 = f_xy(matr, x, y)
            coords_new += [x1 + 250, 200 - y1]
        canvas.coords(line, coords_new)
    
    
def calc_cos():
    matr[0][0].set(cos(radians(matr[0][0].get())))
    matr[1][1].set(cos(radians(matr[1][1].get())))

def calc_sin():
    matr[1][0].set(-sin(radians(matr[1][0].get())))
    matr[0][1].set( sin(radians(matr[0][1].get())))
    
def mouse_click(event):
    def move(event):
        end = selected_line['end']
        line = selected_line['line']
        
        _c = canvas.coords(line)
        __c = []
        for  i in range(0, len(_c)//2):
            x,y = (_c[i * 2], _c[i * 2 + 1])
            if (x,y) == end:
                x_n, y_n = event.x,event.y
                __c += [x_n, y_n]
                selected_line['end'] = (x_n, y_n)
            else:
                __c += [x, y]
        canvas.coords(line, __c)
        
    def stop_move(event):
        canvas.bind("<B1-Motion>", lambda x: x)
        canvas.bind("<ButtonRelease-1>", lambda x: x)
        canvas.itemconfig(current,fill=selected_line['color'],width=2)
        lines[selected_line['n']] = {
            'line': line['line'], 
            'coords': canvas.coords(selected_line['line']),
            'color': selected_line['color']
        }
        print(lines)

    global mouse_clicked
    global lines
    global canvas
    global selected_line
    
    try:
        current = canvas.find_withtag("current")[0]        
        m = 0

        for line in lines:
            if line['line'] == current:
                _c = canvas.coords(current)
                selected_line['line'] = current
                x1,y1 = (_c[0], _c[1])
                for i in range(1, len(_c)//2):
                    x2,y2 = (_c[i * 2], _c[i * 2 + 1])
                    r1 = sqrt(pow(x1 - event.x,2) + pow(y1 - event.y,2))
                    r2 = sqrt(pow(x2 - event.x,2) + pow(y2 - event.y,2))
                    if r1 < 10:
                        selected_line['end'] = (x1, y1)
                    elif r2 < 10:
                        selected_line['end'] = (x2, y2)
                    else:
                        x, y = (event.x, event.y)
                        if x1 < x < x2 and y1 < y < y2:
                            selected_line['end'] = (x, y)
                            n = i * 2
                    x1,y1 = x2,y2
                try:
                    _c.insert(n, y)
                    _c.insert(n, x)
                    canvas.coords(current, _c)
                except NameError:
                    pass
                
                selected_line['n'] = m
                selected_line['line'] = current
                selected_line['color'] = canvas.itemconfig(current)['fill'][4]
                canvas.itemconfig(current,fill="red",width=4)
                canvas.bind("<B1-Motion>", move)
                canvas.bind("<ButtonRelease-1>", stop_move)
            m += 1
                
    except IndexError:
        pass
    
        
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
    
    line = canvas.create_line(x1, y1, x2, y2, fill=color, tags=color ,width=2, activewidth=4)    
    lines += [{'line': line, 'coords': [x1,  y1,  x2,  y2], 'color': color}]
    update_labels()
    

    
def select_line(event):
    global canvas
    try:        
        current = canvas.find_withtag("current")[0]  
        print(canvas.gettags(current))
        assert 'dont_touch' not in canvas.gettags(current)
        canvas.addtag('selected', 'withtag', 'current')
        canvas.itemconfig('selected',fill="red",width=3)
    except (IndexError, AssertionError):
        for line in canvas.find_withtag("selected"):
            color = [ x for x in canvas.gettags(line) if x[0] == '#' ][0]
            canvas.itemconfig(line, fill=color)
        canvas.dtag('selected', 'selected')
    

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
    global matr
    global img_mov
    global img_mir
    global img_pro
    global img_rot
    global img_scl
    global img_lab
    
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
    
    btn_T=Button(root,text='Смещение',width=14,height=1,bg='#FFE180',
                   fg='black',font='arial 14', command=смещение).place(x=520, y=195)

    btn_R=Button(root,text='Вращение',width=14,height=1,bg='#FFE180',
                   fg='black',font='arial 14', command=вращение).place(x=520, y=235)

    btn_S=Button(root,text='Масштабирование',width=14,height=1,bg='#FFE180',
                   fg='black',font='arial 14', command=масштабирование).place(x=520, y=275)

    btn_M=Button(root,text='Зеркалирование',width=14,height=1,bg='#FFE180',
                   fg='black',font='arial 14', command=зеркалирование).place(x=520, y=315)
    
    btn_P=Button(root,text='Проецирование',width=14,height=1,bg='#FFE180',
                   fg='black',font='arial 14', command=проецирование).place(x=520, y=355)
    
    btn_transform=Button(root,text='Разрешите выполнить',width=27,height=1,bg='#FFE261',
                   fg='black',font='arial 14', command=transform).place(x=520, y=400)
    
    poetry = " Сударь, заполните числами \n данную матрицу преобразований: "
    label2 = Label(text=poetry,font="Arial 14",bg='#FFE261', justify=LEFT).place(x=520, y=55)
    
    matr = [
            [DoubleVar(),DoubleVar(),DoubleVar()],
            [DoubleVar(),DoubleVar(),DoubleVar()],
            [DoubleVar(),DoubleVar(),DoubleVar()]
        ]
    
    message_entry00 = Entry(textvariable=matr[0][0],width=5)
    message_entry00.place(x=545, y=130, anchor="c")
    
    message_entry01 = Entry(textvariable=matr[0][1],width=5)
    message_entry01.place(x=590, y=130, anchor="c")
    
    message_entry02 = Entry(textvariable=matr[0][2],width=5)
    message_entry02.place(x=635, y=130, anchor="c")
    
    message_entry10 = Entry(textvariable=matr[1][0],width=5)
    message_entry10.place(x=545, y=150, anchor="c")
    
    message_entry11 = Entry(textvariable=matr[1][1],width=5)
    message_entry11.place(x=590, y=150, anchor="c")
    
    message_entry12 = Entry(textvariable=matr[1][2],width=5)
    message_entry12.place(x=635, y=150, anchor="c")
    
    message_entry20 = Entry(textvariable=matr[2][0],width=5)
    message_entry20.place(x=545, y=170, anchor="c")
    
    message_entry21 = Entry(textvariable=matr[2][1],width=5)
    message_entry21.place(x=590, y=170, anchor="c")
    
    message_entry22 = Entry(textvariable=matr[2][2],width=5)
    message_entry22.place(x=635, y=170, anchor="c")

    
    img_mov = ImageTk.PhotoImage(file = "img/mov.png")
    img_mir = ImageTk.PhotoImage(file = "img/mir.png")
    img_pro = ImageTk.PhotoImage(file = "img/pro.png")
    img_rot = ImageTk.PhotoImage(file = "img/rot.png")
    img_scl = ImageTk.PhotoImage(file = "img/scl.png")
    img_lab = Label(root)
    
    canvas = Canvas(root,bg='#f3ffc5')
    canvas.place(x=15, y=55, width=500, height=400)
    canvas.bind("<Button-1>" ,mouse_click)
    canvas.bind("<Button-2>" ,del_selected_line)
    canvas.bind("<Shift-Button-1>" ,select_line)

    canvas.create_line(250,0, 250,400, fill="#aad400", tags = 'dont_touch')    
    canvas.create_line(0,200, 500,200, fill="#aad400", tags = 'dont_touch')    

    for x in np.linspace(-250,250,11):
        canvas.create_line(x + 250, 195, x + 250, 205, fill="#aad400", tags = 'dont_touch') 
        canvas.create_text(x + 250, 215, text = str(x), justify=CENTER, fill="#aad400", tags = 'dont_touch')
        
    for y in np.linspace(-200,200,11):
        if y != 0:
            canvas.create_line(245, 200 - y, 255, 200 - y, fill="#aad400", tags = 'dont_touch') 
            canvas.create_text(280, 200 - y, text = str(y), fill="#aad400", tags = 'dont_touch')

    
    return root
    
    
if __name__ == '__main__':
    root = create_window()
    root.mainloop()