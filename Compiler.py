# -*- coding: utf-8 -*-
"""
Created on Fri Dec 01 22:43:14 2017

@author: Carson
"""
class Compiler():
    def __init__(self, istream, ostream, tokenizer):
        self.tokenizer = tokenizer;
        self.istream = open(istream, 'r')
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
      ostream.write(code)
      temp = self.tokenizer.advance()
      if(self.tokenizer.tokenType == "SYMBOL"):
          code    = "<symbol>" + temp + "<symbol>"
          ostream.write(code)
      temp = self.tokenizer.advance()
      while temp.lower() in ["static", "field"]:
          temp = self.compileClassVarDec(temp)
      while temp.lower() in ["method", "constructor", "function"]:
          temp = self.compileSubroutine(temp)
      code = "<symbol>" + str(temp) + "</symbol></class>"
      ostream.write(code)
      ostream.close()
      
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
      ostream.write(code)
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
          self.compileParamList(var)
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
      code += "</statements><symbol>" + var + "</symbol></subroutineBody></subroutineDec>"
      self.ostream.write(code)
      code = ""
      var = self.tokenizer.advance()
      if var in ["method", "constructor", "function"]:
          var = self.compileSubroutine(var)
      return var
  
    def compileParameterList():
      #Example:
      #  <parameterList>
      #  </parameterList>

        
    def compileVarDec():
      #Example:
      #<varDec>
      #  <keyword> var </keyword>
      #  <identifier> SquareGame </identifier>
      #  <identifier> game </identifier>
      #  <symbol> ; </symbol>
      #</varDec>
        
    def compileStatements():
        
    def compileDo():
        
    def compileLet():
        
    def compileWhile():
        
    def compileReturn():
        
    def compileIf():
        
    def compileExpression():
        
    def compileTerm():
        
    def compileExpressionList():
