"""
Streamlit Web UI for the Weather Agent
Uses the existing modular structure without changes
"""

import streamlit as st
import json
from weather_agent import WeatherAgent
from config import Config

# Configure Streamlit page
st.set_page_config(
    page_title="Weather Agent",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class StreamlitWeatherApp:
    """Streamlit web interface for the Weather Agent"""
    
    def __init__(self):
        self.agent = None
        self.config = Config()
    
    def initialize_agent(self):
        """Initialize the weather agent (with caching)"""
        if 'agent' not in st.session_state:
            try:
                st.session_state.agent = WeatherAgent()
                st.session_state.agent_initialized = True
            except Exception as e:
                st.session_state.agent = None
                st.session_state.agent_error = str(e)
                st.session_state.agent_initialized = False
    
    def render_header(self):
        """Render the app header"""
        st.title("🌤️ Weather Agent")
        st.markdown("*Ask me about the weather in any city!*")
        
        # Show API key status
        if self.config.has_api_key():
            st.success("✅ Using real Google Gemini LLM")
        else:
            st.info("🎭 Running in mock mode (no API key)")
            with st.expander("How to add your API key"):
                st.markdown("""
                1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
                2. Create a `.env` file in your project root
                3. Add: `GOOGLE_API_KEY=your-api-key-here`
                4. Restart the Streamlit app
                """)
    
    def render_sidebar(self):
        """Render the sidebar with info and examples"""
        with st.sidebar:
            st.header("ℹ️ About")
            st.markdown("""
            This is a simple agentic application that demonstrates:
            - LLM function calling
            - Tool integration
            - Natural language processing
            """)
            
            st.header("🎯 Example Questions")
            examples = [
                "What's the weather in London?",
                "How hot is it in Tokyo?",
                "Is it humid in New York?",
                "What's the temperature in Paris?",
                "How's the weather in San Francisco?"
            ]
            
            for example in examples:
                if st.button(example, key=f"example_{hash(example)}"):
                    st.session_state.user_input = example
                    st.rerun()
            
            st.header("🏙️ Available Cities")
            st.markdown("""
            **Hardcoded data for:**
            - San Francisco (18°C, Partly cloudy)
            - New York (12°C, Sunny)  
            - London (8°C, Rainy)
            - Tokyo (22°C, Clear)
            - Paris (15°C, Cloudy)
            
            *Other cities return default pleasant weather*
            """)
    
    def render_chat_interface(self):
        """Render the main chat interface"""
        # Initialize chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "Hello! I'm your weather assistant. Ask me about the weather in any city!"
                }
            ]
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
                # Show debug info for assistant messages if in mock mode
                if (message["role"] == "assistant" and 
                    not self.config.has_api_key() and 
                    "debug_info" in message):
                    with st.expander("🔧 Debug Info (Mock Mode)"):
                        st.json(message["debug_info"])
        
        # Chat input
        if prompt := st.chat_input("Ask about the weather..."):
            self.handle_user_input(prompt)
    
    def handle_user_input(self, user_input: str):
        """Handle user input and get agent response"""
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    agent = st.session_state.agent
                    
                    # Capture debug info for mock mode
                    if not self.config.has_api_key():
                        # For mock mode, we'll capture the printed debug info
                        import io
                        import contextlib
                        
                        captured_output = io.StringIO()
                        with contextlib.redirect_stdout(captured_output):
                            response = agent.answer_question(user_input)
                        
                        debug_output = captured_output.getvalue()
                        debug_info = {"mock_output": debug_output.strip()}
                    else:
                        response = agent.answer_question(user_input)
                        debug_info = None
                    
                    # Display response
                    st.write(response)
                    
                    # Add to chat history
                    message_data = {"role": "assistant", "content": response}
                    if debug_info:
                        message_data["debug_info"] = debug_info
                    
                    st.session_state.messages.append(message_data)
                    
                    # Show debug info in mock mode
                    if debug_info and not self.config.has_api_key():
                        with st.expander("🔧 Debug Info (Mock Mode)"):
                            st.text(debug_info["mock_output"])
                
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
    
    def render_footer(self):
        """Render the footer with additional info"""
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🏗️ Architecture**")
            st.markdown("Modular design with separate classes")
        
        with col2:
            st.markdown("**🧠 LLM**")
            st.markdown("Google Gemini with function calling")
        
        with col3:
            st.markdown("**⚡ Tools**")
            st.markdown("UV package manager + Streamlit")
    
    def run(self):
        """Main function to run the Streamlit app"""
        # Initialize agent
        self.initialize_agent()
        
        # Check if agent initialized successfully
        if not st.session_state.get('agent_initialized', False):
            st.error("❌ Failed to initialize Weather Agent")
            if 'agent_error' in st.session_state:
                st.error(f"Error: {st.session_state.agent_error}")
            return
        
        # Render the UI
        self.render_header()
        self.render_sidebar()
        self.render_chat_interface()
        self.render_footer()


def main():
    """Main function"""
    app = StreamlitWeatherApp()
    app.run()


if __name__ == "__main__":
    main()