# -*- coding: utf-8 -*-
"""
Created on Mon Dec 04 01:20:38 2017

@author: Carson
"""
import sys
from JackTokenizer import JackTokenizer
#from Compiler import Compiler

class JackAnalyzer():
    def __init__(self, filename):
        self.filename  = filename
        self.tokenizer = JackTokenizer(filename)
        self.testToken()
        
    def testToken(self):
        while(self.tokenizer.hasMoreTokens()):
            token = self.tokenizer.advance()
            print token
            
JackAnalyzer(sys.argv[1])
