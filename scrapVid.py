import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ScrapVideos:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def extract_and_save_videos(self):
        try:
            # Send an HTTP GET request to the webpage and get the HTML content
            response = requests.get(self.url)
            response.raise_for_status()
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all video tags
            video_tags = soup.find_all('video')

            # Extract video URLs and store them in a list
            video_urls = []
            for video_tag in video_tags:
                if 'src' in video_tag.attrs:
                    video_url = video_tag['src']
                    absolute_url = urljoin(self.url, video_url)
                    video_urls.append(absolute_url)

            # Create the output folder if it doesn't exist
            os.makedirs(self.output_folder, exist_ok=True)

            # Save video URLs to videolink.txt
            videolink_path = os.path.join(self.output_folder, 'videolink.txt')
            with open(videolink_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(video_urls))

            print(f"Video links saved to {videolink_path}")
        except requests.exceptions.MissingSchema:
            print(f"Skipping download from {self.url} (Invalid URL)")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch content from {self.url}: {e}")
        except OSError as e:
            print(f"Failed to save video links: {e}")
