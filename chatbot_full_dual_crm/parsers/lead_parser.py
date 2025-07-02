def parse_lead(name, email, phone):
    return {
        "name": name.strip(),
        "email": email.strip(),
        "phone": phone.strip()
    }
