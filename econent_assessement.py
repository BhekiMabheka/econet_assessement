import json
import pandas as pd
from fastapi import FastAPI
import openai

# Provided data
dat1 = {'country': ['A', 'B', 'C'],
        'Tarrif':[0.5, 0.2, 0.3],
        'Currency': ['USD', 'USD', 'USD'],
        'Unit': ['minute', 'minute', 'minute']}

dat2 = {'country': ['A', 'B', 'C'],
        'Tarrif':[0.8, 0.9, 5.0],
        'Currency': ['USD', 'USD', 'USD'],
        'Unit': ['megabytes', 'megabytes', 'megabytes']}

# Convert dictionaries to DataFrames
data_bundle_tariff_df = pd.DataFrame(data=dat1)
voice_bundle_tariff_df = pd.DataFrame(data=dat2)


def data_bundle_tariff(country):
    # Assuming data_bundle_tariff_df is available
    row = data_bundle_tariff_df[data_bundle_tariff_df['country'] == country]
    if not row.empty:
        return json.dumps({
            "country": country,
            "tariff": row['Tarrif'].values[0],
            "currency": row['Currency'].values[0],
            "unit": row['Unit'].values[0]
        })
    else:
        return json.dumps({"error": f"Tariff information not found for {country}."})

def voice_bundle_tariff(country):
    # Assuming voice_bundle_tariff_df is available
    row = voice_bundle_tariff_df[voice_bundle_tariff_df['country'] == country]
    if not row.empty:
        return json.dumps({
            "country": country,
            "tariff": row['Tarrif'].values[0],
            "currency": row['Currency'].values[0],
            "unit": row['Unit'].values[0]
        })
    else:
        return json.dumps({"error": f"Tariff information not found for {country}."})
    

class ConversationManager:
    def __init__(self):
        self.conversation_history = []

    def add_to_history(self, user_message, model_response):
        self.conversation_history.append((user_message, model_response))

    def get_history(self):
        return self.conversation_history
    

def call_data_bundle_tariff(country, data_df):
    row = data_df[data_df['country'] == country]
    if not row.empty:
        tariff_info = {
            "tariff": row['Tarrif'].values[0],
            "currency": row['Currency'].values[0],
            "unit": row['Unit'].values[0]
        }
        return tariff_info
    else:
        return None
    

def call_voice_bundle_tariff(country, voice_df):
    row = voice_df[voice_df['country'] == country]
    if not row.empty:
        tariff_info = {
            "tariff": row['Tarrif'].values[0],
            "currency": row['Currency'].values[0],
            "unit": row['Unit'].values[0]
        }
        return tariff_info
    else:
        return None

   

def generate_response(user_input):
    response = ""
    if "data1" in user_input.lower():
        country = input("Which country? ")
        response = call_data_bundle_tariff(country, data_bundle_tariff_df)
        if response:
            response = f"Data1 Bundle Tariff for {country}: {response}"
        else:
            response = f"Sorry, I couldn't find data1 bundle tariff information for {country}."
    elif "data2" in user_input.lower():
        country = input("Which country? ")
        response = call_voice_bundle_tariff(country, voice_bundle_tariff_df)
        if response:
            response = f"Data2 Bundle Tariff for {country}: {response}"
        else:
            response = f"Sorry, I couldn't find data2 bundle tariff information for {country}."
    else:
 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant."},
                {"role": "user", "content": user_input},
            ],
        )['choices'][0]['message']['content']

    return response




app = FastAPI()

@app.post("/get_response/")
async def get_response(username: str, question: str):
    conversation_manager = ConversationManager()
    response = generate_response(question)
    conversation_manager.add_to_history(question, response)
    return {"username": username, "response": response}


