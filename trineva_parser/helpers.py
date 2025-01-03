import re

ERROR_EMPTY_EXPRESSION = "Expression cannot be empty."
ERROR_MISMATCHED_PARENTHESES = "Mismatched parentheses."
ERROR_INVALID_OPERATOR = "Invalid operator: {}"
ERROR_INVALID_STRUCTURE = "Invalid expression structure."
ERROR_DIVISION_BY_ZERO = "Division by zero is not allowed."
ERROR_INVALID_VARIABLE = "Invalid variable name: {}"
ERROR_UNDEFINED_VARIABLE = "Undefined variable: {}"

class InvalidExpressionException(Exception):
    pass

def evaluate(expression_list, variables=None):
    if variables is None:
        variables = {}

    parts = expression_list.split(';')
    for part in parts[:-1]:
        if '=' not in part:
            raise InvalidExpressionException(ERROR_INVALID_STRUCTURE)
        var, value = map(str.strip, part.split('=', 1))
        if not re.match(r'\b[a-zA-Z_]\w*\b', var):
            raise InvalidExpressionException(ERROR_INVALID_VARIABLE.format(var))

        variables[var] = evaluate(value, variables)

    expression_list = parts[-1].strip()
    if not expression_list:
        raise InvalidExpressionException(ERROR_EMPTY_EXPRESSION)

    expression_list = re.sub(r'//.*?//', '', expression_list).strip()
    tokens = re.split(r'(\b[a-zA-Z_]\w*\b|\d+\.\d+|\d+|[+\-*/()])', expression_list)
    tokens = [t.strip() for t in tokens if t.strip()]

    for i, token in enumerate(tokens):
        if re.match(r'\b[a-zA-Z_]\w*\b', token):
            if token in variables:
                tokens[i] = str(variables[token])
            else:
                raise InvalidExpressionException(ERROR_UNDEFINED_VARIABLE.format(token))

    expression_list = ''.join(tokens)

    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    def apply_operator(o, v):
        if len(v) < 2:
            raise InvalidExpressionException(ERROR_INVALID_STRUCTURE)
        operator = o.pop()
        right = v.pop()
        left = v.pop()
        if operator == '+':
            v.append(left + right)
        elif operator == '-':
            v.append(left - right)
        elif operator == '*':
            v.append(left * right)
        elif operator == '/':
            if right == 0:
                raise InvalidExpressionException(ERROR_DIVISION_BY_ZERO)
            v.append(left / right)

    values = []
    operators = []
    i = 0

    while i < len(expression_list):
        char = expression_list[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit() or char == '.' or (char == '-' and (i == 0 or expression_list[i - 1] in '(*+-/')):
            num_str = ''
            if char == '-':
                num_str += '-'
                i += 1
            while i < len(expression_list) and (expression_list[i].isdigit() or expression_list[i] == '.'):
                num_str += expression_list[i]
                i += 1
            values.append(float(num_str) if '.' in num_str else int(num_str))
            i -= 1

        elif char == '(':
            operators.append(char)

        elif char == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            if not operators or operators[-1] != '(':
                raise InvalidExpressionException(ERROR_MISMATCHED_PARENTHESES)
            operators.pop()

        elif char in '+-*/':
            while (operators and operators[-1] != '(' and
                   precedence(operators[-1]) >= precedence(char)):
                apply_operator(operators, values)
            operators.append(char)

        else:
            raise InvalidExpressionException(ERROR_INVALID_OPERATOR.format(char))

        i += 1

    while operators:
        if operators[-1] == '(':
            raise InvalidExpressionException(ERROR_MISMATCHED_PARENTHESES)
        apply_operator(operators, values)

    if len(values) != 1:
        raise InvalidExpressionException(ERROR_INVALID_STRUCTURE)

    return values[0]