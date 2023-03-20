#!/usr/bin/env python
import openai
import pandas as pd
import os
import re
import string

openai.api_key = "your api key"

messages = [{"role": "system", 
             "content": """
Extract FoodName: mandatory, Description:Optional, Price:mandatory, Rating:Optional
...
Remember:
If you can't parse the text return N/a for all fields but do reply with any other text that's not parsed!
Each item must be separated by \n
...
Example:
user:Appetizers  HummusMade with the freshest ingredients, including chickpeas, tahini and lemon juice, resulting in a creamy and flavorful dip that's perfect for any occasion.AED 21.00
assistant:FoodName:Hummus\nDescription:Made with the freshest ingredients\nincluding chickpeas\ntahini and lemon juice, resulting in a creamy and flavorful dip that's perfect for any occasion.\nPrice:AED 21.00, Rating:N/a
""" }]

path = './all_menus'

files = [x for x in os.listdir(path) if x[-3:] == 'txt']
df = pd.DataFrame(columns=['FoodName', 'Description', 'Price', 'Rating', 'RestaurantName'])

for doc in files:
    doc_path = os.path.join(path, doc)
    print(doc_path)
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        content = ''.join(filter(lambda x: x in string.printable, content))
        split_text = content.split('Add')
        cleaned_text = []
        pattern = r"AED \d+\.\d{2}"
        for text in split_text:
            match = re.search(pattern, text)
            if match:
                cleaned_text.append(text)
        restaurant_name = cleaned_text[0].split('|')[0].strip()
        cleaned_text.pop(0)

    for content in cleaned_text[:-1]:
        messages.append({"role": "user", "content": content})
        print(f'INPUT ➡️ {content}')
        try:
            print('Atempting to connect to API')
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.1
            )
        except Exception as e:
            print(f"Connectivity issue with API, retrying attempt {i+1} out of 5")

        chat_response = completion.choices[0].message.content.strip().split('\n')
        print(f'🧠 {chat_response}')
        messages.append({"role": "assistant", "content": chat_response})
        chat_response[0] = chat_response[0].split('FoodName:')[1].strip()
        chat_response[1] = chat_response[1].split('Description:')[1].strip()
        chat_response[2] = chat_response[2].split('Price:')[1].strip()
        chat_response[3] = chat_response[3].split('Rating:')[1].strip()
        chat_response.append(restaurant_name)
        print(f'restaurnat name: {restaurant_name}')
        df = pd.concat([df, pd.DataFrame([chat_response], columns=['FoodName', 'Description', 'Price', 'Rating', 'RestaurantName'])], ignore_index=True)
        messages = messages[:1]
        
        #if messages has more than 3 items remove all but the that one
        if len(messages) > 3:
            messages = messages[0:1]
df.to_csv('menu_items.csv')