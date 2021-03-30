from flask import Flask, url_for
import os

app = Flask(__name__)
app._static_folder = os.path.abspath("app/static")

#print(app._static_folder)

from app import routes

if __name__ == '__main__':
    app.run(debug=True)
    