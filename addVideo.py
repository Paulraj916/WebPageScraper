import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class AddVideo:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def add_absolute_video_urls(self):
        try:
            # Read the downloaded HTML file from the output folder
            html_file_path = os.path.join(self.output_folder, 'index.html')

            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Create the BeautifulSoup object using the downloaded HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all video tags
            video_tags = soup.find_all('video')

            # Extract video URLs and store them in a list
            video_urls = []
            for video_tag in video_tags:
                if 'src' in video_tag.attrs:
                    video_url = video_tag['src']
                    absolute_url = urljoin(self.url, video_url)
                    video_urls.append((video_url, absolute_url))

            # Replace video URLs in the HTML code with absolute URLs
            for video_url, absolute_url in video_urls:
                soup.find('video', src=video_url)['src'] = absolute_url

            # Save the updated HTML code to video_updated.html
            updated_html_path = os.path.join(self.output_folder, 'index.html')
            with open(updated_html_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))

            print(f"Updated HTML code saved to {updated_html_path}")
        except FileNotFoundError:
            print("HTML file not found. Make sure to run the other scrapers first.")
        except Exception as e:
            print(f"Failed to update video URLs: {e}")
