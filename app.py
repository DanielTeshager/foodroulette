from flask import Flask, jsonify, render_template, make_response
import pandas as pd
import random
import openai
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

app = Flask(__name__)
csv_file = 'new_menu_items.csv'
df = pd.read_csv(csv_file)
openai.api_key = os.environ.get('OPENAI_API_KEY')
#use openai to get nutrition info
def get_nutrition_info(food_name):
    # search for food name
    print(f"searching for {food_name}")
    nutrition_facts = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f""""
show nutritional fact and classify as healthy or indulgent 
{food_name}
provide a brief answer in json format. no explanation is need just the json formatted response. no disclaimer or any additional information is required

Example"""+"""
{
  "name": "food name emoji of the food",
  "nutrition": {
    "ingredients": "value"
  } | {"nutrition": "not found"},
  "classification": "indulgent | healthy | not found"
}
add more ingredients: value pairs as needed

don't replay with any other text that's not parsed!
don't add Response: or any other text before the json response
only reply with the json response allways in the same format both key and value must be in double quotes check if the response is valid json before submitting
be creative with the emojis the more the better just don't replace the food name with emoji put it next to it and make sure it's a valid emoji
use two or more emojis if you can't find a single emoji for the food name
if the value is zero or empty string don't include it in the response
""",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3,
    ).choices
    # if no results return empty dict
    if len(nutrition_facts) == 0:
        return {}
    # if results return random result
    else:
        print(nutrition_facts[0].text)
        return nutrition_facts[0].text

def spin_the_wheel(df):
    random_index = random.randint(0, len(df) - 1)
    chosen_item = df.loc[random_index]
    return chosen_item.to_dict()

#get all the restaurants build dropdown
def get_restaurants(df):
    restaurants = df['RestaurantName'].unique()
    return list(restaurants)

# get similar food items in df based on the item returned from the wheel
def get_similar_items(df, item):
    # get restaurant names and price that has a similar item
    similar_items = df.loc[df['FoodName'].str.contains(item)][['RestaurantName', 'Price']]
    
    # if no similar items return empty dict
    if len(similar_items) == 0:
        return {}
    # if results return random result
    else:
        return similar_items.to_dict('records')



def find_similar_food(df, food_name, restaurant_name, price, threshold=80):
    def get_similarity(row):
        return fuzz.token_set_ratio(row["FoodName"], food_name)

    df["similarity"] = df.apply(get_similarity, axis=1)
    similar_food_df = df[(df["similarity"] >= threshold) & (df["RestaurantName"] != restaurant_name) & (df["Price"].astype(float) < price)].drop("similarity", axis=1)
    filter_columns = ['FoodName', 'RestaurantName', 'Price']
    similar_food_df = similar_food_df[filter_columns].sort_values(by=['Price']).head(3)

    # if no similar items return empty dict
    if len(similar_food_df) == 0:
        return {}
    # if results return random result
    else:
        # serialize the dataframe to json
        return similar_food_df.to_json(orient='records')



@app.route('/')
def index():
    restaurants = get_restaurants(df)
    json_restaurants = jsonify(restaurants)
    print(json_restaurants)
    return render_template('index.html', restaurants=restaurants)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/spin')
def spin():
    item = spin_the_wheel(df)
    print(item)
    return jsonify(item)
    
# search for nutrition info based on food name
@app.route('/search/<food_restaurant_price>')
def search(food_restaurant_price):
    # search for food name
    food_name, restaurant_name, price = food_restaurant_price.split(':')
    # print(food_name, restaurant_name, price)
    # price = re.search(r"[0-9]{:3}",price)
    price_pattern = re.compile(r"([0-9]{1,3})")
    price = price_pattern.search(price).group(1)
    price = float(price)
    
    nutrition_facts = get_nutrition_info(food_name)
    similar_food_df = find_similar_food(df, food_name, restaurant_name, price, threshold=70)
    print(similar_food_df)
    # if no results return empty dict
    if len(nutrition_facts) == 0:
        return jsonify({})
    # if results return random result
    elif len(similar_food_df) == 0:
        return jsonify({"nutrition_facts":nutrition_facts, "similar_food": {}})
    else:
        print(nutrition_facts)
        print("--------------------------")
        print(similar_food_df)
        return jsonify({"nutrition_facts": nutrition_facts, "similar_food": similar_food_df})
    #

if __name__ == '__main__':
    app.run(debug=True,port=5005)
