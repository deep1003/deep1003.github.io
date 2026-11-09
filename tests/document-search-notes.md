# Document risk search validation

The search uses the unchanged v10 JSON with 55 L3 categories and 592 active L4 cards. It performs local bilingual lexical retrieval with document-frequency weighting, title boosts, Korean stem/character overlap and a small synonym list. It does not run an LLM, infer incident probabilities, or establish the existence of a risk. Negation and scenario applicability need human review. No document content is transmitted or stored.

Browser verification on Chrome covered Markdown, PDF text extraction, DOCX, TXT, CSV, and a two-sheet XLSX. Each file imported successfully and the sheet labels were retained. Scanned PDFs require prior OCR. File limits are 10 MB, 100 PDF pages, and 100000 extracted characters.

Automated checks are in document-search.test.mjs. The UI renders input snippets through textContent and links candidates to canonical risk IDs. Existing taxonomy files and comment scripts remain unchanged.
