from flask import Flask, request ,jsonify, redirect, url_for, render_template
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


@app.route("/generate_keys", methods=["GET"])
def generate_keys_endpoint():
    if request.method == "GET":
        ecc_setup = get_ecc_setup()
        priv, pub = generate_keypair(ecc_setup)
        result = {"private_key": str(priv.secret), "public_key": str(pub.W.x) + ", " + str(pub.W.y)}
        return jsonify(result)

@app.route("/sign", methods=["POST"])
def sign_endpoint():
    if request.method == "POST":
        print("request JSON...........", request.json)
        private_key = request.json["private_key"]
        message = request.json["message"].encode() # convt to bytes array

        ecc_setup = get_ecc_setup()
        priv, _ = generate_keypair(ecc_setup, int(private_key))
        signature = sign(priv, message)
        result = {"signature": str(signature.c) + ", " + str(signature.d)}
        return jsonify(result)

@app.route("/verify", methods=["POST"])
def verify_endpoint():
    if request.method == "POST":
        print("request JSON...........", request.json)
        private_key = request.json["private_key"]
        message = request.json["message"].encode()
        signature_c, signature_d = request.json["signature"]["c"], request.json["signature"]["d"]

        ecc_setup = get_ecc_setup()
        priv, pub = generate_keypair(ecc_setup, int(private_key))

        signature = ECDSASignature(c=int(signature_c), d=int(signature_d))

        validation = verify_signature(pub, message, signature)
        result = {"validation": validation}
        return jsonify(result)

if __name__ == "__main__":
 app.run(debug = True)