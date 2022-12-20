# kindle_to_pdf
Creates PDF annotations from Kindle clippings. My use case is: I have an e-book in ePub or Mobi format or a PDF created by [k2pdfopt](https://willus.com/k2pdfopt/) and read and annotate it on my kindle (where reading a scanned pdf is bothersome). Because I need citeable page numbers and want to continue working in Zotero, I now want to transfer my kindle annotations to a pdf of the book in question (for example an OCRed scan). The script does that.

# Requirements
To install the necessary modules run `python pip install pymupdf fuzzysearch`

# Usage
`python highlight.py document.pdf clippings.txt`

The first argument needs to be a PDF document of the book with a text layer. The second argument needs to be a txt-file which should only include clippings from the book. The script does not yet highlight all quotes from the Clippings (for example because it has problems with page breaks and certain special characters) but outputs all quotes that it did not highlight for manual highlighting.
