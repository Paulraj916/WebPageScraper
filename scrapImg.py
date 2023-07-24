import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ScrapImages:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def scrape_images(self):
        try:
            # Fetch the webpage content
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an exception if the request was not successful

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract image URLs from the webpage and convert to absolute URLs
            base_url = self.url
            image_urls = [urljoin(base_url, img['src']) for img in soup.find_all('img', src=True)]

            # Store the image URLs in a text file
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)

            output_path = os.path.join(self.output_folder, 'imglink.txt')
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(image_urls))

            print(f"Image URLs saved to {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch content from {self.url}: {e}")
        except Exception as e:
            print(f"Failed to scrape images: {e}")
