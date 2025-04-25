"""
GitHub-Only Orchestrator Module - Simplified Version

This module defines a simplified orchestrator that manages the workflow between
the GitHub-specific research agent and the answer drafter agent without using LangGraph.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from dotenv import load_dotenv
import os

# Import our GitHub-specific agent implementations
from github_research_agent import ResearchAgent
from github_answer_drafter_agent import AnswerDrafterAgent

# Load environment variables
load_dotenv()

class GithubResearchWorkflow:
    """
    GitHub-only orchestrator class that manages the workflow between research and answer drafting agents
    using a simple sequential workflow.
    """
    
    def __init__(self):
        """
        Initialize the research workflow with GitHub-specific agents
        """
        self.research_agent = ResearchAgent()
        self.answer_drafter = AnswerDrafterAgent()
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query through the complete workflow
        
        Args:
            query (str): The user's research query
            
        Returns:
            Dict[str, Any]: The final result with both research and answer
        """
        # Initialize the state
        state = {
            "query": query,
            "status": "initializing",
            "research_results": None,
            "answer": None,
            "error": None
        }
        
        try:
            # Step 1: Conduct research
            state["status"] = "researching"
            research_results = self.research_agent.research(query)
            state["research_results"] = research_results
            state["status"] = "research_completed"
            
            # Step 2: Draft answer
            state["status"] = "drafting"
            answer = self.answer_drafter.draft_answer(query, research_results)
            # Add timestamp
            answer["metadata"]["timestamp"] = datetime.now().isoformat()
            state["answer"] = answer
            state["status"] = "drafting_completed"
            
            # Step 3: Finalize
            state["status"] = "completed"
            
        except Exception as e:
            state["status"] = "error"
            state["error"] = str(e)
        
        # Return the final state
        return state