import scrapy
import pandas as pd
import sqlite3


i = 0

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        
        for book_link in response.css("ol.row article.product_pod a"):
            yield response.follow(book_link.attrib["href"] , callback=self.extract_book)
        
        for next_page_link in response.css("ul.pager li.next a"):
            yield response.follow(next_page_link.attrib["href"] , callback=self.parse)


    def extract_book(self, response):
        title = response.css("div.product_main h1::text").get()
        price = response.css("div.product_main p::text").get()
        description = response.css("#product_description + p::text").get()
        table_info = response.css("table.table").get()
        book_info = pd.read_html(table_info)[0].set_index(0).to_dict()[1]
        book_info["title"] = title
        book_info["categories"] = response.css("div.page_inner ul.breadcrumb li a ::text").getall()
        book_info['price'] = price
        book_info['description'] = description
        return book_info
    
        
    
  