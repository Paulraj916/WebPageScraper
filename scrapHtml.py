import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ScrapHtml:
    def __init__(self, url):
        self.url = url
        self.output_folder = 'output'
        self.html_path = os.path.join(self.output_folder, 'index.html')

    def scrape_html_files(self):
        # Send an HTTP GET request to the URL and get the response
        response = requests.get(self.url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags with 'href' attribute and download linked HTML files
        os.makedirs(self.output_folder, exist_ok=True)

        for anchor_tag in soup.find_all('a', href=True):
            href = anchor_tag['href']
            if href.endswith('.html'):  # Check if the link points to an HTML file
                filename = os.path.basename(href)
                file_url = urljoin(self.url, href)  # Construct the absolute URL
                try:
                    html_response = requests.get(file_url)
                    html_response.raise_for_status()
                    file_path = os.path.join(self.output_folder, filename)

                    # Save the HTML content with readable formatting to a file
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(BeautifulSoup(html_response.text, 'html.parser').prettify())

                    print(f"Downloaded: {file_url}")
                except requests.exceptions.HTTPError as e:
                    print(f"Failed to download {file_url}: {e}")

        # Find all script tags with inline JavaScript code and remove them from the soup
        script_tags = soup.find_all('script')
        for script_tag in script_tags:
            if script_tag.string:
                script_tag.decompose()

        # Save the HTML content with readable formatting to a file in the output folder
        with open(self.html_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        print(f"HTML content and linked HTML files saved to {self.html_path} and {self.output_folder}.")
