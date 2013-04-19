from Tkinter import *
from tkMessageBox import showinfo
from tkFileDialog import askopenfilename
from os import listdir
from fnmatch import fnmatch
from OctoBearFormHandler import OctoBearFormHandler
from OctoBearCrawler import OctoBearCrawler


class OctoBearApp(Frame):
    def __init__(self, root = None):
        Frame.__init__(self, root)
        self.master.title('Octo-Bear')
        self.master.resizable(0, 0)
        self.master.bind('<Control-q>', self.quit)
        
        self.__setMenuBar()
        
        config = listdir('config')
        self.configs = []
        for f in config:
            if f.find('~') == -1:
                self.configs.append((f, IntVar()))
        
        
        class IORedirector(object):
            def __init__(self, widget):
                self.widget = widget
        
        class StdoutRedirector(IORedirector):
            def write(self, s):
                self.widget.config(state = NORMAL)
                self.widget.insert(END, str(s))
                self.widget.config(state = DISABLED)
        
        self.__setGUI()
        
        #redirect stdout to gui
        sys.stdout = StdoutRedirector(self.workOutput)
        sys.stderr = StdoutRedirector(self.workOutput)
        


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
            print '\n'
        except:
            links = {}
            
        if len(links) > 0:
            for url, state in links.items():
                #self.forms = []
                print "found url:" , url
                if state:
#                    try:
                        obfh = OctoBearFormHandler(url)
                        for form in obfh.forms:
                            #form[1] = IntVar()
                            #self.createCheckbutton(self.formsFrame, form)
                            Label(self.formsFrame, text='action='+form['action'], background='white').pack()
                            
                        for config in self.configs:
                            obfh.sendRequest(config)
 #                   except:
  #                      sys.stderr.write('Invalid URL: "' + url + '"\n')
        else:
            print "no links found"
            
            
        self.startButton.config(state = NORMAL)
        self.urlEntry.config(state = NORMAL)
                
        
    def __setMenuBar(self):
        self.menubar = Menu(self)
        self.master.config(menu = self.menubar)
        
        fileMenu = Menu(self.menubar, tearoff = 0)
        helpMenu = Menu(self.menubar, tearoff = 0)
        
        self.menubar.add_cascade(label = 'File', menu = fileMenu)
        self.menubar.add_cascade(label = 'Help', menu = helpMenu)
        
        
        fileMenu.add_command(label = 'Exit', command = self.quit)
        
        helpMenu.add_command(label = 'About', command = self.about)
        
    def __setGUI(self):

        '''Config Dir / Commands'''
        self.configsContainer = Frame(self.master)
        Label(self.configsContainer, text='Commands').pack()
        self.configsCanvas = Canvas(self.configsContainer, background='white', width=175)
        self.configsFrame = Frame(self.configsCanvas)
        self.configsScrollbar = Scrollbar(self.configsContainer, command = self.configsCanvas.yview)
        self.configsCanvas.config(yscrollcommand = self.configsScrollbar.set)
        self.configsScrollbar.pack(side = LEFT, fill = Y)
        self.configsCanvas.pack(side = LEFT, fill = BOTH)
        self.configsCanvas.create_window((0,0), window = self.configsFrame, anchor = 'nw')
        self.configsFrame.bind('<Configure>', self.onFrameConfigure)
        
        '''create the checkbuttons for each config file'''
        for config in self.configs:
            self.createCheckbutton(self.configsFrame, config)
            
        self.configsContainer.grid(row = 0, column = 0)
	        
        '''Logo'''        
        self.path = 'logo/octobear__bearctopus_by_blazegryph-d4pte5b.gif'
        self.logoFrame = Frame(self.master)
        self.canvas = Canvas(self.logoFrame, width = 200, height = 267)
        self.canvas.pack(side=TOP, fill = BOTH)
        self.logo = PhotoImage(file = self.path)
        self.canvas.create_image(100, 0, image = self.logo, anchor = N)
        self.logoFrame.grid(row = 0, column = 1)
             
        
        '''Forms'''
        self.formsContainer = Frame(self.master)
        Label(self.formsContainer, text='Forms').pack()
        self.formsCanvas = Canvas(self.formsContainer, width=175, background='white')
        self.formsFrame = Frame(self.formsCanvas)
        self.formsScrollbar = Scrollbar(self.formsContainer, command = self.formsCanvas.yview)
        self.formsCanvas.config(yscrollcommand = self.formsScrollbar.set)
        self.formsScrollbar.pack(side = RIGHT, fill = Y)
        self.formsCanvas.pack(side = RIGHT, fill = BOTH)
        self.formsCanvas.create_window((0,0), window = self.formsFrame, anchor = 'ne')
        self.formsFrame.bind('<Configure>', self.onFrameConfigure)
        self.formsContainer.grid(row = 0, column = 2)
	
	
        '''URL Entry'''
        self.urlFrame = Frame(self.master)
        Label(self.urlFrame, text = 'Target URL:').pack(side = LEFT)
        self.targetURL = StringVar()
        self.urlEntry = Entry(self.urlFrame, textvariable = self.targetURL, width=50)
        self.urlEntry.bind('<Return>', self.start)
        self.urlEntry.bind('<Button-1>', self.selectAll)
        self.urlEntry.pack(side = LEFT, expand = YES, fill = BOTH)
        self.urlEntry.focus()
        self.startButton = Button(self.urlFrame, text = 'Start', command = self.start)
        self.startButton.pack(side = RIGHT)
        
        self.urlFrame.grid(row = 2, column = 0, columnspan = 3)
        
        
        '''Output'''
        self.outputFrame = Frame(self.master)
        self.outputScrollbar = Scrollbar(self.outputFrame)
        self.outputScrollbar.pack(side = RIGHT, fill = Y)


        self.workOutput = Text(self.outputFrame, wrap = WORD, yscrollcommand = self.outputScrollbar.set)
        self.workOutput.config(state = DISABLED)
        self.workOutput.pack(fill = BOTH)

        self.outputScrollbar.config(command = self.workOutput.yview)
        
        self.outputFrame.grid(row = 3, column = 0, columnspan = 3)

    def onFrameConfigure(self, event):
        self.formsCanvas.configure(scrollregion = self.formsCanvas.bbox('all'))
        self.configsCanvas.configure(scrollregion = self.configsCanvas.bbox('all'))
        
    def createCheckbutton(self, parent, command):
        c = Checkbutton(parent, text = command[0], background = 'white', highlightthickness=0, variable = command[1])
        c.select()
        c.pack()
        

    def quit(self, event = None):
        exit(0)
        
    def about(self):
        showinfo('About', 'Octo-Bear is a penetration testing tool for web pages.\n\nCreate by:\n\tSung Jin Kang\n\tHayden Waisanen\n\nCSC492 Spring 2013')

    def importFile(self):
        fin = askopenfilename()
        if fin:
            pass
        


root = Tk();
OctoBearApp(root)
root.mainloop()
