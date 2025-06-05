"""
Simple Weather Tool with hardcoded responses for LLM function calling
"""

import json


class WeatherTool:
    """A simple tool that returns hardcoded weather information"""
    
    def __init__(self):
        # Hardcoded weather data for demo purposes
        self.weather_data = {
            "san francisco": {
                "temperature": 18,
                "description": "Partly cloudy",
                "humidity": 65
            },
            "new york": {
                "temperature": 12,
                "description": "Sunny", 
                "humidity": 45
            },
            "london": {
                "temperature": 8,
                "description": "Rainy",
                "humidity": 80
            },
            "tokyo": {
                "temperature": 22,
                "description": "Clear",
                "humidity": 55
            },
            "paris": {
                "temperature": 15,
                "description": "Cloudy",
                "humidity": 70
            }
        }
    
    def get_weather(self, location: str) -> str:
        """
        Get weather for a location (hardcoded data)
        This function will be called by the LLM as a tool
        
        Args:
            location: City name
            
        Returns:
            JSON string with weather info
        """
        location_key = location.lower().strip()
        
        # Return hardcoded data if location is known
        if location_key in self.weather_data:
            data = self.weather_data[location_key]
            result = {
                "location": location.title(),
                "temperature": data["temperature"],
                "description": data["description"],
                "humidity": data["humidity"],
                "success": True
            }
        else:
            # Default response for unknown locations
            result = {
                "location": location.title(),
                "temperature": 20,
                "description": "Pleasant",
                "humidity": 60,
                "success": True,
                "note": "Using default weather data"
            }
        
        return json.dumps(result)
    
    def get_function_schema(self):
        """
        Return the function schema for LLM tool calling
        """
        return {
            "name": "get_weather",
            "description": "Get current weather information for a specific location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name to get weather for (e.g., 'London', 'New York')"
                    }
                },
                "required": ["location"]
            }
        }
    
    def extract_location_fallback(self, question: str) -> str:
        """Extract location from question (simple fallback for mock mode)"""
        question_lower = question.lower()
        
        if "in " in question_lower:
            parts = question_lower.split("in ")
            if len(parts) > 1:
                return parts[-1].replace("?", "").strip()
        
        # Check for known cities
        for city in self.weather_data.keys():
            if city in question_lower:
                return city
        
        return "San Francisco"