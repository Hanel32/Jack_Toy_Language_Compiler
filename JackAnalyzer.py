# -*- coding: utf-8 -*-
"""
Created on Mon Dec 04 01:20:38 2017

@author: Carson
"""
import sys
from JackTokenizer import JackTokenizer
from Compiler import Compiler

class JackAnalyzer():
    def __init__(self, filename):
        self.filename  = filename
        selection = input("Enter 1 for tokenizing, 2 for parsing: ")
        self.tokenizer = JackTokenizer(filename)
        self.filename = self.filename.replace("jack", "xml")
        self.tokens = ["<tokens>\n"]
        self.testToken()
        if(selection == 2):
            Compiler(self.filename)
        
    def testToken(self):
        while(self.tokenizer.hasMoreTokens()):
            token = self.tokenizer.advance()
            self.tokens += token
        self.tokens += "</tokens>\n"
        self.ostream = open(self.filename, mode = 'w')
        for token in self.tokens:
            self.ostream.write(token)

JackAnalyzer(sys.argv[1])
