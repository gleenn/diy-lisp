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

    if ast == "#t":
        return True

    if ast == "#f":
        return False

    if is_symbol(ast):
        symbol_value = env.lookup(ast)
        # if is_closure(symbol_value):
        #     return evaluate(symbol_value, env)
        return symbol_value

    if is_integer(ast):
        return ast

    first_element = ast[0]

    if first_element == "quote":
        if len(ast) == 2:
            return ast[1]
        else:
            return []

    if first_element == "atom":
        return is_atom(evaluate(ast[1], env))

    if first_element == "if":
        if evaluate(ast[1], env):
            return evaluate(ast[2], env)
        else:
            return evaluate(ast[3], env)

    if first_element == "define":
        if len(ast) != 3:
            raise LispError("Wrong number of arguments")

        symbol_name = ast[1]

        if not is_symbol(symbol_name):
            raise LispError("non-symbol")

        value = evaluate(ast[2], env)
        env.set(symbol_name, value)
        return value

    if first_element == "eq":
        evaluated_items = [evaluate(item, env) for item in ast[1:]]
        for i in range(len(evaluated_items) - 1):
            return is_atom(evaluated_items[i]) and evaluated_items[i] == evaluated_items[i + 1]
        else:
            return True

    if first_element in ["+", "-", "*", "/", "mod", "<", ">"] and not (is_integer(evaluate(ast[1], env)) and is_integer(
            evaluate(ast[2], env))):
        error_message = "Math functions only take integer args but you tried to do (%s, %s, %s)" % (
        first_element, (evaluate(ast[1], env)), (evaluate(ast[2], env)))
        raise LispError(error_message)

    if first_element == "+":
        return evaluate(ast[1], env) + evaluate(ast[2], env)

    if first_element == "-":
        return evaluate(ast[1], env) - evaluate(ast[2], env)

    if first_element == "*":
        return evaluate(ast[1], env) * evaluate(ast[2], env)

    if first_element == "/":
        return evaluate(ast[1], env) / evaluate(ast[2], env)

    if first_element == "mod":
        return evaluate(ast[1], env) % evaluate(ast[2], env)

    if first_element == ">":
        return evaluate(ast[1], env) > evaluate(ast[2], env)

    if first_element == "<":
        return evaluate(ast[1], env) < evaluate(ast[2], env)

    if first_element == "lambda":
        if len(ast) != 3:
            raise LispError("number of arguments")
        params = ast[1]
        if not is_list(params):
            raise LispError("params must be a list")
        body = ast[2]
        return Closure(env, params, body)

    if is_list(ast):
        print first_element

        if len(ast) == 0:
            return []

        if is_symbol(first_element) and env.has_symbol(first_element):
            closure = env.lookup(first_element)

        elif is_closure(first_element):
            closure = first_element

        else:
            closure = evaluate(first_element, env)
            if not is_closure(closure):
                raise LispError("not a function")

        argument_bindings = {}
        if len(ast) > 1:
            param_values = ast[1:]
            closure_params = closure.params
            if len(closure_params) != len(param_values):
                raise LispError("wrong number of arguments, expected %i got %i" % (len(closure_params), len(param_values)))
            for i in range(len(closure_params)):
                param_name = closure_params[i]
                argument_bindings[param_name] = evaluate(param_values[i], env)

        result = evaluate(closure.body, closure.env.extend(argument_bindings))
        print result
        if is_closure(result):
            return evaluate(result.body, result.env)
        return result