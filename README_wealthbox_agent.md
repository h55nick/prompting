# Wealthbox Agent with Agno

This project demonstrates an agentic workflow that processes raw text, JSON, or image descriptions and finds relevant records in Wealthbox CRM using the Agno framework.

## Overview

The Wealthbox Agent is designed to:

1. Take various types of input (text, JSON, or image descriptions)
2. Analyze the input to extract key information (names, emails, phone numbers, etc.)
3. Use the Wealthbox API to search for relevant records
4. Return a concise summary of the most relevant records found

## Components

### WealthboxTools

A custom toolkit that provides methods for interacting with the Wealthbox API:

- `search_contacts`: Search for contacts based on name, email, phone, tags, etc.
- `get_contact_details`: Get detailed information about a specific contact
- `search_tasks`: Search for tasks related to a resource
- `search_notes`: Search for notes related to a resource
- `search_opportunities`: Search for opportunities related to a resource
- `search_events`: Search for events related to a resource

### WealthboxAgent

A wrapper class that:

1. Initializes an Agno agent with the WealthboxTools toolkit
2. Provides a method to process input data and find relevant records
3. Returns the agent's response with relevant Wealthbox records

## Usage

```python
from wealthbox_agent import WealthboxAgent

# Create the Wealthbox agent
agent = WealthboxAgent()

# Process text input
text_input = """
I just got off the phone with Kevin Anderson. He mentioned he's interested in 
discussing retirement planning options next week. He also mentioned his wife Sarah 
might join the call. His email is kevin.anderson@example.com.
"""
response = agent.process_input(text_input)
print(response)

# Process JSON input
json_input = {
    "meeting_notes": {
        "client": "Anderson, Kevin",
        "date": "2023-05-15",
        "topics": ["Retirement planning", "Portfolio rebalancing"],
        "action_items": [
            "Send updated financial plan",
            "Schedule follow-up in 2 weeks"
        ],
        "contact_info": {
            "email": "kevin.anderson@example.com",
            "phone": "(555) 555-5555"
        }
    }
}
response = agent.process_input(json_input)
print(response)

# Process image description (simulating image analysis)
image_description = """
The image shows a business card with the following information:
Name: Kevin Anderson
Title: CEO, Acme Co.
Email: kevin.anderson@example.com
Phone: (555) 555-5555
"""
response = agent.process_input(image_description)
print(response)
```

## Requirements

- Python 3.8+
- Agno
- httpx
- OpenAI API key (for GPT-4o)

## Installation

1. Install the required packages:

```bash
pip install agno httpx openai
```

2. Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run the example script:

```bash
python wealthbox_agent.py
```

## Extending the Agent

You can extend the agent's capabilities by:

1. Adding more methods to the WealthboxTools class to interact with additional Wealthbox API endpoints
2. Enhancing the agent's instructions to handle more complex scenarios
3. Integrating with other tools or APIs to provide additional context or functionality

## Notes

- The Wealthbox API token is included in the script for demonstration purposes. In a production environment, you should store this securely (e.g., using environment variables).
- The agent currently processes text, JSON, and image descriptions. To process actual images, you would need to integrate with an image analysis service or use a multimodal model.