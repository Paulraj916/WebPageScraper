import os
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin

class ScrapScss:
    def __init__(self, link):
        self.link = link

    def scrap_scss(self):
        try:
            # Send an HTTP GET request to the webpage
            response = requests.get(self.link)
            response.raise_for_status()

            # Get the HTML content of the page
            html_content = response.text

            # Extract SCSS file URLs from the webpage and convert to absolute URLs
            base_url = response.url
            soup = BeautifulSoup(html_content, 'html.parser')
            scss_urls = [urljoin(base_url, link['href']) for link in soup.find_all('link', rel='stylesheet/scss')]

            # Create an "output" folder if it doesn't exist
            output_path = "output"
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Download and store SCSS files in the "output" folder
            for scss_url in scss_urls:
                folder_name = os.path.dirname(scss_url.replace(base_url, "").replace("http://", "").replace("https://", ""))
                if folder_name.startswith("/"):
                    folder_name = folder_name[1:]
                folder_path = os.path.join(output_path, folder_name)
                try:
                    os.makedirs(folder_path, exist_ok=True)
                    filename = os.path.basename(scss_url)
                    try:
                        scss_content = requests.get(scss_url).text
                        with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as file:
                            file.write(scss_content)
                        print("Downloaded:", scss_url)
                    except Exception as e:
                        print(f"Failed to download {scss_url}: {e}")
                except Exception as e:
                    print(f"Failed to download {scss_url}: {e}")

            print("SCSS files downloaded and saved successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch content from {self.link}: {e}")
