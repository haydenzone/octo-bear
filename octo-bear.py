from Tkinter import *
from tkMessageBox import showinfo
from tkFileDialog import askopenfilename
from os import listdir
from fnmatch import fnmatch
from OctoBearFormHandler import OctoBearFormHandler
from OctoBearCrawler import OctoBearCrawler
import mysql.connector

class OctoBearApp(Frame):
    def __init__(self, root = None):
        Frame.__init__(self, root)
        
        class IORedirector(object):
            def __init__(self, widget):
                    self.widget = widget
            
        class StdoutRedirector(IORedirector):
            
            def write(self, s):
                self.widget.config(state = NORMAL)
                if str(s).find('FAILED') >= 0:
                    self.widget.tag_config('error', background='red', foreground='black')
        
                    self.widget.insert(END, str(s), ('error'))
                else:
                    self.widget.insert(END, str(s), ('pass'))
                self.widget.config(state = DISABLED)

        self.master.title('Octo-Bear')
        self.master.resizable(0, 0)
        self.master.bind('<Control-q>', self.quit)
        self.__setMenuBar()
        self.__loadConfig()
        self.__setGUI()
        self.__loadDBInfo()
        
        #redirect stdout to gui
        sys.stdout = StdoutRedirector(self.workOutput)
        sys.stderr = StdoutRedirector(self.workOutput)
        
        
    def __loadConfig(self):
        config = listdir('config')
        self.configs = []
        for name in config:
            if name.find('~') == -1:
                self.configs.append((name, IntVar(), []))
                fin = open('config/'+name)
                for line in fin:
                    if line[0] != '#':
                        self.configs[-1][2].append(line.strip('\n'))
                fin.close()
                
    def __loadDBInfo(self):
        dbFile = open('db')
        self.dbInfo = {}
        for line in dbFile:
            line = line.split('=')
            self.dbInfo[line[0]] = line[1].strip('\n')
        
    def __checkDB(self, query):
        cnx = mysql.connector.connect(**self.dbInfo)
        cursor = cnx.cursor()
        query = (query)
        cursor.execute(query)
        retval = []
        for item in cursor:
            retval.append(item)
        cursor.close()
        cnx.close()
        return retval
        
        

    def selectAll(self, event = None):
        self.urlEntry.select_range(0, END)
        self.urlEntry.focus()
        return 'break'
        
    def clear(self, event = None):
        self.workOutput.config(state = NORMAL)
        self.workOutput.delete('1.0', END)
        self.workOutput.config(state = DISABLED)

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
        print links
        if len(links) > 0:
            for url, state in links.items():
                print "found url:" , url
                if state:
