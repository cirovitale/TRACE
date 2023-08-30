from flask import Flask
from flask import jsonify
import requests
import os
import json
import math
from dotenv import load_dotenv

from modules.serviceMethods import getRepoReadmeGIT, getRepoInfoGIT, getRepoContributors_Predicts

load_dotenv()
app = Flask(__name__)
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')

@app.route("/repos/<owner>/<repo>/readme")
def getRepoReadme(owner, repo):
    return getRepoReadmeGIT(owner, repo, GITHUB_API_TOKEN)

@app.route("/repos/<owner>/<repo>")
def getRepoInfo(owner, repo):
    return getRepoInfoGIT(owner, repo, GITHUB_API_TOKEN)


@app.route("/repos/<owner>/<repo>/contributors")
def getRepoContributors(owner, repo):
    return getRepoContributors_Predicts(owner, repo, GITHUB_API_TOKEN, GOOGLE_API_KEY)

