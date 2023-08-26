from flask import Flask
from flask import jsonify
import requests
import os
# import logging
import openai
from business_logic.searchPdf import searchPdf
import threading
import json
from langdetect import detect
from geopy.geocoders import Nominatim
# from flask_compress import Compress
import math
# from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
# translate_client = translate.Client(key=GOOGLE_APPLICATION_CREDENTIALS)
# Compress(app)

GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')
geolocator = Nominatim(user_agent="DCDTool")
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# OPENAI_ORGANIZATION_ID = os.getenv('OPENAI_ORGANIZATION_ID')

# OPEN AI setup
# openai.organization = os.getenv("OPENAI_ORGANIZATION_ID")
# openai.api_key = os.getenv("OPENAI_API_KEY")

# WEIGHT of prediction for final resul, from 0.1 to 0.5
WEIGHT_NAME = 0.4
WEIGHT_USERNAME = 0.2
WEIGHT_PDFS = 0.3
WEIGHT_COMMITS = 0.2
# English is international language and commits in english aren't weighted
WEIGHT_COMMITS_EN = 0
WEIGHT_LOCATION = 0.2

# N/A limit percent to alert the noise in the info --- if update NA_LIMIT_PERCENT here, update also in Alert message in front-end (RepositoryInfo.js - MUI Alert Component)
NA_LIMIT_PERCENT = 0.3

def isAlertNAinRepo(culturalDispersion):
    total = sum(culturalDispersion.values())
    if("N/A" in culturalDispersion):
        countNA = culturalDispersion["N/A"]
        percentNA = countNA / total

        if(percentNA > NA_LIMIT_PERCENT):
            return True
        else:
            return False
    else:
        return False

def getIsoFromLocation(location):    
    # Retrieve Location object from location github info
    try:
        locationCoded = geolocator.geocode(location, addressdetails=True)
        
        if locationCoded:
            # Extract ISO Code
            countryCode = locationCoded.raw.get("address", {}).get("country_code", "").upper()

            if countryCode:
                return countryCode
    except Exception as e:
        # If an error occured during the call
        print(f"Error geopy: {e}")
        return jsonify({
            "error": str(e),
            "status": "403"
        })
    
    
    return None

def shannonIndex(culturalDispersion):
    total = sum(culturalDispersion.values())

    index = 0
    for value in culturalDispersion.values():
        proportion = value / total
        index += proportion * math.log(proportion)

    index = -index

    if len(culturalDispersion) > 1:
        percent = index / math.log(len(culturalDispersion)) * 100
    else:
        percent = 0
    
    

    return {
        'index':index,
        'percent': percent
    }

def detectUsernameCountryOpenAI(username, results):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"FORNISCI RISPOSTA IN LINGUA INGLESE. Dato il seguente username [[[ {username} ]]], tenta di prevedere la nazionalità più probabile dell'utente in base al solo nome utente. Restituisci la previsione nel formato JSON indicato, usando 'NULL' se non puoi fare una previsione. Assicurati di utilizzare SOLO singole ('') o doppie (\") virgolette nel formato JSON. Non utilizzare virgolette doppie non escape all'interno delle stringhe JSON. Restituisci SOLO ed ESCLUSIVAMENTE un JSON con il formato seguente: {json.dumps({'isoPredicted': '[PREDIZIONE ISO 3166-1 alpha-2 o NULL]', 'reasons': '[MOTIVAZIONI DELLA SCELTA in LINGUA INGLESE]', 'completeAnswers': '[RISPOSTA DETTAGLIATA in LINGUA INGLESE]'})}"
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
    timeout_seconds = 15
    thread = threading.Thread(target=detectUsernameCountryOpenAI, args=(username, results))
    thread.start()
    thread.join(timeout=timeout_seconds)

    if thread.is_alive():
        # Timeout handling
        return {
            "error": "API call timed out",
            "status": "408"
        }

    if 'error' in results:
        return {
            "error": results['error'],
            "status": "403"
        }

    return results['data']['choices'][0]['message']['content']

