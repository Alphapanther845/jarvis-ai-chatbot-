import openai
from config import apikey  # Make sure your apikey is correctly imported from your config

# Set your OpenAI API key
openai.api_key = apikey

# Function to handle chat queries
def chat(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate GPT model
        messages=[{"role": "user", "content": query}],  # Pass the user query
        max_tokens=50  # Define the maximum number of tokens in the response
    )
    
    # Get and return the AI's response content
    return response['choices'][0]['message']['content']

# Example usage
if __name__ == "__main__":
    query = input("Please enter your query: ")  # Take user input as the query
    print("Chatting...")
    response = chat(query)  # Call the chat function and pass the query
    print("Response from OpenAI:", response)  # Print
