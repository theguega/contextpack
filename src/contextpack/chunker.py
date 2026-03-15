from typing import List

def split_into_chunks(text: str, min_words: int = 400, max_words: int = 600) -> List[str]:
    """
    Splits text into chunks of approximately 400-600 words,
    trying to avoid splitting paragraphs.
    """
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_word_count = 0

    for paragraph in paragraphs:
        paragraph_word_count = len(paragraph.split())
        
        if current_word_count + paragraph_word_count > max_words and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_word_count = 0
            
        current_chunk.append(paragraph)
        current_word_count += paragraph_word_count
        
        if current_word_count >= min_words:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_word_count = 0
            
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
        
    return chunks
