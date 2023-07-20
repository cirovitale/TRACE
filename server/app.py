from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/test")
def test():
    return { 'name': 'Henry', 'surname': 'Lerry', 'country': 'EN' }

if __name__ == "__main__":
    app.run(debug = True)