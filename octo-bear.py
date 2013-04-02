from Tkinter import *
from OctoBearFormHandler import OctoBearFormHandler
from OctoBearCrawler import OctoBearCrawler


class OctoBearApp:
    def __init__(self, root):
        root.title('Octo-Bear')
        root.resizable(0, 0)
        root.bind('<Control-q>', self.quit)
        
        class IORedirector(object):
            def __init__(self, widget):
                self.widget = widget
        
        class StdoutRedirector(IORedirector):
            def write(self, s):
                self.widget.config(state = NORMAL)
                self.widget.insert(END, str(s))
                #self.TEXT_INFO.config(text=self.TEXT_INFO.cget('text') + str)
                self.widget.config(state = DISABLED)

        self.path = 'logo/octobear__bearctopus_by_blazegryph-d4pte5b.gif'

        self.canvas = Canvas(root, width=200, height = 267)
        self.canvas.pack(side=TOP, expand = YES, fill = BOTH)

        self.logo = PhotoImage(file = self.path)
        self.canvas.create_image(300, 0, image = self.logo, anchor = N)
	
        self.frame = Frame(root)

        Label(self.frame, text = 'Target URL:').pack(side = LEFT)
        self.targetURL = StringVar()
        self.urlEntry = Entry(self.frame, textvariable = self.targetURL)
        self.urlEntry.bind('<Return>', self.start)
        self.urlEntry.pack(side = LEFT, expand = YES, fill = X)
        self.startButton = Button(self.frame, text = 'Start', command = self.start)
        self.startButton.pack(side = RIGHT)


        self.frame.pack(expand = YES, fill = X)

        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack(side = RIGHT, fill = Y)


        self.workOutput = Text(root, wrap = WORD, yscrollcommand = self.scrollbar.set)
        self.workOutput.config(state = DISABLED)
        self.workOutput.pack()

        self.scrollbar.config(command = self.workOutput.yview)
        
        sys.stdout = StdoutRedirector(self.workOutput)
        root.mainloop()

    def start(self, event = None):
        self.targetURL
        #get url list from targetURL
        links = []
        links.append(self.targetURL.get())
        
        #print 'hello there'
        #crawler = OctoBearCrawler(self.targetURL.get())
        for url in links:
            try:
                obfh = OctoBearFormHandler(url)
                obfh.sendRequest()
            except:
                sys.stdout.write('Invalid URL: "' + url + '"\n')
        

    def quit(self, event):
        exit(0)
        


#root = Tk()
#app = OctoBearApp(root)
#root.mainloop()

OctoBearApp(Tk())

