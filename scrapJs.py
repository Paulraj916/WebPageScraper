import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class ScrapJs:
    def __init__(self, link):
        # Replace 'https://example.com' with the website you want to scrape
        self.url = link

    def scrap_js(self):
        # Send a GET request to the website and retrieve the content
        response = requests.get(self.url)
        if response.status_code == 200:
            content = response.text
        else:
            print(f"Failed to fetch content from {self.url}")
            exit()

        # Extract JavaScript file URLs from the webpage
        js_urls = [script['src'] for script in BeautifulSoup(content, 'html.parser').find_all('script', src=True)]

        # Create a folder to store the downloaded JavaScript files
        output_folder = 'output'  # Choose a folder name you have write permissions for
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Download and save each JavaScript file
        for js_url in js_urls:
            # Convert relative URLs to absolute URLs
            js_url = urljoin(self.url, js_url)

            try:
                js_content = requests.get(js_url).text

                # Get the path to the JavaScript file
                path = urlparse(js_url).path
                filename = os.path.join(output_folder, path.strip('/'))

                # Create subdirectories if needed
                os.makedirs(os.path.dirname(filename), exist_ok=True)

                # Save the JavaScript content to the file
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(js_content)

                print(f"Downloaded: {js_url}")
            except requests.exceptions.MissingSchema:
                print(f"Skipping download of {js_url} (Invalid URL)")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {js_url}: {e}")
            except OSError as e:
                print(f"Failed to save {js_url}: {e}")

        print("JavaScript files downloaded and saved successfully.")
