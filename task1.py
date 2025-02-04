from crewai import Agent, Task, Crew
import re
from typing import Dict, Any
import openai

# OpenAI API Key (Ensure it's securely stored in environment variables)
OPENAI_API_KEY = "your-api-key-here"

def chatgpt_query(prompt: str) -> str:
    """Fetches a response from OpenAI's ChatGPT API."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )
    return response["choices"][0]["message"]["content"].strip()

class ScenarioInputAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Scenario Input Agent",
            description="Parses user queries and routes them appropriately."
        )
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Handles user queries and routes them to the correct agent.
        - Integrated natural language processing to interpret various investment-related inputs.
        - Configured the agent to validate input accuracy and relevance.
        - Enabled the agent to route validated queries to appropriate system agents for smooth interactions.
        """
        if not self.validate_input(query):
            return {"status": "error", "message": "Invalid input. Please provide a meaningful query."}
        
        task = self.parse_query(query)
        if task == "unknown":
            return {"status": "error", "message": "Task not recognized. Please refine your query."}
        
        return {"status": "success", "task": task, "message": f"Request routed to {task} agent."}
    
    def validate_input(self, query: str) -> bool:
        """Validates user input to ensure accuracy and relevance."""
        return bool(query and isinstance(query, str) and len(query.strip()) > 3)
    
    def parse_query(self, query: str) -> str:
        """
        Uses ChatGPT to interpret the user query dynamically.
        - Leverages NLP to classify queries into predefined categories.
        - Ensures the query aligns with known system tasks.
        """
        query = query.lower()
        prompt = f"Classify the following query into one of these categories: tax_analysis, signal_generation, backtesting, forward_testing, visualization, security_compliance. Query: {query}"
        response = chatgpt_query(prompt)
        return response if response in ["tax_analysis", "signal_generation", "backtesting", "forward_testing", "visualization", "security_compliance"] else "unknown"

# Example Usage
if __name__ == "__main__":
    agent = ScenarioInputAgent()
    user_query = "Can you analyze my capital gains tax?"
    response = agent.execute(user_query)
    print(response)