#                    try:
                        self.obfh = OctoBearFormHandler(url)
                        for form in self.obfh.forms:
                            Label(self.formsFrame, text='action='+form['action'], background='white').pack()
                            self.__permutePayloads(form['action'], form['input'])
                        
        else:
            print "no links found"
            
            
        self.startButton.config(state = NORMAL)
        self.urlEntry.config(state = NORMAL)

    def __permutePayloads(self, action, inputs, payload = None, offset = 0):
        if offset == len(inputs):
            try:
                startCount = self.__checkDB(self.checkQuery)
            except:
                pass
            self.obfh.sendRequest(action, payload)
            try:
                endCount = self.__checkDB(self.checkQuery)
                if endCount != startCount:
                    print 'FAILED', payload
            except:
                pass
            return
        if payload is None:
            payload = {}
        payload[inputs[offset]['name']] = None
        
        temp = [i for i in self.configs if i[0] == inputs[offset]['name']]
        if len(temp) > 0 and temp[0][1].get() == 1:
            for i in temp[0][2]:
                payload[inputs[offset]['name']] = i
                self.__permutePayloads(action, inputs, payload, offset + 1)
            
        else:
            self.__permutePayloads(action, inputs, payload, offset + 1)
        
        temp = [i for i in self.configs if i[0] == 'sql_injections']
        for i in temp[0][2]:
            i = i.split('~')
            payload[inputs[offset]['name']] = i[0]
            self.__permutePayloads(action, inputs, payload, offset + 1)
            if len(i) > 1:
                self.checkQuery = i[1]
        
        
        
        
        
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
        self.configsFrame = Frame(self.configsCanvas, background = 'white')
        self.configsScrollbar = Scrollbar(self.configsContainer, command = self.configsCanvas.yview)
        self.configsCanvas.config(yscrollcommand = self.configsScrollbar.set)
        self.configsScrollbar.pack(side = RIGHT, fill = Y)
        self.configsCanvas.pack(side = RIGHT, fill = BOTH)
        self.configsCanvas.create_window((0,0), window = self.configsFrame, anchor = 'nw')
        self.configsFrame.bind('<Configure>', self.onFrameConfigure)
        
        '''create the checkbuttons for each config file'''
        for config in self.configs:
            self.createCheckbutton(self.configsFrame, config)
            
        self.configsContainer.grid(row = 1, column = 0)
	        
        '''Logo'''        
        self.path = 'logo/octobear__bearctopus_by_blazegryph-d4pte5b.gif'
        self.logoFrame = Frame(self.master)
        self.canvas = Canvas(self.logoFrame, width = 75, height = 100)
        self.canvas.pack(side=TOP, fill = BOTH)
        self.logo = PhotoImage(file = self.path)
        self.canvas.create_image(75/2, 0, image = self.logo, anchor = N)
        self.logoFrame.grid(row = 0, column = 0)
             
        
        '''Forms'''
        self.formsContainer = Frame(self.master)
        Label(self.formsContainer, text='Forms').pack()
        self.formsCanvas = Canvas(self.formsContainer, width=175, background='white')
        self.formsFrame = Frame(self.formsCanvas, background = 'white')
        self.formsScrollbar = Scrollbar(self.formsContainer, command = self.formsCanvas.yview)
        self.formsCanvas.config(yscrollcommand = self.formsScrollbar.set)
        self.formsScrollbar.pack(side = RIGHT, fill = Y)
        self.formsCanvas.pack(side = RIGHT, fill = BOTH)
        self.formsCanvas.create_window((0,0), window = self.formsFrame, anchor = 'ne')
        self.formsFrame.bind('<Configure>', self.onFrameConfigure)
        self.formsContainer.grid(row = 2, column = 0)
	
	
        '''URL Entry'''
        self.urlFrame = Frame(self.master)
        Label(self.urlFrame, text = 'Target URL:').pack(side = LEFT)
        self.targetURL = StringVar()
        self.urlEntry = Entry(self.urlFrame, textvariable = self.targetURL, width=50)
        self.urlEntry.bind('<Return>', self.start)
        self.urlEntry.bind('<Button-1>', self.selectAll)
        self.urlEntry.pack(side = LEFT, expand = YES, fill = BOTH)
        self.urlEntry.focus()
        
        
        self.clearButton = Button(self.urlFrame, text = 'Clear', command = self.clear)
        self.clearButton.pack(side = RIGHT)
        
        self.startButton = Button(self.urlFrame, text = 'Start', command = self.start)
        self.startButton.pack(side = RIGHT)
        
        self.urlFrame.grid(row = 0, column = 1)
        
        
        '''Output'''
        self.outputFrame = Frame(self.master)
        self.outputScrollbar = Scrollbar(self.outputFrame)
        self.outputScrollbar.pack(side = RIGHT, fill = Y)


        self.workOutput = Text(self.outputFrame, wrap = WORD, yscrollcommand = self.outputScrollbar.set, height=40)
        self.workOutput.config(state = DISABLED)
        self.workOutput.pack(fill = BOTH)

        self.outputScrollbar.config(command = self.workOutput.yview)
        
        self.outputFrame.grid(row = 1, column = 1, rowspan= 3)

    def onFrameConfigure(self, event):
        self.formsCanvas.configure(scrollregion = self.formsCanvas.bbox('all'))
        self.configsCanvas.configure(scrollregion = self.configsCanvas.bbox('all'))
        
    def createCheckbutton(self, parent, command):
        c = Checkbutton(parent, text = command[0], background = 'white', highlightthickness=0, variable = command[1])
        c.select()
        c.pack(anchor = W)
        

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

