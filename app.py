from flask import Flask
from config import app
from models import User, Store, Product, Request



if __name__ == "__main__":
    app.run(port=5555,debug=True)