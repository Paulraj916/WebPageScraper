import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ScrapFonts:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def extract_and_save_fonts(self):
        try:
            # Send an HTTP GET request to the webpage and get the HTML content
            response = requests.get(self.url)
            response.raise_for_status()
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all font tags
            font_tags = soup.find_all('link', {'rel': 'stylesheet', 'type': 'text/css'})

            # Extract font URLs and store them in a list
            font_urls = []
            for font_tag in font_tags:
                if 'href' in font_tag.attrs:
                    font_url = font_tag['href']
                    absolute_url = urljoin(self.url, font_url)
                    font_urls.append(absolute_url)

            # Create the output folder if it doesn't exist
            os.makedirs(self.output_folder, exist_ok=True)

            # Download and save fonts in the output folder
            for font_url in font_urls:
                try:
                    font_content = requests.get(font_url).content

                    # Get the path to the font file
                    path = urljoin(self.url, font_url).replace(self.url, '').lstrip('/')
                    filename = os.path.join(self.output_folder, path)

                    # Create subdirectories if needed
                    os.makedirs(os.path.dirname(filename), exist_ok=True)

                    # Save the font content to the file
                    with open(filename, 'wb') as file:
                        file.write(font_content)

                    print(f"Downloaded: {font_url}")
                except Exception as e:
                    print(f"Failed to download {font_url}: {e}")

            print("Fonts downloaded and saved successfully.")
        except requests.exceptions.MissingSchema:
            print(f"Skipping download from {self.url} (Invalid URL)")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch content from {self.url}: {e}")
        except OSError as e:
            print(f"Failed to save font: {e}")
