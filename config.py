
"""
Configuration settings for the Weather Agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Simple configuration class"""
    
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = "gemini-1.5-flash"
        self.default_location = "San Francisco"
    
    def has_api_key(self) -> bool:
        """Check if Google API key is available"""
        return bool(self.google_api_key)
    
    def get_api_key(self) -> str:
        """Get the Google API key"""
        return self.google_api_key or ""