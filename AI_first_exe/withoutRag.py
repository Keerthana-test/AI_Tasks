import ollama

response = ollama.chat(
    model='phi3:mini',
    messages=[
        {'role': 'user', 'content': 'what is python? explain in 3 lines'}
    ]
)
print("WITHOUT RAG:\n")
print(response['message']['content'])