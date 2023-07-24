import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ScrapAudio:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def extract_and_save_audio(self):
        try:
            # Send an HTTP GET request to the webpage and get the HTML content
            response = requests.get(self.url)
            response.raise_for_status()
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all audio tags
            audio_tags = soup.find_all('audio')

            # Extract audio URLs and store them in a list
            audio_urls = []
            for audio_tag in audio_tags:
                if 'src' in audio_tag.attrs:
                    audio_url = audio_tag['src']
                    absolute_url = urljoin(self.url, audio_url)
                    audio_urls.append(absolute_url)

            # Create the output folder if it doesn't exist
            os.makedirs(self.output_folder, exist_ok=True)

            # Download and save audio files in the output folder
            for audio_url in audio_urls:
                audio_content = requests.get(audio_url).content

                # Get the path to the audio file
                path = urljoin(self.url, audio_url).replace(self.url, '').lstrip('/')
                filename = os.path.join(self.output_folder, path)

                # Create subdirectories if needed
                os.makedirs(os.path.dirname(filename), exist_ok=True)

                # Save the audio content to the file
                with open(filename, 'wb') as file:
                    file.write(audio_content)

                print(f"Downloaded: {audio_url}")

            print("Audio files downloaded and saved successfully.")
        except requests.exceptions.MissingSchema:
            print(f"Skipping download from {self.url} (Invalid URL)")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch content from {self.url}: {e}")
        except OSError as e:
            print(f"Failed to save audio files: {e}")
