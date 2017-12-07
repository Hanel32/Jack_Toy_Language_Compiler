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
      code  = "<class>\n<keyword>" + str(token) + "</keyword>\n" 
      code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>\n"
      self.ostream.write(code)
      temp = self.tokenizer.advance()
      print "MAXFLAG" + self.tokenizer.tokenType(temp)
      if(self.tokenizer.tokenType(temp) == "SYMBOL"):
          code    = "<symbol>" + temp + "</symbol>\n"
          self.ostream.write(code)
      temp = self.tokenizer.advance()
      while temp.lower() in ["static", "field"]:
          temp = self.compileClassVarDec(temp)
      while temp.lower() in ["method", "constructor", "function"]:
          temp = self.compileSubroutine(temp)
      code = "<symbol>" + str(temp) + "</symbol>\n</class>\n"
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
      code  = "<classVarDec>\n<keyword>" + str(token) + "</keyword>\n"
      var   = self.tokenizer.advance()
      if var in ["int", "boolean", "char"]:
          code += "<keyword>" + var + "</keyword>\n"
      else:
          code += "<identifier>" + var + "</identifier>\n"
      code += "<identifier>" + self.tokenizer.advance() + "</identifier>\n"
      self.ostream.write(code)
      code  = ""
      var   = self.tokenizer.advance()
      while var == ",":
          code += "<symbol>" + str(var) + "</symbol>\n"
          var = self.tokenizer.advance()
          code += "<identifier>" + str(var) + "</identifier>\n"
          var = self.tokenizer.advance()
      code += "<symbol>" + var + "</symbol>\n</classVarDec>\n"
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
      code = "<subroutineDec>\n<keyword>" + str(token) + "</keyword>\n"
      var = ""
      if token == "constructor":
          var = self.tokenizer.advance()
          code += "<identifier>" + str(var) + "</identifier>\n"
      else:
          var = self.tokenizer.advance()
          code += "<keyword>" + str(var) + "</keyword>\n"
      code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>\n"
      code += "<symbol>" + str(self.tokenizer.advance()) + "</symbol>\n"
      self.ostream.write(code)
      code  = ""
      var   = self.tokenizer.advance()
      if var != ")":
          var = self.compileParameterList(var)
      else:
          code += "<parameterList>\n</parameterList>\n"
      code += "<symbol>" + str(var) + "</symbol>\n"
      code += "<subroutineBody>\n<symbol>" + str(self.tokenizer.advance()) + "</symbol>\n"
      self.ostream.write(code)
      code  = ""
      var = self.tokenizer.advance()
      if var == "var":
          var = self.compileVarDec(var)
      self.ostream.write("<statements>\n")
      while var not in ["}", None]:
          var = self.compileStatement(var)
      code += "</statements>\n<symbol>" + str(var) + "</symbol>\n</subroutineBody>\n</subroutineDec>\n"
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
      code  = "<parameterList>\n"
      code += "<keyword>" + str(token) + "</keyword>\n"
      code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>\n"
      self.ostream.write(code)
      code  = ""
      var   = self.tokenizer.advance()
      while var == ",":
          code += "<symbol>" + var + "</symbol>\n"
          code += "<keyword>" + str(self.tokenizer.advance()) + "</keyword>\n"
          code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>\n"
          self.ostream.write(code)
          var = self.tokenizer.advance()
          code  = ""
      self.ostream.write("</parameterList>\n")
      return var  
        
    def compileVarDec(self, token):
      #Example:
      #<varDec>
      #  <keyword> var </keyword>
      #  <identifier> SquareGame </identifier>
      #  <identifier> game </identifier>
      #  <symbol> ; </symbol>
      #</varDec>
      code = "<varDec>\n<keyword>" + str(token) + "</keyword>\n"
      var  = self.tokenizer.advance()
      if var in ["char", "boolean", "int"]:
          code += "<keyword>" + str(var) + "</keyword>\n"
      else:
          code += "<identifier>" + str(var) + "</identifier>\n"
      var  = self.tokenizer.advance()
      code+= "<identifier>" + str(var) + "</identifier>\n"
      self.ostream.write(code)
      code = ""
      var  = self.tokenizer.advance()
      while var == ",":
          code += "<symbol>" + str(var) + "</symbol>\n"
          code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>\n"
          self.ostream.write(code)
          code  = ""
          var   = self.tokenizer.advance()
      code = "<symbol>" + str(var) + "</symbol>\n</varDec>\n"
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
        code  = "<doStatement>\n<keyword>" + str(token) + "</keyword>\n"
        code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>\n"
        var   = self.tokenizer.advance()
        print "Var: " + str(var)
        if var == ".":
            print "Period in do statement!"
            code += "<symbol>" + str(var) + "</symbol>\n"
            code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>\n"
            code += "<symbol>" + str(self.tokenizer.advance()) + "</symbol>\n"
            print "Generated code: " + code
        else:
            code += "<symbol>" + str(var) + "</symbol>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        if var != ")":
            var   = self.compileExpressionList(var)
        else:
            code += "<expressionList>\n"
        code += "</expressionList>\n<symbol>" + str(var) + "</symbol>\n"
        var   = self.tokenizer.advance()
        code += "<symbol>" + str(var) + "</symbol>\n</doStatement>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        
        return var
    
    def compileLet(self, token):
        code  = "<letStatement>\n<keyword>" + str(token) + "</keyword>\n"
        code += "<identifier>" + str(self.tokenizer.advance()) + "</identifier>\n"
        self.ostream.write(code)
        var   = self.tokenizer.advance()
        if var  == "[":
            code = "<symbol>" + str(var) + "</symbol>\n"
            self.ostream.write(code)
            code = ""
            var  = self.tokenizer.advance()
            var  = self.compileExpression(var)
            code = "<symbol>" + str(var) + "</symbol>\n"
            self.ostream.write(code)
            code = ""
            var  = self.tokenizer.advance()
            
        code = "<symbol>" + str(var) + "</symbol>\n"
        self.ostream.write(code)
        code = ""
        var  = self.tokenizer.advance()
        var  = self.compileExpression(var)
        code = "<symbol>" + str(var) + "</symbol>\n</letStatement>\n"
        self.ostream.write(code)
        code = ""
        var  = self.tokenizer.advance()
        return var
        
        
    def compileWhile(self, token):
        var   = self.tokenizer.advance()
        code  = "<whileStatement>\n<keyword>" + str(token) + "</keyword>\n"
        code += "<symbol>" + str(var) + "</symbol>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        var   = self.compileExpression(var)
        code  = "<symbol>" + str(var) + "</symbol>\n"
        var   = self.tokenizer.advance()
        code += "<symbol>" + str(var) + "</symbol>\n<statements>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        while var != "}":
            var    = self.compileStatement(var)
        code  = "</statements>\n<symbol>" + str(var) + "</symbol>\n</whileStatement>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        return var
        
    def compileReturn(self, token):
        code  = "<returnStatement>\n<keyword>" + str(token) + "</keyword>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        if var != ";":
            var = self.compileExpression(var)
        code  = "<symbol>" + str(var) + "</symbol>\n</returnStatement>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        return var
        
    def compileIf(self, token):
        code  = "<ifStatement>\n<keyword>" + str(token) + "</keyword>\n"
        var   = self.tokenizer.advance()
        code += "<symbol>" + str(var) + "</symbol>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        var   = self.compileExpression(var)
        code  = "<symbol>" + str(var) + "</symbol>\n"
        var   = self.tokenizer.advance()
        code  += "<symbol>" + str(var) + "</symbol>\n<statements>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        while var != "}":
            var = self.compileStatement(var)
        code  = "</statements>\n<symbol>" + str(var) + "</symbol>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        if var == "else":
            var = self.compileElse(var)
        code  = "</ifStatement>\n"
        self.ostream.write(code)
        return var
    
    def compileElse(self, token):
        code  = "<elseStatement>\n<keyword>" + str(token) + "</keyword>\n"
        var   = self.tokenizer.advance()
        code += "<symbol>" + str(var) + "</symbol>\n<statements>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        while var != "}":
            var = self.compileStatement(var)
        code  = "</statements>\n<symbol>" + str(var) + "</symbol>\n</elseStatement>\n"
        self.ostream.write(code)
        code  = ""
        return var
    
    def RepresentsInt(self, s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
        
    def compileTerm(self, token):
        var = token
        print "Compiling" + str(token)
        self.ostream.write("<term>\n")
        code = ""
        if self.RepresentsInt(token):
            code = "<integerConstant>" + str(token) + "</integerConstant>\n"
        elif token[0] == "\"":
            print "Handling a string constant: " + str(token)
            temp = token.replace("\"", "")
            code  = "<stringConstant>" + str(temp) + "</stringConstant>\n"
            print "Code generated: " + str(code)
        elif token in ["this", "null", "true", "false"]:
            code  = "<keyword>" + str(token) + "</keyword>\n"
        elif token == "-":
            code  = "<symbol>" + str(token) + "</symbol>\n"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            var   = self.compileTerm(var)
        elif token == "~":
            return self.compileNotOperator(token)
        elif token == "(":
            code  = "<symbol>" + str(token) + "</symbol>\n"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            var   = self.compileExpression(var)
            code  = "<symbol>" + str(token) + "</symbol>\n"
            self.ostream.write(code)
            code  = ""
        elif self.tokenizer.peekAhead() == "[":
            print "PEEKIN!" + str(self.tokenizer.peekAhead())
            code  = "<identifier>" + str(token) + "</identifier>\n"
            var   = self.tokenizer.advance()
            code += "<symbol>" + str(var) + "</symbol>\n"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            var   = self.compileExpression(var)
            code  = "<symbol>" + str(var) + "</symbol>\n"
            self.ostream.write(code)
            code  = ""
        elif self.tokenizer.peekAhead() == ".":
            print "PEEKIN!" + str(self.tokenizer.peekAhead())
            code  = "<identifier>" + token + "</identifier>\n"
            var   = self.tokenizer.advance()
            code += "<symbol>" + str(var) + "</symbol>\n"
            var   = self.tokenizer.advance()
            code += "<identifier>" + str(var) + "</identifier>\n"
            var   = self.tokenizer.advance()
            code += "<symbol>" + str(var) + "</symbol>\n"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            if var != ")":
                var = self.compileExpressionList(var)
                print "Token after expressionList = " + str(var)
                code  = "</expressionList>\n<symbol>" + str(var) + "</symbol>\n"
        else:
            code = "<identifier>" + str(token) + "</identifier>\n"
        print "At the end: " + code
        code += "</term>\n"
        self.ostream.write(code)
        code  = ""
        var   = self.tokenizer.advance()
        if var in ["+","<",">","=","&","-","*"]:
            if var in ["<",">","\"","&"]:
                if var == "<":
                    code = "<symbol>&lt;</symbol>\n"
                elif var == ">":
                    code = "<symbol>&gt;</symbol>\n"
                elif var == "\"":
                    code = "<symbol>&quot;</symbol>\n"
                elif var == "&":
                    code = "<symbol>&amp;</symbol>\n"
            else:
                code = "<symbol>" + str(var) + "</symbol>\n"
            self.ostream.write(code)
            code = ""
            var  = self.tokenizer.advance()
            var  = self.compileTerm(var)
        return var
                        
    def compileNotOperator(self, token):
        code = "<symbol>" + str(token) + "</symbol>\n"
        self.ostream.write(code)
        var  = self.tokenizer.advance()
        if var != "(":
            var   = self.compileTerm(var)
            code  = "</term>\n"
            self.ostream.write(code)
            code  = ""
            return var
        else:
            code  = "<term>\n<symbol>" + str(var) + "</symbol>\n"
            self.ostream.write(code)
            var   = self.tokenizer.advance()
            var   = self.compileExpression(var)
            code += "<symbol>" + str(var) + "</symbol>\n</term>\n</term>\n"
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            return var
        
    def compileExpression(self, token):
        self.ostream.write("<expression>\n")
        var  = self.compileTerm(token)
        print "WORKING A SINGLE EXPRESSION"
        print "Var is: " + str(var)
        while var in ["+","<",">","=","&","-","*", "\"", "/"]:
            print "Var is: " + str(var)
            if var in ["<",">","\"","&"]:
                if var == "<":
                    code = "<symbol>&lt;</symbol>\n"
                elif var == ">":
                    code = "<symbol>&gt;</symbol>\n"
                elif var == "\"":
                    code = "<symbol>&quot;</symbol>\n"
                elif var == "&":
                    code = "<symbol>&amp;</symbol>\n"
            else:
                code  = "<symbol>" + str(var) + "</symbol>\n"
            print "CompileExpression code: " + str(code)
            self.ostream.write(code)
            code  = ""
            var   = self.tokenizer.advance()
            print "CALLING ANOTHER TERM"
            var   = self.compileTerm(var)
        self.ostream.write("</expression>\n")
        print "COMPILED A SINGLE EXPRESSION"
        return var
        
    def compileExpressionList(self, token):
        print "Working in expressionList"
        self.ostream.write("<expressionList>\n")
        var  = self.compileExpression(token)
        print "Var is: " + str(var)
        while var == ",":
            print "More expressions! for " + self.tokenizer.peekAhead()
            self.ostream.write("<symbol>" + str(var) + "</symbol>\n")
            var = self.compileExpression(self.tokenizer.advance())
        return var
