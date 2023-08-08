from flask import Flask
from flask import jsonify
import requests
import os
import logging
import openai
from business_logic.searchPdf import searchPdf
import threading
import json
from langdetect import detect
from geopy.geocoders import Nominatim
from collections import Counter


app = Flask(__name__)

GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')
geolocator = Nominatim(user_agent="DCDTool")
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# OPENAI_ORGANIZATION_ID = os.getenv('OPENAI_ORGANIZATION_ID')

# OPEN AI setup
# openai.organization = os.getenv("OPENAI_ORGANIZATION_ID")
# openai.api_key = os.getenv("OPENAI_API_KEY")

def getIsoFromLocation(location):    
    # Retrieve Location object from location github info
    locationCoded = geolocator.geocode(location, addressdetails=True)
    
    if locationCoded:
        # Extract ISO Code
        countryCode = locationCoded.raw.get("address", {}).get("country_code", "").upper()

        if countryCode:
            return countryCode
    
    
    return None

def detectUsernameCountryOpenAI(username, results):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Dato il seguente username [[[ {username} ]]], tenta di prevedere la nazionalità più probabile dell'utente in base al solo nome utente. Restituisci la previsione nel formato JSON indicato, usando 'NULL' se non puoi fare una previsione. Assicurati di utilizzare SOLO singole ('') o doppie (\") virgolette nel formato JSON. Non utilizzare virgolette doppie non escape all'interno delle stringhe JSON. Restituisci SOLO ed ESCLUSIVAMENTE un JSON con il formato seguente: {json.dumps({'isoPredicted': '[PREDIZIONE ISO 3166-1 alpha-2 o NULL]', 'reasons': '[MOTIVAZIONI DELLA SCELTA]', 'completeAnswers': '[RISPOSTA DETTAGLIATA]'})}"
                }
            ],
            temperature=1
        )
        results['data'] = response
    except Exception as e:
        results['error'] = str(e)

def detectCountryFromUsername(username):
    results = {}
    # Setup thread call and start it
    timeout_seconds = 10
    thread = threading.Thread(target=detectUsernameCountryOpenAI, args=(username, results))
    thread.start()
    thread.join(timeout=timeout_seconds)

    if thread.is_alive():
        # Timeout handling
        print("API call timed out.")
        return jsonify({
            "error": "API call timed out",
            "status": "408"
        })

    if 'error' in results:
        print(f"Error OpenAI API: {results['error']}")
        return jsonify({
            "error": results['error'],
            "status": "403"
        })

    return results['data']

@app.route("/exampleOpenAI")
def exampleOpenAI():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello world"}],
            temperature=1
        )
        print(response)
        return response
    except Exception as e:
        # If an error occured during the api call
        print(f"Error OpenAI api example: {e}")
        return jsonify({
            "error": str(e),
            "status": "403"
        })
    

