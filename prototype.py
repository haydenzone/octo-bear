from Tkinter import *

root = Tk()
root.wm_title('Octo-Bear')

Label(root, text='target URL:').pack()
Entry(root).pack()
Button(root, text='GO').pack()


scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

text = Text(root, wrap=WORD, yscrollcommand=scrollbar.set)
text.pack()

scrollbar.config(command=text.yview)


root.mainloop()
