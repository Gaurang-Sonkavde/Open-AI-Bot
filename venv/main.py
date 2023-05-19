import openai

# Set your OpenAI API key
openai.api_key = "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"

# Define your prompt
prompt = "What is the meaning of life?"

# Generate a response using the OpenAI API
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=50,
    n=1,
    stop=None,
    temperature=0.7,
)

# Print the generated response
print(response.choices[0].text.strip())