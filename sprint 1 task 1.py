import re
from typing import Dict, Any

class ScenarioInputAgent:
    """
    A class to process user queries by extracting relevant tasks and routing them
    to appropriate internal processing modules.
    """
    
    def __init__(self):
        self.supported_tasks = {
            "tax analysis": "Tax Calculation Module",
            "stock trading": "Trading Signal Module",
            "backtesting": "Backtesting Module",
            "forward testing": "Live Testing Module",
            "visualization": "Data Visualization Module"
        }
    
    def extract_tasks(self, user_query: str) -> Dict[str, Any]:
        """Extract relevant tasks from user input."""
        identified_tasks = [task for task in self.supported_tasks if task in user_query.lower()]
        if not identified_tasks:
            return {"error": "No recognizable tasks found. Please refine your request."}
        
        return {
            "tasks": identified_tasks,
            "modules": [self.supported_tasks[task] for task in identified_tasks]
        }
    
    def validate_query(self, user_query: str) -> bool:
        """Ensure the query meets basic structure requirements."""
        return len(user_query.split()) >= 3 and any(char.isalnum() for char in user_query)
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process and route the user query to relevant modules."""
        if not self.validate_query(user_query):
            return {"error": "Invalid query. Please provide more details."}
        
        return self.extract_tasks(user_query)
    
    def fetch_data_from_source(self) -> Dict[str, Any]:
        """Placeholder for future integration with external data sources."""
        return {"message": "External data retrieval not yet implemented."}
    
    def integrate_portfolio_data(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate integration with a portfolio data system."""
        if not portfolio_data:
            return {"error": "Portfolio data is missing."}
        
        return {"message": "Portfolio data successfully processed.", "data": portfolio_data}

# Example usage
if __name__ == "__main__":
    agent = ScenarioInputAgent()
    user_query = "I need tax analysis and stock trading insights."
    print(agent.process_query(user_query))
    
    portfolio_data = {"stocks": ["AAPL", "GOOGL"], "balance": 50000}
    print(agent.integrate_portfolio_data(portfolio_data))
    
    print(agent.fetch_data_from_source())
