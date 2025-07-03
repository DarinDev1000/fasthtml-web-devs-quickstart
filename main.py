import json
from fasthtml.common import *

app, rt = fast_app(
    live=True, # Hot reload
    debug=True,
    pico=False,
    hdrs=(
        Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css", type="text/css"),
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/sakura.css/css/sakura.css", type="text/css"),
        Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js"),
    ),
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


@app.get("/")
def home():
    return Titled("FastHTML",
        P("Let's do this!"),
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


@rt("/{name}/{age}")
def get(name: str, age: int):
    return Titled(f"Hello {name.title()}, age {age}")


@rt("/")
def post():
    return Titled("HTTP POST", P("Handle POST"))


serve()
