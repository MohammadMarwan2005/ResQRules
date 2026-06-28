#!/usr/bin/env python3
"""Rasterize SARC SOP PDFs to PNG @ ~180 DPI for VISUAL extraction.

The flowchart logic lives in arrows + layout, so we READ THE IMAGE — never pdftotext.
PDFs live at the repo root and in Traumatic/ and Non-Traumatic/. Images -> build/png/.

    python rasterize.py            # rasterize all PDFs
    python rasterize.py Heimlich   # only PDFs whose path matches the substring
"""
import glob
import os
import sys

import fitz  # PyMuPDF

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "build", "png")
DPI = 180


def main(filt=None):
    os.makedirs(OUT, exist_ok=True)
    pdfs = (glob.glob(os.path.join(ROOT, "*.pdf"))
            + glob.glob(os.path.join(ROOT, "Traumatic", "*.pdf"))
            + glob.glob(os.path.join(ROOT, "Non-Traumatic", "*.pdf")))
    mat = fitz.Matrix(DPI / 72.0, DPI / 72.0)
    for p in sorted(pdfs):
        if filt and filt.lower() not in p.lower():
            continue
        doc = fitz.open(p)
        stem = os.path.splitext(os.path.basename(p))[0].replace(" ", "_")
        for i in range(doc.page_count):
            pix = doc.load_page(i).get_pixmap(matrix=mat)
            out = os.path.join(OUT, f"{stem}__p{i + 1}.png")
            pix.save(out)
            print(f"{out}  ({pix.width}x{pix.height})")
        doc.close()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
