"""
Configuration settings for the SOP Question Generator project.
"""
from pathlib import Path

# Project root directory (aiqg)
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
INPUT_FILE = DATA_DIR / "data.csv"
OUTPUT_DIR = DATA_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "all_questions.txt"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# LLM Configuration
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_HOST = "http://localhost:11434"

# Column names from the dataset
COLUMNS = {
    'serial_no': 'Serial No',
    'spec': 'Spec',
    'q1': '1. State 10 Random Things/statements About You (each Statement Should Not Be More Than 10 Words) A Few Examples Are: </br>A. Born In An Another Country, I Might Be </br>B. If I Had A Different Set Of Parents </br>C. I Would Love To Switch Roles With </br>D. If I Could Relive One Moment',
    'q2': '2. Describe One Instance Of A Time You Significantly Contributed To Enhancing Someoneâ€™s Sense Of Inclusion In Your Professional Or Personal Community (choose Either Professional /personal ). (max 150 Words)',
    'q3': '3. Describe An Achievement, Experience, Or Realization That Led To Significant Personal Growth / Deepened Your Self-awareness. (max 150 Words)',
    'q4': '4. Describe A Situation Where You Failed. How Did You Handle This Failure?  (max 150 Words)'
}

# Prompt template
PROMPT_TEMPLATE = """You are an expert interviewer tasked with creating thoughtful interview questions based on a candidate's Statement of Purpose (SOP).

The SOP consists of 4 questions that the candidate answered. For each of the 4 SOP questions, generate exactly 2 interview questions (8 questions total) that assess the candidate based on these criteria:

a) Curiosity: Does the candidate show evidence to learn new things and is curious about new knowledge?

b) Adaptive and agile:
   - Does the candidate show evidence of adapting to various life situations and agility to adapt their viewpoints?
   - Does the candidate have an open mind?
   - Does the candidate think out-of-the-box?

c) Self and social awareness:
   - Does the candidate have a good understanding of their strengths and weaknesses?
   - Does the candidate show evidence to empathize and recognize other stimulus and the needs of others?

CRITICAL ANTI-HALLUCINATION RULES:
1. ONLY ask questions about information EXPLICITLY stated in the SOP below
2. Each question MUST reference a SPECIFIC detail, experience, or statement from the candidate's SOP
3. Begin questions with phrases like "You mentioned...", "In your response, you stated...", "You described..."
4. DO NOT ask hypothetical questions unrelated to the SOP content
5. DO NOT make assumptions about experiences, feelings, or situations not mentioned by the candidate
6. DO NOT ask generic interview questions like "Can you give an example from your past experiences" unless directly tied to specific SOP content
7. DO NOT invent details, scenarios, or contexts not present in the SOP
8. If the SOP section is too brief, ask deeper questions about what IS stated, not what could be

EXAMPLES OF WHAT NOT TO DO:
❌ "How would this skill benefit you in a team environment?" (if team environment was never mentioned)
❌ "Can you give an example from your past experiences where..." (generic, not tied to SOP)
❌ "What challenges did you face during this process?" (if challenges were not mentioned)

EXAMPLES OF GOOD QUESTIONS:
✅ "You mentioned learning to digitally sketch anime characters. What specifically drew you to this skill?"
✅ "In your response, you stated you welcomed your sister-in-law with Telugu-Marathi rituals. Can you describe what this experience taught you about cultural understanding?"

SOP:
{sop_text}

Generate 8 specific, thoughtful interview questions that probe deeper into the experiences and qualities ACTUALLY demonstrated in this SOP. Each pair of questions should be based on the corresponding SOP question and assess the criteria above.

Format your response EXACTLY as:
AI Q 1.1: [Your first question based on SOP Question 1]
AI Q 1.2: [Your second question based on SOP Question 1]
AI Q 2.1: [Your first question based on SOP Question 2]
AI Q 2.2: [Your second question based on SOP Question 2]
AI Q 3.1: [Your first question based on SOP Question 3]
AI Q 3.2: [Your second question based on SOP Question 3]
AI Q 4.1: [Your first question based on SOP Question 4]
AI Q 4.2: [Your second question based on SOP Question 4]
"""
