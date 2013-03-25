#$Id: entryfield.py,v 1.2 2004/03/17 04:29:31 mandava Exp $
#this is a program depicting the use of entry field widget.
#entry widgets are basic widgets used to collect input from the user.
def appendstuff():
   global text
   text.config(state=NORMAL)
   text.insert(END, "TEST\n")
   text.config(state=DISABLED)
#entry widgets are limited to a single line of text which can be in only
#one font. 
#the root is also packed with 4 buttons along with the entry widget..

import Tkinter 
from Tkinter import *
root =Tk()
root.title('entry widget')
Label (text='URL:').pack(side=TOP,padx=10,pady=10)
Entry(root, width=40).pack(side=TOP,padx=10,pady=10)
Button(root, text='open', command=appendstuff).pack(side= BOTTOM)
Button(root, text='edit').pack(side= BOTTOM)
Button(root, text='exit').pack(side= BOTTOM)
Button(root, text='close').pack(side= BOTTOM)
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

text = Text(root, wrap=WORD, yscrollcommand=scrollbar.set)
text.insert(END, "TEST\n")
text.insert(END, "TEST\n")
text.insert(END, "TEST\n")
text.insert(END, "TEST\n")
text.insert(END, "TEST\n")
text.insert(END, "TEST\n")
text.config(state=DISABLED)
text.pack()



scrollbar.config(command=text.yview)
root.mainloop()

