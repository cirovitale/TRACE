from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/repoUsers")
def repoUsers():
    users = [
        {
            'id': 1,
            'name': "John",
            'surname': "Doe",
            'nationality': "USA",
            'avatarUrl': "https://example.com/avatar1.jpg",
        },
        {
            'id': 2,
            'name': "Ciro",
            'surname': "Vitale",
            'nationality': "IT",
            'avatarUrl': "https://example.com/avatar2.jpg",
        },
    ]
    return users

if __name__ == "__main__":
    app.run(debug = True)