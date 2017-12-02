# -*- coding: utf-8 -*-
"""
Created on Fri Dec 01 21:32:53 2017

@author: Carson
"""
import re

keywords = {'class'       : "CLASS",
            'constructor' : "CONSTRUCTOR",
            'function'    : "FUNCTION",
            'method'      : "METHOD",
            'field'       : "FIELD",
            'static'      : "STATIC",
            'var'         : "VAR",
            'int'         : "INT",
            'char'        : "CHAR",
            'boolean'     : "BOOLEAN",
            'void'        : "VOID",
            'true'        : "TRUE",
            'false'       : "FALSE",
            'null'        : "NULL",
            'this'        : "THIS",
            'let'         : "LET",
            'do'          : "DO",
            'if'          : "IF",
            'else'        : "ELSE",
            'while'       : "WHILE",
            'return'      : "RETURN"}
symbols  = {'{','}','(',')','[',']',
            '.',',',';','+','-','*',
            '/','&','|','<','>','=',
                                '~'}
stringConst = '\"[a-zA-Z0-9]\"'
identifier  = '^(\d)[a-zA-Z0-9_]*'


def isValidConstant(num):
    if num > -1 and num < 32768:
        return True
    else:
        return False
    
class JackTokenizer():
    def __init__(self, instream):
        self.currToken = ""
        self.curritr   = -1
        self.filename  = instream
        self.filecont  = []
        self.stream    = open(instream, mode = 'r')
        for line in self.stream:
            line = line.split("//")[0] #Should split to the right of the //, may do left. -1 if so
            if line != "":
                for word in line:
                    self.filecont.append(word.replace("\n",""))
        self.currCmd   = ""
        
        
    def hasMoreTokens(self):
        if self.curritr < len(self.filecont):
            return True
        else:
            return False
        
    def advance(self):
        self.curritr += 1
        if self.hasMoreTokens():
            self.currCmd = self.filecont[self.curritr]
            return
        print "No additional commands. Advance impossible."
        return
    
    def tokenType(self):
        token = self.currToken
        if token in keywords:
            return "KEYWORD"
        if token in symbols:
            return "SYMBOL"
        if re.findall(identifier, token):
            return "IDENTIFIER"
        if isValidConstant(int(token)):
            return "INT_CONST"
        if re.findall(stringConst, token):
            return "STRING_CONST"
        
    def keyWord(self):
        if self.tokenType() == "KEYWORD":
            return keywords[self.currToken]
        else:
            print "Invalid Type! Not a keyword..."
            
    def symbol(self):
        if self.tokenType() == "SYMBOL":
            return self.currToken
        else:
            print "Invalid Type! Not a symbol..."
    
    def identifier(self):
        if self.tokenType() == "IDENTIFIER":
            return self.currToken
        else:
            print "Invalid Type! Not an identifier..."
            
    def intVal(self):
        if self.tokenType() == "INT_CONST":
            return int(self.curr)
        else:
            print "Invalid Type! Not an integer constant..."
            
    def stringVal(self):
        token = self.currToken
        if self.tokenType() == "STRING_CONST":
            token = token.replace("\"", "")
            return token
            
            
        


















