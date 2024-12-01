import os
from pathlib import Path

import fitz
from dotenv import load_dotenv


def redact_text(pdf_file, text_to_redact, out_file_name):
    doc = fitz.open(pdf_file)
    for i in range(doc.page_count):
        page = doc.load_page(i)
        rl = page.search_for(text_to_redact, quads=True)

        if rl:  # Ensure results were found before proceeding
            page.add_redact_annot(rl[0])  # Add redaction annotation for the first match
            page.apply_redactions()  # Apply redactions

    doc.save(out_file_name, compression_effort=10)
    print(f"Redacted PDF saved as {out_file_name}")


def main():
    base_path = Path.joinpath(
        Path("G:\\"), Path("Meu Drive"), Path("Desafio Detox 15 dias")
    )

    for file in base_path.rglob("*.pdf"):
        file_stem_without_last_suffix = file.stem.rsplit("_", 1)[0]
        redact_text(
            file,
            os.environ.get("TEXT_TO_REDACT"),
            file.with_name(file_stem_without_last_suffix + "_compressed.pdf"),
        )
        os.remove(file)


if __name__ == "__main__":
    load_dotenv()
    main()
