import os.path
import logging
import bs4
import requests
from src import constants


URL = "https://www.edistribucion.com/es/red-electrica/Nodos_capacidad_acceso.html"


def get_request():
    response = requests.get(URL)
    if response.status_code != 200:
        return None
    return response


def download_pdf(url, file_name):
    path = os.path.join(constants.DATA_PATH, file_name)
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)


def retrieve_pdf_from_website():
    logging.info(f"Getting file from {URL}")
    pdf_file_name = None

    if response := get_request():
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        if pdf_button := soup.find('a', attrs={'class': 'btn-pdf'}):
            relative_link = pdf_button.get('href')
            split_url = URL.split('/')
            domain = '/'.join(split_url[:3])
            pdf_url = domain + relative_link
            pdf_file_name = pdf_url.split("/")[-1]
            download_pdf(pdf_url, pdf_file_name)

    return pdf_file_name


if __name__ == "__main__":
    retrieve_pdf_from_website()