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
'''
float mathresult1 = 5*4.3 + 2.1; 
float mathresult2 = 4.1 + 2*5.5; 
if(mathresult1>mathresult2):
print("I just built some parse trees");
'''
'''
BNF:

exp -> id = math;                           *exp1()
math -> multi + multi
multi -> int * float | float

exp -> if ( comparison_exp ) :              *exp2()
comparison_exp -> identifier > identifier

exp -> print( p_statement ):                *exp3()
p_statement -> string
'''

### PARSER LOGIC ##
class Parser:
    def __init__(self,guiObj):
        self.token = ("","")
        self.tokenArr = []
        self.guiObj = guiObj
    
    def parse(self,tokenArr):
        if self.tokenArr: self.tokenArr.clear()
        self.tokenArr = tokenArr
        print(self.tokenArr)
        self.token=self.tokenArr.pop(0)
       
        
        if(self.token[0] == "id" or self.token[1] == "float"): self.exp1()
        elif(self.token[1] == "if"): self.exp2()
        elif(self.token[1] == "print"): self.exp3()
        else: self.guiObj.print_line_parser("ERROR: invalid syntax")
        

    def accept_token(self):
        self.guiObj.print_line_parser("     accept token from the list:"+self.token[1]+'\n')
        if(self.token[1] != ';' and self.token[1] != ':' and self.tokenArr):
            self.token=self.tokenArr.pop(0)

    # for expressions that start with a keyword (type)
    def exp1(self):
        self.guiObj.print_line_parser("\n----parent node exp1, finding children nodes:"+'\n')
        if(self.token[1]=="float"):    # for cases of identifiers
            self.guiObj.print_line_parser("child node (internal): keyword"+'\n')
            self.guiObj.print_line_parser("   keyword has child node (token):"+self.token[1]+'\n')
            self.accept_token()
        
        else:
            self.guiObj.print_line_parser("ERROR: expect keyword (type) as the first element of the expression!")
            return
        
        if(self.token[0]=="id"):    # for cases of identifiers
            self.guiObj.print_line_parser("child node (internal): identifier"+'\n')
            self.guiObj.print_line_parser("   identifier has child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected identifier (id) as the first element after (type)")
            return
        if(self.token[1]=="="):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected '='")
            return

        self.guiObj.print_line_parser("Child node (internal): math"+'\n')
        self.math()

    # for expresssions that start with an "if"
    def exp2(self):
        self.guiObj.print_line_parser("\n----parent node exp2, finding children nodes:"+'\n')
        if(self.token[1]=="if"): 
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected 'if'")
            return
        if(self.token[1]=="("):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
            self.guiObj.print_line_parser("child node (internal): comparison"+'\n')
            self.comparison()
            self.guiObj.print_line_parser("\n----parent node exp2, finding children nodes:"+'\n')
        else:
            self.guiObj.print_line_parser("ERROR: expected '('")
            return
        if(self.token[1]==")"):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected ')'")
            return
        if(self.token[1]==":"):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
            return
        else:
            self.guiObj.print_line_parser("ERROR: expected ':'")
            return

    # for expressions that start with "print"
    def exp3(self):
        self.guiObj.print_line_parser("\n----parent node exp3, finding children nodes:"+'\n')
        if(self.token[1]=="print"): 
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected 'print'")
            return
        if(self.token[1]=="("):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
            self.guiObj.print_line_parser("child node (internal): p_statement"+'\n')
            self.print_statement()
            self.guiObj.print_line_parser("\n----parent node exp3, finding children nodes:"+'\n')
        else:
            self.guiObj.print_line_parser("ERROR: expected '('")
            return
        if(self.token[1]==")"):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected ')'")
            return
        if(self.token[1]==";"):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
            return
        else:
            self.guiObj.print_line_parser("ERROR: expected ';'")
            return

    def math(self,firstRun = True):
        self.guiObj.print_line_parser("\n----parent node math, finding children nodes:"+'\n')
        if(self.token[0]=="float_lit"):
            self.guiObj.print_line_parser("child node (internal): multi"+'\n')
            self.multi()
            if(self.token[1]=="+"):
                self.guiObj.print_line_parser("\n----parent node math, finding children nodes:"+'\n')
                self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
                self.accept_token()
                self.math(False)
            elif(self.token[1]==";" and firstRun == False):
                self.guiObj.print_line_parser("\n----parent node math, finding children nodes:"+'\n')
                self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
                self.accept_token()
                return
            elif(not self.tokenArr and self.token[1] != ';'):
                self.guiObj.print_line_parser("ERROR: expected ';'")
                return                
            else:
                self.guiObj.print_line_parser("ERROR: math -> multi + multi only!")

        elif (self.token[0]=="int_lit"):
            self.guiObj.print_line_parser("child node (internal): multi"+'\n')
            if(self.multi()==False):return
            if(self.token[1]=="+"):
                self.guiObj.print_line_parser("\n----parent node math, finding children nodes:"+'\n')
                self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
                self.accept_token()
                self.math(False)
                return
            elif(self.token[1]==";" and firstRun == False):
                self.guiObj.print_line_parser("\n----parent node math, finding children nodes:"+'\n')
                self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
                self.accept_token()
                return
            elif(not self.tokenArr and self.token[1] != ';'):
                self.guiObj.print_line_parser("ERROR: expected ';'")
                return      
            else:
                self.guiObj.print_line_parser("ERROR: math -> multi + multi only!")
        else:
            self.guiObj.print_line_parser("ERROR: math -> multi + multi only!")
            return

    def multi(self):
        self.guiObj.print_line_parser("\n----parent node multi, finding children nodes:"+'\n')
        if(self.token[0]=="float_lit"): # for float literals in multi
            self.guiObj.print_line_parser("child node (internal): float literal"+'\n')
            self.guiObj.print_line_parser("   float literal has child node (token):"+self.token[1]+'\n')
            self.accept_token()
            if(self.token[1]==";" or self.token[1]=="+" or len(self.tokenArr)==0):
                return
            elif(self.token[1]=="*"):
                self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
                self.accept_token()
                if(self.token[0]=="int_lit"):
                    self.guiObj.print_line_parser("child node (internal): int literal"+'\n')
                    self.guiObj.print_line_parser("   int literal has child node (token):"+self.token[1]+'\n')
                    self.accept_token()
                else:
                    self.guiObj.print_line_parser("ERROR: multi only supports int*float || float")
            else:
                self.guiObj.print_line_parser("ERROR: multi only supports int*float || float")
        else:                           # for int literal's in multi
            self.guiObj.print_line_parser("child node (internal): int literal"+'\n')
            self.guiObj.print_line_parser("   int literal has child node (token):"+self.token[1]+'\n')
            self.accept_token()
            if(self.token[1]==";" or self.token[1]=="+" or len(self.tokenArr)==0):
                self.guiObj.print_line_parser("ERROR: multi only supports int*float || float")
                return False # scpecial return case for int literals
            elif(self.token[1]=="*"):
                self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
                self.accept_token()
                if(self.token[0]=="float_lit"):
                    self.guiObj.print_line_parser("child node (internal): float literal"+'\n')
                    self.guiObj.print_line_parser("   float literal has child node (token):"+self.token[1]+'\n')
                    self.accept_token()
                else:
                    self.guiObj.print_line_parser("ERROR: multi only supports int*float || float")
            else:
                self.guiObj.print_line_parser("ERROR: multi only supports int*float || float")

    def comparison(self):
        self.guiObj.print_line_parser("\n----parent node comparison, finding children nodes:"+'\n')
        if(self.token[0]=="id"):
            self.guiObj.print_line_parser("child node (internal): id"+'\n')
            self.guiObj.print_line_parser("   id has child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected (id) as first token in comparison")
            return
        if(self.token[1] == '>'):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected (operator) '>'")
            return
        if(self.token[0]=="id"):
            self.guiObj.print_line_parser("child node (internal): id"+'\n')
            self.guiObj.print_line_parser("   id has child node (token):"+self.token[1]+'\n')
            self.accept_token()
            return
        else:
            self.guiObj.print_line_parser("ERROR: expected (id) as third token in comparison")
            return
        
    def print_statement(self):
        self.guiObj.print_line_parser("\n----parent node p_statement, finding children nodes:"+'\n')
        if(self.token[1]=='"'or'“'or'”'or"'"):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected (separator) '\"'")
        if(self.token[0]=="str_lit"):
            self.guiObj.print_line_parser("child node (internal): string literal"+'\n')
            self.guiObj.print_line_parser("   string literal has child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected (str_lit)")
        if(self.token[1]=='"'or'“'or'”'or"'"):
            self.guiObj.print_line_parser("child node (token):"+self.token[1]+'\n')
            self.accept_token()
        else:
            self.guiObj.print_line_parser("ERROR: expected (separator) '\"'")

