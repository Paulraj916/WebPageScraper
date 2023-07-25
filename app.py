import os
import streamlit as st
from scrapJs import ScrapJs
from scrapCss import ScrapCss
from scrapTs import ScrapTs
from scrapOtherFiles import ScrapOtherFiles
from scrapFonts import ScrapFonts
from scrapVid import ScrapVideos
from scrapAudio import ScrapAudio
from scrapIcon import ScrapIcon
from addVideo import AddVideo
from scrapImg import ScrapImages
from addImg import AddImages
from scrapHtml import ScrapHtml
from scrapScss import ScrapScss
import shutil
from zipfile import ZipFile

def main():
    st.title("Web Page Scraper")

    link = st.text_input("Enter the URL of the website you want to scrape:")
    if not link:
        st.stop()

    output = "output"
    
    if st.button("Start Scraping"):
        st.text("Scraping in progress...")
        st.spinner()
        
        # Scrape JS
        scraper_js = ScrapJs(link)
        scraper_js.scrap_js()

        # Scrape CSS
        scraper_css = ScrapCss(link)
        scraper_css.scrap_css()

        # Scrape HTML Files
        scraper_html = ScrapHtml(link)
        scraper_html.scrape_html_files()

        # Scrape SCSS
        scraper_scss = ScrapScss(link)
        scraper_scss.scrap_scss()

        # Scrape TypeScript
        scraper_ts = ScrapTs(link)
        scraper_ts.extract_and_save_typescript()

        # Scrape Other Files
        output_folder_other = output
        file_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.tar.gz', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.mp4', '.avi', '.webm', '.mkv', '.mp3', '.wav', '.ogg']
        scraper_other = ScrapOtherFiles(link, output_folder_other, file_extensions)
        scraper_other.extract_and_save_files()

        # Scrape Fonts
        output_folder_fonts = output
        scraper_fonts = ScrapFonts(link, output_folder_fonts)
        scraper_fonts.extract_and_save_fonts()

        # Scrape Videos
        output_folder_videos = output
        scraper_videos = ScrapVideos(link, output_folder_videos)
        scraper_videos.extract_and_save_videos()

        # Scrape Audio
        output_folder_audio = output
        scraper_audio = ScrapAudio(link, output_folder_audio)
        scraper_audio.extract_and_save_audio()

        # Scrape Icons
        output_folder_icons = output
        scraper_icons = ScrapIcon(link, output_folder_icons)
        scraper_icons.extract_and_save_icons()

        # Scrape Images
        output_folder_images = output
        scraper_images = ScrapImages(link, output_folder_images)
        scraper_images.scrape_images()

        # Add Absolute Video URLs
        add_video = AddVideo(link, output)
        add_video.add_absolute_video_urls()

        # Add Absolute Image URLs
        add_images = AddImages(link, output)
        add_images.add_absolute_image_urls()

        st.success("Scraping completed successfully!")

        st.text("Creating zip file....(This may take time based on the content in webpage)")

        # Create a zip file containing the output folder and its contents
        output_zip = os.path.join(output, "output")
        shutil.make_archive(output_zip, 'zip', output)

        # Provide a download link for the zip file with the correct file name and type
        with open(output_zip + ".zip", "rb") as file:
            st.download_button("Download Output Folder", file, file_name="output.zip", mime="application/zip")

        # Remove the temporary output folder
        shutil.rmtree(output)

if __name__ == "__main__":
    main()
