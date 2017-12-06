 # -*- coding: utf-8 -*-
"""
Created on Fri Dec 01 22:43:14 2017

@author: Carson
"""

class Compiler():
    def __init__(self, istream):
        self.ostream = istream.replace(".xml","F.xml")
        self.istream = open(istream, mode = 'r')
        self.stream = open(self.ostream, mode = 'w')
        self.lastWrittenLine = ""

        nextLine()
        generalParse(nextLine())
        nextLine()

    def nextLine(self):
        self.istream.readline()
    
    def writeLine(self, s):
        self.lastWrittenLine = s
        self.stream.write(s + "\n")

    def generalParse(self, line):
            segments = line.split()
            if segments[0] == "<keyword>":
                keyWordParse(line)
                generalParse(nextLine())
            
            if segments[0] == "<symbol>":
                symbolParse(line)
                generalParse(nextLine())
                 
            if segments[0] == "<identifier>":
                writeLine(line)
                generalParse(nextLine())
            
            if segments[0] == "<stringConstant>":
                writeLine(line)
                generalParse(nextLine())
            
            if segments[0] == "<intConstant>":
                writeLine(line)
                generalParse(nextLine())

    def keyWordParse(self, line):
        segments = line.split()
            if segments[1] == "class":
                writeLine("<class>")
                writeLine(line)
                writeLine(nextLint())
                writeLine(nextLine())
                line  = nextLine()
                if(line.split()[1] == "static" | line.split()[1] == "field"):
                    writeLine("<classVarDec>")
                    while(line.split()[1] == "static" | line.split()[1] == "field"):
                        writeLine(line)
                        writeLine(nextLint())
                        writeLine(nextLine())
                        writeLine(nextLine())
                        temp = nextLine()
                    writeLine("</classVarDec>")
                    
                if(line.split()[1] == "constructor" | line.split()[1] == "function" | line.split()[1] == "method"):
                    writeLine("<subRoutineDec>")
                    while(line.split()[1] == "constructor" | line.split()[1] == "function" | line.split()[1] == "method"):
                        writeLine(line)
                        writeLine(nextLint())
                        writeLine(nextLine())
                        parameterListParse(nextLine())
                        temp = nextLine()
                    writeLine("<subRoutineBody>")
                    writeLine(temp)
                    temp = nextLine()
                    writeLine("<varDec>")
                    while(temp.split()[1] == "var"):
                        writeLine(temp)
                        writeLine(nextLine())
                        writeLine(nextLine())
                        writeLine(nextLine())
                        temp = nextLine()
                    writeLine("</varDec>")
                    writeLine("<statements>")

                    writeLine(temp)
                    writeLine("</statements>")
                    writeLine(nextLine())
                    writeLine("</subRoutineBody>")
                    writeLine("</subRoutineDec>")
                writeLine(nextLine())
                writeLine("<class>")

                        
            if segments[1] == "function":
                writeLine(line)

            if segments[1] == "if":
            if segments[1] == "else":
            if segments[1] == "while":
            if segments[1] == "var":
            if segments[1] == "let":
            if segments[1] == "do":
            if segments[1] == "return":
                
            if segments[1] == "constructor":
            if segments[1] == "method":
            if segments[1] == "field":
            if segments[1] == "static":
            
            else:
                writeLine(line)                

    def parameterListParse(self, line):
        writeLine(line)
        writeline("<parameterList>")
        line = nextLine()
        while(line.split()[1] != ")"):
            writeLine(line)
            writeLine(nextLine())
            line = nextLine()
        writeline("</parameterList>")
        writeLine(line)

    def symbolParse(self, line):
        segments = line.split()
        
        if segments[1] == "(":
            if self.lastWrittenLine.split()[0] != "<symbol>":
                writeLine(line)
                writeLine("<parameterList>")
                temp = nextLine()
                while(temp.split()[1] != ")"):
                    writeLine(temp)
                    temp = nextLine()
                writeLine("</parameterList>")
                writeLine(temp)

