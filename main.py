from lib2to3.pgen2.token import NEWLINE
from linecache import getline
from sre_parse import State
from tkinter import *
import re
from unittest import result
keywords = re.compile(r'float|int|else|if|print')
operators = re.compile(r'=|\+|>|\*')
separators = re.compile(r'\(|\)|:|\'|;|^"|^“|^”')
indentifiers = re.compile(r'[a-zA-Z]+\d|[a-zA-Z]+')
int_literal = re.compile(r'\d+')
float_literal = re.compile(r'\d+\.+\d+')
string_literal = re.compile(r'\w+')

def CutOneLineTokens(line,obj):
    outputList = []
    while(len(line)!=0):
        line = line.lstrip()
        if(keywords.match(line) != None):   #keywords
            result = keywords.match(line)
            outputList.append(f"<key,{result.group(0)}>")
            line = line[result.end():]
        elif(indentifiers.match(line) != None):   #identifiers
            result = indentifiers.search(line)
            outputList.append(f'<id,{result.group(0)}>')
            line = line[result.end():]
        elif(operators.match(line) != None): #operators
            result = operators.search(line)
            outputList.append(f'<op,{result.group(0)}>')
            line = line[result.end():]
        elif(separators.match(line) != None):   #separators 
            result = separators.search(line)
            outputList.append(f'<sep,{result.group(0)}>')
            line = line[result.end():]
            if(result.group(0) == '\'' or result.group(0) == '"' or result.group(0) == '“' or result.group(0) == '”'):
                if(string_literal.search(line) != None):   #string-literals
                    result = string_literal.search(line)
                    outputList.append(f'<lit,{result.group(0)}>')
                    line = line[result.end():]
                    line = line.lstrip()
        elif(float_literal.match(line) != None):   #float-literals
            result = float_literal.search(line)
            outputList.append(f'<lit,{result.group(0)}>')
            line = line[result.end():]
        elif(int_literal.search(line) != None):   #int-literals
            result = int_literal.search(line)
            outputList.append(f'<lit,{result.group(0)}>')
            line = line[result.end():]
    obj.print_line(outputList)

class GUI:
    def __init__(self, root):
        # base window attributes
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")
        self.master.geometry("1100x600")
        self.master.maxsize(1100,600)
        self.master.config(bg="black")

        self.line_num = 0 # number to hold current line
        self.line_num_out = 1   # current line number of the output

        # top left and right frames
        self.UI_frame_top_left = Frame(self.master,width=550,height=100,bg="black").grid(row=0,column=0)
        self.UI_frame_top_right = Frame(self.master,width=550,height=100,bg="black").grid(row=0,column=1)

        # UI left side
        self.UI_frame_left = Frame(self.master,width=550,height=320,bg="black").grid(row=1,column=0,padx=5,sticky=N)

        # source input
        Label(self.UI_frame_left,text="Sorce Code Input:",bg="#92c7d1").grid(row=0,column=0,padx=50,pady=5,sticky=S)
        self.input_code = Text(self.UI_frame_left,width=50,height=20,bg="#393b40",fg="#92c7d1",bd=5)
        self.input_code.grid(row=1,column=0,sticky=N)

        # line counter
        Label(self.UI_frame_left,text="Current Processing Line:",bg="#92c7d1").grid(row=2,column=0,padx=80,pady=5,sticky=W)
        self.line = Entry(self.master,bg="#92c7d1")
        self.line.grid(row=2,column=0,padx=5,pady=5)
        self.line.insert(0,str(self.line_num))
        self.line.config(state=DISABLED)
    
        # next button
        self.next_button = Button(self.master,text="Next Line",command=self.get_line,bg="#92c7d1")
        self.next_button.grid(row=3,column=0)

        # reset button
        # self.reset_button = Button(self.master,text="Reset",command=self.get_line,bg="#92c7d1")
        # self.reset_button.grid(row=3,column=1)

        # UI right side
        self.UI_frame_right = Frame(self.master,width=550,height=320,pady=5,bg="black").grid(row=1,column=1,padx=5,sticky=N)

        # lex output
        Label(self.UI_frame_right,text="Lexical Analyzed Result:",bg="#92c7d1").grid(row=0,column=1,padx=50,pady=5,sticky=S)
        self.output_lex = Text(self.UI_frame_right,width=50,height=20,state=DISABLED,bg="#393b40",fg="#92c7d1",bd=5)
        self.output_lex.grid(row=1,column=1,sticky=N)

        # quit button
        self.quit_button = Button(self.master,text="Quit",command=self.quit,bg="#92c7d1")
        self.quit_button.grid(row=3,column=1)

    ### FUNCTIONS ###

    # function to copy and paste line by line from input box to output box
    def get_line(self):
        if(self.input_code.get(str(self.line_num+1)+'.0',str(self.line_num+1)+".0 lineend") != ""):
            
            input = self.input_code.get(str(self.line_num+1)+'.0',str(self.line_num+1)+".0 lineend")
            self.line_num += 1
            self.line.config(state=NORMAL)
            self.line.delete(0,END)
            self.line.insert(0,str(self.line_num))
            self.line.config(state=DISABLED)

            input = input.lstrip()
            CutOneLineTokens(input,self)

    def print_line(self,arr):
        self.output_lex.config(state=NORMAL)
        
        for x in arr:
            self.output_lex.insert(str(self.line_num_out)+'.0',x+'\n\n')
            self.line_num_out += 2
        self.output_lex.config(state=DISABLED)

    # function to reset both text boxes along with setting the initial value of line counter to 0
    def reset(self):
        self.line_num_out = 0
        self.line_num = 0
        self.line.config(state=NORMAL)
        self.line.delete(0,END)
        self.line.insert(0,"0")
        self.line.config(state=DISABLED)

        self.input_code.delete("1.0","end")

        self.output_lex.config(state=NORMAL)
        self.output_lex.delete("1.0","end")
        self.output_lex.config(state=DISABLED)

    def quit(self):
        self.master.destroy()

if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = GUI(myTkRoot)
    myTkRoot.mainloop()
    