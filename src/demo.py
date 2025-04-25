"""
Demo Module

This module provides a demonstration of the AI agent-based Deep Research system.
It includes a set of sample queries and runs the research workflow on them.
"""

from orchestrator import ResearchWorkflow
from dotenv import load_dotenv
import json
import os
import argparse
from datetime import datetime

# Load environment variables
load_dotenv()

def run_demo(model_name="gpt-4o-mini", api_type="openai"):
    """
    Run a demonstration of the research system with sample queries
    
    Args:
        model_name (str): The model to use for the agents
        api_type (str): The API provider type ('openai' or 'github')
    """
    
    # Sample research queries
    sample_queries = [
        "What are the latest advancements in quantum computing?",
        "Explain the environmental impact of electric vehicles compared to traditional vehicles",
        "How is artificial intelligence being used in healthcare diagnostics?"
    ]
    
    # Create a directory for storing demo results
    demo_dir = os.path.join("..", "data", "demo")
    if not os.path.exists(demo_dir):
        os.makedirs(demo_dir)
        
    # Initialize the workflow
    workflow = ResearchWorkflow(model_name=model_name, api_type=api_type)
    
    print(f"Running demo with {model_name} model via {api_type.upper()} API")
    
    # Process each query
    results = []
    for i, query in enumerate(sample_queries, 1):
        print(f"\n[{i}/{len(sample_queries)}] Processing query: {query}")
        print("This may take a moment...")
        
        try:
            # Process the query
            query_results = workflow.process_query(query)
            results.append(query_results)
            
            # Save individual result
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = os.path.join(demo_dir, f"demo_query_{i}_{timestamp}.json")
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(query_results, f, indent=2, ensure_ascii=False)
            
            # Print summary
            print(f"Status: {query_results['status']}")
            if query_results['status'] == 'completed':
                if query_results['answer'] and 'answer' in query_results['answer']:
                    answer_text = query_results['answer']['answer']
                    summary = answer_text[:150] + ('...' if len(answer_text) > 150 else '')
                    print(f"Answer: {summary}")
                    print(f"Full result saved to: {result_file}")
            else:
                print(f"Error: {query_results['error']}")
                
        except Exception as e:
            print(f"Error processing query: {str(e)}")
    
    # Save combined results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_file = os.path.join(demo_dir, f"demo_all_results_{timestamp}.json")
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDemo completed. All results saved to: {combined_file}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Demo for AI agent-based Deep Research System')
    parser.add_argument('--model', '-m', type=str, default='gpt-4o-mini',
                        help='The model to use (default: gpt-4o-mini)')
    parser.add_argument('--api', '-a', type=str, choices=['openai', 'github'], default='openai',
                        help='API provider to use (openai or github)')
    args = parser.parse_args()
    
    run_demo(model_name=args.model, api_type=args.api)