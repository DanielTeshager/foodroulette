import openai
import pandas as pd
import re
import pandas as pd
import io

csv_file = 'menu_items.csv'
df = pd.read_csv(csv_file)

#make sure price is xx.xx format anything else should be removed
df['Price'] = df['Price'].apply(lambda x: re.sub(r'[^0-9.]', '', x))
df['Price'] = df['Price'].apply(lambda x: re.sub(r'\.{2,}', '.', x))
df['Price'] = df['Price'].apply(lambda x: re.sub(r'^\.', '0.', x))
df['Price'] = df['Price'].apply(lambda x: re.sub(r'\.$', '.00', x))

#make sure pice is float
df['Price'] = df['Price'].apply(lambda x: float(x))

openai.api_key = "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"
while True:
    globals()
    messages = [{"role": "system", 
                "content": """
    There's a dataframe df that has columns ['RestaurantName', 'FoodName', 'Description', 'Price']

    Instruction 
    ...
    Interpret the english queries into python's df queries and respond with executable python code.
    Never respond in plain english. No explanation is required so please only respond in python code. 
    There query should be more tolerant to typos and misspellings, case insensitive and whitespace insensitive,
    it should also check for more tolerant equality or existence of words and phrases.

    If you dont know the answer, just respond with an empty string.

    Definition of columns:
    RestaurantName: name of the restaurant
    FoodName: name of the food item
    Description: description of the food item
    Price: price of the food item

    """ }]

    content = input("what's your query: ")

    if content == 'quit':
        exit()
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    response = completion.choices[0].message.content
    #add response to message
    data = ''
    try:
        print('trying to execute')
        print(response)
        exec(f'data={response}', globals())
        messages.append({"role":"assistant","content":response})
        print(data)
    except:
        print('I dont know the answer')
    if len(messages) > 3:
        messages = messages[:1]
