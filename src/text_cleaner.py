# """
# Text cleaning utilities for processing SOP responses.
# """
# import re
# import html


# class TextCleaner:
#     """Clean and normalize text from SOP responses."""
    
#     @staticmethod
#     def clean_text(text: str) -> str:
#         """
#         Clean and normalize text by removing HTML entities, extra whitespace,
#         and standardizing formatting.
        
#         Args:
#             text: Raw text string to clean
            
#         Returns:
#             Cleaned text string
#         """
#         if not isinstance(text, str) or not text.strip():
#             return ""
        
#         # Decode HTML entities
#         text = html.unescape(text)
        
#         # Remove HTML tags (e.g., </br>)
#         text = re.sub(r'<[^>]+>', ' ', text)
        
#         # Replace multiple spaces with single space
#         text = re.sub(r'\s+', ' ', text)
        
#         # Remove leading/trailing whitespace
#         text = text.strip()
        
#         return text
    
#     @staticmethod
#     def concatenate_sop(q1: str, q2: str, q3: str, q4: str) -> str:
#         """
#         Concatenate all SOP responses into a single text.
        
#         Args:
#             q1, q2, q3, q4: Individual question responses
            
#         Returns:
#             Concatenated and cleaned SOP text
#         """
#         responses = []
        
#         # Clean each response and add to list if not empty
#         for response in [q1, q2, q3, q4]:
#             cleaned = TextCleaner.clean_text(str(response))
#             if cleaned and cleaned.lower() != 'nan':
#                 responses.append(cleaned)
        
#         # Join all responses with double newline
#         return "\n\n".join(responses)
"""
Text utilities for processing SOP responses.
"""


class TextCleaner:
    """Concatenate SOP responses."""
    
    @staticmethod
    def concatenate_sop(q1: str, q2: str, q3: str, q4: str) -> str:
        """
        Simply concatenate all SOP responses in order.
        
        Args:
            q1, q2, q3, q4: Individual question responses
            
        Returns:
            Concatenated SOP text
        """
        responses = []
        
        # Just concatenate, no cleaning
        for response in [q1, q2, q3, q4]:
            text = str(response).strip()
            if text and text.lower() != 'nan':
                responses.append(text)
        
        # Join with double newline
        return "\n\n".join(responses)
