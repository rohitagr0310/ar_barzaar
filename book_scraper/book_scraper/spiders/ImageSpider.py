import os
import scrapy
from urllib.parse import urljoin
import sqlite3

class ImageSpider(scrapy.Spider):
    name = "ImageSpider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]
    counter = 1  # Initialize a counter

    def parse(self, response):
        
        for book_link in response.css("ol.row article.product_pod a"):
            yield response.follow(book_link.attrib["href"] , callback=self.image)
        
        for next_page_link in response.css("ul.pager li.next a"):
            yield response.follow(next_page_link.attrib["href"] , callback=self.parse)

    def image(self, response):
        base_url = response.url
        image_urls = response.css('div#product_gallery img::attr(src)').getall()
        for image_url in image_urls:
            absolute_image_url = urljoin(base_url, image_url)
            yield scrapy.Request(absolute_image_url, callback=self.save_image)

    def save_image(self, response):
        image_name = f'{self.counter}.jpg'  # Generate a unique image name
        self.counter += 1  # Increment the counter for the next image
        folder = 'images'  # Folder name to save the images
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_path = os.path.join(folder, image_name)
        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved image: {file_path}')
        
        # Save data to SQLite database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO images (image_url, file_name) VALUES (?, ?)", (response.meta['image_url'], image_name))
        conn.commit()
        conn.close()