# @app.route("/exampleOpenAI")
# def exampleOpenAI():
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": "Hello world"}],
#             temperature=1
#         )
#         print(response)
#         return response
#     except Exception as e:
#         # If an error occured during the api call
#         print(f"Error OpenAI api example: {e}")
#         return jsonify({
#             "error": str(e),
#             "status": "403"
#         })
    
@app.route("/repos/<owner>/<repo>/readme")
def getRepoReadme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_API_TOKEN}"
    }
    
    try:
        # Do GET request to GitHub API
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        # If an error occurred during the API call
        errorFullMessage = str(e.args[0]) if e.args else "Unknown error"
        
        if " " in errorFullMessage:
            errorCode = errorFullMessage.split(" ")[0]
            errorMessage = " ".join(errorFullMessage.split(" ")[1:])
        else:
            errorCode = "Unknown"
            errorMessage = errorFullMessage
        
        print(f"Error GitHub accessing repo info: {e}")
        return jsonify({
            "error": errorMessage,
            "status": errorCode
        }), 500

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
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        # If an error occurred during the API call
        errorFullMessage = str(e.args[0]) if e.args else "Unknown error"
        
        if " " in errorFullMessage:
            errorCode = errorFullMessage.split(" ")[0]
            errorMessage = " ".join(errorFullMessage.split(" ")[1:])
        else:
            errorCode = "Unknown"
            errorMessage = errorFullMessage
        
        print(f"Error GitHub accessing repo info: {e}")
        return jsonify({
            "error": errorMessage,
            "status": errorCode
        }), 500


