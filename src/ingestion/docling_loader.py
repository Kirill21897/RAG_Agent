# src/ingestion/docling_loader.py
import logging
from pathlib import Path
from typing import List, Tuple
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

# Отключим многословные логи
logging.getLogger("docling").setLevel(logging.WARNING)

def load_pdf_with_docling(file_path: Path) -> Tuple[str, dict]:
    """Загружает PDF через Docling 2.x, возвращает текст и метаданные."""
    print(f"Обрабатываю PDF через Docling: {file_path.name}")
    
    # Опционально: включить OCR и улучшенное распознавание таблиц
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True          # OCR для сканов
    pipeline_options.do_table_structure = True  # Точная структура таблиц
    pipeline_options.do_table_body = True   # Содержимое ячеек
    
    converter = DocumentConverter(pipeline_options=pipeline_options)
    
    try:
        # В Docling 2.x convert() возвращает ConversionResult
        result = converter.convert(file_path)
        
        # Извлекаем Document Object (DO)
        doc = result.document  # ← Это Document, не ConvertedDocument!
        
        # Экспорт в Markdown — теперь метод у document
        md_text = doc.export_to_markdown()
        
        # Статистика
        num_pages = len(doc.pages) if hasattr(doc, 'pages') else 0
        word_count = len(md_text.split())
        char_count = len(md_text)
        
        print(f"   → {num_pages} стр., {char_count:,} симв., {word_count:,} слов")
        print(f"   → Формат: Markdown (заголовки, таблицы, формулы)")
        
        # Метаданные (опционально для дальнейшего использования)
        metadata = {
            "title": getattr(doc, "title", None),
            "authors": getattr(doc, "authors", []),
            "filename": file_path.name,
            "pages": num_pages
        }
        
        return md_text, metadata

    except Exception as e:
        print(f"Ошибка Docling: {e}")
        raise

def load_all_pdfs_with_docling(raw_dir: Path) -> List[Tuple[str, dict]]:
    pdf_files = list(raw_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"В {raw_dir} нет PDF-файлов!")
        return []
    
    results = []
    for pdf_file in pdf_files:
        try:
            text, meta = load_pdf_with_docling(pdf_file)
            results.append((text, meta))
        except Exception as e:
            print(f"Пропущен {pdf_file.name}: {e}")
            continue
    return results