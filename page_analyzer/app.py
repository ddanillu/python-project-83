from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def welcome():
    return jsonify("Welcome to Page Analyzer!")


if __name__ == "__main__":
    app.run(debug=True)