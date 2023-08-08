from urllib import response
import requests
from bs4 import BeautifulSoup
import urllib
from flask import jsonify
import sys
import os
import PyPDF2
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import BytesIO
import openai
import threading
import json

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
maxFileSize = 5 * 1024 * 1024  # 5MB in bytes

def detectCVCountryOpenAI(textPdf, results):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user", 
                    "content": f"Data la seguente informazione dal Curriculum Vitae di uno sviluppatore, analizza Nome, Indirizzi, Numeri di Telefono, Esperienza Lavorative, Formazione, Lingua, Progetti e tutto ciò che può essere utile per tentare di prevedere la sua nazionalità. Restituisci la previsione nel formato JSON indicato, usando 'NULL' se non puoi fare una previsione. Assicurati di utilizzare SOLO singole ('') o doppie (\") virgolette nel formato JSON. Non utilizzare virgolette doppie non escape all'interno delle stringhe JSON. Restituisci SOLO ed ESCLUSIVAMENTE un JSON con il formato seguente: {json.dumps({ 'isoPredicted': '[PREDIZIONE ISO 3166-1 alpha-2 NAZIONALITÀ o NULL]', 'reasons': '[MOTIVAZIONI DELLA SCELTA]', 'completeAnswers': '[RISPOSTA DETTAGLIATA]' })} Contenuto CV: [[[ {textPdf} ]]]"
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
    timeout_seconds = 10
    textPdf = getTextByPdf(urlPdf, docType)
    thread = threading.Thread(target=detectCVCountryOpenAI, args=(textPdf, results))
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

    print(results['data'])
    return results['data']

def isCV(urlPdf):
    # Check for common CV file name keywords
    fileName = urllib.parse.unquote(urlPdf.split('/')[-1]).lower()

    fileNameKeywords = ['cv', 'resume', 'curriculum', 'vitae']
    if not any(keyword in fileName for keyword in fileNameKeywords):
        return False
    
    try:
        # Download the PDF content
        response = requests.get(urlPdf)

        # Check file size (tipically less then 5MB)
        fileSize = int(response.headers.get('Content-Length', 0))
        if fileSize > maxFileSize:
            return False
    
        with BytesIO(response.content) as open_pdf_file:
            pdf = PyPDF2.PdfReader(open_pdf_file)

            # Check number of pages (typically between 1 to 5)
            if 1 <= len(pdf.pages) <= 5:
                return True

    except Exception as e:
        print(f"Error processing PDF from {urlPdf}. Error: {e}")

    return False

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
        try:
            # Set up the API
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.fromJsonKeyfileName(GOOGLE_API_KEY, scope)
            client = gspread.authorize(creds)

            # Open the document
            document = client.openByUrl(url)
            worksheet = document.getWorksheet(0) 
            text = worksheet.getAllValues()
        except Exception as e:
            print(f"Error accessing Google document: {e}")

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
            if(isCV(urlPdf)):
                response = detectCountryFromCV(urlPdf, docType)
                pdf = {
                    'url': urlPdf,
                    'isoPredicted': response
                }
                pdfs.append(pdf)

    return pdfs