from flask import Flask, request, render_template
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time

app = Flask(__name__)

def get_course_price(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

    try:
        # Launch a Chrome browser
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        

        driver = webdriver.Chrome(options=options)

        # Navigate to the Udemy course page
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        # Get the HTML of the page
        html = driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find the element containing the course price
        price_element = soup.find('div', {'class': ['price-text--container--103D9 slider-menu--price-text--2zHqE ud-clp-price-text','price-text--container--103D9 slider-menu--price-text--2zHqE ud-clp-price-text']}).find_all('span')[1]
        print(price_element)
        # Extract the price from the element
        price_text = price_element.text.strip()
        print(price_text)
        if price_text.lower() == 'free':
            price = 'Free'
        else:
            # Extract the price from the element
            price = re.search(r'\d+\.\d+', price_text).group()

        # Close the browser
        driver.quit()

        return price
    except:
        return 'Error: Could not fetch course price.'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = request.form.get('urls')
        courses = []
        for url in urls.split():
            price = get_course_price(url)
            courses.append({'url': url, 'price': price})
        return render_template('result.html', courses=courses)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

