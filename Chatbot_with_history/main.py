# main.py

from chat_session import ChatSession
from gemini_bot import generate_response_gemini
from ollama_bot import generate_response_ollama

def main():
    print("🤖 Welcome to Multi-LLM CLI Chatbot!")
    print("Select backend: (1) Gemini 1.5 Pro (2) Ollama (phi3:mini)")

    choice = input("Enter 1 or 2: ").strip()
    if choice not in ("1", "2"):
        print("Invalid choice. Exiting.")
        return

    use_gemini = choice == "1"
    session = ChatSession()

    print("Type your message. Type '/reset' to clear memory. Type '/exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input == "/exit":
            print("👋 Exiting. Goodbye!")
            break
        elif user_input == "/reset":
            session.clear()
            print("🔄 Chat history cleared.")
            continue

        session.add_message("user", user_input)

        try:
            if use_gemini:
                response = generate_response_gemini(session, user_input)
            else:
                response = generate_response_ollama(session, user_input)

            print(f"{'Gemini' if use_gemini else 'Ollama'}: {response}")
            session.add_message("model", response)

        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    main()
