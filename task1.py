from crewai import Agent, Task, Crew
from datetime import datetime

# Mock LLMAgent for the sake of this example
class LLMAgent:
    def validate(self, user_input):
        """Simulate LLM validation by checking if the input is non-empty."""
        return bool(user_input.strip())
    
    def analyze(self, user_input):
        """Simulate LLM analysis to check if the query is related to portfolio."""
        if "portfolio" in user_input.lower():
            return "portfolio"
        return "unknown"

# Portfolio Data Agent - Responsible for retrieving portfolio data
class PortfolioDataAgent:
    def __init__(self):
        self.agent = Agent(
            name="Portfolio Data Agent",
            role="Fetches and processes portfolio data securely.",
            description="This agent interacts with the database to fetch portfolio information.",
            function=self.fetch_portfolio_data
        )
    
    def fetch_portfolio_data(self):
        """Fetch portfolio data securely."""
        portfolio_data = {"portfolio": "Sample portfolio data"}
        return portfolio_data

# Scenario Input Agent - Handles user queries, validates and routes tasks
class ScenarioInputAgent:
    def __init__(self, portfolio_agent, llm_agent):
        self.agent = Agent(
            name="Scenario Input Agent",
            role="Analyzes user queries and routes them to the appropriate agents.",
            description="This agent uses LLM for processing user input and collaborates with the Portfolio Data Agent.",
            function=self.process_query
        )
        self.portfolio_agent = portfolio_agent
        self.llm_agent = llm_agent  # LLM used for validating and analyzing input
    
    def validate_input(self, user_input):
        """Use LLM to validate if input is relevant and meaningful."""
        # LLM validation for user input
        return self.llm_agent.validate(user_input)
    
    def process_query(self, user_input):
        """Analyze the query, validate it, and route to the appropriate agent."""
        # Step 1: Validate the user input
        if not self.validate_input(user_input):
            return {"task": "Invalid Input", "response": "Please provide a valid query."}
        
        # Step 2: Analyze the query using LLM (e.g., check if the query is about portfolio)
        task_result = self.llm_agent.analyze(user_input)
        
        if "portfolio" in task_result:
            # If the query is related to portfolio, route to Portfolio Data Agent
            portfolio_data = self.portfolio_agent.fetch_portfolio_data()
            return {"task": "Retrieve Portfolio Data", "data": portfolio_data}
        
        # Handle other types of queries (tax implications, etc.)
        return {"task": "Unknown Task", "response": "Unable to process this query."}

if __name__ == "__main__":
    # Initialize Portfolio Data Agent
    portfolio_agent = PortfolioDataAgent()
    
    # Initialize LLM agent for query validation and analysis
    llm_agent = LLMAgent()
    
    # Initialize the Scenario Input Agent
    scenario_agent = ScenarioInputAgent(portfolio_agent, llm_agent)
    
    # Setup the CrewAI environment with the agents
    crew = Crew(
        agents=[portfolio_agent.agent, scenario_agent.agent],
        tasks=[]
    )
    
    # Simulate some user queries
    user_queries = ["Fetch my portfolio data.", "", "Show tax implications."]
    for query in user_queries:
        result = scenario_agent.process_query(query)
        print(f"User query: '{query}' routed to: {result['task']}")
        if 'data' in result:
            print(f"Portfolio Data: {result['data']}")
