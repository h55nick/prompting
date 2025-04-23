from wealthbox_agent import WealthboxAgent

def run_text_example():
    """Example of processing text input."""
    agent = WealthboxAgent()
    
    text_input = """
    I just had a meeting with John Smith from ABC Financial. He's interested in our 
    wealth management services and wants to discuss investment options for his retirement.
    His email is john.smith@abcfinancial.com and his phone number is (123) 456-7890.
    He mentioned he's looking to invest around $500,000 and is particularly interested
    in ESG investments. We scheduled a follow-up meeting for next Tuesday at 2pm.
    """
    
    print("\n=== Processing Text Input ===")
    print("Input:")
    print(text_input)
    print("\nResponse:")
    response = agent.process_input(text_input)
    print(response)

def run_json_example():
    """Example of processing JSON input."""
    agent = WealthboxAgent()
    
    json_input = {
        "client_interaction": {
            "client_name": "Emily Johnson",
            "interaction_type": "Phone Call",
            "date": "2023-06-10",
            "duration_minutes": 45,
            "summary": "Discussed portfolio performance and tax planning strategies",
            "contact_info": {
                "email": "emily.johnson@example.com",
                "phone": "(987) 654-3210"
            },
            "action_items": [
                "Send updated portfolio analysis",
                "Schedule meeting with tax advisor",
                "Research municipal bond options"
            ],
            "notes": "Emily expressed concern about market volatility. She's planning to retire in 5 years and wants to ensure her portfolio is properly balanced."
        }
    }
    
    print("\n=== Processing JSON Input ===")
    print("Input:")
    print(json_input)
    print("\nResponse:")
    response = agent.process_input(json_input)
    print(response)

def run_image_description_example():
    """Example of processing an image description (simulating image analysis)."""
    agent = WealthboxAgent()
    
    image_description = """
    The image shows a handwritten note from a client meeting with the following information:
    
    Client: Robert Chen
    Company: Innovative Tech Solutions
    Email: robert.chen@innovativetech.com
    Phone: (555) 123-4567
    
    Meeting Notes:
    - Interested in setting up 401(k) for employees (approx. 50 people)
    - Currently has personal investments with competitor
    - Wants to discuss fee structure and investment options
    - Prefers conservative investment approach
    - Available for follow-up next month
    """
    
    print("\n=== Processing Image Description ===")
    print("Input:")
    print(image_description)
    print("\nResponse:")
    response = agent.process_input(image_description)
    print(response)

if __name__ == "__main__":
    print("Wealthbox Agent Examples")
    print("========================")
    
    # Run all examples
    run_text_example()
    run_json_example()
    run_image_description_example()