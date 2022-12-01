# Lexical-Analysis-and-Parsing-GUI
## Description:
This program is made to simulate the lexical analysis and parsing of a compilier process and to visualize the process through a GUI with use of the Tkinter and Regex 
libraries in python. Accepts three expressions *shown below in the BNF Grammer section*
## Functionality:
- The program would first take in multiple lines of code from the user input on the GUI
- This code is then tokenized with the help of Regex.
- Once tokenized, one line of the tokenized code is then sent to the parsing logic that checks the grammer through our predefined BNF Grammer logic with *Recusive Descent*
- After checking one line of code the program then outputs what the expected parse tree would look like on the GUI
- One feature is error catching in our parsing logic that will notify the user of a syntax error
### The BNF Grammer Rules & code example:
```
BNF:
exp -> id = math;                           *exp1()
math -> multi + multi
multi -> int * float | float

exp -> if ( comparison_exp ) :              *exp2()
comparison_exp -> identifier > identifier

exp -> print( p_statement ):                *exp3()
p_statement -> string
```
Example code to input:
```
float mathresult1 = 5*4.3 + 2.1; 
float mathresult2 = 4.1 + 2*5.5; 
if(mathresult1>mathresult2):
  print("I just built some parse trees");
```
### Tokens Accepted (Regex)
```python
keywords = re.compile(r'float|int|else|if|print')
operators = re.compile(r'=|\+|>|\*')
separators = re.compile(r'\(|\)|:|\'|;|^"|^“|^”')
indentifiers = re.compile(r'[a-zA-Z]+\d|[a-zA-Z]+')
int_literal = re.compile(r'\d+')
float_literal = re.compile(r'\d+\.+\d+')
string_literal = re.compile(r'\w+')
```
## How to run:
- There is an included executable file ```main.exe```
- To run on terminal with main.py: ```python3 .\main.py```