### END PARSER LOGIC


### LEXER LOGIC ###
def CutOneLineTokens(line,guiObj,parseObj):
    outputList = []
    while(len(line)!=0):
        line = line.lstrip()
        if(keywords.match(line) != None):   #keywords
            result = keywords.match(line)
            #outputList.append(f"<key,{result.group(0)}>")
            outputList.append(("key",result.group(0)))
            line = line[result.end():]
        elif(indentifiers.match(line) != None):   #identifiers
            result = indentifiers.search(line)
            #outputList.append(f'<id,{result.group(0)}>')
            outputList.append(("id",result.group(0)))
            line = line[result.end():]
        elif(operators.match(line) != None): #operators
            result = operators.search(line)
            #outputList.append(f'<op,{result.group(0)}>')
            outputList.append(("op",result.group(0)))
            line = line[result.end():]
        elif(separators.match(line) != None):   #separators 
            result = separators.search(line)
            #outputList.append(f'<sep,{result.group(0)}>')
            outputList.append(("sep",result.group(0)))
            line = line[result.end():]
            if(result.group(0) == '\'' or result.group(0) == '"' or result.group(0) == '“' or result.group(0) == '”'):
                if(string_literal.search(line) != None):   #string-literals
                    #result = string_literal.search(line)
                    result = line[:line.find('"')]
                    #outputList.append(f'<str_lit,{result.group(0)}>')
                    #outputList.append(("str_lit",result.group(0)))
                    outputList.append(("str_lit",result))
                    #line = line[result.end():]
                    line = line[line.find('"'):]
                    line = line.lstrip()
        elif(float_literal.match(line) != None):   #float-literals
            result = float_literal.search(line)
            #outputList.append(f'<float_lit,{result.group(0)}>')
            outputList.append(("float_lit",result.group(0)))
            line = line[result.end():]
        elif(int_literal.search(line) != None):   #int-literals
            result = int_literal.search(line)
            #outputList.append(f'<int_lit,{result.group(0)}>')
            outputList.append(("int_lit",result.group(0)))
            line = line[result.end():]
    
    guiObj.print_line(outputList)
    parseObj.parse(outputList)
    ### END LEXER LOGIC ###

