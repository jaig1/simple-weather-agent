"""
Simple Weather Agent using LLM with Function Calling
"""

import json
import google.generativeai as genai
from config import Config
from weather_tool import WeatherTool


class WeatherAgent:
    """A simple agent that uses LLM to make tool calls for weather questions"""
    
    def __init__(self):
        self.config = Config()
        self.weather_tool = WeatherTool()
        self.name = "Weather Assistant"
        
        # Setup LLM or mock mode
        self._setup_llm()
    
    def _setup_llm(self):
        """Setup Google Gemini LLM or use mock mode"""
        if self.config.has_api_key():
            try:
                genai.configure(api_key=self.config.get_api_key())
                self.model = genai.GenerativeModel(self.config.model_name)
                self.use_mock = False
                print("✅ Using real LLM (Gemini)")
            except Exception as e:
                print(f"⚠️  Failed to setup LLM: {e}")
                print("🎭 Falling back to mock mode")
                self.use_mock = True
                self.model = None
        else:
            print("⚠️  No GOOGLE_API_KEY found. Using mock mode.")
            self.use_mock = True
            self.model = None
    
    def answer_question(self, question: str) -> str:
        """
        Answer a weather question using LLM with function calling
        
        Args:
            question: User's weather question
            
        Returns:
            Natural language response from LLM
        """
        if self.use_mock:
            return self._mock_llm_response(question)
        
        return self._real_llm_response(question)
    
    def _real_llm_response(self, question: str) -> str:
        """Handle real LLM response with function calling"""
        try:
            # Define the function schema for the LLM
            tools = [self.weather_tool.get_function_schema()]
            
            # Create the prompt
            prompt = f"""
You are a helpful weather assistant. Answer the user's weather question by calling the get_weather function when needed.

User question: {question}
"""
            
            # Generate response with function calling
            response = self.model.generate_content(
                prompt,
                tools=tools,
                tool_config={'function_calling_config': 'AUTO'}
            )
            
            # Check if the model wants to call a function
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        # Execute the function call
                        function_name = part.function_call.name
                        function_args = dict(part.function_call.args)
                        
                        if function_name == "get_weather":
                            # Call our weather tool
                            weather_result = self.weather_tool.get_weather(
                                function_args.get("location", "")
                            )
                            
                            # Send the function result back to the model
                            function_response = genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=function_name,
                                    response={"result": weather_result}
                                )
                            )
                            
                            # Generate final response
                            final_response = self.model.generate_content([
                                genai.protos.Content(parts=[
                                    genai.protos.Part(text=prompt)
                                ]),
                                response.candidates[0].content,
                                genai.protos.Content(parts=[function_response])
                            ])
                            
                            return final_response.text.strip()
            
            # If no function call, return the direct response
            return response.text.strip()
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _mock_llm_response(self, question: str) -> str:
        """
        Mock LLM response when no API key is available
        Shows what the LLM interaction would look like
        """
        # Extract location (simple approach for demo)
        location = self.weather_tool.extract_location_fallback(question)
        
        # Simulate function call
        print(f"🔧 [Mock] LLM is calling: get_weather(location='{location}')")
        weather_data = json.loads(self.weather_tool.get_weather(location))
        print(f"🔧 [Mock] Tool returned: {weather_data}")
        
        # Simulate LLM generating natural response
        response = self._format_mock_response(weather_data, question)
        
        print(f"🤖 [Mock] LLM generated response: {response}")
        return response
    
    def _format_mock_response(self, weather_data: dict, question: str) -> str:
        """Format a natural response for mock mode"""
        temp = weather_data["temperature"]
        desc = weather_data["description"]
        loc = weather_data["location"]
        
        question_lower = question.lower()
        
        if "temperature" in question_lower or "temp" in question_lower:
            return f"The current temperature in {loc} is {temp}°C."
        elif "humid" in question_lower:
            return f"The humidity in {loc} is {weather_data['humidity']}%."
        else:
            return f"The weather in {loc} is currently {desc.lower()} with a temperature of {temp}°C."