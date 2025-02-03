import re
from typing import Dict, Any

class UserQueryProcessor:
    """
    A class to process user queries by extracting relevant tasks and mapping them
    to appropriate internal processing modules.
    """
    
    def __init__(self):
        self.supported_tasks = ["tax analysis", "stock trading", "backtesting", "forward testing", "visualization"]
        self.task_to_module = {
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
            "modules": [self.task_to_module[task] for task in identified_tasks]
        }
    
    def validate_query(self, user_query: str) -> bool:
        """Ensure the query meets basic structure requirements."""
        return len(user_query.split()) >= 3 and bool(re.search(r'\w+', user_query))
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process and route the user query to relevant modules."""
        if not self.validate_query(user_query):
            return {"error": "Invalid query. Please provide more details."}
        
        return self.extract_tasks(user_query)
    
    def integrate_portfolio_data(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate integration with a portfolio data system."""
        if not portfolio_data:
            return {"error": "Portfolio data is missing."}
        
        return {"message": "Portfolio data successfully processed.", "data": portfolio_data}

# Example usage
processor = UserQueryProcessor()
user_query = "I need tax analysis and stock trading insights."
response = processor.process_query(user_query)
print(response)

portfolio_data = {"stocks": ["AAPL", "GOOGL"], "balance": 50000}
integration_response = processor.integrate_portfolio_data(portfolio_data)
print(integration_response)
