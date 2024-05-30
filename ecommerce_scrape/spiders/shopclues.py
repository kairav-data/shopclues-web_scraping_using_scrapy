import scrapy

class ShopcluesSpider(scrapy.Spider):
    name = "shopclues"
    allowed_domains = ["shopclues.com"]
    start_urls = ["https://www.shopclues.com/mens-clothing-t-shirts.html?page=1"]

    def parse(self, response):
        # Parse the initial page to extract product information
        products = self.extract_products(response)
        if not products:
            # Stop if no products are found on the current page
            self.log("No products found on page, stopping spider.")
            return

        # Yield each product
        for product in products:
            yield product

        # Manually construct the next page URL
        current_page = response.url.split('=')[-1]
        next_page = int(current_page) + 1

        next_page_url = f'https://www.shopclues.com/mens-clothing-t-shirts.html?page={next_page}'
        yield response.follow(next_page_url, callback=self.parse)

    def extract_products(self, response):
        # Logic to extract products from the page HTML
        products = []
        for product in response.xpath("//div[@class='column col3']"):
            name = product.xpath(".//span[@class='prod_name ']/text()").get()
            price = product.xpath(".//span[@class='p_price']/text()").get()
            old_price = product.xpath(".//span[@class='old_prices']/span/text()").get()
            discount = product.xpath(".//span[@class='prd_discount ']/text()").get()

            products.append({
                'name': name.strip() if name else None,
                'price': price.strip() if price else None,
                'old_price': old_price.strip() if old_price else None,
                'discount': discount.strip() if discount else None,
            })
        return products
