"""
wechat_images_to_pdf.py

这是一个用于从微信公众号文章中提取图片并将其转换为 PDF 文件的 Python 脚本。
它能够自动从文章页面中识别图片，下载它们，并根据文章标题生成规范化的 PDF 文件名。

功能:
- 从给定的微信文章 URL 中抓取所有图片。
- 将抓取到的图片合并为一个 PDF 文件。
- 自动从文章标题生成 PDF 文件名，支持中文标题。
- 处理常见的图片格式，并转换为 RGB 模式以确保兼容性。

依赖安装:
在运行此脚本之前，请确保您已安装所有必要的 Python 库。您可以使用 pip 来安装它们：

pip install requests beautifulsoup4 Pillow

如何运行:
1. 确保您已安装上述依赖。
2. 运行脚本并提供微信文章的 URL 作为命令行参数：

   python wechat_images_to_pdf.py <微信文章URL>

示例:
   python wechat_images_to_pdf.py https://mp.weixin.qq.com/s/tuGBXLYjjeKbR1PqGPw7Rg

输出的 PDF 文件将根据文章标题命名，并保存在脚本当前运行的目录下。
"""
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import sys
import re

def get_images_from_url(url):
    """
    Fetches images from a given URL.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', id='js_content')
    
    if not content_div:
        print("Could not find the main content div with id 'js_content'.")
        return []

    img_tags = content_div.find_all('img')
    
    image_urls = []
    for img in img_tags:
        # Weixin images are often in 'data-src' attribute
        if 'data-src' in img.attrs:
            image_urls.append(img['data-src'])
        elif 'src' in img.attrs:
            image_urls.append(img['src'])
            
    return image_urls

def create_pdf_from_images(image_urls, output_pdf_path):
    """
    Creates a PDF from a list of image URLs.
    """
    images = []
    
    # Create a directory to store downloaded images temporarily
    temp_dir = "temp_images"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for i, img_url in enumerate(image_urls):
        try:
            print(f"Downloading image {i+1}/{len(image_urls)}: {img_url}")
            img_response = requests.get(img_url)
            img_response.raise_for_status()
            
            # Open image from bytes
            img = Image.open(BytesIO(img_response.content))
            
            # Convert to RGB if necessary (e.g., for WEBP with alpha)
            if img.mode == 'RGBA' or img.mode == 'P':
                img = img.convert('RGB')

            images.append(img)

        except Exception as e:
            print(f"Could not download or process image {img_url}. Error: {e}")

    if not images:
        print("No images were downloaded. PDF cannot be created.")
        return

    # Save the first image and append the rest
    images[0].save(
        output_pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )
    
    print(f"Successfully created PDF: {output_pdf_path}")

def get_normalized_filename_from_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('h1', class_='rich_media_title', id='activity-name')
        if title_tag:
            title = title_tag.get_text(strip=True)
            # Remove invalid characters for filenames and replace spaces with underscores
            normalized_title = re.sub(r'[\\/:*?"<>|]', '', title).replace(' ', '_')
            return f"{normalized_title}.pdf"
    except Exception as e:
        print(f"Error extracting title from URL {url}: {e}")
    return "微信文章.pdf"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wechat_images_to_pdf.py <article_url>")
        sys.exit(1)

    article_url = sys.argv[1]
    output_pdf = get_normalized_filename_from_url(article_url)

    # 1. Get all image URLs from the article
    image_urls = get_images_from_url(article_url)

    if image_urls:
        # 2. Create a PDF from the downloaded images
        create_pdf_from_images(image_urls, output_pdf)
    else:
        print("No images found in the article.")
