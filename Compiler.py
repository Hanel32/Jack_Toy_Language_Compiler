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
        self.compileClass()
        
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
      code  = "<class><keyword>" + token + "</keyword>"
      tokenizer.advance()      
      code += "<identifier>" + tokenizer.identifier() + "</identifier>"
      ostream.write(code)
      tokenizer.advance()
      if(tokenizer.tokenType == "SYMBOL"):
        bracket = tokenizer.symbol()
        code    = "<symbol>" + bracket + "<symbol>"
      tokenizer.advance()
      
      
    def compileClassVarDec():  
      # Example:
      #   <classVarDec>
      #    <keyword> static </keyword>
      #    <keyword> boolean </keyword>
      #    <identifier> test </identifier>
      #    <symbol> ; </symbol>
      #   </classVarDec>

        
    def compileSubroutine():
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