'''
                
                if segments[1] == "function":
                    fileCont.insert(i,"<subroutineDec>\n")
                    self.ostream.write(token)
                    self.parseClass(self.istream.readline())
                    self.parseClass(self.istream.readline())
                    self.ostream.write(self.istream.readline()+"\n")
                    self.ostream.write("<parameterList>\n")
                    temp = self.istream.readline() 
                    while temp != "<symbol> ) </symbol>":
                        self.ostream.write(temp + "\n")
                        temp = self.istream.readline() 
                    self.ostream.write("</parameterList>\n")
                    self.ostream.write(temp)
                    self.ostream.write("<subroutineBody>\n")
                    self.parseClass(self.istream.readline())
                    self.ostream.write("</subroutineBody>\n")
                    return

                if segments[1] == "var":
                    self.ostream.write("<varDec>\n")
                    self.ostream.write(token)
                    self.parseClass(self.istream.readline())
                    self.parseClass(self.istream.readline())
                    self.parseClass(self.istream.readline())
                    self.ostream.write("</varDec>\n")
                    self.parseClass(self, self.istream.readline())
                    return

                if segments[1] == "let": #not done
                    endFlag = False
                    if self.stateFlag == False:
                        endFlag = True
                        self.stateFlag = True
                        self.ostream.write("<statements>\n")
                    self.ostream.write("<letStatement>\n")
                    self.ostream.write(token + "\n")
                    self.parseClass(self.istream.readline())
                    self.parseClass(self.istream.readline())
                    self.parseClass(self.istream.readline())
                    self.ostream.write("<expression>\n")
                    self.ostream.write("<term>\n")
                    self.ostream.write("<term>\n")
                    self.ostream.write("</expression>\n")
                    self.ostream.write("</letStatement>\n")
                    if self.endFlag == True:
                        self.ostream.write("<\statements>\n")
                    self.parseClass(self.istream.readline())

                if segments[1] == "do":
                    endFlag = False
                    if self.stateFlag == False:
                        endFlag = True
                        self.stateFlag = True
                        self.ostream.write("<statements>\n")

                    self.ostream.write("<doStatement>\n")
                    self.ostream.write(token + "\n")
                    self.parseClass(self.istream.readline())
                    self.parseClass(self.istream.readline())
                    self.parseClass(self.istream.readline())
                    self.parseClass(self.istream.readline())
                    self.parseClass(self.istream.readline())
                    self.ostream.write("</doStatement>\n")
                    
                    if self.endFlag == True:
                        self.ostream.write("<\statements>\n")
                    
                    self.parseClass(self.istream.readline())


                if segments[1] == "return":
                    self.ostream.write("<returnStatement>\n")
                    self.ostream.write(token + "\n")
                    self.parseClass(self.istream.readline())
                    self.ostream.write("</returnStatement>\n")
                    return
           
                if segments[1] == "void":
                    self.ostream.write(token + "\n")
                    return
                     
                print "error! unknown keyword: " + token
                return

'''

