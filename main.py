import json
from fasthtml.common import *

hdrs = (
    MarkdownJS(),
    HighlightJS(langs=["python", "javascript", "html", "css"]),
    Link(
        rel="stylesheet",
        href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css",
        type="text/css",
    ),
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/sakura.css/css/sakura.css",
        type="text/css",
    ),
    Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js"),
)

app, rt = fast_app(
    live=True,  # Hot reload
    debug=True,
    pico=False,
    hdrs=hdrs,
    static_path="public",
)

data = json.dumps(
    {
        "data": [
            {"x": [1, 2, 3, 4], "type": "scatter"},
            {"x": [1, 2, 3, 4], "y": [16, 5, 11, 9], "type": "scatter"},
        ],
        "title": "Plotly chart in FastHTML ",
        "description": "This is a demo dashboard",
        "type": "scatter",
    }
)

content = """
Here are some _markdown_ elements.

- This is a list item
- This is another list item
- And this is a third list item

**Fenced code blocks work here.**
"""


@rt("/markdown")
def get(req):
    return Titled("Markdown rendering example", Div(content, cls="marked"))


code_example = """
import datetime
import time

for i in range(10):
    print(f"{datetime.datetime.now()}")
    time.sleep(1)
"""


@rt("/code")
def get(req):
    return Titled(
        "Markdown rendering example",
        Div(
            # The code example needs to be surrounded by
            # Pre & Code elements
            Pre(Code(code_example))
        ),
    )


def layout(*args, **kwargs):
    """Dashboard layout for all our dashboard views"""
    return Main(
        H1("Dashboard"),
        Div(*args, **kwargs),
        cls="dashboard",
    )


@app.get("/")
def home():
    return Titled(
        "FastHTML",
        P("Let's do this!"),
        # usage example
        layout(
            Ul(*[Li(o) for o in range(3)]),
            P("Some content", cls="description"),
        ),
    )


@rt("/hello")
def get():
    return Titled("Hello, world!")


@rt("/chart")
def get():
    return Titled(
        "Chart Demo",
        Div(id="myDiv"),
        Script(f"var data = {data}; Plotly.newPlot('myDiv', data);"),
    )


@rt("/person/{name}/{age}")
def get(name: str, age: int):
    return Titled(f"Hello {name.title()}, age {age}")


@rt("/")
def post():
    return Titled("HTTP POST", P("Handle POST"))


@rt("/{fname:path}.{ext:static}")
async def get(fname: str, ext: str):
    return FileResponse(f"public/{fname}.{ext}")


serve()