@app.route("/repos/<owner>/<repo>/contributors")
def getRepoContributors(owner, repo):
    page = 1
    flag = True
    contributors = []
    culturalDispersion = {}

    while flag == True:
        
        
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
                usernamePredict = {}
                response = detectCountryFromUsername(username)

                # Check if response is dict and contains 'error' key
                if isinstance(response, dict) and 'error' in response:
                    if response.get('status') == "408":
                        print("[USERNAME PREDICT] Timeout error: ", response.get('error'))
                    elif response.get('status') == "403":
                        print("[USERNAME PREDICT] OpenAI API error: ", response.get('error'))
                    else:
                        print("[USERNAME PREDICT] Unknown error: ", response.get('error'))
                    usernamePredict = None
                else:
                    usernamePredict = response

                # MODULO LOCATION
                locationPredict = None
                if (user['location'] is not None):
                    print('Search location ISO of  ', user['login'])
                    locationPredict = getIsoFromLocation(user['location'])

                if(isinstance(locationPredict, dict) and locationPredict['status'] == "403"):
                    # If an error occured
                    locationPredict = None

                # MODULO COMMIT
                # Search 3 commits of contributor
                print('Searching commits of ', user['login'])
                commitsPredict = getCommits(user['login'], owner, repo, 3)  

                if(isinstance(commitsPredict, dict) and 'error' in commitsPredict):
                    # If an error occured
                    commitsPredict = None

                # MODULO NAME
                namePredict = None

                

                

                final = {}
                if(usernamePredict is not None):
                    try:
                        usernamePredictJson = json.loads(usernamePredict)
                    except json.decoder.JSONDecodeError:
                        print(f"Error decoding JSON for value: {usernamePredict}")
                    if ('isoPredicted' in usernamePredictJson):
                            usernameIso = usernamePredictJson['isoPredicted']
                    else:
                        usernameIso = None
                    
                else:
                    usernameIso = None
                    usernamePredictJson = None

                
                if(usernameIso is None or usernameIso.lower() == 'null' or len(usernameIso) > 2):
                    usernameIso = None

                nameIso = namePredict


                pdfsIso = None
                ############ try except
                if pdfsPredict is not None and len(pdfsPredict) != 0:
                    # for isoPredicted of pdf: pdfsPredict[0]['isoPredicted']['isoPredicted']
                    pdfCountIso = {}
                    for pdf in pdfsPredict:
                        isoValue = None
                        if pdf['isoPredicted']:
                            try:
                                isoValue = json.loads(pdf['isoPredicted'])['isoPredicted']
                            except json.decoder.JSONDecodeError:
                                print(f"Error decoding JSON for value: {pdf['isoPredicted']}")
                                continue  # If error occured, skip to the next iteration
                        if isoValue is not None and isoValue.upper() != 'NULL':
                            if isoValue in pdfCountIso:
                                pdfCountIso[isoValue] += 1
                            else:
                                pdfCountIso[isoValue] = 1
                    
                    # Check if dict is not empty
                    if pdfCountIso:
                        pdfsIso = max(pdfCountIso, key=pdfCountIso.get)
                    
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
                        # if(commitsIso == 'EN'):
                        #     final[commitsIso] += WEIGHT_COMMITS_EN
                        # else:
                        #     final[commitsIso] += WEIGHT_COMMITS
                        if(commitsIso != 'EN'):
                            final[commitsIso] += WEIGHT_COMMITS
                    else:
                        # if(commitsIso == 'EN'):
                        #     final[commitsIso] = WEIGHT_COMMITS_EN
                        # else:
                        #     final[commitsIso] = WEIGHT_COMMITS
                        if(commitsIso != 'EN'):
                            final[commitsIso] = WEIGHT_COMMITS
                    print(f'COMMIT PREDICTED ({WEIGHT_COMMITS} || if EN : {WEIGHT_COMMITS_EN}): ', commitsIso)
                else:
                    print(f'COMMIT PREDICTED ({WEIGHT_COMMITS} || if EN : {WEIGHT_COMMITS_EN}): ', commitsIso)

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
                else:
                    estimatedCountry = estimatedCountry.upper()
                    if(estimatedCountry in culturalDispersion):
                        culturalDispersion[estimatedCountry] += 1
                    elif(estimatedCountry not in culturalDispersion):
                        culturalDispersion[estimatedCountry] = 1

                user['prediction'] = {
                    'name': namePredict,
                    'pdfs': pdfsPredict,
                    'username': usernamePredictJson,
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

        # if flag == False:
        #     contributorsObj = {
        #         'contributors': contributors,
        #         'culturalDispersion': culturalDispersion
        #     }
        #     print('contributorsObj:', contributorsObj)
        #     return contributorsObj
        
    alert = isAlertNAinRepo(culturalDispersion)
    shannon = shannonIndex(culturalDispersion)
    contributorsObj = {
        'contributors': contributors,
        'culturalDispersion': {
            'countryDisp': culturalDispersion,
            'shannonIndex': shannon['index'],
            'percentCultDisp': shannon['percent']
        },
        'alert': alert
    }

    print('\n#################################')
    print(f'Prediction for Contributors: {culturalDispersion}')
    print(f'Shannon Index: {shannon["index"]}')
    print(f'Cultural Dispersion Percent: {shannon["percent"]}')
    print(f'Alert N/A Noise: {alert}')
    print('#################################\n')
    try:
        # print('contributorsObj:', contributorsObj)
        return contributorsObj
    except Exception as e:
        print(f"Error during final jsonify: {e}")
        return jsonify({
            "error": str(e),
            "status": "403"
        }), "403"   

def detectLanguageFromCommitGoogle(text):
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
        return jsonify({"error": str(e), "status": "500"}), 500

    except Exception as e:
        # Gestisci altri errori imprevisti
        return jsonify({"error": "Unknown error: {e}", "status": "500"}), 500

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
            if(GOOGLE_API_KEY != ""):
                isoDetected = detectLanguageFromCommitGoogle(commit['commit']['message']).upper()
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
