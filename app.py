from flask import Flask, redirect
from lab1 import lab1
from lab2 import lab2

app = Flask(__name__)

@app.route("/")
def start():
    return redirect('/lab2/', code=302)


app.register_blueprint(lab1)
app.register_blueprint(lab2)

if __name__ == "__main__":
    app.run(debug=True)
