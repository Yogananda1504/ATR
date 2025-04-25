"""
Research Agent Module - GitHub-only Version

This module defines the research agent responsible for data collection and information gathering
using Tavily's search API, operating only with GitHub AI models.
"""

from typing import Dict, Any, List, Optional
import json
from langchain.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os

# Import Azure AI SDK for GitHub model
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

class ResearchAgent:
    """
    Agent responsible for conducting web research using Tavily's search API
    and collecting relevant information based on user queries (GitHub-only version).
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini", api_type: str = "github"):
        """
        Initialize the research agent with the specified model.
        
        Args:
            model_name (str): The model to use for the agent (ignored in GitHub-only version)
            api_type (str): The API provider type (only 'github' supported in this version)
        """
        # Use the model specified in the .env file
        self.github_model = os.getenv("GITHUB_MODEL", "openai/gpt-4.1")
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        self.endpoint = "https://models.github.ai/inference"
        
        # Initialize Azure SDK client for GitHub AI model
        self.github_client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.github_token),
        )
        
        self.search_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
        self.api_type = "github"  # Force GitHub API type
        
    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Perform a web search using Tavily's search API
        
        Args:
            query (str): The search query
            max_results (int): Maximum number of results to return
            
        Returns:
            Dict[str, Any]: The search results
        """
        results = self.search_tool.invoke({"query": query, "max_results": max_results})
        return results
        
    def research(self, query: str) -> Dict[str, Any]:
        """
        Conduct research on a given query
        
        Args:
            query (str): The research query
            
        Returns:
            Dict[str, Any]: Structured research findings
        """
        # First, perform the search to gather raw information
        search_results = self.search(query)
        
        # Use GitHub model to analyze and structure the search results
        response = self.github_client.complete(
            messages=[
                SystemMessage(content="""You are an expert researcher tasked with gathering comprehensive information.
                Extract key facts, data points, and insights from the search results.
                Format your research findings as structured JSON with the following fields:
                - main_findings: A list of the most important facts discovered
                - detailed_notes: More in-depth information organized by subtopic
                - sources: The sources you consulted, with URLs when available
                
                Your goal is to collect thorough, accurate, and well-organized information."""),
                UserMessage(content=f"Analyze and organize these search results about '{query}': {json.dumps(search_results)}")
            ],
            temperature=0.7,
            top_p=1.0,
            model=self.github_model
        )
        structured_research_content = response.choices[0].message.content
        
        # Extract and return the content
        try:
            # Try to extract JSON from the response
            if isinstance(structured_research_content, str):
                if "{" in structured_research_content and "}" in structured_research_content:
                    # Extract the JSON part if it's embedded in text
                    import re
                    json_match = re.search(r'({.*})', structured_research_content.replace('\n', ' '), re.DOTALL)
                    if json_match:
                        structured_research_content = json_match.group(1)
                    return json.loads(structured_research_content)
                return {"research_text": structured_research_content}
            else:
                return structured_research_content
        except (json.JSONDecodeError, AttributeError):
            # Return the raw content if JSON extraction fails
            return {"research_text": structured_research_content}