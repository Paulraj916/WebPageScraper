import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ScrapIcon:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def extract_and_save_icons(self):
        try:
            # Send an HTTP GET request to the webpage and get the HTML content
            response = requests.get(self.url)
            response.raise_for_status()
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all icon tags
            icon_tags = soup.find_all('link', {'rel': 'icon'})

            # Extract icon URLs and store them in a list
            icon_urls = []
            for icon_tag in icon_tags:
                if 'href' in icon_tag.attrs:
                    icon_url = icon_tag['href']
                    absolute_url = urljoin(self.url, icon_url)
                    icon_urls.append(absolute_url)

            # Create the output folder if it doesn't exist
            os.makedirs(self.output_folder, exist_ok=True)

            # Download and save icons in the output folder
            for icon_url in icon_urls:
                icon_content = requests.get(icon_url).content

                # Get the path to the icon file
                path = urljoin(self.url, icon_url).replace(self.url, '').lstrip('/')
                filename = os.path.join(self.output_folder, path)

                # Create subdirectories if needed
                os.makedirs(os.path.dirname(filename), exist_ok=True)

                # Save the icon content to the file
                with open(filename, 'wb') as file:
                    file.write(icon_content)

                print(f"Downloaded: {icon_url}")

            print("Icons downloaded and saved successfully.")
        except requests.exceptions.MissingSchema:
            print(f"Skipping download from {self.url} (Invalid URL)")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch content from {self.url}: {e}")
        except OSError as e:
            print(f"Failed to save icons: {e}")
