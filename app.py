import os

from flask import Flask, render_template, request

@app.route('/')
def hello_world():
    return 'Hello, World!'