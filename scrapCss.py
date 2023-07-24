import os
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cssbeautifier
from webdriver_manager.chrome import ChromeDriverManager 

class ScrapCss:
    def __init__(self, link):
        self.link = link

    def scrap_css(self):
        try:
            # Set up Chrome WebDriver
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no visible browser window)
            
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


            # Send an HTTP GET request to the webpage
            response = requests.get(self.link)
            response.raise_for_status()

            # Get the HTML content of the page
            html_content = response.text

            # Extract CSS file URLs from the webpage and convert to absolute URLs
            base_url = response.url
            soup = BeautifulSoup(html_content, 'html.parser')
            css_urls = [urljoin(base_url, link['href']) for link in soup.find_all('link', rel='stylesheet')]

            # Quit the driver
            driver.quit()

            # Create an "output" folder if it doesn't exist
            output_path = "output"
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Download and store CSS files in the "output" folder
            for css_url in css_urls:
                folder_name = os.path.dirname(css_url.replace(base_url, "").replace("http://", "").replace("https://", ""))
                if folder_name.startswith("/"):
                    folder_name = folder_name[1:]
                folder_path = os.path.join(output_path, folder_name)
                try:
                    os.makedirs(folder_path, exist_ok=True)
                    filename = os.path.basename(css_url)
                    try:
                        css_content = requests.get(css_url).text
                        # Beautify CSS content
                        css_content = cssbeautifier.beautify(css_content)
                        with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as file:
                            file.write(css_content)
                        print("Downloaded and beautified:", css_url)
                    except Exception as e:
                        print(f"Failed to download {css_url}: {e}")
                except Exception as e:
                    print(f"Failed to download {css_url}: {e}")

            print("CSS files downloaded and saved successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch content from {self.link}: {e}")

