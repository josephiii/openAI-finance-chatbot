import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=APIKEY)

def chatbot(userInput, convoHistory=None):

    try:
        if convoHistory == None:
            convoHistory = []
        
        response = client.chat.completions.create(
            model = 'gpt-3.5-turbo',

            messages = [
                {'role': 'system', 'content': 'you are a helpful financial assistant'},
                *convoHistory,
                {'role': 'user', 'content': userInput}
            ]
        )

        return response.choices[0].message.content
    
    except Exception as error:
        print(f'there was an issue: {error}')
        return 'error'

def main():

    convoHistory = []

    print("Welcome to your Financial Assistant Chatbot! Type 'exit' to quit.")

    while True:
        userInput = input('You: ')

        if userInput.lower() == 'exit':
            break

        response = chatbot(userInput, convoHistory)
        print(f'Chatbot: {response}')

        convoHistory.append({'role': 'user', 'content': userInput})
        convoHistory.append({'role': 'assistant', 'content': response})


main()