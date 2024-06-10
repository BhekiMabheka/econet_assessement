import json  
import pandas as pd  
from fastapi import FastAPI  
import openai  

# Provided data for data bundle tariffs
dat1 = {'country': ['A', 'B', 'C'],
        'Tarrif':[0.5, 0.2, 0.3],
        'Currency': ['USD', 'USD', 'USD'],
        'Unit': ['minute', 'minute', 'minute']}

# Provided data for voice bundle tariffs
dat2 = {'country': ['A', 'B', 'C'],
        'Tarrif':[0.8, 0.9, 5.0],
        'Currency': ['USD', 'USD', 'USD'],
        'Unit': ['megabytes', 'megabytes', 'megabytes']}

data_bundle_tariff_df = pd.DataFrame(data=dat1)  # Creating a DataFrame for data bundle tariffs
voice_bundle_tariff_df = pd.DataFrame(data=dat2)  # Creating a DataFrame for voice bundle tariffs


# Function to fetch data bundle tariff for a country
def data_bundle_tariff(country):
    # Finding the row corresponding to the given country
    row = data_bundle_tariff_df[data_bundle_tariff_df['country'] == country]
    if not row.empty:  # If the row is not empty (i.e., country found)
        # Return tariff information for the country in JSON format
        return json.dumps({
            "country": country,
            "tariff": row['Tarrif'].values[0],
            "currency": row['Currency'].values[0],
            "unit": row['Unit'].values[0]
        })
    else:  # If the row is empty (i.e., country not found)
        # Return error message in JSON format
        return json.dumps({"error": f"Tariff information not found for {country}."})


# Function to fetch voice bundle tariff for a country
def voice_bundle_tariff(country):
    # Finding the row corresponding to the given country
    row = voice_bundle_tariff_df[voice_bundle_tariff_df['country'] == country]
    if not row.empty:  # If the row is not empty (i.e., country found)
        # Return tariff information for the country in JSON format
        return json.dumps({
            "country": country,
            "tariff": row['Tarrif'].values[0],
            "currency": row['Currency'].values[0],
            "unit": row['Unit'].values[0]
        })
    else:  # If the row is empty (i.e., country not found)
        # Return error message in JSON format
        return json.dumps({"error": f"Tariff information not found for {country}."})
    

# Class to manage conversation history
class ConversationManager:
    def __init__(self):
        self.conversation_history = []  # Initialize conversation history as an empty list

    def add_to_history(self, user_message, model_response):
        # Method to add user message and model response to conversation history
        self.conversation_history.append((user_message, model_response))

    def get_history(self):
        return self.conversation_history  # Method to retrieve conversation history
    

# Function to call data bundle tariff
def call_data_bundle_tariff(country, data_df):
    # Finding the row corresponding to the given country
    row = data_df[data_df['country'] == country]
    if not row.empty:  # If the row is not empty (i.e., country found)
        # Constructing tariff information dictionary
        tariff_info = {
            "tariff": row['Tarrif'].values[0],
            "currency": row['Currency'].values[0],
            "unit": row['Unit'].values[0]
        }
        return tariff_info  # Return tariff information
    else:  # If the row is empty (i.e., country not found)
        return None  # Return None


# Function to call voice bundle tariff
def call_voice_bundle_tariff(country, voice_df):
    # Finding the row corresponding to the given country
    row = voice_df[voice_df['country'] == country]
    if not row.empty:  # If the row is not empty (i.e., country found)
        # Constructing tariff information dictionary
        tariff_info = {
            "tariff": row['Tarrif'].values[0],
            "currency": row['Currency'].values[0],
            "unit": row['Unit'].values[0]
        }
        return tariff_info  # Return tariff information
    else:  # If the row is empty (i.e., country not found)
        return None  # Return None


# Function to generate response
def generate_response(user_input):
    response = ""  # Initialize response variable
    if "data1" in user_input.lower():  # If user input contains "data1"
        country = input("Which country? ")  # Prompt user to input country
        response = call_data_bundle_tariff(country, data_bundle_tariff_df)  # Call function to fetch data bundle tariff
        if response:  # If response is not None (i.e., country found)
            response = f"Data1 Bundle Tariff for {country}: {response}"  # Construct response message
        else:  # If response is None (i.e., country not found)
            response = f"Sorry, I couldn't find data1 bundle tariff information for {country}."  # Construct error message
    elif "data2" in user_input.lower():  # If user input contains "data2"
        country = input("Which country? ")  # Prompt user to input country
        response = call_voice_bundle_tariff(country, voice_bundle_tariff_df)  # Call function to fetch voice bundle tariff
        if response:  # If response is not None (i.e., country found)
            response = f"Data2 Bundle Tariff for {country}: {response}"  # Construct response message
        else:  # If response is None (i.e., country not found)
            response = f"Sorry, I couldn't find data2 bundle tariff information for {country}."  # Construct error message
    else:  # If user input doesn't match "data1" or "data2"
        # Use GPT-3.5 to generate a response based on user input
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant."},  # System message
                {"role": "user", "content": user_input},  # User message
            ],
        )['choices'][0]['message']['content']  # Retrieve AI model response

    return response  # Return generated response
