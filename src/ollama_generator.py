"""
LLM integration for generating interview questions using Ollama.
"""
import ollama
from typing import Optional


class OllamaGenerator:
    """Generate interview questions using local LLM via Ollama."""
    
    def __init__(self, model_name: str = "llama3.2:3b", host: str = "http://localhost:11434"):
        """
        Initialize the Ollama generator.
        
        Args:
            model_name: Name of the Ollama model to use
            host: Ollama server host URL
        """
        self.model_name = model_name
        self.host = host
        self.client = ollama.Client(host=host)
        
    def generate_questions(self, sop_text: str, prompt_template: str) -> Optional[str]:
        """
        Generate interview questions based on the SOP text.
        
        Args:
            sop_text: The candidate's cleaned SOP text
            prompt_template: Template for the prompt with {sop_text} placeholder
            
        Returns:
            Generated questions as a string, or None if generation fails
        """
        try:
            # Format the prompt with the SOP text
            prompt = prompt_template.format(sop_text=sop_text)
            
            # Generate response using Ollama
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.3,  # Lower temperature to reduce hallucination
                    'top_p': 0.9,
                    'num_predict': 500,
                }
            )
            
            # Extract the generated text
            generated_text = response['message']['content']
            return generated_text
            
        except Exception as e:
            print(f"Error generating questions: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test connection to Ollama server and model availability.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Simple test - try to use the model directly
            test_response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': 'Hello'
                    }
                ],
                options={
                    'num_predict': 5,
                }
            )
            
            if test_response and 'message' in test_response:
                print(f"✓ Successfully connected to Ollama")
                print(f"✓ Model '{self.model_name}' is available and responding")
                return True
            else:
                print(f"✗ Unexpected response from model")
                return False
                
        except Exception as e:
            print(f"✗ Failed to connect to Ollama or model not found: {str(e)}")
            print(f"Make sure:")
            print(f"  1. Ollama is running (ollama serve)")
            print(f"  2. Model is downloaded: ollama list")
            return False
