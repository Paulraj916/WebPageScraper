import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class AddImages:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def add_absolute_image_urls(self):
        try:
            # Read the image URLs from the imglink.txt file
            imglink_path = os.path.join(self.output_folder, 'imglink.txt')

            image_urls = []
            with open(imglink_path, 'r', encoding='utf-8') as file:
                image_urls = file.read().splitlines()

            # Replace the src attribute in the HTML code with the absolute URLs
            html_file_path = os.path.join(self.output_folder, 'index.html')
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, 'html.parser')
            base_url = self.url

            for img_tag in soup.find_all('img', src=True):
                src_value = img_tag['src']
                absolute_src = urljoin(base_url, src_value)
                img_tag['src'] = absolute_src

            # Save the updated HTML code to a new file or overwrite the original file
            output_html_path = os.path.join(self.output_folder, 'index.html')
            with open(output_html_path, 'w', encoding='utf-8') as file:
                file.write(soup.prettify())

            print(f"HTML code with updated image URLs saved to {output_html_path}")
        except Exception as e:
            print(f"Failed to update image URLs: {e}")
