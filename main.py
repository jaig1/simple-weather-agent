#!/usr/bin/env python3
"""
Simple Weather Agent with LLM Function Calling
"""

from weather_agent import WeatherAgent


class WeatherApp:
    """Main application class"""
    
    def __init__(self):
        self.agent = None
    
    def initialize(self):
        """Initialize the weather agent"""
        print("🌤️  Weather Agent with LLM Function Calling")
        print("The LLM will decide when to call the weather tool!")
        print()
        
        try:
            self.agent = WeatherAgent()
            print("✅ Agent initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            return False
    
    def show_instructions(self):
        """Show user instructions"""
        print("💬 Ask me about the weather!")
        print("Examples:")
        print("  - 'What's the weather in London?'")
        print("  - 'How hot is it in Tokyo?'") 
        print("  - 'Is it humid in New York?'")
        print("Type 'quit' to exit.\n")
    
    def run(self):
        """Run the main chat loop"""
        if not self.initialize():
            return
        
        self.show_instructions()
        
        while True:
            try:
                # Get user input
                question = input("You: ").strip()
                
                # Exit condition
                if question.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye! 👋")
                    break
                
                # Skip empty input
                if not question:
                    continue
                
                print("🤔 LLM is thinking...")
                
                # Get answer from LLM agent
                answer = self.agent.answer_question(question)
                
                # Show response
                print(f"🤖 Agent: {answer}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")


def main():
    """Main function"""
    app = WeatherApp()
    app.run()


if __name__ == "__main__":
    main()