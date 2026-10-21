import json
import sys
import zipfile
from pathlib import Path

from docx import Document
from lxml import etree


def main() -> None:
    path = Path(sys.argv[1])
    doc = Document(path)
    payload = {
        "core_properties": {
            "title": doc.core_properties.title,
            "subject": doc.core_properties.subject,
            "author": doc.core_properties.author,
        },
        "paragraphs": [
            {"index": i, "style": p.style.name if p.style else None, "text": p.text}
            for i, p in enumerate(doc.paragraphs)
        ],
        "tables": [
            {
                "index": ti,
                "rows": [
                    [cell.text for cell in row.cells]
                    for row in table.rows
                ],
            }
            for ti, table in enumerate(doc.tables)
        ],
        "headers": [
            [p.text for p in section.header.paragraphs]
            for section in doc.sections
        ],
        "footers": [
            [p.text for p in section.footer.paragraphs]
            for section in doc.sections
        ],
    }
    with zipfile.ZipFile(path) as zf:
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        full_text = {}
        for name in zf.namelist():
            if name == "word/document.xml" or name.startswith("word/header") or name.startswith("word/footer"):
                root = etree.fromstring(zf.read(name))
                full_text[name] = [
                    "".join(node.xpath(".//w:t/text()", namespaces=ns))
                    for node in root.xpath(".//w:p", namespaces=ns)
                ]
        payload["all_package_paragraph_text"] = full_text
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
