from flask import Flask, redirect, url_for, render_template
from ecdsa import *

app = Flask(__name__)


# Defining the home page of our site
@app.route("/")  # this sets the route to this page
def home():
 ecc_setup = get_ecc_setup()
 print(f"E: y^2 = x^3 + {ecc_setup.E.a}x + {ecc_setup.E.b} (mod {ecc_setup.E.p})")
 print(f"base point G({ecc_setup.G.x}, {ecc_setup.G.y})")
 print(f"order(G, E) = {ecc_setup.r}")
 return render_template("sample-ecdsa.html")  # some basic inline html

if __name__ == "__main__":
 app.run(debug = True)