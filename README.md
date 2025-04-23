# Prompting

This repository contains some general, although perhaps opinionated prompts, as well as examples of agentic workflows.

## Wealthbox Agent with Agno

This project demonstrates an agentic workflow that processes raw text, JSON, or images and finds relevant records in Wealthbox CRM using the Agno framework.

### Overview

The Wealthbox Agent is designed to:

1. Take various types of input (text, JSON, or images)
2. Analyze the input to extract key information (names, emails, phone numbers, etc.)
3. Use the Wealthbox API to search for relevant records
4. Return a concise summary of the most relevant records found

### Components

#### WealthboxTools

A custom toolkit that provides methods for interacting with the Wealthbox API:

- `search_contacts`: Search for contacts based on name, email, phone, tags, etc.
- `get_contact_details`: Get detailed information about a specific contact
- `search_tasks`: Search for tasks related to a resource
- `search_notes`: Search for notes related to a resource
- `search_opportunities`: Search for opportunities related to a resource
- `search_events`: Search for events related to a resource

#### WealthboxAgent (Basic Version)

A wrapper class that:

1. Initializes an Agno agent with the WealthboxTools toolkit
2. Provides a method to process text or JSON input and find relevant records
3. Can process image descriptions (but not actual images)

#### WealthboxMultimodalAgent (Advanced Version)

An enhanced version that:

1. Can process actual images using GPT-4o's multimodal capabilities
2. Provides separate methods for processing text, JSON, and images
3. Uses base64 encoding to send images to the model

### Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

### Usage

#### Basic Agent (Text and JSON only)

```python
from wealthbox_agent import WealthboxAgent

# Create the Wealthbox agent
agent = WealthboxAgent()

# Process text input
text_input = "I just got off the phone with Kevin Anderson..."
response = agent.process_input(text_input)
print(response)

# Process JSON input
json_input = {"meeting_notes": {"client": "Anderson, Kevin", ...}}
response = agent.process_input(json_input)
print(response)
```

#### Multimodal Agent (Text, JSON, and Images)

```python
from wealthbox_multimodal_agent import WealthboxMultimodalAgent

# Create the Wealthbox multimodal agent
agent = WealthboxMultimodalAgent()

# Process text input
text_input = "I just got off the phone with Kevin Anderson..."
response = agent.process_text(text_input)
print(response)

# Process JSON input
json_input = {"meeting_notes": {"client": "Anderson, Kevin", ...}}
response = agent.process_json(json_input)
print(response)

# Process an image
image_path = "business_card.jpg"
response = agent.process_image(image_path)
print(response)
```

### Example Scripts

- `wealthbox_agent.py`: Basic agent implementation
- `wealthbox_multimodal_agent.py`: Advanced multimodal agent implementation
- `example_usage.py`: Examples of using the basic agent with different types of input

### Notes

- The Wealthbox API token is included in the script for demonstration purposes. In a production environment, you should store this securely (e.g., using environment variables).
- The multimodal agent requires an OpenAI API key with access to GPT-4o.
- For image processing, the image is encoded as base64 and sent to the model as part of the message.
