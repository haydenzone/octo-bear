from Tkinter import *

def foo(event = None):
    global targetURL
    global workOutput
    s = targetURL.get() + '\n'
    workOutput.config(state = NORMAL)
    workOutput.insert(END, s)
    workOutput.config(state = DISABLED)
    targetURL.set('')



root = Tk()
root.title('Octo-Bear')
root.resizable(0, 0)
root.bind('<Command-q>', foo)



path = 'logo/octobear__bearctopus_by_blazegryph-d4pte5b.gif'

canvas = Canvas(root, width=200, height = 267)
canvas.pack(side=TOP, expand = YES, fill = BOTH)

logo = PhotoImage(file = path)
canvas.create_image(300, 0, image = logo, anchor = N)

frame = Frame(root)

Label(frame, text = 'Target URL:').pack(side = LEFT)
targetURL = StringVar()
urlEntry = Entry(frame, textvariable = targetURL)
urlEntry.bind('<Return>', foo)
urlEntry.pack(side = LEFT, expand = YES, fill = X)
startButton = Button(frame, text = 'Start', command = foo)
startButton.pack(side = RIGHT)


frame.pack(expand = YES, fill = X)

scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = Y)

workOutput = Text(root, wrap = WORD, yscrollcommand = scrollbar.set)
workOutput.config(state = DISABLED)
workOutput.pack()

scrollbar.config(command = workOutput.yview)


root.mainloop()
