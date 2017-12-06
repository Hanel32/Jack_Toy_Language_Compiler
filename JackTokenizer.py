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
stringConst = '\".+\"'
identifier  = '^[a-zA-Z0-9_]+'


def isValidConstant(num):
    try:
        int(num)
        return True
    except ValueError:
        return False
    if num > -1 and num < 32768:
        return True
    else:
        return False
    
class JackTokenizer():
    def __init__(self, instream):
        self.currToken = ""
        self.curritr   = 0
        self.filename  = instream
        self.filecont  = []
        self.stream    = open(instream, mode = 'r')
        self.commentFlag = False
        for line in self.stream:
            line = line.split("//")[0]
            if(line.find("/**") != -1):
                if(line.find("*/") != -1):
                    tempLine = line
                    tempLine = tempLine.split("*/")[-1]
                    line = line.split("/**")[0] + tempLine
                else:
                    line = line.split("/**")[0]
                    self.commentFlag = True
            if(line.find("*/") != -1):
                self.commentFlag = False
                line = line.split("*/")[-1]
            if(self.commentFlag and (line.find("*") != -1)):
                line = ""
            if(line.find("\"") != -1):
                tempLine = line
                line = []
                i = 0
                j = 0
                i = tempLine.find("\"", 0)
                j = tempLine.find("\"", i+1)
                line += tempLine[0:i].split()
                line.append(tempLine[i:(j+1)])
                line += tempLine[(j+1):].split()
            else:
                line = line.split()
            for char in line:
                sym_split = "{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~"
                self.filecont += re.split("(" + sym_split + ")", char)
        self.filecont = [word for word in self.filecont if word not in ["",'']]
        
    def hasMoreTokens(self):
        if self.curritr < len(self.filecont):
            return True
        else:
            return False
        
    def advance(self):
        if self.hasMoreTokens():
            self.currToken = self.filecont[self.curritr]
            self.curritr += 1
            return self.evalToken()
        return 
    
    def tokenType(self):
        token = self.currToken
        if token in keywords:
            return "KEYWORD"
        if token in symbols:
            return "SYMBOL"
        if isValidConstant(token):
            return "INT_CONST"
        if re.findall(identifier, token):
            return "IDENTIFIER"
        if re.findall(stringConst, token):
            return "STRING_CONST"
        
    def evalToken(self):
        token = self.currToken
        if self.tokenType() == "KEYWORD":
            return "<keyword> " + self.currToken + " </keyword>\n"
        if self.tokenType() == "SYMBOL":
            token = token.replace("&", "&amp;")
            token = token.replace("\"", "&quot;")
            token = token.replace(">", "&gt;")
            token = token.replace("<", "&lt;")
            return "<symbol> " + token + " </symbol>\n"
        if self.tokenType() == "IDENTIFIER":
            return "<identifier> " + token + " </identifier>\n"
        if self.tokenType() == "INT_CONST":
            return "<integerConstant> " + token + " </integerConstant>\n"
        if self.tokenType() == "STRING_CONST":
            token = token.replace("\"", "")
            return "<stringConstant> " + token + " </stringConstant>\n"
        print "error! TokenType not properly handled. token: " + token
