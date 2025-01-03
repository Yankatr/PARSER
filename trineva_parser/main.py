from flask import Flask, render_template, request

from helpers import *


app = Flask(__name__)

expressions_list = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global expressions_list
    solved_expression = None
    result = None

    if request.method == 'POST':
        action = request.form.get('action')
        idx = request.form.get('index')

        try:
            if action == 'add':
                new_expression = request.form.get('expression')
                if not new_expression.strip():
                    raise InvalidExpressionException(ERROR_EMPTY_EXPRESSION)
                expressions_list.append(new_expression)
            elif action == 'delete' and idx is not None:
                idx = int(idx)
                if 0 <= idx < len(expressions_list):
                    del expressions_list[idx]
            elif action == 'solve' and idx is not None:
                idx = int(idx)
                if 0 <= idx < len(expressions_list):
                    solved_expression = expressions_list[idx]
                    result = evaluate(solved_expression)
        except InvalidExpressionException as e:
            result = str(e)

    return render_template(
        'index.html',
        expressions=expressions_list,
        solved_expression=solved_expression,
        result=result,
    )

if __name__ == '__main__':
    app.run(debug=True)
