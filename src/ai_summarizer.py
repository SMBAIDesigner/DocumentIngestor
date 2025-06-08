import os
import requests
import json
import glob
import re
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_URL = os.getenv('OLLAMA_API_URL')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL')
MARKDOWN_DIR = os.getenv('MARKDOWN_DIR')
SUMMARIZE_DIR = os.getenv('SUMMARIZE_DIR')
SUMMARY_MAX_LENGTH = int(os.getenv('SUMMARY_MAX_LENGTH', 200))

def summarize_with_ollama(text):
    """
    Summarize the given text using the Ollama API.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The summarized text or error message.
    """

    prompt = f"""
    请将以下文档内容总结在{SUMMARY_MAX_LENGTH}字以内:
    
    {text}
    
    请使用中文回答
    """ 
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False 
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text}")
        
        response.raise_for_status() 
        
        response_data = response.json()
        summary = response_data.get("response", "").strip()
        pattern = r'<think>.*?</think>'
        output_summary = re.sub(pattern, '', summary, flags=re.DOTALL)
        
        # 再次确保摘要长度不超过限制
        return output_summary[:SUMMARY_MAX_LENGTH]

    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response status code: {e.response.status_code}")
            print(f"Response headers: {e.response.headers}")
            print(f"Response content: {e.response.text}")
        return "Error: Unable to generate summary."
    except json.JSONDecodeError as e:
        print(f"Error decoding Ollama API response JSON:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"Raw response content: {response.text}")
        return "Error: Unable to parse response from Ollama."
    except Exception as e:
        print(f"An unknown error occurred:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        return "Error: An unknown error occurred during processing."

def process_all_documents():
    """
    Read all Markdown files, generate summaries for each file, and save them to the output directory.
    """
    if not os.path.exists(SUMMARIZE_DIR):
        os.makedirs(SUMMARIZE_DIR)
        print(f"Created output directory: {SUMMARIZE_DIR}")

    markdown_files = glob.glob(os.path.join(MARKDOWN_DIR, '*.md'))
    if not markdown_files:
        print(f"No Markdown files found in directory {MARKDOWN_DIR}.")
        return

    print(f"Found {len(markdown_files)} Markdown files to process.")

    for filepath in markdown_files:
        filename = os.path.basename(filepath)
        print(f"Processing {filename}...")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print(f"File is empty, skipping: {filename}")
                continue

            summary = summarize_with_ollama(content)
            
            output_filepath = os.path.join(SUMMARIZE_DIR, filename)
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            print(f"Successfully generated summary and saved to: {output_filepath}")

        except Exception as e:
            print(f"Unknown error occurred while processing file {filename}: {e}")

if __name__ == "__main__":
    process_all_documents() 