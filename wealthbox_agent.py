import json
import os
import re
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


class WealthboxAgent:
    """Agent for processing input and finding relevant records in Wealthbox."""
    
    def __init__(self):
        # Initialize the Agno agent with OpenAI model and Wealthbox tools
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            tools=[WealthboxTools()],
            description="""
            You are a financial advisor's assistant that helps find relevant client information in Wealthbox CRM.
            Your job is to analyze input (text, JSON, or descriptions of images) and find the most relevant
            client records in Wealthbox.
            """,
            instructions="""
            1. Analyze the input to identify key information like names, emails, phone numbers, or topics.
            2. Use the Wealthbox tools to search for relevant records based on the identified information.
            3. If the initial search returns too many results, refine your search using additional criteria.
            4. Provide a concise summary of the most relevant records found.
            5. Include direct links to the most important records for easy access.
            
            Always prioritize accuracy over speed. If you're unsure about a match, explain your reasoning
            and provide multiple possible matches.
            """,
            markdown=True,
            show_tool_calls=True,
        )
    
    def process_input(self, input_data: Union[str, Dict, Any]) -> str:
        """
        Process input data and find relevant records in Wealthbox.
        
        Args:
            input_data: Input data (text, JSON, or image description)
            
        Returns:
            Agent's response with relevant Wealthbox records
        """
        # Convert input to string if it's not already
        if isinstance(input_data, dict):
            input_text = json.dumps(input_data)
        else:
            input_text = str(input_data)
            
        # Run the agent with the input
        response = self.agent.run(input_text)
        return response


# Example usage
if __name__ == "__main__":
    # Create the Wealthbox agent
    agent = WealthboxAgent()
    
    # Example 1: Process text input
    text_input = """
    I just got off the phone with Kevin Anderson. He mentioned he's interested in 
    discussing retirement planning options next week. He also mentioned his wife Sarah 
    might join the call. His email is kevin.anderson@example.com.
    """
    print("\n=== Example 1: Processing Text Input ===")
    response = agent.process_input(text_input)
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
    response = agent.process_input(json_input)
    print(response)
    
    # Example 3: Process image description (simulating image analysis)
    image_description = """
    The image shows a business card with the following information:
    Name: Kevin Anderson
    Title: CEO, Acme Co.
    Email: kevin.anderson@example.com
    Phone: (555) 555-5555
    """
    print("\n=== Example 3: Processing Image Description ===")
    response = agent.process_input(image_description)
    print(response)