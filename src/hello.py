from flask import Flask

app = Flask('hello')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def flask_run():
    app.run(port=8000)
