class ContactManager:
    def __init__(self):
        self.contacts = {}

    def add(self, name, phone, email):
        self.contacts[name] = {"phone": phone, "email": email}

    def get(self, name):
        return self.contacts.get(name)

    def delete(self, name):
        return self.contacts.pop(name, None)


def destructure_json(data):
    return [
        {
            "name": f"{item['user']['first_name']} {item['user']['last_name']}",
            "phone": item['contacts'][0]['value'],
            "city": item['location']['city']
        }
        for item in data.get("users", [])
    ]


cm = ContactManager()
cm.add("John Doe", "1234567890", "john@example.com")
print(cm.contacts)

sample_json = {
    "users": [
        {
            "user": {"first_name": "Alice", "last_name": "Smith"},
            "contacts": [{"type": "phone", "value": "9876543210"}],
            "location": {"city": "New York"}
        }
    ]
}
print(destructure_json(sample_json))
