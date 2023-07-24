import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ScrapOtherFiles:
    def __init__(self, url, output_folder, file_extensions):
        self.url = url
        self.output_folder = output_folder
        self.file_extensions = file_extensions

    def extract_and_save_files(self):
        try:
            # Send an HTTP GET request to the webpage and get the HTML content
            response = requests.get(self.url)
            response.raise_for_status()
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all links with file extensions in the 'file_extensions' list
            file_links = [link['href'] for link in soup.find_all('a', href=True) if any(link['href'].endswith(ext) for ext in self.file_extensions)]

            # Create the output folder if it doesn't exist
            os.makedirs(self.output_folder, exist_ok=True)

            # Download and save files in the output folder
            for file_link in file_links:
                file_url = urljoin(self.url, file_link)
                folder_name = os.path.dirname(file_link)
                if folder_name.startswith("/"):
                    folder_name = folder_name[1:]
                folder_name = folder_name.replace("/", "_")  # Replace invalid characters in folder_name
                folder_path = os.path.join(self.output_folder, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                filename = os.path.basename(file_link)
                try:
                    file_content = requests.get(file_url).content
                    with open(os.path.join(folder_path, filename), 'wb') as file:
                        file.write(file_content)
                    print(f"Downloaded: {file_url}")
                except Exception as e:
                    print(f"Failed to download {file_url}: {e}")

            print("Files downloaded and saved successfully.")
        except requests.exceptions.MissingSchema:
            print(f"Skipping download from {self.url} (Invalid URL)")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch content from {self.url}: {e}")
        except OSError as e:
            print(f"Failed to save file: {e}")
