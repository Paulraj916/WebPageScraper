import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class ScrapTs:
    def __init__(self, url):
        self.url = url

    def extract_and_save_typescript(self):
        try:
            # Send an HTTP GET request to the webpage and get the HTML content
            response = requests.get(self.url)
            response.raise_for_status()
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all <script> tags with "type" attribute set to "text/typescript" or "text/tsx"
            typescript_scripts = soup.find_all('script', type=['text/typescript', 'text/tsx'])

            # Create the output folder if it doesn't exist
            os.makedirs("output", exist_ok=True)

            # Download and save TypeScript files in the output folder
            for script in typescript_scripts:
                if 'src' in script.attrs:
                    ts_url = urljoin(self.url, script['src'])
                    folder_name = os.path.dirname(ts_url)
                    if folder_name.startswith("/"):
                        folder_name = folder_name[1:]
                    folder_path = os.path.join("output", folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    filename = os.path.basename(ts_url)
                    try:
                        ts_content = requests.get(ts_url).text
                        with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as file:
                            file.write(ts_content)
                        print(f"Downloaded: {ts_url}")
                    except Exception as e:
                        print(f"Failed to download {ts_url}: {e}")

            print("TypeScript files downloaded and saved successfully.")
        except requests.exceptions.MissingSchema:
            print(f"Skipping download from {self.url} (Invalid URL)")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch content from {self.url}: {e}")
        except OSError as e:
            print(f"Failed to save TypeScript file: {e}")
