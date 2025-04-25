"""
GitHub-Only Main Module

This module provides the main entry point for running the AI agent-based Deep Research system
using only the GitHub AI model.
"""

import argparse
import json
import os
from dotenv import load_dotenv
from github_orchestrator import GithubResearchWorkflow
import time
import markdown  # Import markdown library for rendering

# Load environment variables
load_dotenv()

def save_results(results, output_dir="./data"):
    """
    Save research results to a JSON file and optionally create an HTML version
    
    Args:
        results (dict): The research results
        output_dir (str): Directory to save output files
        
    Returns:
        tuple: Paths to the saved JSON and HTML files
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Generate a filename based on the query and timestamp
    timestamp = int(time.time())
    query_slug = results['query'].lower()[:30].replace(' ', '_').replace('?', '').replace('!', '')
    json_filename = f"{query_slug}_{timestamp}.json"
    html_filename = f"{query_slug}_{timestamp}.html"
    
    json_path = os.path.join(output_dir, json_filename)
    html_path = os.path.join(output_dir, html_filename)
    
    # Save the results as JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Save the results as HTML for better readability
    if results['status'] == 'completed' and results['answer'] and 'answer' in results['answer']:
        with open(html_path, 'w', encoding='utf-8') as f:
            answer_text = results['answer']['answer']
            sources = results['answer'].get('sources', [])
            
            # Define the HTML template parts
            html_header = '<!DOCTYPE html>\n<html>\n<head>\n'
            html_header += f'    <title>Research: {results["query"]}</title>\n'
            html_header += '    <meta charset="UTF-8">\n    <style>\n'
            html_header += '        body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }\n'
            html_header += '        h1 { color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }\n'
            html_header += '        h2 { color: #3498db; margin-top: 30px; }\n'
            html_header += '        .metadata { color: #7f8c8d; font-size: 0.9em; margin-bottom: 30px; }\n'
            html_header += '        .answer { background-color: #f9f9f9; padding: 20px; border-radius: 5px; }\n'
            html_header += '        .sources { margin-top: 30px; }\n'
            html_header += '        .source-item { margin-bottom: 10px; }\n'
            # Add styles for markdown content
            html_header += '        .answer code { background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px; font-family: monospace; }\n'
            html_header += '        .answer pre { background-color: #f0f0f0; padding: 10px; border-radius: 5px; overflow-x: auto; }\n'
            html_header += '        .answer blockquote { border-left: 4px solid #ccc; margin-left: 0; padding-left: 15px; color: #555; }\n'
            html_header += '        .answer img { max-width: 100%; }\n'
            html_header += '        .answer table { border-collapse: collapse; width: 100%; }\n'
            html_header += '        .answer th, .answer td { border: 1px solid #ddd; padding: 8px; }\n'
            html_header += '    </style>\n</head>\n<body>\n'
            
            # Research header and metadata
            html_body = f'    <h1>Research Results: {results["query"]}</h1>\n'
            html_body += '    <div class="metadata">\n'
            html_body += f'        <p>Generated on: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))}</p>\n'
            html_body += f'        <p>Model used: {results["answer"]["metadata"].get("model_used", "Unknown")}</p>\n'
            html_body += '    </div>\n\n'
            
            # Answer section - render markdown instead of replacing newlines with <br>
            html_body += '    <h2>Answer</h2>\n'
            html_body += '    <div class="answer">\n'
            # Convert markdown to HTML using the markdown library
            formatted_answer = markdown.markdown(answer_text, extensions=['tables', 'fenced_code'])
            html_body += f'        {formatted_answer}\n'
            html_body += '    </div>\n'
            
            # Sources section
            if sources:
                html_body += '\n    <h2>Sources</h2>\n'
                html_body += '    <div class="sources">\n'
                for i, source in enumerate(sources, 1):
                    source_str = str(source)
                    html_body += f'        <div class="source-item">\n'
                    html_body += f'            <strong>Source {i}:</strong> {source_str}\n'
                    html_body += '        </div>\n'
                html_body += '    </div>\n'
            
            # Footer
            html_footer = '</body>\n</html>'
            
            # Write the complete HTML to the file
            f.write(html_header + html_body + html_footer)
        
    print(f"Results saved to: {json_path}")
    if os.path.exists(html_path):
        print(f"HTML report saved to: {html_path}")
    
    return json_path, html_path if os.path.exists(html_path) else None

def main():
    """Main function to run the research system"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='GitHub-Only AI Agent-based Deep Research System')
    parser.add_argument('--query', '-q', type=str, help='The research query to process')
    parser.add_argument('--output', '-o', type=str, default='./data', 
                        help='Output directory for saving results')
    parser.add_argument('--full', '-f', action='store_true',
                        help='Display the full answer in the terminal')
    args = parser.parse_args()
    
    # Get query from args or prompt user
    query = args.query
    if not query:
        query = input("Enter your research query: ")
    
    # Initialize the GitHub-only workflow
    workflow = GithubResearchWorkflow()
    
    print(f"\n{'-'*50}")
    print(f"Processing query: {query}")
    print(f"Using GitHub AI model: {os.getenv('GITHUB_MODEL', 'openai/gpt-4.1')}")
    print("This may take a moment...")
    print(f"{'-'*50}\n")
    
    # Process the query
    start_time = time.time()
    results = workflow.process_query(query)
    end_time = time.time()
    
    # Print processing time
    print(f"\nQuery processed in {end_time - start_time:.2f} seconds")
    
    # Save the results
    if results['status'] == 'completed':
        json_path, html_path = save_results(results, args.output)
        
        # Print the answer with better formatting
        if results['answer'] and 'answer' in results['answer']:
            answer_text = results['answer']['answer']
            sources = results['answer'].get('sources', [])
            
            print(f"\n{'='*80}")
            print(f"RESEARCH RESULTS: {query}")
            print(f"{'='*80}")
            
            # Print metadata
            print(f"\nGenerated on: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Model used: {results['answer']['metadata'].get('model_used', 'Unknown')}")
            print(f"{'='*80}\n")
            
            # Print answer (full or summary)
            print("ANSWER:")
            print(f"{'-'*80}")
            
            if args.full:
                # Print the full answer with paragraph breaks
                print(f"\n{answer_text}\n")
            else:
                # Print a more substantial summary (first ~500 chars with paragraph detection)
                summary_length = 500
                if len(answer_text) > summary_length:
                    # Find the end of a paragraph near the summary length if possible
                    paragraph_end = answer_text.find('\n\n', summary_length//2, summary_length*2)
                    if paragraph_end != -1:
                        summary = answer_text[:paragraph_end]
                    else:
                        # If no paragraph break, find the end of a sentence
                        sentence_end = max(
                            answer_text.rfind('. ', 0, summary_length+100),
                            answer_text.rfind('! ', 0, summary_length+100),
                            answer_text.rfind('? ', 0, summary_length+100)
                        )
                        if sentence_end != -1:
                            summary = answer_text[:sentence_end+1]
                        else:
                            summary = answer_text[:summary_length] + '...'
                else:
                    summary = answer_text
                
                print(f"\n{summary}\n")
                print(f"[...Summary only. Use --full or -f to see the complete answer...]")
            
            print(f"{'-'*80}\n")
            
            # Print sources if available
            if sources and len(sources) > 0:
                print("SOURCES:")
                print(f"{'-'*80}")
                for i, source in enumerate(sources, 1):
                    print(f"{i}. {source}")
                print(f"{'-'*80}\n")
            
            # Print file paths
            print(f"Full results available in:")
            print(f"- JSON: {json_path}")
            if html_path:
                print(f"- HTML: {html_path} (Recommended for better readability)")
            print(f"{'='*80}")
        else:
            print("No answer was generated.")
    else:
        print(f"\nError processing query: {results['error']}")
        print("Please check your query and try again.")
    
if __name__ == "__main__":
    main()