import ast
import traceback

import panel as pn

pn.config.sizing_mode = "stretch_both"
pn.extension()

source_template = """\
def greet(name):
    return "Hello, " + name

def main():
    name = input("What's your name? ")
    print(greet(name))

if __name__ == "__main__":
    main()
"""

source_editor = pn.widgets.Ace(
    value=source_template,
    language="python",
)


def _dump_tree(source_code: str) -> str:
    tree = ast.parse(source_code)
    return ast.dump(tree, indent=4)


def run_ast_dump(
    source_code: str,
) -> pn.widgets.Ace:
    try:
        result = _dump_tree(source_code)
        language = "python"
    except Exception:
        result = traceback.format_exc()
        language = "text"

    return pn.widgets.Ace(
        value=result,
        language=language,
        readonly=True,
    )


result_editor = pn.bind(run_ast_dump, source_editor)

docs_button = pn.widgets.Button(name="AST docs", button_type="primary", width=100)
docs_button.js_on_click(
    code="window.open('https://docs.python.org/3/library/ast.html')"
)

app_row = pn.Row(source_editor, result_editor)


bootstrap = pn.template.MaterialTemplate(title="Print an AST node")
bootstrap.header.append(pn.Row(docs_button))
bootstrap.main.append(app_row)
bootstrap.servable()
