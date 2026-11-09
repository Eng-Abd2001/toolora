# Test report

**Status: 27 of 30 tools were tested in headless Chromium on Linux, at 1280 px and 360 px width.** PDF to Images, Compress PDF and QR Code Generator were not tested, because their libraries cannot be loaded offline. No other browser and no real phone was used.

| Tool | What was tested | Result |
|---|---|---|
| Word Counter | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| Character Counter | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| Case Converter | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| Remove Duplicate Lines | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| Text Reverser | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| Password Generator | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| UUID Generator | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| Random Number Generator | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| Lorem Ipsum Generator | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| JSON Formatter | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| Base64 Encoder / Decoder | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| URL Encoder / Decoder | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| Image Compressor | JPEG and WebP output, smaller result, wrong file type, damaged file | Passed |
| Image Resizer | Keep ratio, free resize, PNG transparency kept | Passed |
| JPG to PNG | Conversion, wrong file type | Passed |
| PNG to JPG | Transparent areas become white | Passed |
| WebP Converter | WebP to WebP, WebP to PNG | Passed |
| Image to Base64 | Prefix on and off, wrong file type | Passed |
| Image Color Picker | Two pixel colours as HEX and RGB | Passed |
| Text Diff Checker | Added and removed lines, identical texts, empty input | Passed |
| HTML Formatter | Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node) | Passed |
| QR Code Generator | Only the hidden canvas and the message shown when the library cannot load | Not tested |
| Merge PDF | Merge, reorder, single file, damaged PDF, wrong file type | Passed |
| Split PDF | Ranges 1-2 and 4- | Passed |
| Extract PDF Pages | Page order 5, 1-2; invalid ranges | Passed |
| Rotate PDF | Overlapping pages rotate once; all pages at 270 degrees | Passed |
| JPG to PDF | Page size same as image, A4 | Passed |
| PDF to Images | Only the message shown when PDF.js cannot load | Not tested |
| Compress PDF | Only the message shown when PDF.js cannot load | Not tested |
| Image Cropper | Numeric crop, 1:1 ratio, mouse drag, wrong file type | Passed |

## How it was tested

- All 71 HTML files loaded without console errors and without horizontal scrolling at 360 px and 1280 px.
- Tool interfaces were driven with Playwright: typing, uploading files, buttons and downloads. Downloaded images and PDFs were opened with Pillow and pypdf to check size, format and page order.
- The PDF tools that use pdf-lib ran against a local copy of version 1.17.1, the version the site loads from the CDN.
- The logic of the 13 text, generator and developer tools was also run in Node with valid, empty and invalid input.
- Arabic pages were checked for untranslated interface text.
- Copy and download buttons were tested on JSON Formatter only, and the clipboard only in desktop Chromium.

## Fixed during review

- Random numbers froze the page for ranges wider than 4 billion.
- The QR canvas showed before any text was entered.
- Rotating a PDF with overlapping page ranges rotated pages twice.
- The cropper could throw an error after a failed second image.
- The sitemap and canonical URLs disagreed for home pages.
- The header overflowed on narrow phones, and its links overlapped in the Arabic version.
- The theme button icon was a tiny glyph, the tool list had uneven row spacing, and the home page headline did not mention images and PDFs.

## Not tested

PDF to Images, Compress PDF and QR code generation; Firefox and Safari; real phones; the site served from a real domain with ads enabled.

## Not built yet

Nothing planned is missing. The Arabic text has not been reviewed by a native editor.
