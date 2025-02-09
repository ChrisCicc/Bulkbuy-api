import requests
from bs4 import BeautifulSoup

def scrape_product(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract product details
        product_name_tag = soup.find("h1", class_="product-information_title__3jR8K")
        product_price_meta = soup.find("meta", {"name": "twitter:data1"})
        product_image_meta = soup.find("meta", {"property": "og:image"})

        # Extract sizes
        size_tags = soup.find_all("label", {"data-locator-id": lambda x: x and "pdp-size" in x})
        sizes = [size.text.strip() for size in size_tags] if size_tags else ["Size information not found"]

        # Extract colors and their images
        color_tags = soup.find_all("a", {"data-locator-id": lambda x: x and "pdp-colourVariant" in x})
        colors = [
            {
                "color": color.find("img")["alt"].replace(" in ", "").strip(),
                "image": color.find("img")["src"]
            }
            for color in color_tags if color.find("img")
        ] if color_tags else [{"color": "Color information not found", "image": "Image not found"}]

        # Extract text or attributes
        product_name = product_name_tag.text.strip() if product_name_tag else "Product name not found"
        product_price = product_price_meta["content"] if product_price_meta else "Price not found"
        product_image = product_image_meta["content"] if product_image_meta else "Image not found"

        return {
            "name": product_name,
            "price": product_price,
            "image": product_image,
            "sizes": sizes,
            "colors": colors
        }

    except Exception as e:
        # Handle exceptions and return the error message
        return {"error": f"An error occurred: {str(e)}"}

# Test with the given product URL
if __name__ == "__main__":
    test_url = "https://eu.gymshark.com/products/gymshark-vital-seamless-2-0-leggings-woodland-green-marl-aw22"
    product_details = scrape_product(test_url)
    print(product_details)
