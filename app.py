from flask import Flask, request, render_template, send_file
import os
import random
import html
import re
import time
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

def get_html_from_page(url: str) -> str:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(random.randint(2000, 4000) / 100)
        html_content = driver.page_source
    finally:
        driver.quit()

    return html_content

def clean_single_url(raw_url):
    url = raw_url.replace('\\/', '/')
    url = url.replace('&amp;', "&")
    url = bytes(url, "utf-8").decode("unicode_escape")
    url = html.unescape(url)
    return url

def clean_instagram_urls(raw_text):
    raw_urls = re.findall(r'https:\\/\\/[^ \n"<>\']+', raw_text)
    cleaned_urls = []

    for raw_url in raw_urls:
        url = clean_single_url(raw_url)
        url = url.replace("</BaseURL><SegmentBase", "")
        cleaned_urls.append(url)

    return cleaned_urls

def extract_reel_id(instagram_url: str) -> str:
    path = urlparse(instagram_url).path
    parts = [p for p in path.split('/') if p]
    if 'reel' in parts:
        return parts[parts.index('reel') + 1]
    elif 'p' in parts:
        return parts[parts.index('p') + 1]
    return "video"

def download_video(url: str, filename: str):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return filename
    except requests.RequestException as e:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    video_url = ""
    filename = ""
    error = ""
    if request.method == "POST":
        instagram_url = request.form["url"]
        should_download = "download" in request.form

        try:
            page_html = get_html_from_page(instagram_url)
            counter = 0
            while video_url == "" and counter < 4:
                counter += 1
                for i in page_html.split('"'):
                    if "http" in i and ".mp4" in i:
                        cleaned = clean_instagram_urls(i)
                        if cleaned:
                            video_url = cleaned[0]
                            if should_download:
                                reel_id = extract_reel_id(instagram_url)
                                filename = f"{reel_id}.mp4"
                                download_video(video_url, filename)
                            break
        except Exception as e:
            error = str(e)

    return render_template("index.html", video_url=video_url, filename=filename, error=error)

@app.route("/download/<filename>")
def serve_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
