# -*- coding: utf-8 -*-
"""
Created on Fri Dec 01 22:43:14 2017

@author: Carson
"""
class Compiler():
    def __init__(self, ostream, tokenizer):
        self.tokenizer = tokenizer;
        self.ostream = open(ostream, 'w')
        self.compileClass(tokenizer.advance())
        
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
      code  = "<class><keyword>" + str(token) + "</keyword>" 
      code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>"
      self.ostream.write(code)
      temp = self.tokenizer.advance()
      if(self.tokenizer.tokenType == "SYMBOL"):
          code    = "<symbol>" + temp + "<symbol>"
          self.ostream.write(code)
      temp = self.tokenizer.advance()
      while temp.lower() in ["static", "field"]:
          temp = self.compileClassVarDec(temp)
      while temp.lower() in ["method", "constructor", "function"]:
          temp = self.compileSubroutine(temp)
      code = "<symbol>" + str(temp) + "</symbol></class>"
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
      code  = "<classVarDec><keyword>" + str(token) + "</keyword>"
      var   = self.tokenizer.advance()
      if var in ["int", "boolean", "char"]:
          code += "<keyword>" + var + "</keyword>"
      else:
          code += "<identifier>" + var + "</identifier>"
      code += "<identifier>" + self.tokenizer.advance() + "</identifier>"
      self.ostream.write(code)
      code  = ""
      var   = self.tokenizer.advance()
      while var == ",":
          var = self.tokenizer.advance()
          code += "<symbol>" + str(var) + "</symbol>"
          var = self.tokenizer.advance()
          code += "<identifier>" + str(var) + "</identifier>"
          var = self.tokenizer.advance()
      code += "<symbol>" + token + "</symbol></classVarDec>"
      self.ostream.write(code)
      code = ""
      var = self.tokenizer.advance()
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
      code = "<subroutineDec><keyword>" + str(token) + "</keyword>"
      var = ""
      if token == "constructor":
          var = self.tokenizer.advance()
          code += "<identifier>" + str(var) + "</identifier>"
      else:
          var = self.tokenizer.advance()
          code += "<keyword>" + str(var) + "</keyword>"
      code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>"
      code += "<symbol>" + str(self.tokenizer.advance()) + "</symbol>"
      self.ostream.write(code)
      code  = ""
      var   = self.tokenizer.advance()
      if var != ")":
          self.compileParameterList(var)
      else:
          code += "<parameterList></parameterList>"
      code += "<symbol>" + str(var) + "</symbol>"
      code += "<subroutineBody><symbol>" + str(self.tokenizer.advance()) + "</symbol>"
      self.ostream.write(code)
      code  = ""
      var = self.tokenizer.advance()
      if var == "var":
          var = self.compileVarDec(var)
      self.ostream.write("<statements>")
      while var not in ["}", None]:
          var = self.compileStatement(var)
      code += "</statements><symbol>" + str(var) + "</symbol></subroutineBody></subroutineDec>"
      self.ostream.write(code)
      code = ""
      var = self.tokenizer.advance()
      if var in ["method", "constructor", "function"]:
          var = self.compileSubroutine(var)
      return var
  
    def compileParameterList(self, token):
      #Example:
      #  <parameterList>
      #  </parameterList>
      code  = "<parameterList>"
      code += "<keyword>" + str(token) + "</keyword>"
      code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>"
      self.ostream.write(code)
      code  = ""
      var   = self.tokenizer.advance()
      if var == ",":
          code += "<symbol>" + var + "</symbol>"
          self.ostream.write(code)
          var = self.tokenizer.advance()
          return self.compileParamList(token)
      self.ostream.write("</parameterList>")
      return var  
        
    def compileVarDec(self, token):
      #Example:
      #<varDec>
      #  <keyword> var </keyword>
      #  <identifier> SquareGame </identifier>
      #  <identifier> game </identifier>
      #  <symbol> ; </symbol>
      #</varDec>
      code = "<varDec><keyword>" + str(token) + "</keyword>"
      var  = self.tokenizer.advance()
      if var in ["char", "boolean", "int"]:
          code += "<keyword>" + str(var) + "</keyword>"
      else:
          code += "<identifier>" + str(var) + "</identifier>"
      var  = self.tokenizer.advance()
      code+= "<identifier>" + str(var) + "</identifier>"
      self.ostream.write(code)
      code = ""
      var  = self.tokenizer.advance()
      while var == ",":
          code += "<symbol>" + str(var) + "</symbol>"
          code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>"
          self.ostream.write(code)
          code  = ""
          var   = self.tokenizer.advance()
      code = "<symbol>" + str(var) + "</symbol></varDec>"
      self.ostream.write(code)
      code = ""
      var  = self.tokenizer.advance()
      if var == "var":
          return self.compileVarDec(var)
      return var
  
    def compileStatement(self, token):
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
        code  = "<doStatement><keyword>" + str(token) + "</keyword>"
        code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>"
        var   = self.tokenizer.advance()
        if var == ".":
            code += "<symbol>" + str(var) + "</symbol>"
            code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>"
            code += "<symbol>" + str(self.tokenizer.advance()) + "</symbol>"
        else:
            code += "<symbol>" + str(var) + "</symbol>"
        self.ostream.write(code)
        code = ""
        var  = self.tokenizer.advance()
        return var
    
    def compileLet(self, token):
        code  = "<letstatement><keyword>" + str(token) + "</keyword>"
        code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>"
        self.ostream.write(code)
        var   = self.tokenizer.advance()
        if var  == "[":
            code = "<symbol>" + str(var) + "</symbol>"
            self.ostream.write(code)
            code = ""
            var  = self.tokenizer.advance()
            var  = self.compileExpression(var)
            code = "<symbol>" + str(var) + "</symbol>"
            self.ostream.write(code)
            code = ""
            var  = self.tokenizer.advance()
            
        code = "<symbol>" + str(var) + "</symbol>"
        self.ostream.write(code)
        code = ""
        var  = self.tokenizer.advance()
        var  = self.compileExpression(var)
        code = "<symbol>" + str(var) + "</symbol></letstatement>"
        self.ostream.write(code)
        code = ""
        var  = self.tokenizer.advance()
        return var
        
        
    def compileWhile(self, token):
        var   = self.tokenizer.advance()
        code  = "<whileStatement><keyword>" + str(token) + "</keyword>"
        code += "<symbol>" + str(var) + "</symbol>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        var   = self.compileExpression(var)
        code  = "<symbol>" + str(var) + "</symbol>"
        var   = self.tokenizer.advance()
        code += "<symbol>" + str(var) + "</symbol><statements>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        while var != "}":
            var    = self.compileStatement(var)
        code  = "</statements><symbol>" + str(var) + "</symbol></whilestatement>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        return var
        
    def compileReturn(self, token):
        code  = "<returnstatement><keyword>" + str(token) + "</keyword>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        if var != ";":
            var = self.compileExpression(var)
        code  = "<symbol>" + str(var) + "</symbol></returnStatement>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        return var
        
    def compileIf(self, token):
        code  = "<ifStatement><keyword>" + str(token) + "</keyword>"
        var   = self.tokenizer.advance()
        code += "<symbol>" + str(var) + "</symbol>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        var   = self.compileExpression(var)
        code  = "<symbol>" + str(var) + "</symbol>"
        var   = self.tokenizer.advance()
        code  = "<symbol>" + str(var) + "</symbol><statements>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        while var != "}":
            var = self.compileStatement(var)
        code  = "</statements><symbol>" + token + "</symbol>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        if var == "else":
            var = self.compileElse(var)
        code  = "</ifStatement>"
        self.ostream.write(code)
        return var
    
    def compileElse(self, token):
        code  = "<elseStatement><keyword>" + str(token) + "</keyword>"
        var   = self.tokenizer.advance()
        code += "<symbol>" + str(var) + "</symbol><statements>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        while var != "}":
            var = self.compileStatement(var)
        code  = "</statements><symbol>" + str(var) + "</symbol></elseStatement>"
        self.ostream.write(code)
        code  = ""
        return var
        
        
        
    def compileExpression(self, token):
        self.ostream.write("<expression>")
        var  = self.compileTerm(token)
        self.ostream.write("</expression>")
        return var
    
    def RepresentsInt(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
        
    def compileTerm(self, token):
        print "Compiling" + str(token)
        self.ostream.write("<term>")
        code = ""
        if token.isdigit():
            code += "<integerConstant>" + str(token) + "</integerConstant>"
        elif token[0] == "\"":
            code  = "<stringConstant>" + str(token) + "</stringConstant>"
        elif token in ["this", "null", "true", "false"]:
            code  = "<keyword>" + str(token) + "</keyword>"
        elif token == "-":
            code  = "<symbol>" + str(token) + "</symbol>"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            var   = self.compileTerm(var)
            token = var
        elif token == "~":
            return self.compileNotOperator(token)
        elif token == "(":
            code  = "<symbol>" + str(token) + "</symbol>"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            var   = self.compileExpression(var)
            code  = "<symbol>" + str(token) + "</symbol>"
            self.ostream.write(code)
            code  = ""
            token = var
        elif self.tokenizer.peekAhead() == "[":
            code  = "<identifier>" + str(token) + "</identifier>"
            var   = self.tokenizer.advance()
            code += "<symbol>" + str(var) + "</symbol>"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            var   = self.compileExpression(var)
            code  = "<symbol>" + str(var) + "</symbol>"
            self.ostream.write(code)
            code  = ""
            token = var
        elif self.tokenizer.peekAhead() == ".":
            print "PEEKIN!"
            code  = "<identifier>" + token + "</identifier>"
            var   = self.tokenizer.advance()
            code += "<symbol>" + str(var) + "</symbol>"
            var   = self.tokenizer.advance()
            code += "<identifier>" + str(var) + "</identifier>"
            var   = self.tokenizer.advance()
            code += "<symbol>" + str(var) + "</symbol>"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            if var != ")":
                var = self.compileExpressionList(var)
                code  = "</expressionList><symbol>" + str(var) + "</symbol>"
            token = var
        else:
            code = "<identifier>" + str(token) + "</identifier>"
        code += "</term>"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        if var in ["+","<",">","=",",","&","-","*"]:
            if var in ["<",">","\"","&"]:
                if var == "<":
                    code = "<symbol>&lt;</symbol>"
                elif var == ">":
                    code = "<symbol>&gt;</symbol>"
                elif var == "\"":
                    code = "<symbol>&quot;</symbol>"
                elif var == "&":
                    code = "<symbol>&amp;</symbol>"
            else:
                code = "<symbol>" + str(var) + "</symbol>"
            self.ostream.write(code)
            code = ""
            var  = self.tokenizer.advance()
            var  = self.compileTerm(var)
            token = var
        return token
                        
    def compileNotOperator(self, token):
        code = "<symbol>" + str(token) + "</symbol>"
        self.ostream.write(code)
        var  = self.tokenizer.advance()
        if var != "(":
            var   = self.compileTerm(var)
            code  = "</term>"
            self.ostream.write(code)
            code  = ""
            return var
        else:
            code  = "<term><symbol>" + str(var) + "</symbol>"
            self.ostream.write(code)
            var   = self.tokenizer.advance()
            var   = self.compileExpression(var)
            code += "<symbol>" + str(var) + "</symbol></term></term>"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            return var
        
    def compileExpressionList(self, token):
        self.ostream.write("<expressionList>")
        var  = self.compileExpression(token)
        while var == ",":
            self.ostream.write("<symbol>" + str(var) + "</symbol>")
            var = self.compileExpression(self.tokenizer.advance())
        return var
            
