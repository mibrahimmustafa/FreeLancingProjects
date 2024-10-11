import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class WebsiteScraper:
    def __init__(self, url, download_dir='website_content'):
        self.url = url
        self.download_dir = download_dir
        self.base_url = "{0.scheme}://{0.netloc}".format(urlparse(self.url))
        
        # Create the download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def fetch_page_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page content: {e}")
            return None

    def save_file(self, file_url, folder, file_name=None):
        try:
            if not file_name:
                # Extract the filename from the URL and remove query parameters (anything after `?`)
                file_name = file_url.split("/")[-1].split('?')[0]
            
            # Sanitize the file_name by removing any invalid characters for the file system
            file_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)
            
            file_path = os.path.join(self.download_dir, folder, file_name)
            
            # Create the folder if it doesn't exist
            if not os.path.exists(os.path.join(self.download_dir, folder)):
                os.makedirs(os.path.join(self.download_dir, folder))
            
            response = requests.get(file_url)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {file_url}: {e}")
            
    def scrape(self):
        page_content = self.fetch_page_content()
        if not page_content:
            return
        
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Save the main HTML file
        with open(os.path.join(self.download_dir, 'index.html'), 'a', encoding='utf-8') as file:
            file.write(soup.prettify())
        
        # Extract and download all CSS, JS, and images
        self.download_resources(soup, 'link', 'href', 'css', 'stylesheet')
        self.download_resources(soup, 'script', 'src', 'js')
        self.download_resources(soup, 'img', 'src', 'images')

    def download_resources(self, soup, tag, attribute, folder, condition=None):
        for element in soup.find_all(tag):
            file_url = element.get(attribute)
            if file_url and (condition is None or condition in element.get('rel', [])):
                full_url = urljoin(self.base_url, file_url)
                self.save_file(full_url, folder)

# for medscastle
if __name__ == '__main__':
    # urls = ['https://www.medscastle.com' ,'https://www.medscastle.com/ourpartners','https://www.medscastle.com/wecare','https://www.medscastle.com/ar','https://www.medscastle.com/ar/ourpartners','https://www.medscastle.com/ar/wecare'] 
    # for url in urls:
    #     scraper = WebsiteScraper(url,'medscastle' )
    #     scraper.scrape()
# for elkomy
# if __name__ == '__main__':
    urls = ['https://www.elkomyco.com/' ,'https://www.elkomyco.com/about-company/','https://www.elkomyco.com/products/','https://www.elkomyco.com/contact-us/','https://www.elkomyco.com/welcome','https://www.elkomyco.com/wp-content',
            'https://www.elkomyco.com/feed/','https://www.elkomyco.com/comments/feed/','https://www.elkomyco.com/wp-includes','https://www.elkomyco.com/wp-content/','https://www.elkomyco.com/wp-json',
            'https://www.elkomyco.com/xmlrpc.php','https://www.elkomyco.com/wp-content','https://www.elkomyco.com/portfolio-item/','https://www.elkomyco.com/arvina-eh2/','https://www.elkomyco.com/copaslip',
            'https://www.elkomyco.com/arivera-fm2/','https://www.elkomyco.com/dry-graphite/','https://www.elkomyco.com/arvina-sg3','https://www.elkomyco.com/arvina-fx2/','https://www.elkomyco.com/ferroslip/',
            'https://www.elkomyco.com/ferroslip/','https://www.elkomyco.com/grease/','https://www.elkomyco.com/copper-anti-seize/','https://www.elkomyco.com/multi-purpose/',
            'https://www.elkomyco.com/white-safe','https://www.elkomyco.com/cartridge-grease','https://www.elkomyco.com/moly-high/','https://www.elkomyco.com/moly-air-drying-film/',
            'https://www.elkomyco.com/palco-grease/','https://www.elkomyco.com/palco-grease-100-gram','https://www.elkomyco.com/palco-grease-500-gram','https://www.elkomyco.com/palco-grease-1-kilo',
            'https://www.elkomyco.com/palco-grease-5-kilo/','https://www.elkomyco.com/accor-bearings/','https://www.elkomyco.com/anarobic-adhisives/','https://www.elkomyco.com/portfolio-item','https://elkomyco.com/palco-grease','https://www.elkomyco.com/wp-includes',
            'https://www.elkomyco.com/wp-json','https://www.elkomyco.com/xmlrpc.php'] 
    for url in urls:
        scraper = WebsiteScraper(url, 'elkomyco')
        scraper.scrape()
