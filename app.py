from flask import Flask, jsonify, render_template, make_response
import pandas as pd
import random

app = Flask(__name__)
csv_file = 'menu_items.csv'
df = pd.read_csv(csv_file)

def spin_the_wheel(df):
    random_index = random.randint(0, len(df) - 1)
    chosen_item = df.loc[random_index]
    return chosen_item.to_dict()

#get all the restaurants build dropdown
def get_restaurants(df):
    restaurants = df['RestaurantName'].unique()
    return list(restaurants)

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

if __name__ == '__main__':
    app.run(debug=True,port=5003)
