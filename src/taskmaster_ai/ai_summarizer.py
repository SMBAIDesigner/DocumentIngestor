from transformers import pipeline

def summarize_text(text, max_length=200):
    """
    Summarizes the given text using a pre-trained model.

    Args:
        text (str): The text to summarize.
        max_length (int): The maximum length of the summary in characters.

    Returns:
        str: The summarized text.
    """
    try:
        # Using a model that supports Chinese summarization
        summarizer = pipeline("summarization", model="csebuetnlp/mT5-small-sum")
        
        # The model uses max_length in terms of tokens, not characters.
        # We will use a simple heuristic to estimate token count, and then truncate.
        # A more robust solution might involve a specific Chinese tokenizer.
        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
        
        summary_text = summary[0]['summary_text']
        
        # Truncate to ensure it's under the character limit
        return summary_text[:max_length]

    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Error: Could not generate summary." 