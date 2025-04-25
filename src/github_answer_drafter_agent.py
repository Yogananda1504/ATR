"""
Answer Drafter Agent Module - GitHub-only Version

This module defines the answer drafter agent that processes research findings
and formulates well-structured answers based on the collected information.
"""

from typing import Dict, Any, List, Optional
import json
from dotenv import load_dotenv
import os

# Import Azure AI SDK for GitHub model
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

class AnswerDrafterAgent:
    """
    Agent responsible for drafting comprehensive answers based on research findings
    (GitHub-only version)
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini", api_type: str = "github"):
        """
        Initialize the answer drafter agent with the specified model.
        
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
        
        self.model_name = self.github_model
        self.api_type = "github"  # Force GitHub API type
    
    def draft_answer(self, query: str, research_findings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Draft a comprehensive answer based on research findings
        
        Args:
            query (str): The original research query
            research_findings (Dict[str, Any]): The structured research findings
            
        Returns:
            Dict[str, Any]: The drafted answer with additional metadata
        """
        # Convert research findings to a string if it's not already
        if isinstance(research_findings, dict):
            research_str = json.dumps(research_findings)
        else:
            research_str = str(research_findings)
        
        # Generate the answer draft using the GitHub model
        response = self.github_client.complete(
            messages=[
                SystemMessage(content="""You are an expert answer drafter responsible for creating comprehensive, 
                accurate, and well-structured responses based on research findings.
                
                For each set of research findings you receive:
                1. Synthesize the key information into a coherent narrative
                2. Organize the content logically with appropriate headings and structure
                3. Cite sources appropriately when presenting specific facts or claims
                4. Ensure the answer is comprehensive but concise
                5. Use language that is clear, professional, and accessible
                
                Your goal is to transform raw research into a polished, informative response that 
                directly addresses the original query."""),
                UserMessage(content=f"""Original Query: {query}
                
                Research Findings: {research_str}
                
                Please draft a comprehensive answer based on this information.""")
            ],
            temperature=0.7,
            top_p=1.0,
            model=self.github_model
        )
        answer_content = response.choices[0].message.content
        
        # Package the answer with metadata
        return {
            "original_query": query,
            "answer": answer_content,
            "sources": research_findings.get("sources", []) if isinstance(research_findings, dict) else [],
            "metadata": {
                "model_used": self.model_name,
                "timestamp": None  # Can be filled in by the calling application
            }
        }