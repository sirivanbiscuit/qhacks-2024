import openai

openai.api_key = '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'

def chat(prompt):
    # Use the OpenAI Chat API with GPT-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and return the assistant's reply
    reply = response['choices'][0]['message']['content']
    return reply

# Example prompt
user_prompt = "Tell me a fact about space."

# Get the assistant's reply
assistant_reply = chat(user_prompt)

# Print the response
print("User: ", user_prompt)
print("Assistant: ", assistant_reply)