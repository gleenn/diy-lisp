# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    if is_atom(ast):
        return ast

    function_name = ast[0]

    if function_name == "quote":
        if len(ast) == 2:
            return ast[1]
        else:
            return []

    first_arg = evaluate(ast[1], env)

    if function_name == "atom":
        return is_atom(first_arg)

    if function_name == "if":
        if first_arg:
            return evaluate(ast[2], env)
        else:
            return evaluate(ast[3], env)

    second_arg = evaluate(ast[2], env)

    if function_name == "eq":
        evaluated_items = [evaluate(item, env) for item in ast[1:]]
        for i in range(len(evaluated_items) - 1):
            return is_atom(evaluated_items[i]) and evaluated_items[i] == evaluated_items[i + 1]
        else:
            return True

    if function_name in ["+", "-", "*", "/", "mod", "<", ">"] and not (is_integer(first_arg) and is_integer(second_arg)):
        error_message = "Math functions only take integer args but you tried to do (%s, %s, %s)" % (
        function_name, first_arg, second_arg)
        raise LispError(error_message)

    if function_name == "+":
        return first_arg + second_arg

    if function_name == "-":
        return first_arg - second_arg

    if function_name == "*":
        return first_arg * second_arg

    if function_name == "/":
        return first_arg / second_arg

    if function_name == "mod":
        return first_arg % second_arg

    if function_name == ">":
        return first_arg > second_arg

    if function_name == "<":
        return first_arg < second_arg

    return [evaluate(x, env) for x in ast]