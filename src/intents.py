# intents.py
# Define the taxonomy for the chosen brand (AppleSupport)

INTENTS = [
    {
        "name": "account_issue",
        "description": "User is having problems logging in, accessing Apple ID, iCloud account issues, or password resets."
    },
    {
        "name": "hardware_issue",
        "description": "User is reporting a physical problem with their device (iPhone, Mac, iPad), screen broken, battery drain, or unexpected shutdowns."
    },
    {
        "name": "software_issue",
        "description": "User is experiencing bugs with iOS, macOS, apps crashing, or update failing."
    },
    {
        "name": "order_and_billing",
        "description": "User has a question or issue regarding a purchase, refund, App Store billing, or order delivery."
    },
    {
        "name": "other",
        "description": "Any other issue that does not fit into the above categories."
    }
]

def get_intent_names():
    return [intent["name"] for intent in INTENTS]
