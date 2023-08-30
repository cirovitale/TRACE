from flask import jsonify
import requests
from langdetect import detect

def getCommits(username, owner, repo, perPage, GITHUB_API_TOKEN):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?committer={username}&page=1&per_page={perPage}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_API_TOKEN}"
    }

    try:
        # Do GET request to GitHub API
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        commits = response.json()
        if len(commits) == 0:
            return None
        else:
            return commits
        
    except requests.exceptions.RequestException as e:
        # If an error occured during api call
        errorFullMessage = e.args[0]
        errorCode = errorFullMessage.split(" ")[0]
        errorMessage = " ".join(errorFullMessage.split(" ")[1:])

        print(f"[GITHUB API] Error GitHub accessing repo's commits: {e}")
        return jsonify({
            "error": errorMessage,
            "status": errorCode
        }, errorCode)
    except Exception as e:
        # If an error occured during api call
        errorFullMessage = e.args[0]
        errorCode = errorFullMessage.split(" ")[0]
        errorMessage = " ".join(errorFullMessage.split(" ")[1:])

        print(f"[GITHUB API] Error GitHub accessing repo's commits: {e}")
        return jsonify({
            "error": errorMessage,
            "status": errorCode
        }, errorCode)

def predictFromCommits(username, owner, repo, perPage, GITHUB_API_TOKEN, GOOGLE_API_KEY):
    print('Searching commits of ', username + '...')
    commits = getCommits(username, owner, repo, perPage, GITHUB_API_TOKEN)
    if commits is None:
        return
    isoDectCounter = {}
    maxIsoCounter = 0
    maxIsoCode = None
    flag = False
    # For each commit detect language and count type of language detected, counts EN only if it is the only language detected
    for index, commit in enumerate(commits):
        if(GOOGLE_API_KEY != ""):
            isoDetected = detectLanguageFromCommitGoogle(commit['commit']['message'], GOOGLE_API_KEY).upper()
        else:
            isoDetected = detect(commit['commit']['message']).upper()
        if(isoDetected == "EN"):
            flag = True
        else: 
            if isoDetected in isoDectCounter:
                isoDectCounter[isoDetected] = isoDectCounter[isoDetected] + 1
                if(isoDectCounter[isoDetected] > maxIsoCounter):
                    maxIsoCounter = isoDectCounter[isoDetected]
                    maxIsoCode = isoDetected
            else:
                isoDectCounter[isoDetected] = 1
                if(isoDectCounter[isoDetected] > maxIsoCounter):
                    maxIsoCounter = isoDectCounter[isoDetected]
                    maxIsoCode = isoDetected
        commits[index] = {
            'commit': commit,
            'isoDetected': isoDetected
        }
    if(maxIsoCounter == 0 and flag is True):
        maxIsoCode = "EN"
    commits = {
        'commits': commits,
        'isoDetected': maxIsoCode
    }
    return commits

def detectLanguageFromCommitGoogle(text, GOOGLE_API_KEY):
    if not text:
        return jsonify({
            "error": "Text is required",
            "status": "403"
        }), "403" 

    # Detect Language
    url = "https://translation.googleapis.com/language/translate/v2/detect"
    params = {
        "q": text,
        "key": GOOGLE_API_KEY
    }

    try:
        response = requests.post(url, params=params)
        data = response.json()
        result = data['data']['detections'][0][0]
    

        return result["language"]
    except requests.RequestException as e:
        print(f"[GOOGLE CLOUD API] {str(e)}")
        return jsonify({"error": str(e), "status": "500"}), 500

    except Exception as e:
        # Gestisci altri errori imprevisti
        print(f"[GOOGLE CLOUD API] {str(e)}")
        return jsonify({"error": "Unknown error: {e}", "status": "500"}), 500