@app.route("/repos/<owner>/<repo>")
def getRepoInfo(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_API_TOKEN}"
    }
    
    try:
        # Do GET request to GitHub API
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print('QUI 1', jsonify(data))
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        # If an error occured during api call
        errorFullMessage = e.args[0]
        errorCode = errorFullMessage.split(" ")[0]
        errorMessage = " ".join(errorFullMessage.split(" ")[1:])
        
        print(f"Error GitHub accessing repo info: {e}")
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
        culturalDispersion = {}
        
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100&page={page}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {GITHUB_API_TOKEN}",
        }

        try:
            # Do GET request to GitHub API
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
        
        except requests.exceptions.RequestException as e:
            # If an error occured during api call
            errorFullMessage = e.args[0]
            errorCode = errorFullMessage.split(" ")[0]
            errorMessage = " ".join(errorFullMessage.split(" ")[1:])
            
            print(f"Error GitHub accessing repo's contribur info: {e}")
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
                # If an error occured
                return jsonify(user[0]), user[0]['status']
            else:
                print('\n#################################')
                print(user['login'])
                print('#################################')
                contributors.append(user)

                # MODULO CV
                # Search CV in contributor's portfolio
                url = user['blog']
                pdfsPredict = None
                if(url != ''):
                    if not (url.startswith("http://") or url.startswith("https://")):
                        url = "http://" + url
                    print('Searching pdfs in ', url, ' website of ', user['login'])
                    pdfsPredict = searchPdf(url)

                # MODULO USERNAME
                # Predict nationality from username
                username = user['login']
                print('Prediction by username of ', user['login'])
                usernamePredict = detectCountryFromUsername(username)

                # MODULO LOCATION
                locationPredict = None
                if (user['location'] is not None):
                    print('Search location ISO of  ', user['login'])
                    locationPredict = getIsoFromLocation(user['location'])

                # MODULO COMMIT
                # Search 3 commits of contributor
                print('Searching commits of ', user['login'])
                commitsPredict = getCommits(user['login'], owner, repo, 3)  

                # MODULO NAME
                namePredict = None

                # WEIGHT of prediction for final resul, from 0.1 to 0.5
                WEIGHT_NAME = 0.4
                WEIGHT_USERNAME = 0.2
                WEIGHT_PDFS = 0.3
                WEIGHT_COMMITS = 0.2
                # English is international language and commits in english aren't weighted
                WEIGHT_COMMITS_EN = 0.001
                WEIGHT_LOCATION = 0.2

                

                final = {}
                if (isinstance(usernamePredict, dict) and 'choices' in usernamePredict):
                    print(usernamePredict['choices'][0]['message']['content'])
                    try:
                        usernameIso = json.loads(usernamePredict['choices'][0]['message']['content'])['isoPredicted']
                    except Exception as e:
                        usernameIso = None
                        print(f"***************************************************************************************************************************Error during processing of OpenAI response: {e}")
                else:
                    usernameIso = None
                if(usernameIso is None or usernameIso.lower() == 'null'):
                    usernameIso = None
                nameIso = namePredict
                pdfsIso = None
                
                ############ try except
                # if pdfsPredict is not None and len(pdfsPredict) != 0 and pdfsPredict != 'NULL'  and pdfsPredict != 'Null'  and pdfsPredict != 'null':
                #     pdfCountIso = {}
                #     for pdf in pdfsPredict:
                #         if pdf['isoPredicted'] is not None:
                #             if pdf['isoPredicted'] in pdfCountIso:
                #                 pdfCountIso[pdf['isoPredicted']] += 1
                #             else:
                #                 pdfCountIso[pdf['isoPredicted']] = 1
                #     pdfsIso = max(pdfCountIso, key=pdfCountIso.get)
                    
                    # Create Counter of iso prediction in case of multiple CVs
                    # counterIso = Counter(pdf['isoPredicted'] for pdf in pdfsPredict)
                    # Sort collection descending and take the max
                    # most_common_isoPrediction = counterIso.most_common(1)[0]
                    # pdfsIso = most_common_isoPrediction
                    # pdfsIso = max(pdfCountIso, key=pdfCountIso.get)
                if commitsPredict is not None:
                    commitsIso = commitsPredict['isoDetected']
                else:
                    commitsIso = None
                locationIso = locationPredict

                print('#################################')

                # Calculate estimated country for developer

                ### NAME ###
                if(nameIso is not None):
                    print(f'NAME PREDICTED ({WEIGHT_NAME}): ', nameIso)
                    if(nameIso in final):
                        final[nameIso] += WEIGHT_NAME
                    else:
                        final[nameIso] = WEIGHT_NAME
                else:
                    print(f'NAME PREDICTED ({WEIGHT_NAME}): ', nameIso)

                ### USERNAME ###
                print(f'USERNAME PREDICTED ({WEIGHT_LOCATION}): ', usernameIso)

                if(usernameIso is not None):
                    if(usernameIso in final):
                        final[usernameIso] += WEIGHT_USERNAME
                    else:
                        final[usernameIso] = WEIGHT_USERNAME

                ### PDFS ###
                if pdfsIso is not None:
                    print(f'PDF PREDICTED ({WEIGHT_PDFS}): ', pdfsIso)
                    if(pdfsIso in final):
                        final[pdfsIso] += WEIGHT_PDFS
                    else:
                        final[pdfsIso] = WEIGHT_PDFS
                else:
                    print(f'PDF PREDICTED ({WEIGHT_PDFS}): ', pdfsIso)
                
                ### COMMITS ###
                if(commitsIso is not None):
                    if(commitsIso in final):
                        if(commitsIso == 'EN'):
                            final[commitsIso] += WEIGHT_COMMITS_EN
                        else:
                            final[commitsIso] += WEIGHT_COMMITS
                    else:
                        if(commitsIso == 'EN'):
                            final[commitsIso] = WEIGHT_COMMITS_EN
                        else:
                            final[commitsIso] = WEIGHT_COMMITS
                    print(f'COMMIT PREDICTED ({WEIGHT_COMMITS}): ', commitsIso)
                else:
                    print(f'COMMIT PREDICTED ({WEIGHT_COMMITS}): ', commitsIso)

                ### LOCATION ###
                if(locationIso is not None):
                    if(locationIso in final):
                        final[locationIso] += WEIGHT_LOCATION
                    else:
                        final[locationIso] = WEIGHT_LOCATION
                    print(f'LOCATION PREDICTED ({WEIGHT_LOCATION}): ', locationIso)
                else:
                    print(f'LOCATION PREDICTED ({WEIGHT_LOCATION}): ', locationIso)

                print('#################################')

                if(len(final) != 0):
                    estimatedCountry = max(final, key=final.get)
                else:
                    estimatedCountry = None

                # Update cultural disperion var, with info of all devs
                if(estimatedCountry is None):
                    if('N/A' in culturalDispersion):
                        culturalDispersion['N/A'] += 1
                    else:
                        culturalDispersion['N/A'] = 1
                if(estimatedCountry in culturalDispersion):
                    culturalDispersion[estimatedCountry] += 1
                else:
                    culturalDispersion[estimatedCountry] = 1

                user['prediction'] = {
                    'name': namePredict,
                    'pdfs': pdfsPredict,
                    'username': usernamePredict,
                    'commits': commitsPredict,
                    'location': locationPredict,
                    'estimatedCountry': estimatedCountry
                }

                if(len(final) != 0):
                    print('estimatedCountry: ', estimatedCountry, ' ', str(final[estimatedCountry]))
                else:
                    print('estimatedCountry: N/A')
                
                print('#################################\n')
                

        if(count == 100):
            page += 1
            flag = True
        else:
            flag = False

        if flag == False:
            contributorsObj = {
                'contributors': contributors,
                'culturalDispersion': culturalDispersion
            }
            print('contributorsObj:', contributorsObj)
            return jsonify(contributorsObj)
        
    
    contributorsObj = {
        'contributors': contributors,
        'culturalDispersion': culturalDispersion
    }
    print('contributorsObj:', contributorsObj)
    return jsonify(contributorsObj)

