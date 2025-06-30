import google.generativeai as genai
genai.configure(api_key="AIzaSyA0icHYG7Ghx_Q5l7WRTOQfD_LmTaXAGvo")

model = genai.GenerativeModel("gemini-2.0-flash")

def query_gemini(messages):
    prompt = "\n".join(messages)
    response = model.generate_content(prompt)
    return response.text
