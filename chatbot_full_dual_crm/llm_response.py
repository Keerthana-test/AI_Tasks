def generate_confirmation_message(name, email, phone):
    return f"""
Hey {name}! 👋

Your details have been successfully saved in our CRM system. 🎯

📧 Email: {email}  
📱 Phone: {phone}

We’ll get back to you soon. Thanks for contacting us! 😊
    """.strip()
