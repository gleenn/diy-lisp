# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The LispError class you can have for free :)
"""

class LispError(Exception): 
    """General lisp error class."""
    pass

class Closure:
    
    def __init__(self, env, params, body):
        self.env = env
        self.params = params
        self.body = body

    def __str__(self):
        return "<closure/%d>" % len(self.params)

class Environment:

    def __init__(self, variables=None):
        self.variables = variables if variables else {}

    def lookup(self, symbol):
        if self.variables.has_key(symbol):
            return self.variables[symbol]
        else:
            raise LispError("symbol not found: %s" % symbol)

    def has_symbol(self, symbol):
        return self.variables.has_key(symbol)

    def extend(self, variables):
        environment_copy = self.variables.copy()
        environment_copy.update(variables)
        return Environment(environment_copy)

    def set(self, symbol, value):
        if self.variables.has_key(symbol):
            raise LispError("symbol %s already defined" % symbol)
        else:
            self.variables[symbol] = value
