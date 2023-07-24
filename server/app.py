from flask import Flask
from flask import jsonify
import requests
import os
import logging
from business_logic.search_pdf import search_pdf

app = Flask(__name__)

github_api_token = os.getenv('github_api_token')

@app.route("/repos/<owner>/<repo>")
def getRepoInfo(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_api_token}"
    }
    
    try:
        # Do GET request to GitHub API
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print('QUI 1', jsonify(data))
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        # If an error occurs during the request, extract the error message and code
        errorFullMessage = e.args[0]
        errorCode = errorFullMessage.split(" ")[0]
        errorMessage = " ".join(errorFullMessage.split(" ")[1:])
        
        return jsonify({
            "error": errorMessage,
            "status": errorCode
        }), errorCode

@app.route("/repos/<owner>/<repo>/contributors")
def getRepoContributors(owner, repo):
    page = 1
    flag = True
    contributors = []

    while flag == True:
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100&page={page}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {github_api_token}",
        }

        try:
            # Do GET request to GitHub API
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
        
        except requests.exceptions.RequestException as e:
            # If an error occurs during the request, extract the error message and code
            errorFullMessage = e.args[0]
            errorCode = errorFullMessage.split(" ")[0]
            errorMessage = " ".join(errorFullMessage.split(" ")[1:])
            
            return jsonify({
                "error": errorMessage,
                "status": errorCode
            }), errorCode        

        # Find all contributors info
        count = 0
        for record in data:
            count += 1
            user = getUser(record['login'])

            if(not isinstance(user, dict) and user[0]['status'] == "403"):
                return jsonify(user[0]), user[0]['status']
            else:
                # If there aren't error in getUser call
                contributors.append(user)

                # MODULO CV
                # Search CV in contributor's portfolio
                url = user['blog']
                if(url != ''):
                    if not (url.startswith("http://") or url.startswith("https://")):
                        url = "http://" + url
                    print('Searching pdfs in ', url, ' website of ', user['login'])
                    
                    pdfs = search_pdf(url)

                    if pdfs is not None and len(pdfs) > 0:
                        user['pdfs'] = pdfs

                # MODULO COMMIT
                # Search 10 commits of contributor
                commits = getCommits(user['login'], owner, repo, 3)
                print('Searching commits of ', user['login'])
                user['commits'] = commits

        if(count == 100):
            page += 1
            flag = True
        else:
            flag = False

        if flag == False:
            return jsonify(contributors)

def getCommits(username, owner, repo, perPage):
    i = 0
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?committer={username}&page=1&per_page={perPage}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_api_token}"
    }

    try:
        # Do GET request to GitHub API
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        commits = response.json()
        if len(commits) == 0:
            return None
        return commits
    except requests.exceptions.RequestException as e:
        # If an error occurs during the request, extract the error message and code
        errorFullMessage = e.args[0]
        errorCode = errorFullMessage.split(" ")[0]
        errorMessage = " ".join(errorFullMessage.split(" ")[1:])

        return {
            "error": errorMessage,
            "status": errorCode
        }, errorCode

def getUser(username):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_api_token}"
    }
    
    try:
        # Do GET request to GitHub API
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        # If an error occurs during the request, extract the error message and code
        errorFullMessage = e.args[0]
        errorCode = errorFullMessage.split(" ")[0]
        errorMessage = " ".join(errorFullMessage.split(" ")[1:])

        return {
            "error": errorMessage,
            "status": errorCode
        }, errorCode
