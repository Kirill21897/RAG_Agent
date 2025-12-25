# src/ingestion/splitter.py
from langchain_text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

def get_markdown_splitter(chunk_size: int = 500, chunk_overlap: int = 50):
    # Сначала разобьём по заголовкам, потом — по символам
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return markdown_splitter, text_splitter

def split_markdown_texts(texts: list[str], chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    markdown_splitter, text_splitter = get_markdown_splitter(chunk_size, chunk_overlap)
    all_chunks = []
    
    for i, text in enumerate(texts):
        print(f"Чанкинг документа {i+1} по структуре Markdown...")
        md_chunks = markdown_splitter.split_text(text)
        final_chunks = []
        for chunk in md_chunks:
            # Делим большие секции (например, длинный параграф под заголовком)
            final_chunks.extend(text_splitter.split_text(chunk.page_content))
        print(f"   → {len(md_chunks)} секций → {len(final_chunks)} чанков")
        all_chunks.extend(final_chunks)
    return all_chunks