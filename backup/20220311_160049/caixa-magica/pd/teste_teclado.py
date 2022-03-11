from tkinter import *
from functools import partial

root = Tk()
root.geometry("200x100")

num_run = 0
btn_funcid = 0


def click(btn):
    global num_run
    text = "%s" % btn
    # if not text == "Del" and not text == "Close":
    #     e.insert(END, text)
    # if text == 'Del':
    #     e.delete(0, END)
    if text == 'Close':
        boot.destroy()
        num_run = 0
        root.unbind('<Button-1>', btn_funcid)


def numpad():
    global num_run, boot
    boot = Tk()
    boot['bg'] = 'green'
    lf = LabelFrame(boot, text=" keypad ", bd=3)
    lf.pack(padx=15, pady=10)
    btn_list = [
        '7',  '8',  '9',
        '4',  '5',  '6',
        '1',  '2',  '3',
        '0',  'Del',  'Close']
    r = 1
    c = 0
    n = 0
    btn = list(range(len(btn_list)))
    for label in btn_list:
        cmd = partial(click, label)
        btn[n] = Button(lf, text=label, width=10, height=5, command=cmd)
        btn[n].grid(row=r, column=c)
        n += 1
        c += 1
        if c == 3:
            c = 0
            r += 1


def close(event):
    global num_run, btn_funcid
    if num_run == 1:
        boot.destroy()
        num_run = 0
        root.unbind('<Button-1>', btn_funcid)


def run(event):
    global num_run, btn_funcid
    if num_run == 0:
        num_run = 1
        numpad()
        btn_funcid = root.bind('<Button-1>', close)


# e = Entry(root, width=10, background='white', textvariable=, justify=CENTER, font='-weight bold')
# e.bind('<Button-1>', run)


# e.grid(padx=10, pady=5, row=17, column=1, sticky='W,E,N,S')
numpad()
root.mainloop()
