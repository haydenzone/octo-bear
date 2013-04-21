import os
import sys
import re
from tkinter import *
from tkinter.filedialog import asksaveasfile,askdirectory
from tkinter.messagebox import *

####################################################################
#   GUI
####################################################################
class Application(Frame):
    text = 0
    query_list = []
    query_i = 0
    injections = {}

    def load_file_highlight(self, filename, start, end):
        self.text.config(state=NORMAL)
        self.text.delete("1.0", END)
        f = open(filename)
        self.text.tag_config("n", background="yellow", foreground="blue")
        line_i = 0
        for line in f:
            if line_i in range(start, end+1):
                self.text.insert(END, line, ("n"))
            else:
                self.text.insert(END, line)
            line_i += 1
        self.text.see(str(int((start+end)/2))+".0")
        self.text.config(state=DISABLED)
    def load_query(self,query):
        self.load_file_highlight(query.filename, query.start_line, query.end_line)
    
    def save(self):
        file = asksaveasfile()
        self.save_injection()
        for i, entry in self.injections.items():
            file.write(entry[0]+" ~ "+entry[1]+"\n")

    def save_injection(self):
        check = self.check_entry.get(1.0, END)
        injection = self.injection_entry.get(1.0, END)
        check = check.strip()
        injection = injection.strip()
        if check != "" or injection != "":
            self.injections[self.query_i] = (injection, check)
    def open_injection(self):
        self.check_entry.delete(1.0, END)
        self.injection_entry.delete(1.0, END)
        if self.query_i in self.injections:
            self.check_entry.insert(END,self.injections[self.query_i][1])
            self.injection_entry.insert(END,self.injections[self.query_i][0])
        self.check_entry.mark_set("insert", "%d.%d" % (0, 0))
        self.injection_entry.mark_set("insert", "%d.%d" % (0, 0))
        
    def next_query(self):
        self.save_injection();
        if self.query_i+1 < len(self.query_list):
            self.query_i += 1
        self.open_injection()
        self.load_query(self.query_list[self.query_i])
    def prev_query(self):
        self.save_injection();
        if self.query_i-1 >= 0:
            self.query_i -= 1
        self.open_injection()
        self.load_query(self.query_list[self.query_i])
        
    def createWidgets(self):
        self.text = Text(self, relief=SUNKEN)
        self.text.pack(side=TOP, expand=YES, fill=BOTH) 

        #Create Injection entry label and textbox 
        injection_label = Label(self, text="SQL Injection")
        injection_label.pack()
        self.injection_entry = Text(self,height=5)
        self.injection_entry.pack()

        #Create check entry label and textbox 
        check_label = Label(self, text="SQL Injection Check")
        check_label.pack()
        self.check_entry = Text(self,height=5)
        self.check_entry.pack()

        #Create buttons
        buttons = Frame(self)
        buttons.pack(side=BOTTOM, fill=X)

        #Prev Button
        prev_query = Button(buttons)
        prev_query["text"] = "<< Previous Query"
        prev_query["command"] = self.prev_query
        prev_query.pack({"side": "left"})

        #Next Button
        next_query = Button(buttons)
        next_query["text"] = "Next Query >>"
        next_query["command"] = self.next_query
        next_query.pack({"side": "left"})

        #Save Button
        save_button = Button(buttons)
        save_button["text"] = "Save"
        save_button["command"] = self.save
        save_button.pack({"side": "left"})

        #Quit Button
        QUIT = Button(buttons)
        QUIT["text"] = "QUIT"
        QUIT["fg"]   = "red"
        QUIT["command"] =  self.quit
        QUIT.pack({"side": "left"})

    def __init__(self, master=None, queries=None):
        self.query_list = queries
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.master.title("SQL Injection Creator")
        #Load first file
        query = self.query_list[0]
        self.load_query(query)
####################################################################
#   Classes
####################################################################
class Function:
    name = ""
    start_line = 0
    end_line = 0
    db = False
    def __str__(self):
        if self.db:
            db_str = "True"
        else:
            db_str = "False"
        return "{0} {1}-{2} {3}".format(self.name, self.start_line, self.end_line, db_str)
class Query:
    filename = ""
    start_line = 0
    end_line = 0

####################################################################
#   Functions
####################################################################
def bracket_delta(str):
    delta = 0
    matches = re.findall("[{}]", str)
    for match in matches:
        if match == '{':
            delta += 1
        else:
            delta -= 1
    return delta

####################################################################
#   Main
####################################################################

#Check for correct command line usage, otherwise prompt for directory
if len(sys.argv) != 2:
    rootdir = askdirectory()
else:
    rootdir = sys.argv[1]
    
#Crawl rootdir for php files
fileList = []
for root, subFolders, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[1]
        if ext == ".php":
            fileList.append(os.path.join(root,file))


#Compile necessary regex
function_reg = re.compile(".*?function[ ]*([a-zA-Z0-9_-]*)\(.*?\)")
db_reg = re.compile(".*\$this->db->")

queries = []
#Loop through files
for filename in fileList:
    funs = []
    #print(filename)
    testfile = open(filename)
    line_num = 0
    function_started = False
    bracket_depth = 0
    for line in testfile:
        if not function_started:
            match = function_reg.match(line)
            #print line
            if match:
                fun = Function()
                fun.name = match.group(1)
                fun.start_line = line_num 
                #print match.group(1)+" "+str(line_num) ,
                bracket_depth = bracket_delta(line)
                function_started = True
        else:
            bracket_depth += bracket_delta(line)
            if bracket_depth <= 0:
                fun.end_line = line_num
                funs.append(fun)
                function_started = False
                #print line_num
            else: #Check for database query
                match = db_reg.match(line)
                if match:
                    fun.db = True
                
                
        line_num += 1
    for fun in funs:
        #print("   ",fun)
        if fun.db:
            temp = Query()
            temp.filename = filename
            temp.start_line = fun.start_line
            temp.end_line = fun.end_line
            queries.append(temp)
#print(queries)

if len(queries) == 0:
    showerror('SQL Injection Creator', message="No PHP source found")
    exit()
    
root = Tk()
app = Application(master=root, queries=queries)
app.mainloop()
root.destroy()