'''
            if segments [1] == "(":
                self.ostream.write(token)
                self.ostream.write("<expressionList>\n")
                self.parseClass(self.istream.readline())
                temp = self.istream.readline() 
                while temp != "<symbol> ) </symbol>":
                    if temp.split()[0] == "identifier":
                        self.ostream.write("<term>\n")
                        self.ostream.write(temp + "\n")
                        self.ostream.write("</term>\n")
                    if temp.split()[0] == "<symbol>":
                        self.ostream.write(temp + "\n")
                    else:
                        print "unknown token in expression: " + temp + "\n"

                self.ostream.write("</expressionList>\n")
                self.ostream.write(temp + "\n")
                self.parseClass(self.istream.readline())
                return
            
            if segments [1] == ")":
                self.ostream.write(token)
                self.ostream.write("<\expression>\n")
                return
            
            if segments [1] == "{":
                self.ostream.write(token)
                self.parseClass(self.istream.readline())
                return
            
            if segments [1] == "}":
                self.ostream.write(token)
                return
            
            if segments [1] == ";":
                self.ostream.write(token)
                return
            if segments [1] == ".":
                self.ostream.write(token)
                return
            
            print "error! unknown symbol: " + token
            return

'''
'''
    def compileClass(self, token):
      #Example:
      #    <class>
      #    <keyword> class </keyword>
      #    <identifier> Main </identifier>
      #    <symbol> { </symbol>
      #              <classVarDec>
      #              <keyword> static </keyword>
      #              <keyword> boolean </keyword>
      #              <identifier> test </identifier>
      #              <symbol> ; </symbol>
      #             </classVarDec>
      code  = "<class>\n" + str(token) 
      code += self.istream.readline()
      self.ostream.write(code)
      temp = self.istream.readline()
      if(temp == "<symbol> { </symbol>\n"):
          code    = temp
          self.ostream.write(code)
      temp = self.istream.readline()
      while temp.lower() in ["static", "field"]:
          temp = self.compileClassVarDec(temp)
      while temp.lower() in ["method", "constructor", "function"]:
          temp = self.compileSubroutine(temp)
      code = str(temp) + "\n</class>"
      self.ostream.write(code)
      self.ostream.close()
      
    def compileClassVarDec(self, token):  
      # Example:
      #   <classVarDec>
      #    <keyword> static </keyword>
      #    <keyword> boolean </keyword>
      #    <identifier> test </identifier>
      #    <symbol> ; </symbol>
      #   </classVarDec>
      code  = "<classVarDec>\n" + str(token)
      var   = self.istream.readline()
      if var in ["int", "boolean", "char"]:
          code += var
      else:
          code += var
      code += self.istream.readline()
      self.ostream.write(code)
      code  = ""
      var   = self.istream.readline()
      while var == ",":
          var = self.istream.readline()
          code += str(var)
          var = self.istream.readline()
          code += str(var)
          var = self.istream.readline()
      code += token + "\n</classVarDec>"
      self.ostream.write(code)
      code = ""
      var = self.istream.readline()
      if var in ["static", "field"]:
          return self.compileClassVarDec(var)
      return var

        
    def compileSubroutine(self, token):
      # Example:
      #    <subroutineDec>
      #    <keyword> function </keyword>
      #    <keyword> void </keyword>
      #    <identifier> main </identifier>
      #   <symbol> ( </symbol>
      #              <parameterList>
      #              </parameterList>
      #              <symbol> ) </symbol>
      #             <subroutineBody>
      #              <symbol> { </symbol>
      #                        <varDec>
      code = "<subroutineDec>\n" + str(token)
      var = ""
      if token == "constructor":
          var = self.istream.readline()
          code += str(var)
      else:
          var = self.istream.readline()
          code += str(var)
      code += str(self.istream.readline())
      code += str(self.istream.readline())
      self.ostream.write(code)
      code  = ""
      var   = self.istream.readline()
      if var != ")":
          self.compileParameterList(var)
      else:
          code += "<parameterList></parameterList>"
      code += str(var)
      code += "<subroutineBody>\n" + str(self.istream.readline())
      self.ostream.write(code)
      code  = ""
      var = self.istream.readline()
      if var == "var":
          var = self.compileVarDec(var)
      self.ostream.write("<statements>\n")
      while var not in ["}", None]:
          var = self.compileStatement(var)
      code += "</statements>" + var + "\n</subroutineBody>\n</subroutineDec>"
      self.ostream.write(code)
      code = ""
      var = self.istream.readline()
      if var in ["method", "constructor", "function"]:
          var = self.compileSubroutine(var)
      return var
  
    def compileParameterList(self, token):
      #Example:
      #  <parameterList>
      #  </parameterList>
      code  = "<parameterList>\n"
      code += str(token)
      code += str(self.istream.readline())
      self.ostream.write(code)
      code  = ""
      var   = self.istream.readline()
      if var == ",":
          code += var
          self.ostream.write(code)
          var = self.istream.readline()
          return self.compileParamList(token)
      self.ostream.write("\n</parameterList>")
      return var  
        
    def compileVarDec(self, token):
      #Example:
      #<varDec>
      #  <keyword> var </keyword>
      #  <identifier> SquareGame </identifier>
      #  <identifier> game </identifier>
      #  <symbol> ; </symbol>
      #</varDec>
      code = "<varDec>\n" + str(token)
      var  = self.istream.readline()
      if var in ["char", "boolean", "int"]:
          code += str(var)
      else:
          code += str(var)
      var  = self.istream.readline()
      code += str(var)
      self.ostream.write(code)
      code = ""
      var  = self.istream.readline()
      while var == ",":
          code += str(var)
          code += str(self.istream.readline())
          self.ostream.write(code)
          code  = ""
          var   = self.istream.readline()
      code = str(var) + "<\n/varDec>"
      self.ostream.write(code)
      code = ""
      var  = self.istream.readline()
      if var == "var":
          return self.compileVarDec(var)
      return var
  
    def compileStatements(self, token):
        if token == "while":
            return self.compileWhile(token)
        elif token == "if":
            return self.compileIf(token)
        elif token == "return":
            return self.compileReturn(token)
        elif token == "do":
            return self.compileDo(token)
        elif token == "let":
            return self.compileLet(token)
        
    def compileDo(self, token):
        return token
        
    def compileLet(self, token):
        return token
        
    def compileWhile(self, token):
        return token
        
    def compileReturn(self, token):
        return token
        
    def compileIf(self, token):
        return token

    def compileExpression(self, token):
        self.ostream.write("<expression>")
        var  = self.compileTerm(token)
        self.ostream.write("</expression")
        return var
        
    def compileTerm(self, token):
        return token
        
    def compileExpressionList(self, token):
        self.ostream.write("<expressionlist>")
        var  = self.compileExpression(token)
        code = ""
        while var == ",":
            self.ostream.write(str(var))
            var = self.compileExpression(self.istream.readline())
        return var
        '''