def getCommits(username, owner, repo, perPage):
    i = 0
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
        isoDectCounter = {}
        maxIsoCounter = 0
        maxIsoCode = None
        flag = False
        # For each commit detect language and count type of language detected, counts EN only if it is the only language detected
        for index, commit in enumerate(commits):
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
    except requests.exceptions.RequestException as e:
        # If an error occured during api call
        errorFullMessage = e.args[0]
        errorCode = errorFullMessage.split(" ")[0]
        errorMessage = " ".join(errorFullMessage.split(" ")[1:])

        print(f"Error GitHub accessing repo's commits: {e}")
        return jsonify({
            "error": errorMessage,
            "status": errorCode
        }, errorCode)
    except Exception as e:
        # If an error occured during api call
        errorFullMessage = e.args[0]
        errorCode = errorFullMessage.split(" ")[0]
        errorMessage = " ".join(errorFullMessage.split(" ")[1:])

        print(f"Error GitHub accessing repo's commits: {e}")
        return jsonify({
            "error": errorMessage,
            "status": errorCode
        }, errorCode)

def getUser(username):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_API_TOKEN}"
    }
    
    try:
        # Do GET request to GitHub API
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        # If an error occured during api call
        errorFullMessage = e.args[0]
        errorCode = errorFullMessage.split(" ")[0]
        errorMessage = " ".join(errorFullMessage.split(" ")[1:])

        print(f"Error GitHub accessing user info: {e}")
        return jsonify({
            "error": errorMessage,
            "status": errorCode
        }), errorCode
