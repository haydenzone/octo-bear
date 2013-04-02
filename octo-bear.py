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
        self.urlEntry.bind('<Button-1>', self.selectAll)
        self.urlEntry.pack(side = LEFT, expand = YES, fill = X)
        self.urlEntry.focus()
        self.startButton = Button(self.frame, text = 'Start', command = self.start)
        self.startButton.pack(side = RIGHT)


        self.frame.pack(expand = YES, fill = X)

        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack(side = RIGHT, fill = Y)


        self.workOutput = Text(root, wrap = WORD, yscrollcommand = self.scrollbar.set)
        self.workOutput.config(state = DISABLED)
        self.workOutput.pack()

        self.scrollbar.config(command = self.workOutput.yview)
        
        
        #redirect stdout to gui
        sys.stdout = StdoutRedirector(self.workOutput)
        sys.stderr = StdoutRedirector(self.workOutput)
        
        root.mainloop()


    def selectAll(self, event = None):
        self.urlEntry.select_range(0, END)
        self.urlEntry.focus()
        return 'break'

    def start(self, event = None):
        self.targetURL
        self.startButton.config(state = DISABLED)
        self.urlEntry.config(state = DISABLED)
        #get url list from targetURL
        #links = []
        #links.append(self.targetURL.get())
        
        
        try:
            crawler = OctoBearCrawler(str(self.targetURL.get()))
            crawler.crawl()
            links = crawler.links
        except:
            links = {}
            
        if len(links) > 0:
            for url, state in links.items():
                if state:
                    try:
                        obfh = OctoBearFormHandler(url)
                        obfh.sendRequest()
                    except:
                        sys.stderr.write('Invalid URL: "' + url + '"\n')
        else:
            print "no links found"
            
            
        self.startButton.config(state = NORMAL)
        self.urlEntry.config(state = NORMAL)
                
        
        

    def quit(self, event):
        exit(0)
        


OctoBearApp(Tk())

