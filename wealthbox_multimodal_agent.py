import json
import os
import base64
from typing import Dict, List, Optional, Union, Any

import httpx
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import Toolkit
from agno.utils.log import logger

# Wealthbox API configuration
WEALTHBOX_API_TOKEN = "9b2bae00de1641f9a119cae355f55af9"
WEALTHBOX_API_BASE_URL = "https://api.crmworkspace.com/v1"


class WealthboxTools(Toolkit):
    """Toolkit for interacting with the Wealthbox CRM API."""

    def __init__(self, api_token: str = WEALTHBOX_API_TOKEN):
        super().__init__(name="wealthbox_tools")
        self.api_token = api_token
        self.base_url = WEALTHBOX_API_BASE_URL
        self.headers = {"ACCESS_TOKEN": self.api_token}

        # Register all the methods as tools
        self.register(self.search_contacts)
        self.register(self.get_contact_details)
        self.register(self.search_tasks)
        self.register(self.search_notes)
        self.register(self.search_opportunities)
        self.register(self.search_events)

    def _make_request(self, endpoint: str, method: str = "GET", params: Dict = None, data: Dict = None) -> Dict:
        """
        Make a request to the Wealthbox API.
        
        Args:
            endpoint: API endpoint to call
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            data: Request body for POST/PUT requests
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = httpx.get(url, headers=self.headers, params=params)
            elif method.upper() == "POST":
                response = httpx.post(url, headers=self.headers, json=data)
            elif method.upper() == "PUT":
                response = httpx.put(url, headers=self.headers, json=data)
            elif method.upper() == "DELETE":
                response = httpx.delete(url, headers=self.headers)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            return {"error": f"HTTP error: {e}"}
        except Exception as e:
            logger.error(f"Error making request: {e}")
            return {"error": f"Error making request: {e}"}

    def search_contacts(self, 
                       name: Optional[str] = None, 
                       email: Optional[str] = None, 
                       phone: Optional[str] = None,
                       tags: Optional[List[str]] = None,
                       contact_type: Optional[str] = None) -> str:
        """
        Search for contacts in Wealthbox based on various criteria.
        
        Args:
            name: Name to search for (partial matches supported)
            email: Email address to search for
            phone: Phone number to search for
            tags: List of tags to filter by
            contact_type: Type of contact (Client, Past Client, Prospect, Vendor, Organization)
            
        Returns:
            JSON string with matching contacts
        """
        params = {}
        if name:
            params["name"] = name
        if email:
            params["email"] = email
        if phone:
            params["phone"] = phone
        if tags:
            params["tags"] = tags
        if contact_type:
            params["contact_type"] = contact_type
            
        response = self._make_request("contacts", params=params)
        return json.dumps(response, indent=2)

    def get_contact_details(self, contact_id: str) -> str:
        """
        Get detailed information about a specific contact.
        
        Args:
            contact_id: ID of the contact
            
        Returns:
            JSON string with contact details
        """
        response = self._make_request(f"contacts/{contact_id}")
        return json.dumps(response, indent=2)

    def search_tasks(self, 
                    resource_id: Optional[str] = None,
                    resource_type: Optional[str] = None,
                    assigned_to: Optional[str] = None) -> str:
        """
        Search for tasks in Wealthbox.
        
        Args:
            resource_id: ID of the related resource
            resource_type: Type of the related resource
            assigned_to: ID of the user the task is assigned to
            
        Returns:
            JSON string with matching tasks
        """
        params = {}
        if resource_id:
            params["resource_id"] = resource_id
        if resource_type:
            params["resource_type"] = resource_type
        if assigned_to:
            params["assigned_to"] = assigned_to
            
        response = self._make_request("tasks", params=params)
        return json.dumps(response, indent=2)

    def search_notes(self, 
                    resource_id: Optional[str] = None,
                    resource_type: Optional[str] = None) -> str:
        """
        Search for notes in Wealthbox.
        
        Args:
            resource_id: ID of the related resource
            resource_type: Type of the related resource
            
        Returns:
            JSON string with matching notes
        """
        params = {}
        if resource_id:
            params["resource_id"] = resource_id
        if resource_type:
            params["resource_type"] = resource_type
            
        response = self._make_request("notes", params=params)
        return json.dumps(response, indent=2)

    def search_opportunities(self, 
                           resource_id: Optional[str] = None,
                           resource_type: Optional[str] = None,
                           include_closed: bool = False) -> str:
        """
        Search for opportunities in Wealthbox.
        
        Args:
            resource_id: ID of the related resource
            resource_type: Type of the related resource
            include_closed: Whether to include closed opportunities
            
        Returns:
            JSON string with matching opportunities
        """
        params = {}
        if resource_id:
            params["resource_id"] = resource_id
        if resource_type:
            params["resource_type"] = resource_type
        if include_closed:
            params["include_closed"] = "true"
            
        response = self._make_request("opportunities", params=params)
        return json.dumps(response, indent=2)

    def search_events(self, 
                     resource_id: Optional[str] = None,
                     resource_type: Optional[str] = None,
                     start_date_min: Optional[str] = None,
                     start_date_max: Optional[str] = None) -> str:
        """
        Search for events in Wealthbox.
        
        Args:
            resource_id: ID of the related resource
            resource_type: Type of the related resource
            start_date_min: Minimum start date (format: YYYY-MM-DD)
            start_date_max: Maximum start date (format: YYYY-MM-DD)
            
        Returns:
            JSON string with matching events
        """
        params = {}
        if resource_id:
            params["resource_id"] = resource_id
        if resource_type:
            params["resource_type"] = resource_type
        if start_date_min:
            params["start_date_min"] = start_date_min
        if start_date_max:
            params["start_date_max"] = start_date_max
            
        response = self._make_request("events", params=params)
        return json.dumps(response, indent=2)


class WealthboxMultimodalAgent:
    """Multimodal agent for processing text, JSON, and images to find relevant records in Wealthbox."""
    
    def __init__(self):
        # Initialize the Agno agent with OpenAI model and Wealthbox tools
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            tools=[WealthboxTools()],
            description="""
            You are a financial advisor's assistant that helps find relevant client information in Wealthbox CRM.
            Your job is to analyze input (text, JSON, or images) and find the most relevant client records in Wealthbox.
            """,
            instructions="""
            1. Analyze the input to identify key information like names, emails, phone numbers, or topics.
            2. If the input is an image, carefully analyze its content for contact information, business cards, documents, etc.
            3. Use the Wealthbox tools to search for relevant records based on the identified information.
            4. If the initial search returns too many results, refine your search using additional criteria.
            5. Provide a concise summary of the most relevant records found.
            6. Include direct links to the most important records for easy access.
            
            Always prioritize accuracy over speed. If you're unsure about a match, explain your reasoning
            and provide multiple possible matches.
            """,
            markdown=True,
            show_tool_calls=True,
        )
    
    def process_text(self, text: str) -> str:
        """
        Process text input and find relevant records in Wealthbox.
        
        Args:
            text: Text input to process
            
        Returns:
            Agent's response with relevant Wealthbox records
        """
        return self.agent.run(text)
    
    def process_json(self, json_data: Dict) -> str:
        """
        Process JSON input and find relevant records in Wealthbox.
        
        Args:
            json_data: JSON data to process
            
        Returns:
            Agent's response with relevant Wealthbox records
        """
        json_text = json.dumps(json_data)
        return self.agent.run(json_text)
    
    def process_image(self, image_path: str) -> str:
        """
        Process an image and find relevant records in Wealthbox.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Agent's response with relevant Wealthbox records
        """
        # Read the image file and encode it as base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        # Create a message with the image
        message = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                }
            },
            {
                "type": "text",
                "text": "Please analyze this image and find relevant records in Wealthbox CRM."
            }
        ]
        
        # Run the agent with the image
        return self.agent.run(message)


# Example usage
if __name__ == "__main__":
    # Create the Wealthbox multimodal agent
    agent = WealthboxMultimodalAgent()
    
    # Example 1: Process text input
    text_input = """
    I just got off the phone with Kevin Anderson. He mentioned he's interested in 
    discussing retirement planning options next week. He also mentioned his wife Sarah 
    might join the call. His email is kevin.anderson@example.com.
    """
    print("\n=== Example 1: Processing Text Input ===")
    response = agent.process_text(text_input)
    print(response)
    
    # Example 2: Process JSON input
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
    print("\n=== Example 2: Processing JSON Input ===")
    response = agent.process_json(json_input)
    print(response)
    
    # Example 3: Process image (if an image file is available)
    image_path = "business_card.jpg"  # Replace with actual image path
    if os.path.exists(image_path):
        print("\n=== Example 3: Processing Image ===")
        response = agent.process_image(image_path)
        print(response)
    else:
        print(f"\n=== Example 3: Image file '{image_path}' not found ===")
        print("To process an image, place an image file at the specified path and run the script again.")