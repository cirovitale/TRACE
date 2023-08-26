from urllib import response
import requests
from bs4 import BeautifulSoup
import urllib
from flask import jsonify
import sys
import os
import PyPDF2
import re
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import BytesIO
import openai
import threading
import json

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes

def detectCVCountryOpenAI(textPdf, results):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user", 
                    "content": f"Based on the information provided and doing your best, try to make a prediction. Given the following information from a developer's Curriculum Vitae, analyze Name, Addresses, Phone Numbers, Work Experience, Education, Language, Projects, and anything else that may be useful in trying to predict his or her nationality. Return the prediction in the given JSON format, using 'NULL' if you cannot make a prediction. Be sure to use ONLY single ('') or double (\") quotes in the JSON format. Do not use unescaped double quotes within JSON strings. ONLY and EXCLUSIVELY return a JSON with the following format: {json.dumps({ 'isoPredicted': '[PREDICTION ISO 3166-1 alpha-2 COUNTRY or NULL]', 'reasons': '[REASONS FOR THE CHOICE]', 'completeAnswers': '[DETAILED ANSWER]' })} CV CONTENT: [[[ {textPdf} ]]]"
                }
            ],
            temperature=1
        )
        results['data'] = response
    except Exception as e:
        results['error'] = str(e)

def detectCountryFromCV(urlPdf, docType):
    results = {}
    # Setup thread call and start it
    timeout_seconds = 15
    textPdf = getTextByPdf(urlPdf, docType)
    thread = threading.Thread(target=detectCVCountryOpenAI, args=(textPdf, results))
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

    # print(results['data']['choices'][0]['message']['content'])
    return results['data']['choices'][0]['message']['content']


def isCV(urlPdf, docType):
    fileName = ""

    if docType == "pdf":
        fileName = urllib.parse.unquote(urlPdf.split('/')[-1]).lower()
    # elif docType in ["googleDrive", "googleDocs"]:
    #     # fileName = getTitleFromGoogleDocs(urlPdf).lower()



    fileNameKeywords = ['cv', 'resume', 'curriculum', 'vitae']
    if not any(keyword in fileName for keyword in fileNameKeywords):
        return False
    
    if docType == "pdf":
        try:
            # Download the PDF content
            response = requests.get(urlPdf)

            # Check file size (tipically less then 5MB)
            fileSize = int(response.headers.get('Content-Length', 0))
            if fileSize > MAX_FILE_SIZE:
                return False
        
            with BytesIO(response.content) as open_pdf_file:
                pdf = PyPDF2.PdfReader(open_pdf_file)

                # Check number of pages (typically between 1 to 5)
                if 1 <= len(pdf.pages) <= 5:
                    return True

        except Exception as e:
            print(f"Error processing PDF from {urlPdf}. Error: {e}")
    elif docType in ["googleDrive", "googleDocs"]:
        # flag = isValidGoogleDocsPdf(urlPdf)
        flag = True
        # return True    

    return False

def getIdFileFromGoogleUrl(url):
    # Extract idFile from Google DOCS URL
    id = re.search(r"/d/([\w-]+)/", url)
    if id:
        return id.group(1)
    else:
        return None

def getTextByPdf(url, docType):
    text = ""

    # Extract text from PDF
    if docType == "pdf":
        try:
            response = requests.get(url)
            with BytesIO(response.content) as openPdfFile:
                pdf = PyPDF2.PdfReader(openPdfFile)
                for pageNum in range(len(pdf.pages)):
                    text += pdf.pages[pageNum].extract_text()
        except Exception as e:
            print(f"Error processing PDF: {e}")

    # Extract text from Google Drive/Docs
    elif docType in ["googleDrive", "googleDocs"]:
        print("************* Google Document PDF")

        # text = getTextFromGoogleDocs(url)
        
    return text

def searchPdf(urlSite):
    try:
        response = requests.get(urlSite)
    except Exception as e:
        urlSite = urlSite.replace("https://", "http://")
        try:
            response = requests.get(urlSite)
        except Exception as e:
            print(f"Error searching PDF: {e}")
            return None
    # Parse the text of the response with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    pdfs = []
    # For each link that ends with '.pdf', Google Drive or Google Docs links
    for link in soup.find_all('a', href=True):
        # Get the href attribute of the link
        urlPdf = link['href']
        docType = None

        if urlPdf.endswith('.pdf'):
            docType = "pdf"
        elif "drive.google.com" in urlPdf:
            docType = "googleDrive"
        elif "docs.google.com/document" in urlPdf:
            docType = "googleDocs"
        if docType is not None:
            if 'http' not in urlPdf:
                try:
                    # urlPdf = urlPdf.replace("https://", "http://")
                    urlPdf = urllib.parse.urljoin(urlSite, urlPdf)
                except Exception as e:
                    try:
                        urlPdf = urlPdf.replace("http://", "https://")
                        urlPdf = urllib.parse.urljoin(urlSite, urlPdf)
                    except Exception as e:
                        print(f"Error accessing PDF url: {e}")
                        return "Bad Request", 403
            if(isCV(urlPdf, docType)):
                response = detectCountryFromCV(urlPdf, docType)

                # Check if response is dict and contains 'error' key
                if isinstance(response, dict) and 'error' in response:
                    if response.get('status') == "408":
                        print("[PDF PREDICT] Timeout error: ", response.get('error'))
                    elif response.get('status') == "403":
                        print("[PDF PREDICT] OpenAI API error: ", response.get('error'))
                    else:
                        print("[PDF PREDICT] Unknown error: ", response.get('error'))
                    pdf = {
                        'url': urlPdf,
                        'isoPredicted': response.get('error')
                    }
                else:
                    pdf = {
                        'url': urlPdf,
                        'isoPredicted': response
                    }
                pdfs.append(pdf)

    return pdfs