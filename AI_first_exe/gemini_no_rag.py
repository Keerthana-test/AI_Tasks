import os
from dotenv import load_dotenv
import google.generativeai as genai
 
# 🔑 Load API Key
print("🔑 Loading API key...")
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file!")
 
print("✅ API key loaded")
 
# 🚀 Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
print("🤖 Gemini model ready")
 
# ❓ Ask question
query = "What is Lifecode Genorex and how does it operate?"
print(f"❓ Question: {query}")
 
try:
    # 📡 Send question directly to Gemini
    response = model.generate_content(query)
 
    # ✅ Check if response has text
    if hasattr(response, "text"):
        print("\n🌐 GEMINI RESPONSE (No RAG):\n")
        print(response.text)
    else:
        print("⚠️ No text returned in Gemini response!")
        print("Raw response:", response)
 
except Exception as e:
    print("❌ Error while querying Gemini:", e)