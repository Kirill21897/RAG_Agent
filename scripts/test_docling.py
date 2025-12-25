# scripts/test_docling.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import RAW_DATA_DIR
from src.ingestion.docling_loader import load_all_pdfs_with_docling
from src.ingestion.splitter import split_markdown_texts

if __name__ == "__main__":
    print("Тест Docling-ингестии...\n")
    
    # 1. Загрузка
    results = load_all_pdfs_with_docling(RAW_DATA_DIR)
    if not results:
        exit(1)
    
    texts = [text for text, _ in results]
    
    # 2. Чанкинг
    chunks = split_markdown_texts(texts)
    
    # 3. Вывод
    print(f"\nВсего чанков: {len(chunks)}")
    print(f"\nПример структурированного чанка:\n{'─' * 60}")
    print(chunks[5][:500] + "...")
    
    # Сохраним Markdown для проверки (опционально)
    (Path(__file__).parent.parent / "data" / "processed" / "output.md").write_text(texts[0], encoding="utf-8")
    print(f"\nПример Markdown сохранён в: data/processed/output.md")