from flask import Flask, redirect, url_for, render_template
from lab1 import lab1

app=Flask(__name__)
app.register_blueprint(lab1)

