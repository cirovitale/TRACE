from urllib import response
import requests
from bs4 import BeautifulSoup
import urllib
import sys

def download_pdf(url, destination):
    response = requests.get(url)
    # Open the destination file in write-binary mode
    with open(destination, 'wb') as file_output:
        # Write the content of the response to the file
        file_output.write(response.content)

def search_pdf(url_site):
    try:
        response = requests.get(url_site)
    except Exception as e:
        url_site = url_site.replace("https://", "http://")
        try:
            response = requests.get(url_site)
        except Exception as e:
            print(e)
            return None
    # Parse the text of the response with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    i = 0
    pdfs = []
    # For each link that ends with '.pdf'
    for link in soup.select("a[href$='.pdf']"):
        i = i + 1
        # Get the href attribute of the link
        url_pdf = link['href']
        # If the link does not include 'http', add the site url to the start
        if 'http' not in url_pdf:
            try:
                # url_pdf = url_pdf.replace("https://", "http://")
                url_pdf = urllib.parse.urljoin(url_site, url_pdf)
            except Exception as e:
                try:
                    url_pdf = url_pdf.replace("http://", "https://")
                    url_pdf = urllib.parse.urljoin(url_site, url_pdf)
                except Exception as e:
                    return "Bad Request", 403
        # name_pdf = name + '_' + "{:02d}".format(i) + '.pdf'

        pdfs.append(url_pdf)
        
        # download_pdf(url_pdf, name_pdf)
    return pdfs