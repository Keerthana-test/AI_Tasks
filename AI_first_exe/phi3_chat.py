import ollama

def interact_with_phi3_mini(prompt_text: str) -> None:
    """
    Send a prompt to the local Ollama server running the `phi3:mini` model
    and print the model’s reply.
    """
    try:
        response = ollama.chat(
            model='phi3:mini',
            messages=[{'role': 'user', 'content': prompt_text}]
        )
        print("\nPhi‑3 Mini's Response:")
        print(response['message']['content'])
    except ollama.ResponseError as e:
        print(
            f"Error: {e}\n"
            "Make sure the Ollama server is running and the 'phi3:mini' model is pulled."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("--- Local Phi‑3 Mini Chat (type 'exit' or 'quit' to end) ---")
    while True:
        user_prompt = input("\nYou: ")
        if user_prompt.lower() in ('exit', 'quit'):
            print("Exiting. Goodbye!")
            break
        interact_with_phi3_mini(user_prompt)
