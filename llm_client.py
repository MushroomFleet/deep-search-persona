"""
OpenRouter API Client for LLM interactions
"""
import requests
import json
from typing import List, Dict, Any, Optional
from config import Config


class OpenRouterClient:
    """Client for interacting with OpenRouter API"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        self.model = model or Config.DEFAULT_MODEL
        
        if not self.api_key:
            raise ValueError("API key is required")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to OpenRouter
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to configured model)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            API response dictionary
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/research-pipeline",  # Optional
            "X-Title": "Deep Research Pipeline"  # Optional
        }
        
        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature or Config.MODEL_TEMPERATURE,
            "max_tokens": max_tokens or Config.MAX_TOKENS,
            **kwargs
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, stream=stream)
            response.raise_for_status()
            
            if stream:
                return self._handle_stream(response)
            else:
                return response.json()
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def _handle_stream(self, response):
        """Handle streaming responses"""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]
                    if data != '[DONE]':
                        yield json.loads(data)
    
    def get_response_text(self, response: Dict[str, Any]) -> str:
        """Extract text from API response"""
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to extract response text: {str(e)}")
    
    def count_tokens(self, text: str) -> int:
        """
        Rough token count estimation
        In production, use tiktoken or the model's tokenizer
        """
        # Rough approximation: 1 token ≈ 4 characters
        return len(text) // 4
    
    def generate_with_system_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> str:
        """
        Convenient method to generate completion with system and user prompts
        
        Args:
            system_prompt: System message to set context
            user_prompt: User message/query
            **kwargs: Additional parameters
            
        Returns:
            Generated text response
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.chat_completion(messages, **kwargs)
        return self.get_response_text(response)
