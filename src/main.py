"""
Main execution script for SOP Question Generator.
Processes candidates one at a time and appends to a single output file.
"""
import sys
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import time

from config import (
    INPUT_FILE,
    OUTPUT_FILE,
    COLUMNS,
    OLLAMA_MODEL,
    OLLAMA_HOST,
    PROMPT_TEMPLATE
)
from text_cleaner import TextCleaner
from ollama_generator import OllamaGenerator


def initialize_output_file():
    """Initialize the output file with a header."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("INTERVIEW QUESTIONS GENERATED FROM CANDIDATE SOPs\n")
        f.write("=" * 100 + "\n\n")
        f.write("Evaluation Focus (8 questions per candidate - 2 per SOP question):\n\n")
        f.write("a) Curiosity:\n")
        f.write("   - Does the candidate show evidence to learn new things and is curious about new knowledge?\n\n")
        f.write("b) Adaptive and Agile:\n")
        f.write("   - Does the candidate show evidence of adapting to various life situations and agility to adapt their viewpoints?\n")
        f.write("   - Does the candidate have an open mind?\n")
        f.write("   - Does the candidate think out-of-the-box?\n\n")
        f.write("c) Self and Social Awareness:\n")
        f.write("   - Does the candidate have a good understanding of their strengths and weaknesses?\n")
        f.write("   - Does the candidate show evidence to empathize and recognize other stimulus and the needs of others?\n")
        f.write("\n" + "=" * 100 + "\n\n")


def append_to_output_file(serial_no: int, spec: str, questions: str):
    """
    Append generated questions for a candidate to the output file.
    
    Args:
        serial_no: Candidate serial number
        spec: Candidate specialization
        questions: Generated interview questions
    """
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"CANDIDATE {serial_no} ({spec})\n")
        f.write("-" * 100 + "\n\n")
        f.write(questions)
        f.write("\n\n" + "=" * 100 + "\n\n")


def process_candidate(row, generator: OllamaGenerator, text_cleaner: TextCleaner) -> bool:
    """
    Process a single candidate: concatenate SOP, clean, generate questions, and append to file.
    
    Args:
        row: DataFrame row containing candidate data
        generator: OllamaGenerator instance
        text_cleaner: TextCleaner instance
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Extract candidate info
        serial_no = int(row[COLUMNS['serial_no']])
        spec = str(row[COLUMNS['spec']]).strip()
        
        # Extract and concatenate SOP responses
        q1 = str(row[COLUMNS['q1']]) if pd.notna(row[COLUMNS['q1']]) else ""
        q2 = str(row[COLUMNS['q2']]) if pd.notna(row[COLUMNS['q2']]) else ""
        q3 = str(row[COLUMNS['q3']]) if pd.notna(row[COLUMNS['q3']]) else ""
        q4 = str(row[COLUMNS['q4']]) if pd.notna(row[COLUMNS['q4']]) else ""
        
        # Concatenate and clean SOP
        sop_text = text_cleaner.concatenate_sop(q1, q2, q3, q4)
        
        # Validate SOP has content
        if not sop_text or len(sop_text.strip()) < 50:
            print(f"⚠ Skipping candidate {serial_no}: Insufficient SOP content")
            return False
        
        # Generate questions
        questions = generator.generate_questions(sop_text, PROMPT_TEMPLATE)
        
        if not questions:
            print(f"✗ Failed to generate questions for candidate {serial_no}")
            return False
        
        # Append to output file
        append_to_output_file(serial_no, spec, questions)
        
        return True
        
    except Exception as e:
        print(f"✗ Error processing candidate: {str(e)}")
        return False


def main():
    """Main execution function."""
    
    print("=" * 100)
    print("SOP INTERVIEW QUESTION GENERATOR")
    print("=" * 100)
    print()
    
    # Step 1: Initialize components
    print("Step 1: Initializing components...")
    print("-" * 100)
    
    text_cleaner = TextCleaner()
    generator = OllamaGenerator(model_name=OLLAMA_MODEL, host=OLLAMA_HOST)
    
    # Step 2: Test LLM connection
    print("\nStep 2: Testing Ollama connection...")
    print("-" * 100)
    
    if not generator.test_connection():
        print("\n✗ Failed to connect to Ollama. Please ensure:")
        print("  1. Ollama is installed and running (ollama serve)")
        print("  2. The model 'llama3.2:3b' is downloaded (ollama pull llama3.2:3b)")
        sys.exit(1)
    
    # Step 3: Load CSV data
    print("\nStep 3: Loading candidate data...")
    print("-" * 100)
    
    try:
        df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
        print(f"✓ Loaded {len(df)} candidates from {INPUT_FILE.name}")
    except Exception as e:
        print(f"✗ Error loading CSV: {str(e)}")
        sys.exit(1)
    
    # Step 4: Initialize output file
    print("\nStep 4: Initializing output file...")
    print("-" * 100)
    
    initialize_output_file()
    print(f"✓ Output file created: {OUTPUT_FILE}")
    
    # Step 5: Process candidates one by one
    print(f"\nStep 5: Processing {len(df)} candidates...")
    print("-" * 100)
    print()
    
    successful = 0
    failed = 0
    
    # Process each candidate sequentially
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing candidates"):
        success = process_candidate(row, generator, text_cleaner)
        
        if success:
            successful += 1
        else:
            failed += 1
        
        # Small delay between candidates
        time.sleep(0.3)
    
    # Step 6: Summary
    print("\n" + "=" * 100)
    print("PROCESSING COMPLETE")
    print("=" * 100)
    print(f"\n✓ Successfully processed: {successful} candidates")
    if failed > 0:
        print(f"⚠ Skipped/Failed: {failed} candidates")
    print(f"\n✓ All questions saved to: {OUTPUT_FILE}")
    print()


if __name__ == "__main__":
    main()