class GUI:
    def __init__(self, root):
        # base window attributes
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")
        self.master.geometry("1100x600")
        self.master.maxsize(1100,600)
        self.master.config(bg="black")
        self.parseObj = Parser(self)

        self.line_num = 0 # number to hold current line
        self.line_num_out = 1   # current line number of the output
        self.line_num_p = 1

        # top left and right frames
        self.UI_frame_top_left = Frame(self.master,width=366,height=100,bg="black").grid(row=0,column=0)
        self.UI_frame_top_middle = Frame(self.master,width=366,height=100,bg="black").grid(row=0,column=1)
        self.UI_frame_top_right = Frame(self.master,width=366,height=100,bg="black").grid(row=0,column=1)

        # UI left side
        self.UI_frame_left = Frame(self.master,width=366,height=320,bg="black").grid(row=1,column=0,padx=5,sticky=N)

        # UI middle
        self.UI_frame_left = Frame(self.master,width=366,height=320,bg="black").grid(row=1,column=1,padx=5,sticky=N)

        # UI right side
        self.UI_frame_right = Frame(self.master,width=366,height=320,pady=5,bg="black").grid(row=1,column=2,padx=5,sticky=N)

        # source input
        Label(self.UI_frame_left,text="Sorce Code Input:",bg="#92c7d1").grid(row=0,column=0,padx=50,pady=5,sticky=S)
        self.input_code = Text(self.UI_frame_left,width=40,height=20,bg="#393b40",fg="#92c7d1",bd=5)
        self.input_code.grid(row=1,column=0)

        # line counter
        Label(self.UI_frame_left,text="Current Processing Line:",bg="#92c7d1").grid(row=2,column=0,padx=50,pady=5,sticky=W)
        self.line = Entry(self.master,bg="#92c7d1")
        self.line.grid(row=2,column=0,padx=50,pady=5,sticky=E)
        self.line.insert(0,str(self.line_num))
        self.line.config(state=DISABLED)
    
        # next button
        self.next_button = Button(self.master,text="Next Line",command=self.get_line,bg="#92c7d1")
        self.next_button.grid(row=3,column=0)

        # lex output
        Label(self.UI_frame_right,text="Tokens:",bg="#92c7d1").grid(row=0,column=1,padx=50,pady=5,sticky=S)
        self.output_lex = Text(self.UI_frame_right,width=40,height=20,state=DISABLED,bg="#393b40",fg="#92c7d1",bd=5)
        self.output_lex.grid(row=1,column=1,sticky=W)

        # reset button
        self.reset_button = Button(self.master,text="Reset",command=self.reset,bg="#92c7d1")
        self.reset_button.grid(row=3,column=1)

        # Parse output
        Label(self.UI_frame_right,text="Parse Tree:",bg="#92c7d1").grid(row=0,column=2,padx=50,pady=5,sticky=S)
        self.output_parse = Text(self.UI_frame_right,width=40,height=20,state=DISABLED,bg="#393b40",fg="#92c7d1",bd=5)
        self.output_parse.grid(row=1,column=2,sticky=W)

        self.output_parse.tag_add('error',str(self.line_num_p)+'.0')
        self.output_parse.tag_config('error',foreground='red')

        self.output_parse.tag_add('good',str(self.line_num_p)+'.0')
        self.output_parse.tag_config('good',foreground="#92c7d1")

        # quit button
        self.quit_button = Button(self.master,text="Quit",command=self.quit,bg="#92c7d1")
        self.quit_button.grid(row=3,column=2)

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
            CutOneLineTokens(input,self,self.parseObj)

    def print_line(self,arr):
        self.output_lex.config(state=NORMAL)
        
        for x in arr:
            self.output_lex.insert(str(self.line_num_out)+'.0','<'+str(x[0])+','+str(x[1])+'>'+'\n\n')
            self.line_num_out += 2
        self.output_lex.config(state=DISABLED)

    def print_line_parser(self,output):
        if '\n' in output: self.line_num_p += 1
        self.output_parse.config(state=NORMAL)
        if(output.find('ERROR') != -1):
            #self.output_parse.tag_add('error',str(self.line_num_p)+'.0')
            #self.output_parse.tag_config('error',foreground='red')
            self.output_parse.insert(str(self.line_num_p)+'.0',output+' LINE: '+str(self.line_num)+'\n','error')
        else:
            self.output_parse.insert(str(self.line_num_p)+'.0',output,'good')
        self.output_parse.config(state=DISABLED)
        self.line_num_p += 1

    # function to reset both text boxes along with setting the initial value of line counter to 0
    def reset(self):
        self.line_num_out = 1
        self.line_num = 0
        self.line_num_p = 1
        self.line.config(state=NORMAL)
        self.line.delete(0,END)
        self.line.insert(0,"0")
        self.line.config(state=DISABLED)

        self.input_code.delete("1.0","end")

        self.output_lex.config(state=NORMAL)
        self.output_lex.delete("1.0","end")
        self.output_lex.config(state=DISABLED)

        self.output_parse.config(state=NORMAL)
        self.output_parse.delete("1.0","end")
        self.output_parse.config(state=DISABLED)

    def quit(self):
        self.master.destroy()

if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = GUI(myTkRoot)
    myTkRoot.mainloop()
    