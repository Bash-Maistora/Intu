from flask import Flask, request
import string
import re
app = Flask(__name__)


def create_table():
    """Simple SQL Database design mapping the retailer category to the corresponding
    one at intu. For this specific use case a key-value database might be a 
    better solution in terms of scalability and performance
    as there are no complex relations between the data. """
    command = (
        """
        CREATE TABLE category_mappings(
            retailer_category VARCHAR(250) PRIMARY KEY,
            intu_mapping VARCHAR(250) NOT NULL
        )
        """)

categories = [{'name': 'Men', 'matches': ['men', 'mens', 'male', 'males', 'man']},
              {'name': 'Women', 'matches': ['women', 'womens', 'female', 'females', 'woman']}]


sub_categories = {'jewelry': 'jewellery', 'clothes': 'clothing', 'shoes': 'footwear',
          'bag': 'bags', 'skirt': 'dresses', 'dress': 'dresses', 'backpacks': 'bags',
          'boots': 'footwear', 'shirts': 'clothing', 'trousers': 'clothing',
          'pants': 'clothing', 'hats': 'accessories', 'accessory': 'accessories',
          'coats': 'clothing', 'jackets': 'clothing', 'shirt': 'clothing',
          'clothing': 'clothing', 'footwear': 'footwear', 'bags': 'bags',
          'jeans': 'clothing', 'skirts': 'dresses', 'jacket': 'clothing',
          'tops': 'clothing', 'sneakers': 'footwear', 'accessories': 'accessories',
          'jewellery': 'jewellery', 'dresses': 'dresses'}


def categorize(words):
    """Matches intu top and sub categories to
    a list of words from retailer categories"""
    top_category = ''
    sub_category = ''
    for category in categories:
        if set(words) & set(category['matches']):
            top_category = category['name']

    for key, value in sub_categories.items():
        if key in words:
            sub_category = value.capitalize()

    return top_category, sub_category


def normalize(category):
    """Builds a list from the cleaned and standardized category data"""
    cleaned = re.sub('[^a-zA-Z]+', ' ', category)
    translator = str.maketrans("", "", string.punctuation)
    clean_string = cleaned.translate(translator)
    words = clean_string.split()
    return words


@app.route("/")
def category_mapping():
    """Accept retailer category as query parameter and return
    the corresponding intu category"""
    category = request.args.get('category')
    if category:
        words = normalize(category.lower())
        return ''.join(['/%s' % i for i in categorize(words)])
    else:
        return 'Submit a category as query parameter.'

if __name__ == '__main__':
    app.run(debug=False, port=5000)
