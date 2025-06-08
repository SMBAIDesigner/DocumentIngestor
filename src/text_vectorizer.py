from sentence_transformers import SentenceTransformer

# Load a pre-trained model suitable for multiple languages, including Chinese.
# This model creates 384-dimensional vectors.
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def vectorize_text(text):
    """
    Converts a string of text into a vector embedding.

    Args:
        text (str): The input text.

    Returns:
        list[float]: A list of floats representing the vector embedding.
    """
    try:
        embedding = model.encode(text)
        return embedding.tolist()  # Convert numpy array to list for JSON serialization or DB storage
    except Exception as e:
        print(f"Error during vectorization: {e}")
        return None 