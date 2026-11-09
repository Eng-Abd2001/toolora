"""Generates every HTML page, sitemap.xml, robots.txt and TEST-REPORT.md. Run: python3 build.py"""
import json, os, shutil
from html import escape as esc
os.makedirs("ar/tools", exist_ok=True)
os.makedirs("tools", exist_ok=True)

SITE = "https://toolora.example"          # replace with your real domain, then rebuild
EMAIL = "alo494374@gmail.com"
ADS = {"banner": "", "inline": "", "native": "", "footer": ""}   # paste Adsterra snippets here after approval

CATS = ["Image tools", "PDF tools", "Text tools", "Generators", "Developer tools"]
TOOLS = [
("word-counter", "Word Counter", "Text tools", "Count words, sentences, paragraphs and reading time.",
 "Paste an essay, an article draft or a product description and the counts update as you type. Besides words and characters, the tool reports sentences, paragraphs and an estimated reading time, which helps when a brief gives a target length.",
 "Type or paste into the text box. The counts appear beside it immediately; there is nothing to submit. Reading time assumes 238 words per minute, a common average for silent reading of non-fiction.",
 "Words are separated by whitespace, so “well-known” counts as one word, and text in languages written without spaces, such as Chinese or Japanese, will be undercounted."),
("character-counter", "Character Counter", "Text tools", "Check text length against limits for posts, SMS and meta tags.",
 "Many fields enforce a hard limit: 160 characters for a single SMS, roughly 60 for a search result title, 280 for a short post. This tool shows total characters, characters without spaces, lines and the UTF-8 byte size so you can check a text against whichever limit applies.",
 "Paste your text and read the figures. Compare “Characters” with the platform limit, or use “Bytes” when a database or API limits size in bytes rather than characters.",
 "Characters are counted as Unicode code points. Some emoji are built from several code points and count as more than one here, and platforms differ in how they count them."),
("case-converter", "Case Converter", "Text tools", "Change text to upper, lower, title, sentence, camel, snake or kebab case.",
 "Converts text between writing cases without retyping. Title and sentence case suit headings and copy; camelCase, snake_case and kebab-case turn a phrase into a variable name, a file name or a URL slug.",
 "Paste your text, then pick a case from the list. The result updates immediately and can be copied or saved as a .txt file.",
 "Title case capitalises every word, including small ones such as “of” and “the”, so check headings against your style guide. Camel, snake and kebab case drop punctuation and keep only letters and numbers."),
("remove-duplicate-lines", "Remove Duplicate Lines", "Text tools", "Delete repeated lines from a list and keep the first occurrence.",
 "Cleans up lists of email addresses, keywords, URLs or log entries. The first occurrence of each line is kept and the original order is preserved.",
 "Paste one item per line. Use the options to ignore capitalisation, trim spaces around each line, or remove blank lines before the comparison is made.",
 "Lines are compared exactly unless an option says otherwise, so “a@example.com” and “a@example.com ” count as different until trimming is on. The tool does not sort the list."),
("text-reverser", "Text Reverser", "Text tools", "Reverse a text by characters, by words or by line order.",
 "Offers three kinds of reversal: flip every character, reverse the order of the words within each line, or reverse the order of the lines themselves. It is handy for puzzles, quick tests and flipping a list upside down.",
 "Paste your text, choose a mode and copy the result.",
 "Character mode reverses Unicode code points. A letter stored as a base character plus a combining accent can end up with the accent on the neighbouring letter."),
("password-generator", "Password Generator", "Generators", "Create random passwords with the length and character types you choose.",
 "Passwords are generated in your browser with the Web Crypto random number generator, using rejection sampling so that no character is favoured. Every character type you select appears at least once.",
 "Set a length and the character types, then press Generate. Copy the password straight into your password manager.",
 "Some sites reject certain symbols; turn symbols off if a form refuses the result. Passwords are not stored anywhere, so copy one before you generate the next."),
("uuid-generator", "UUID Generator", "Generators", "Generate version 4 UUIDs for databases, tests and APIs.",
 "Produces random (version 4) UUIDs in the standard 8-4-4-4-12 format. It uses crypto.randomUUID where the browser provides it and builds the value from Web Crypto random numbers otherwise.",
 "Choose how many UUIDs you need, from 1 to 100, and press Generate. They are listed one per line, ready to paste into a script or a spreadsheet.",
 "Only version 4 is supported. Time-ordered versions such as v7 are not generated."),
("random-number-generator", "Random Number Generator", "Generators", "Pick random whole numbers in a range, with or without repeats.",
 "Draws one or many integers between a minimum and a maximum, both inclusive. Turn on “No repeats” for raffle-style draws where each number may appear only once.",
 "Enter the range and how many numbers you want, then press Generate.",
 "Whole numbers only, up to 1,000 per draw. Numbers come from Web Crypto, but this page is not an audited system for regulated lotteries or gambling."),
("lorem-ipsum-generator", "Lorem Ipsum Generator", "Generators", "Generate placeholder paragraphs for layouts and mockups.",
 "Builds filler paragraphs from a short Latin word list. The first paragraph opens with the traditional line; everything else is assembled at random, so each run is different.",
 "Pick 1 to 20 paragraphs and press Generate, then copy the text into your design or template.",
 "The text is meaningless filler and should be replaced before anything is published."),
("json-formatter", "JSON Formatter", "Developer tools", "Validate, pretty-print or minify JSON and see why it fails.",
 "Parses your JSON with the browser’s strict parser, then prints it with two or four spaces of indentation or as one compact line. If the input is invalid, the parser’s own error message is shown so you can find the problem.",
 "Paste JSON on the left. Choose an indent size or Minify, and the formatted result appears on the right.",
 "Strict JSON only: comments, trailing commas and single-quoted strings are rejected. Very large integers can lose precision because they are parsed as JavaScript numbers."),
("base64-encoder-decoder", "Base64 Encoder / Decoder", "Developer tools", "Convert text to Base64 and back, with full UTF-8 support.",
 "Encodes text as Base64 or decodes a Base64 string back to text. Unicode is handled as UTF-8, so accented letters and emoji survive the round trip, which the browser’s plain btoa function cannot do on its own.",
 "Choose Encode or Decode, then paste your input. Whitespace in Base64 input is ignored and URL-safe characters (- and _) are accepted.",
 "Decoding assumes the data is UTF-8 text. Binary data such as an image will produce an error."),
("url-encoder-decoder", "URL Encoder / Decoder", "Developer tools", "Percent-encode or decode URLs and query string values.",
 "Use “Encode value” for a single query parameter, “Encode full URL” to keep characters such as : / ? and & intact, or “Decode” to turn %20-style sequences back into readable text.",
 "Select a mode and paste the text. The result updates as you type.",
 "Decoding fails on malformed sequences such as a lone %. A plus sign is not converted to a space, so replace it first if the data came from a form submission."),

("image-compressor", "Image Compressor", "Image tools", "Reduce JPEG, PNG and WebP file sizes by lowering image quality.",
 "Re-encodes your images as JPEG or WebP at the quality you choose. On photos, 70 to 80 percent usually cuts the file size a lot with little visible change, and the new size is shown next to the original so you can judge the trade-off.",
 "Drop one or more images, choose JPEG or WebP and a quality level, and each compressed file appears in a list with its own download button. To try another quality, change the slider and drop the files again.",
 "Compression is lossy. PNG input is converted to JPEG or WebP, and JPEG has no transparency, so transparent areas turn white. An image that is already well compressed can come out larger; the list shows the change."),
("image-resizer", "Image Resizer", "Image tools", "Change image width and height in pixels, with or without keeping proportions.",
 "Scales images to exact pixel dimensions for upload limits, thumbnails and email. With “Keep aspect ratio” on, the image is fitted inside the width and height you give; leave one field empty to set only the other.",
 "Enter a width, a height or both, drop your images and download the resized copies. The output keeps the original format unless you pick another.",
 "Enlarging an image stretches pixels and adds no detail. With aspect ratio off and both sizes set, the image is stretched to fit. The maximum output is 16,384 pixels per side."),
("jpg-to-png", "JPG to PNG", "Image tools", "Convert JPEG photos to PNG files.",
 "Saves JPEG images as PNG, a lossless format accepted by most design and document tools. Pixels are copied exactly as the JPEG decodes them.",
 "Drop one or more .jpg or .jpeg files. Each converted PNG appears in the list with a download button.",
 "Converting does not bring back detail already lost in the JPEG, and PNG files of photos are usually much larger. JPEG has no transparency, so the PNG has none either."),
("png-to-jpg", "PNG to JPG", "Image tools", "Convert PNG images to JPEG with adjustable quality.",
 "Turns PNG files into smaller JPEG files, which suits photos and screenshots that do not need transparency. Transparent areas are filled with white.",
 "Set a quality (90 percent is a good starting point), drop your PNG files and download the JPEGs.",
 "JPEG is lossy and can blur sharp text and thin lines, so keep the PNG for logos and diagrams. Transparency is lost."),
("webp-converter", "WebP Converter", "Image tools", "Convert images to WebP, or from WebP to JPEG or PNG.",
 "Converts between WebP, JPEG and PNG. WebP files are often noticeably smaller than JPEG at similar quality, which helps page speed; converting back to JPEG or PNG helps when a program cannot open WebP.",
 "Pick the output format, set the quality for WebP or JPEG, then drop your files.",
 "An animated WebP is converted as a single still frame. Some older browsers cannot save WebP; the tool tells you when yours cannot."),
("image-to-base64", "Image to Base64", "Image tools", "Turn an image into a Base64 string or data URL for HTML, CSS and JSON.",
 "Reads an image file and produces its Base64 text, with or without the data:image prefix. Keep the prefix when pasting into an img tag or a CSS url(); remove it for APIs that expect raw Base64.",
 "Drop an image or choose a file, then copy the result. Untick the prefix box to switch formats.",
 "Base64 makes data about a third larger, so it suits small icons more than photos. Files over 5 MB are refused."),
("image-color-picker", "Image Color Picker", "Image tools", "Click anywhere on an image to read its HEX and RGB colour.",
 "Load an image, then click or tap a point to get that pixel’s colour as a HEX code and as RGB values, with a swatch so you can see what you picked.",
 "Drop an image, click the spot you want and copy the HEX or RGB value.",
 "Images larger than 1,600 pixels on the long side are shown at reduced size, and the colour is read from that smaller copy. The picker needs a mouse or touch, not the keyboard. JPEG compression means neighbouring pixels can differ slightly."),
("text-diff-checker", "Text Diff Checker", "Text tools", "Compare two texts line by line and see what was added or removed.",
 "Paste an original and a changed version, and every line is listed as unchanged, added (+) or removed (-). Useful for checking edits to a document, a config file or a list.",
 "Paste the original on the left and the changed text on the right, then press Compare. Turn on the spacing option to ignore spaces at the end of lines.",
 "The comparison works on whole lines, so a one-word edit appears as one line removed and one added. Each text is limited to roughly 2,000 lines."),
("html-formatter", "HTML Formatter", "Developer tools", "Indent messy HTML so it is readable, or minify it for production.",
 "Puts each tag on its own line and indents by nesting depth, using 2 spaces, 4 spaces or tabs. Minify removes comments and the whitespace between tags.",
 "Paste HTML, choose a format and copy the result.",
 "This is a simple formatter, not a validator, and it does not repair unclosed tags. Inline tags such as &lt;b&gt; also get their own line, whitespace inside &lt;pre&gt; is not preserved, and scripts or styles that contain a &lt; character may be split in the wrong place."),
("qr-code-generator", "QR Code Generator", "Generators", "Make a QR code from a link or text and download it as a PNG.",
 "Encodes a URL or any text into a QR code that you can download as a PNG. The code is drawn in your browser with a four-module quiet zone around it so scanners can read it.",
 "Type or paste the text, pick an error-correction level (higher levels survive more damage but make a denser code) and a size, then press Download PNG.",
 "The page loads a small open-source library from the jsDelivr CDN, so it needs a network connection. The image size is rounded so each module is a whole number of pixels. Scan the code with a phone before you print it."),

("merge-pdf", "Merge PDF", "PDF tools", "Combine several PDF files into one document in the order you choose.",
 "Joins two or more PDFs into a single file. Pages are copied as they are, so text and images stay the way they were in the originals.",
 "Add your PDFs, use Up and Down to set the order, then press Merge PDFs.",
 "Bookmarks and form fields from the original files may not carry over. Password-protected PDFs cannot be opened; remove the password first."),
("split-pdf", "Split PDF", "PDF tools", "Split a PDF into separate files by page ranges.",
 "Enter one or more page ranges and each range becomes its own PDF. For example, 1-3, 4-6, 7- turns a long document into three files.",
 "Choose a PDF, type the ranges separated by commas and press Split PDF. Each file gets its own Download button.",
 "Pages are numbered from 1, and “7-” means page 7 to the end. Files are downloaded one at a time; there is no ZIP download."),
("extract-pdf-pages", "Extract PDF Pages", "PDF tools", "Pull selected pages out of a PDF into a new file.",
 "Builds a new PDF that contains only the pages you list, in the order you list them. Useful for sending a few pages of a long report.",
 "Choose a PDF, enter pages such as 2, 5-7, 12 and press Extract pages.",
 "A page listed twice appears twice. Bookmarks and form fields from the original are not carried over."),
("rotate-pdf", "Rotate PDF", "PDF tools", "Rotate all or selected PDF pages by 90, 180 or 270 degrees.",
 "Turns sideways or upside-down pages the right way up. The rotation is added to each page’s existing rotation and saved in a new file, so your original is not changed.",
 "Choose a PDF and an angle. Leave the pages box empty to rotate every page, or enter pages such as 1, 3-5.",
 "Rotation is clockwise and is stored in the page settings, so a few viewers or print dialogs may treat it differently from a re-scanned page."),
("jpg-to-pdf", "JPG to PDF", "PDF tools", "Turn JPEG and PNG images into a single PDF.",
 "Places each image on its own page. Choose a page the same size as the image, or A4 with a margin. Images are embedded as they are, without being compressed again.",
 "Add your images, use Up and Down to set the order, pick a page size and press Create PDF.",
 "Only JPEG and PNG are supported; convert other formats first with the WebP Converter. Large photos make large PDFs."),
("pdf-to-images", "PDF to Images", "PDF tools", "Render each page of a PDF as a PNG or JPEG image.",
 "Draws every page at the resolution you choose and gives you one image per page. Handy for sharing a page where PDFs are not accepted or for placing a page in a slide.",
 "Choose a PDF, pick a format and a resolution and press Convert pages. Each page has its own download button.",
 "Up to 100 pages per run. Very high resolution on large pages needs a lot of memory and may fail on phones. Text in the images cannot be selected."),
("compress-pdf", "Compress PDF", "PDF tools", "Reduce PDF size by rebuilding pages as compressed images.",
 "Renders each page, compresses it as a JPEG at the quality and resolution you set, and builds a new PDF from those images. This can shrink scans and image-heavy files considerably.",
 "Choose a PDF, set the quality and resolution and press Compress PDF. Compare the sizes shown, and keep the original if the result is not smaller.",
 "Every page becomes a picture: text can no longer be selected or searched, links and form fields are lost, and vector graphics turn into pixels. PDFs that are mostly text often get larger. Limited to 100 pages."),

("image-cropper", "Image Cropper", "Image tools", "Select an area of an image and save just that part.",
 "Drag on the image to choose the area to keep, or type exact pixel values for X, Y, width and height. Fixed ratios such as 1:1 and 16:9 help with profile pictures, thumbnails and banners. The crop is cut from the full-resolution original, not from the preview.",
 "Choose an image and drag to select an area; drag inside the selection to move it. Adjust the numbers if you need precision, pick a format and press Crop and download.",
 "The preview is scaled down for large images, but the saved crop uses the original pixels. On a touch screen the page stays still while your finger is on the image, so use the number fields to fine-tune. JPEG output fills transparent areas with white."),
]

UI = {
 "en": {"dir": "ltr", "skip": "Skip to content", "tools": "Tools", "about": "About", "privacy": "Privacy", "terms": "Terms", "contact": "Contact", "theme": "Switch between light and dark theme", "tag": "Toolora. Free Online Tools. Fast. Simple. Secure.", "switch": "العربية", "sw_lang": "ar"},
 "ar": {"dir": "rtl", "skip": "انتقل إلى المحتوى", "tools": "الأدوات", "about": "من نحن", "privacy": "الخصوصية", "terms": "الشروط", "contact": "اتصل بنا", "theme": "التبديل بين المظهر الفاتح والداكن", "tag": "Toolora. أدوات مجانية على الإنترنت. سريعة وبسيطة وآمنة.", "switch": "English", "sw_lang": "en"},
}
PAIRS = ["index.html", "about.html", "privacy.html", "terms.html", "contact.html"]
AR_SLUGS = ["word-counter", "character-counter", "text-reverser", "remove-duplicate-lines", "password-generator", "uuid-generator", "case-converter", "random-number-generator", "lorem-ipsum-generator", "json-formatter", "base64-encoder-decoder", "url-encoder-decoder", "html-formatter", "image-compressor", "image-resizer", "jpg-to-png", "png-to-jpg", "webp-converter", "image-to-base64", "image-color-picker", "image-cropper"]
AR_SLUGS += ["merge-pdf", "split-pdf", "extract-pdf-pages", "rotate-pdf", "jpg-to-pdf", "pdf-to-images", "compress-pdf", "text-diff-checker", "qr-code-generator"]
AR_TOOLS = {f"tools/{s}.html" for s in AR_SLUGS}

def slot(n):
    return f'<aside class="ad" aria-label="Advertisement"><!-- AD SLOT: {n} -->{ADS[n]}</aside>' if ADS[n] else f"<!-- AD SLOT: {n} (empty) -->"

def anchor(c): return c.lower().replace(" ", "-")

def page(path, title, desc, body, ld=None, tool=None, lang="en"):
    r = "../" * path.count("/")
    h = "../" * (path.count("/") - 1) if lang == "ar" else r
    u = UI[lang]
    base = path[3:] if path.startswith("ar/") else path
    sw, alts = "", ""
    if base in PAIRS or base in AR_TOOLS:
        alt_rel = "../" * base.count("/") + "ar/" + base if lang == "en" else "../" * path.count("/") + base
        sw = f'<a class="lang" href="{alt_rel}" hreflang="{u["sw_lang"]}" lang="{u["sw_lang"]}">{u["switch"]}</a>'
        alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}/{p.removesuffix("index.html")}">' for l, p in (("en", base), ("ar", "ar/" + base), ("x-default", base)))
    url = f"{SITE}/{path}".removesuffix("index.html")
    ldtag = f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    attr = f' data-tool="{tool}"' if tool else ""
    html = f'''<!doctype html>
<html lang="{lang}" dir="{u["dir"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="Toolora"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
<link rel="icon" href="{r}assets/images/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{r}assets/css/style.css">
<script>try{{var t=localStorage.getItem("theme")}}catch(e){{}}document.documentElement.dataset.theme=t||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light")</script>
{ldtag}</head><body{attr}>
<a class="skip" href="#main">{u["skip"]}</a>
<header><div class="wrap"><a class="brand" href="{h}index.html"><img src="{r}assets/images/logo.svg" alt="" width="28" height="28">Toolora</a><nav aria-label="{u["tools"]}"><a href="{h}index.html#tools">{u["tools"]}</a><a href="{h}about.html">{u["about"]}</a></nav>{sw}<button id="theme" type="button" aria-label="{u["theme"]}"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><circle cx="9" cy="9" r="7" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M9 2a7 7 0 0 0 0 14z" fill="currentColor"/></svg></button></div></header>
<main id="main">{body}</main>
<footer><div class="wrap">{slot("footer")}<p>{u["tag"]}</p><p><a href="{h}about.html">{u["about"]}</a><a href="{h}privacy.html">{u["privacy"]}</a><a href="{h}terms.html">{u["terms"]}</a><a href="{h}contact.html">{u["contact"]}</a></p></div></footer>
<script src="{r}assets/js/ar.js"></script><script src="{r}assets/js/tools.js"></script><script src="{r}assets/js/custom-tools.js"></script><script src="{r}assets/js/pdf-tools.js"></script><script src="{r}assets/js/app.js"></script></body></html>'''
    open(path, "w", encoding="utf-8").write(html)

def prose(h, text): return f'<div class="wrap"><div class="prose"><h1>{h}</h1>{text}</div></div>'

pages = ["index.html"]

BADGE = {
 "image-compressor": "MIN", "image-resizer": "W×H", "jpg-to-png": "JPG", "png-to-jpg": "PNG", "webp-converter": "WBP", "image-cropper": "CRP",
 "image-to-base64": "B64", "image-color-picker": "HEX", "merge-pdf": "MRG", "split-pdf": "SPL", "extract-pdf-pages": "XTR", "rotate-pdf": "ROT",
 "jpg-to-pdf": "JPG", "pdf-to-images": "IMG", "compress-pdf": "MIN", "word-counter": "WRD", "character-counter": "CHR", "case-converter": "Aa",
 "remove-duplicate-lines": "DUP", "text-reverser": "REV", "text-diff-checker": "DIF", "password-generator": "***", "uuid-generator": "ID",
 "random-number-generator": "RND", "lorem-ipsum-generator": "LIP", "qr-code-generator": "QR", "json-formatter": "{ }",
 "base64-encoder-decoder": "B64", "url-encoder-decoder": "%20", "html-formatter": "</>"}
CLS = {"Image tools": "c-image", "PDF tools": "c-pdf", "Text tools": "c-text", "Generators": "c-gen", "Developer tools": "c-dev"}
POPULAR = ["image-compressor", "merge-pdf", "compress-pdf", "jpg-to-pdf", "pdf-to-images", "word-counter", "qr-code-generator", "password-generator"]
cat_of = {t[0]: t[2] for t in TOOLS}
by_slug = {t[0]: t for t in TOOLS}

def tile(slug, href, name, desc, cat):
    return f'<li><a class="tile {CLS[cat]}" href="{href}"><span class="badge" aria-hidden="true">{esc(BADGE[slug])}</span><div><b>{name}</b><p>{desc}</p></div></a></li>'

def directory(labels, name, desc):
    out = ""
    for c in CATS:
        items = "".join(tile(t[0], f"tools/{t[0]}.html", name(t[0]), desc(t[0]), c) for t in TOOLS if t[2] == c)
        out += f'<section class="cat {CLS[c]}" id="{anchor(c)}"><h2>{labels[c]}<small>{sum(1 for t in TOOLS if t[2] == c)}</small></h2><ul class="grid">{items}</ul></section>'
    return out

def popular(title, name, desc):
    return f'<section class="pop" id="popular"><h2>{title}</h2><ul class="grid">' + "".join(tile(s, f"tools/{s}.html", name(s), desc(s), cat_of[s]) for s in POPULAR) + "</ul></section>"

def chips(labels, aria):
    return f'<nav class="chips" aria-label="{aria}">' + "".join(f'<a class="chip {CLS[c]}" href="#{anchor(c)}">{labels[c]}</a>' for c in CATS) + "</nav>"

CATS_EN = {c: c for c in CATS}
home = f'''<section class="hero"><div class="wrap"><h1>Small, fast tools for text, images and PDFs.</h1>
<p>Compress, convert, count, generate and format. Everything runs in your browser, and the files and text you use are not sent to our servers.</p>
<input id="q" class="search" type="search" placeholder="Search tools, for example JSON or password" aria-label="Search tools" autocomplete="off">{chips(CATS_EN, "Tool categories")}</div></section>
<div class="wrap">{slot("banner")}{popular("Popular tools", lambda s: by_slug[s][1], lambda s: by_slug[s][3])}
<div id="tools">{directory(CATS_EN, lambda s: by_slug[s][1], lambda s: by_slug[s][3])}</div><p id="none" hidden>No tool matches that search. Try a shorter word.</p>
{slot("inline")}
<section><h2>Why Toolora</h2><dl class="facts">
<div><dt>Runs on your device</dt><dd>Input is processed by JavaScript in your browser tab. There is no upload step and no database.</dd></div>
<div><dt>No account</dt><dd>Open a tool and use it. Nothing to register, nothing to pay for.</dd></div>
<div><dt>Honest about limits</dt><dd>Each tool page says what it does not handle, so you know before you rely on it.</dd></div></dl></section>
<section><h2>Questions</h2>
<details><summary>Is my text sent anywhere?</summary><p>No. The tools run in your browser and your input stays on your device. Our <a href="privacy.html">privacy policy</a> covers hosting logs and advertising.</p></details>
<details><summary>Does Toolora cost anything?</summary><p>No. The site is free to use and is supported by advertising.</p></details>
<details><summary>Are there image or PDF tools?</summary><p>Yes. Image tools and PDF tools are included. The PDF tools load open-source libraries from a CDN, but your files are not uploaded.</p></details></section></div>'''
ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "Toolora", "url": SITE + "/"}
page("index.html", "Toolora – Free Online Image, PDF, Text and Developer Tools",
     "Free browser-based tools: image compressor, PDF merge, word counter, password generator, JSON formatter and more. No sign-up, and your files are not uploaded.", home, ld)

for t in TOOLS:
    slug, name, cat, short, about, how, limit = t
    rel = ([x for x in TOOLS if x[2] == cat and x[0] != slug] + [x for x in TOOLS if x[2] != cat])[:3]
    links = "".join(tile(x[0], x[0] + ".html", x[1], x[3], x[2]) for x in rel)
    body = f'''<div class="wrap {CLS[cat]}"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="../index.html#{anchor(cat)}">{cat}</a> / <span aria-current="page">{name}</span></nav>
<div class="tool-head"><span class="badge" aria-hidden="true">{esc(BADGE[slug])}</span><div><h1>{name}</h1><p class="lead">{short}</p></div></div>{slot("banner")}
<div id="tool"><p>This tool needs JavaScript. Please enable it in your browser.</p></div>{slot("inline")}
<div class="info"><section><h2>What it does</h2><p>{about}</p></section><section><h2>How to use it</h2><p>{how}</p></section><section><h2>Limits worth knowing</h2><p>{limit}</p></section></div>{slot("native")}
<section class="related"><h2>Related tools</h2><ul class="grid">{links}</ul></section></div>'''
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "description": short,
          "url": f"{SITE}/tools/{slug}.html", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    page(f"tools/{slug}.html", f"{name} Online | Toolora", f"{short} Free, no sign-up, runs in your browser.", body, ld, slug)
    pages.append(f"tools/{slug}.html")

page("about.html", "About Toolora", "Toolora is a small set of free browser-based tools for text, data and generators.", prose("About Toolora",
 "<p>Toolora is a collection of small utilities for jobs that come up again and again: counting words, cleaning a list, generating a password, checking a JSON file. Each tool does one thing, runs in your browser and says plainly what it cannot do.</p><p>The site is free and is supported by advertising. If something is wrong or missing, <a href=\"contact.html\">tell us</a>.</p>"))
page("privacy.html", "Privacy Policy | Toolora", "How Toolora handles your input, hosting logs, advertising and cookies.", prose("Privacy Policy",
 f"<p>Last updated: 9 November 2026</p><h2>Your input</h2><p>The tools run in your browser. Text you type and images you choose are processed on your device and are not sent to Toolora servers. The site has no accounts, no database and no file uploads.</p>"
 "<h2>Hosting logs</h2><p>The site is served by a static hosting provider. Like most web hosts, it may log technical data such as IP address, browser type and the pages requested. Its own privacy policy applies to that data.</p>"
 "<h2>Advertising</h2><p>Toolora may display advertisements from Adsterra. Ad networks and their partners can use cookies or similar technologies to show and measure ads, and may collect data such as IP address and device information. See Adsterra’s privacy policy for details. You can limit this through your browser settings or ad-choice tools.</p>"
 "<h2>Storage on your device</h2><p>Toolora saves your light or dark theme choice in your browser’s local storage. Nothing else is stored.</p>"
 "<h2>External resources</h2><p>Most pages load no third-party files. The QR Code Generator and the PDF tool pages load open-source libraries (qrcode-generator, pdf-lib, PDF.js) from the jsDelivr CDN, which may log the request. Advertising code, when added, loads from the ad network.</p>"
 f"<h2>Contact</h2><p>Questions about this policy: {EMAIL}</p>"))
page("terms.html", "Terms of Service | Toolora", "Terms for using Toolora’s free online tools.", prose("Terms of Service",
 "<p>Last updated: 9 November 2026</p><p>By using Toolora you agree to these terms. The tools are provided as they are, without warranty of any kind. Check results before relying on them, especially for anything with legal, financial or security consequences.</p><p>Do not use the site for unlawful purposes or to interfere with its operation. We may change or remove tools at any time. Advertisements are supplied by third parties and their appearance is not an endorsement.</p>"))
page("contact.html", "Contact Toolora", "Contact Toolora about bugs, suggestions or privacy questions.", prose("Contact",
 f"<p>Bug reports, tool suggestions and privacy questions are welcome at <a href=\"mailto:{EMAIL}\">{EMAIL}</a>.</p><p>When reporting a bug, include the tool name, your browser and what you entered, if it is not sensitive.</p>"))
page("404.html", "Page not found | Toolora", "This page does not exist.", prose("Page not found",
 '<p>The page you asked for does not exist. Try the <a href="index.html#tools">list of tools</a>.</p>'))
pages += ["about.html", "privacy.html", "terms.html", "contact.html"]


AR_CATS = {"Image tools": "أدوات الصور", "PDF tools": "أدوات PDF", "Text tools": "أدوات النصوص", "Generators": "المولّدات", "Developer tools": "أدوات المطورين"}
AR = {
 "image-compressor": ("ضاغط الصور", "تقليل حجم صور JPEG وPNG وWebP بخفض جودتها."),
 "image-resizer": ("تغيير حجم الصور", "تعديل عرض الصور وارتفاعها بالبكسل مع الحفاظ على النسبة إن أردت."),
 "jpg-to-png": ("JPG إلى PNG", "تحويل صور JPEG إلى ملفات PNG."),
 "png-to-jpg": ("PNG إلى JPG", "تحويل صور PNG إلى JPEG مع التحكم في الجودة."),
 "webp-converter": ("محوّل WebP", "التحويل إلى WebP أو منه إلى JPEG وPNG."),
 "image-cropper": ("قص الصور", "اقتطاع جزء من الصورة بتحديده على الشاشة وحفظه."),
 "image-to-base64": ("صورة إلى Base64", "تحويل الصورة إلى نص Base64 أو رابط بيانات."),
 "image-color-picker": ("منتقي الألوان من الصور", "انقر على أي نقطة في الصورة لمعرفة لونها بصيغتي HEX وRGB."),
 "merge-pdf": ("دمج ملفات PDF", "ضمّ عدة ملفات PDF في ملف واحد بالترتيب الذي تختاره."),
 "split-pdf": ("تقسيم PDF", "تقسيم ملف PDF إلى ملفات منفصلة حسب نطاقات الصفحات."),
 "extract-pdf-pages": ("استخراج صفحات PDF", "استخراج صفحات محددة من PDF في ملف جديد."),
 "rotate-pdf": ("تدوير PDF", "تدوير كل الصفحات أو بعضها بزاوية 90 أو 180 أو 270 درجة."),
 "jpg-to-pdf": ("JPG إلى PDF", "تحويل صور JPEG وPNG إلى ملف PDF واحد."),
 "pdf-to-images": ("PDF إلى صور", "تحويل كل صفحة من PDF إلى صورة PNG أو JPEG."),
 "compress-pdf": ("ضغط PDF", "تقليل حجم PDF بإعادة بناء الصفحات كصور مضغوطة."),
 "word-counter": ("عدّاد الكلمات", "عدّ الكلمات والجمل والفقرات ومدة القراءة."),
 "character-counter": ("عدّاد الأحرف", "قياس طول النص مقابل حدود المنشورات والرسائل القصيرة."),
 "case-converter": ("محوّل حالة الأحرف", "تحويل النص اللاتيني إلى أحرف كبيرة أو صغيرة أو بصيغ camelCase وsnake_case."),
 "remove-duplicate-lines": ("حذف الأسطر المكررة", "حذف الأسطر المتكررة من قائمة مع إبقاء أول ظهور."),
 "text-reverser": ("عكس النص", "عكس النص بالأحرف أو بالكلمات أو بترتيب الأسطر."),
 "text-diff-checker": ("مقارنة النصوص", "مقارنة نصين سطرًا بسطر ومعرفة المضاف والمحذوف."),
 "password-generator": ("مولّد كلمات المرور", "إنشاء كلمات مرور عشوائية بالطول وأنواع الأحرف التي تختارها."),
 "uuid-generator": ("مولّد UUID", "إنشاء معرّفات UUID من الإصدار 4 لقواعد البيانات والاختبارات."),
 "random-number-generator": ("مولّد الأرقام العشوائية", "اختيار أعداد صحيحة عشوائية ضمن نطاق، مع التكرار أو بدونه."),
 "lorem-ipsum-generator": ("مولّد نص Lorem Ipsum", "إنشاء فقرات نصية تجريبية للتصاميم والنماذج."),
 "qr-code-generator": ("مولّد رمز QR", "إنشاء رمز QR من رابط أو نص وتنزيله بصيغة PNG."),
 "json-formatter": ("منسّق JSON", "التحقق من JSON وتنسيقه أو ضغطه ومعرفة موضع الخطأ."),
 "base64-encoder-decoder": ("ترميز Base64 وفك ترميزه", "تحويل النص إلى Base64 وبالعكس مع دعم UTF-8 كاملًا."),
 "url-encoder-decoder": ("ترميز الروابط وفك ترميزها", "ترميز الروابط وقيم الاستعلام بالنسبة المئوية أو فك ترميزها."),
 "html-formatter": ("منسّق HTML", "تنسيق شيفرة HTML المبعثرة أو ضغطها للنشر."),
}
assert set(AR) == {t[0] for t in TOOLS}
ar_home = f'''<section class="hero"><div class="wrap"><h1>أدوات صغيرة وسريعة للنصوص والصور وملفات PDF.</h1>
<p>عدّ، حوّل، أنشئ، ونسّق. كل شيء يعمل داخل متصفحك، وما تُدخله لا يُرسل إلى خوادمنا.</p>
<input id="q" class="search" type="search" placeholder="ابحث عن أداة، مثل PDF أو كلمة المرور" aria-label="ابحث عن أداة" autocomplete="off">{chips(AR_CATS, "فئات الأدوات")}</div></section>
<div class="wrap">{slot("banner")}{popular("الأكثر استخدامًا", lambda s: AR[s][0], lambda s: AR[s][1])}
<div id="tools">{directory(AR_CATS, lambda s: AR[s][0], lambda s: AR[s][1])}</div><p id="none" hidden>لا توجد أداة تطابق بحثك. جرّب كلمة أقصر.</p>
{slot("inline")}
<section><h2>لماذا Toolora</h2><dl class="facts">
<div><dt>تعمل على جهازك</dt><dd>تُعالَج مدخلاتك بواسطة JavaScript داخل علامة تبويب المتصفح. لا رفع للملفات ولا قاعدة بيانات.</dd></div>
<div><dt>بلا حساب</dt><dd>افتح الأداة واستخدمها. لا تسجيل ولا دفع.</dd></div>
<div><dt>صريحة بشأن حدودها</dt><dd>توضح كل صفحة أداة ما لا تستطيع فعله، لتعرف ذلك قبل أن تعتمد عليها.</dd></div></dl></section>
<section><h2>أسئلة شائعة</h2>
<details><summary>هل يُرسل نصي أو ملفاتي إلى أي مكان؟</summary><p>لا. تعمل الأدوات داخل متصفحك وتبقى مدخلاتك على جهازك. وتغطي <a href="privacy.html">سياسة الخصوصية</a> سجلات الاستضافة والإعلانات.</p></details>
<details><summary>هل Toolora مجاني؟</summary><p>نعم. الموقع مجاني ويُموَّل بالإعلانات.</p></details>
<details><summary>هل توجد أدوات للصور وملفات PDF؟</summary><p>نعم. أدوات PDF تحمّل مكتبات مفتوحة المصدر من شبكة توصيل محتوى، لكن ملفاتك لا تُرفع.</p></details></section></div>'''
page("ar/index.html", "Toolora – أدوات مجانية للنصوص والصور وملفات PDF",
     "أدوات مجانية تعمل داخل المتصفح: ضغط الصور ودمج PDF وعدّ الكلمات وتوليد كلمات المرور وغيرها. بلا تسجيل، ولا تُرفع بياناتك.", ar_home,
     {"@context": "https://schema.org", "@type": "WebSite", "name": "Toolora", "url": SITE + "/ar/", "inLanguage": "ar"}, lang="ar")
page("ar/about.html", "من نحن | Toolora", "Toolora مجموعة أدوات مجانية تعمل داخل المتصفح للنصوص والبيانات والصور وملفات PDF.", prose("من نحن",
 "<p>Toolora مجموعة من الأدوات الصغيرة لمهام تتكرر كثيرًا: عدّ الكلمات، وتنظيف قائمة، وتوليد كلمة مرور، وفحص ملف JSON، وضغط الصور، ودمج ملفات PDF. كل أداة تؤدي مهمة واحدة، وتعمل داخل متصفحك، وتوضح بصراحة ما لا تستطيع فعله.</p><p>الموقع مجاني ويُموَّل بالإعلانات. وإن لاحظت خطأً أو نقصًا فـ<a href=\"contact.html\">راسلنا</a>.</p>"), lang="ar")
page("ar/privacy.html", "سياسة الخصوصية | Toolora", "كيف يتعامل Toolora مع مدخلاتك وسجلات الاستضافة والإعلانات وملفات تعريف الارتباط.", prose("سياسة الخصوصية",
 "<p>آخر تحديث: 9 نوفمبر 2026</p><h2>مدخلاتك</h2><p>تعمل الأدوات داخل متصفحك. النصوص التي تكتبها أو تلصقها، والصور والملفات التي تختارها، تُعالَج على جهازك ولا تُرسل إلى خوادم Toolora. لا يوجد في الموقع حسابات ولا قاعدة بيانات ولا رفع للملفات.</p>"
 "<h2>سجلات الاستضافة</h2><p>يُقدَّم الموقع عبر مزوّد استضافة ثابتة. وكما تفعل معظم مواقع الويب، قد يسجّل المزوّد بيانات تقنية مثل عنوان IP ونوع المتصفح والصفحات المطلوبة. وتسري سياسة الخصوصية الخاصة بالمزوّد على هذه البيانات.</p>"
 "<h2>الإعلانات</h2><p>قد يعرض Toolora إعلانات من Adsterra. يمكن لشبكات الإعلانات وشركائها استخدام ملفات تعريف الارتباط أو تقنيات مشابهة لعرض الإعلانات وقياسها، وقد تجمع بيانات مثل عنوان IP ومعلومات الجهاز. راجع سياسة خصوصية Adsterra للتفاصيل. ويمكنك الحد من ذلك عبر إعدادات المتصفح أو أدوات التحكم في الإعلانات.</p>"
 "<h2>التخزين على جهازك</h2><p>يحفظ Toolora اختيارك للمظهر الفاتح أو الداكن في التخزين المحلي للمتصفح، ولا يخزّن شيئًا غير ذلك.</p>"
 "<h2>الموارد الخارجية</h2><p>معظم الصفحات لا تحمّل ملفات من أطراف ثالثة. أما صفحات مولّد رمز QR وأدوات PDF فتحمّل مكتبات مفتوحة المصدر (qrcode-generator وpdf-lib وPDF.js) من شبكة jsDelivr، وقد تسجّل الطلب. وعند إضافة شيفرة الإعلانات فإنها تُحمَّل من شبكة الإعلانات.</p>"
 f"<h2>التواصل</h2><p>للاستفسار عن هذه السياسة: {EMAIL}</p>"), lang="ar")
page("ar/terms.html", "شروط الاستخدام | Toolora", "شروط استخدام أدوات Toolora المجانية.", prose("شروط الاستخدام",
 "<p>آخر تحديث: 9 نوفمبر 2026</p><p>باستخدامك Toolora فإنك توافق على هذه الشروط. تُقدَّم الأدوات كما هي ودون أي ضمان. تحقّق من النتائج قبل الاعتماد عليها، خصوصًا في الأمور ذات الأثر القانوني أو المالي أو الأمني.</p><p>لا تستخدم الموقع لأغراض غير مشروعة أو للإضرار بتشغيله. قد نغيّر الأدوات أو نزيلها في أي وقت. الإعلانات مقدَّمة من أطراف ثالثة، وظهورها لا يعني تأييدنا لها.</p>"), lang="ar")
page("ar/contact.html", "اتصل بنا | Toolora", "تواصل مع Toolora لبلاغات الأخطاء والاقتراحات والاستفسارات عن الخصوصية.", prose("اتصل بنا",
 f"<p>نرحّب ببلاغات الأخطاء واقتراحات الأدوات والاستفسارات عن الخصوصية على <a href=\"mailto:{EMAIL}\">{EMAIL}</a>.</p><p>عند الإبلاغ عن خطأ، اذكر اسم الأداة ونوع المتصفح وما أدخلته إن لم يكن حساسًا.</p>"), lang="ar")
pages += ["ar/" + p for p in PAIRS]

AR_TOOL = {
 "word-counter": ("الصق مقالًا أو مسودة أو وصف منتج وستتحدّث الأرقام أثناء الكتابة. تعرض الأداة عدد الكلمات والأحرف والجمل والفقرات ومدة القراءة التقديرية، وهذا مفيد حين يحدد التكليف طولًا معينًا للنص.",
  "اكتب في المربع أو الصق نصك، فتظهر الأرقام بجانبه فورًا دون حاجة إلى زر. تفترض مدة القراءة 238 كلمة في الدقيقة، وهو متوسط شائع للقراءة الصامتة في الإنجليزية، وقد يختلف قليلًا مع العربية.",
  "تُفصل الكلمات بالمسافات، فتُحتسب العبارة المركّبة بشرطة كلمةً واحدة، وتُحتسب الجمل بعلامات الترقيم . ! ? ؟ . أما اللغات التي تُكتب بلا مسافات، مثل الصينية واليابانية، فتُحصى كلماتها بأقل من حقيقتها."),
 "character-counter": ("تفرض حقول كثيرة حدًّا صارمًا للطول: 160 حرفًا للرسالة النصية الواحدة، وقرابة 60 لعنوان نتيجة البحث، و280 لمنشور قصير. تعرض هذه الأداة عدد الأحرف مع المسافات وبدونها، وعدد الأسطر، وحجم النص بالبايت بترميز UTF-8، لتقارنه بالحد المطلوب.",
  "الصق نصك واقرأ الأرقام. قارن «الأحرف» بحد المنصة، واستخدم «البايتات» حين تحدّد قاعدة البيانات أو الواجهة البرمجية الحجم بالبايت لا بالأحرف.",
  "تُحتسب الأحرف وفق نقاط يونيكود. وبعض الرموز التعبيرية تتكوّن من عدة نقاط فتُعدّ هنا أكثر من حرف، وتختلف المنصات في طريقة عدّها. كما أن الحرف العربي يشغل بايتين في UTF-8، فيزيد حجم النص العربي بالبايت عن عدد أحرفه."),
 "text-reverser": ("تقدّم الأداة ثلاثة أنواع من العكس: قلب كل حرف، أو عكس ترتيب الكلمات داخل كل سطر، أو عكس ترتيب الأسطر نفسها. وهي مفيدة للألغاز والاختبارات السريعة وقلب قائمة رأسًا على عقب.",
  "الصق النص، واختر طريقة العكس، ثم انسخ النتيجة.",
  "يعكس وضع الأحرف نقاط يونيكود. وفي العربية يتغيّر شكل الحرف بحسب موقعه في الكلمة، لذا قد يظهر النص المعكوس بأشكال حروف مختلفة، وقد تنتقل علامات التشكيل إلى الحرف المجاور."),
 "remove-duplicate-lines": ("تنظّف قوائم عناوين البريد والكلمات المفتاحية والروابط وسجلات الأحداث. يبقى أول ظهور لكل سطر ويُحفظ الترتيب الأصلي.",
  "الصق عنصرًا واحدًا في كل سطر. استخدم الخيارات لتجاهل حالة الأحرف، أو لحذف المسافات حول كل سطر، أو لإزالة الأسطر الفارغة قبل المقارنة.",
  "تُقارَن الأسطر مطابقةً تامة ما لم يحدّد الخيار غير ذلك، فيُعدّ «a@example.com» و«a@example.com » سطرين مختلفين حتى تفعّل حذف المسافات. ولا ترتّب الأداة القائمة."),
 "password-generator": ("تُولَّد كلمات المرور داخل متصفحك بمولّد الأعداد العشوائية في Web Crypto، وبطريقة تضمن ألا يُفضَّل أي حرف على غيره. ويظهر كل نوع من الأحرف تختاره مرة واحدة على الأقل.",
  "حدّد الطول وأنواع الأحرف، ثم اضغط «توليد». انسخ كلمة المرور مباشرة إلى مدير كلمات المرور لديك.",
  "ترفض بعض المواقع رموزًا معيّنة؛ فأوقف الرموز إن رفض النموذج الناتج. ولا تُحفظ كلمات المرور في أي مكان، فانسخ الكلمة قبل أن تولّد غيرها."),
 "uuid-generator": ("تنتج معرّفات UUID عشوائية (الإصدار 4) بالصيغة القياسية 8-4-4-4-12. وتستخدم crypto.randomUUID حيث يوفّرها المتصفح، وتبني القيمة من أعداد Web Crypto العشوائية في غير ذلك.",
  "اختر عدد المعرّفات من 1 إلى 100 واضغط «توليد». تُعرض في سطر لكل معرّف، جاهزة للصق في سكربت أو جدول بيانات.",
  "الإصدار 4 فقط مدعوم. أما الإصدارات المرتبة زمنيًا مثل v7 فلا تُولَّد."),
}
AR_TOOL.update({
 "case-converter": ("تحوّل النص بين أنماط الكتابة دون إعادة طباعته. نمطا العنوان والجملة يناسبان العناوين والمحتوى، أما camelCase وsnake_case وkebab-case فتحوّل العبارة إلى اسم متغيّر أو اسم ملف أو جزء من رابط.",
  "الصق النص، ثم اختر النمط من القائمة. تتحدّث النتيجة فورًا، ويمكنك نسخها أو حفظها بصيغة .txt.",
  "الأنماط خاصة بالأحرف اللاتينية؛ فالعربية لا تعرف الحروف الكبيرة والصغيرة، ولذلك لا يتغيّر النص العربي. ونمط العنوان يكبّر كل كلمة بما فيها الكلمات الصغيرة مثل of وthe، فراجع العناوين وفق دليل أسلوبك. وتحذف أنماط camel وsnake وkebab علامات الترقيم وتُبقي الحروف والأرقام فقط."),
 "random-number-generator": ("تسحب عددًا صحيحًا أو أكثر بين حدّ أدنى وحدّ أقصى، ويدخل الحدّان في السحب. فعّل «بدون تكرار» للسحوبات التي لا يجوز أن يظهر فيها العدد أكثر من مرة، كالقرعة.",
  "أدخل النطاق وعدد الأرقام المطلوبة، ثم اضغط «توليد».",
  "أعداد صحيحة فقط، وبحد أقصى 1000 رقم في السحبة الواحدة. تأتي الأرقام من Web Crypto، لكن هذه الصفحة ليست نظامًا موثّقًا للاستخدام في اليانصيب المنظّم أو المقامرة."),
 "lorem-ipsum-generator": ("تنشئ فقرات نصية تجريبية من قائمة قصيرة من الكلمات اللاتينية. تبدأ الفقرة الأولى بالجملة التقليدية المعروفة، ويُركَّب الباقي عشوائيًا، فيختلف الناتج في كل مرة.",
  "اختر من 1 إلى 20 فقرة واضغط «توليد»، ثم انسخ النص إلى تصميمك أو قالبك.",
  "النص لاتيني عشوائي بلا معنى، ولا يصلح لتجربة الخطوط العربية أو اتجاه الكتابة من اليمين إلى اليسار؛ استخدم لذلك نصًا عربيًا حقيقيًا. واستبدله قبل نشر أي شيء."),
 "json-formatter": ("تحلّل الأداة نص JSON بمحلّل المتصفح الصارم، ثم تعرضه بمسافتين أو أربع مسافات للإزاحة أو في سطر واحد مضغوط. وإن كان الإدخال غير صالح فتُعرض رسالة الخطأ الصادرة عن المحلّل لتحدّد موضع المشكلة.",
  "الصق JSON في مربع الإدخال، ثم اختر حجم الإزاحة أو الضغط، فيظهر الناتج المنسّق في مربع الناتج.",
  "JSON الصارم فقط: تُرفض التعليقات والفواصل الزائدة والنصوص بين علامتي اقتباس مفردتين. وتظهر رسالة الخطأ بالإنجليزية لأنها تصدر عن المتصفح نفسه. وقد تفقد الأعداد الصحيحة الكبيرة جدًا دقتها لأنها تُحلَّل كأعداد JavaScript."),
 "base64-encoder-decoder": ("ترمّز النص إلى Base64 أو تفك ترميز نص Base64 إلى نص عادي. يُعامَل يونيكود بترميز UTF-8، فتبقى الحروف العربية والمشكّلة والرموز التعبيرية سليمة بعد الذهاب والإياب، وهو ما لا تضمنه دالة btoa في المتصفح وحدها.",
  "اختر الترميز أو فك الترميز، ثم الصق الإدخال. تُتجاهل المسافات الفارغة في إدخال Base64، وتُقبل الأحرف الآمنة للروابط (- و _).",
  "يفترض فك الترميز أن البيانات نص بترميز UTF-8؛ أما البيانات الثنائية مثل الصور فتُظهر خطأً."),
 "url-encoder-decoder": ("استخدم «ترميز قيمة» لمعامل استعلام واحد، و«ترميز الرابط كاملًا» لإبقاء رموز مثل : / ? & على حالها، و«فك الترميز» لتحويل تسلسلات مثل %20 إلى نص مقروء. ويفيد ذلك خصوصًا مع الروابط العربية التي يحوّلها المتصفح إلى رموز بنسبة مئوية.",
  "اختر الوضع والصق النص، فتتحدّث النتيجة أثناء الكتابة.",
  "يفشل فك الترميز مع التسلسلات غير الصالحة مثل % منفردة. ولا تُحوَّل علامة + إلى مسافة، فاستبدلها أولًا إن كانت البيانات قادمة من نموذج."),
 "html-formatter": ("تضع كل وسم في سطر مستقل وتزيحه بحسب عمق التداخل، بمسافتين أو أربع مسافات أو علامات تبويب. أما الضغط فيزيل التعليقات والمسافات بين الوسوم.",
  "الصق HTML، واختر طريقة التنسيق، ثم انسخ الناتج.",
  "منسّق بسيط وليس مدقّقًا، ولا يصلح الوسوم غير المغلقة. وتأخذ الوسوم المضمّنة مثل <bdi>&lt;b&gt;</bdi> سطرًا مستقلًا أيضًا، ولا تُحفظ المسافات داخل <bdi>&lt;pre&gt;</bdi>، وقد تُقسَّم في موضع خاطئ السكربتات أو الأنماط التي تحوي الرمز <bdi>&lt;</bdi>."),
})
AR_TOOL.update({
 "image-compressor": ("تعيد ترميز صورك بصيغة JPEG أو WebP بالجودة التي تختارها. وفي الصور الفوتوغرافية يخفض ضبط الجودة عند 70 إلى 80 في المئة الحجم كثيرًا مع فرق بسيط في المظهر، ويظهر الحجم الجديد بجوار الأصلي لتوازن بين الأمرين.",
  "أسقط صورة أو أكثر، واختر JPEG أو WebP ومستوى الجودة، فيظهر كل ملف مضغوط في قائمة مع زر تنزيل خاص به. ولتجربة جودة أخرى غيّر المنزلق وأسقط الملفات من جديد.",
  "الضغط هنا مع فقدان في الجودة. وتتحول صور PNG إلى JPEG أو WebP، وصيغة JPEG لا تدعم الشفافية فتصبح المناطق الشفافة بيضاء. وقد يخرج الملف أكبر من الأصل إن كان مضغوطًا جيدًا من قبل؛ وتعرض القائمة نسبة التغيّر."),
 "image-resizer": ("تغيّر أبعاد الصور إلى مقاسات بالبكسل بدقة، لمتطلبات الرفع والصور المصغّرة والبريد الإلكتروني. وعند تفعيل «الحفاظ على النسبة» تُلاءَم الصورة داخل العرض والارتفاع اللذين تحددهما؛ واترك أحد الحقلين فارغًا لتحديد الآخر فقط.",
  "أدخل عرضًا أو ارتفاعًا أو كليهما، ثم أسقط صورك ونزّل النسخ المعدَّلة. تبقى صيغة الإخراج كالأصل ما لم تختر غيرها.",
  "التكبير يمدّ البكسلات ولا يضيف تفاصيل. وعند إيقاف الحفاظ على النسبة مع تحديد البعدين تُمدّ الصورة لتناسبهما. والحد الأقصى للإخراج 16384 بكسل لكل ضلع."),
 "jpg-to-png": ("تحفظ صور JPEG بصيغة PNG، وهي صيغة بلا فقدان تقبلها أغلب أدوات التصميم والمستندات. تُنسخ البكسلات كما يفك JPEG ترميزها تمامًا.",
  "أسقط ملفًا أو أكثر بامتداد .jpg أو .jpeg، فيظهر كل ملف PNG محوَّل في القائمة مع زر تنزيل.",
  "التحويل لا يعيد تفاصيل فُقدت في JPEG، وملفات PNG للصور الفوتوغرافية أكبر عادةً بكثير. وJPEG لا يدعم الشفافية، فلا تحتوي صورة PNG الناتجة عليها أيضًا."),
 "png-to-jpg": ("تحوّل ملفات PNG إلى JPEG أصغر حجمًا، وهذا يناسب الصور الفوتوغرافية ولقطات الشاشة التي لا تحتاج شفافية. وتُملأ المناطق الشفافة باللون الأبيض.",
  "اضبط الجودة (90 في المئة بداية جيدة)، ثم أسقط ملفات PNG ونزّل ملفات JPEG.",
  "JPEG يفقد جزءًا من الجودة وقد يشوّش النصوص الحادة والخطوط الرفيعة، فاحتفظ بـ PNG للشعارات والمخططات. وتضيع الشفافية."),
 "webp-converter": ("تحوّل بين WebP وJPEG وPNG. وملفات WebP أصغر عادةً من JPEG بجودة مماثلة، ما يسرّع تحميل الصفحات؛ والتحويل إلى JPEG أو PNG يفيد حين لا يفتح برنامج ما صيغة WebP.",
  "اختر صيغة الإخراج واضبط الجودة لـ WebP أو JPEG، ثم أسقط ملفاتك.",
  "تُحوَّل صورة WebP المتحركة إلى إطار ثابت واحد. وبعض المتصفحات القديمة لا تستطيع حفظ WebP؛ وتخبرك الأداة حين يحدث ذلك."),
 "image-to-base64": ("تقرأ ملف صورة وتنتج نص Base64 الخاص به، مع البادئة data:image أو بدونها. أبقِ البادئة عند اللصق في وسم img أو في url() بـ CSS، واحذفها مع الواجهات البرمجية التي تتوقع Base64 خامًا.",
  "أسقط صورة أو اختر ملفًا، ثم انسخ الناتج. ألغِ تحديد خانة البادئة للتبديل بين الصيغتين.",
  "يزيد Base64 حجم البيانات بنحو الثلث، فهو يناسب الأيقونات الصغيرة أكثر من الصور الفوتوغرافية. وتُرفض الملفات التي يزيد حجمها على 5 ميغابايت."),
 "image-color-picker": ("حمّل صورة ثم انقر أو المس نقطة فيها لتحصل على لون ذلك البكسل برمز HEX وبقيم RGB، مع عيّنة لونية لترى ما اخترته.",
  "أسقط صورة، وانقر الموضع الذي تريده، ثم انسخ قيمة HEX أو RGB.",
  "تُعرض الصور التي يزيد ضلعها الأطول على 1600 بكسل بحجم مصغّر، ويُقرأ اللون من تلك النسخة الأصغر. والملتقط يعمل بالفأرة أو باللمس لا بلوحة المفاتيح. وبسبب ضغط JPEG قد تختلف البكسلات المتجاورة اختلافًا طفيفًا."),
 "image-cropper": ("اسحب على الصورة لتحديد المنطقة التي تريد الإبقاء عليها، أو اكتب قيم X وY والعرض والارتفاع بالبكسل بدقة. وتفيد النسب الثابتة مثل 1:1 و16:9 في الصور الشخصية والصور المصغّرة واللافتات. ويُقتطع القص من الصورة الأصلية بدقتها الكاملة لا من المعاينة.",
  "اختر صورة واسحب لتحديد منطقة؛ واسحب داخل التحديد لتحريكه. عدّل الأرقام إن احتجت دقة، واختر الصيغة، ثم اضغط «قص وتنزيل».",
  "تُصغَّر المعاينة للصور الكبيرة، لكن القص المحفوظ يستخدم البكسلات الأصلية. وعلى شاشات اللمس تبقى الصفحة ثابتة ما دام إصبعك على الصورة، فاستخدم حقول الأرقام للضبط الدقيق. ويملأ إخراج JPEG المناطق الشفافة باللون الأبيض."),
})
AR_TOOL.update({
 "merge-pdf": ("تضمّ ملفَّي PDF أو أكثر في ملف واحد. تُنسخ الصفحات كما هي، فيبقى النص والصور على حالهما في الملفات الأصلية.",
  "أضف ملفاتك، واستخدم «أعلى» و«أسفل» لضبط الترتيب، ثم اضغط «دمج الملفات».",
  "قد لا تنتقل الإشارات المرجعية وحقول النماذج من الملفات الأصلية. ولا يمكن فتح الملفات المحمية بكلمة مرور؛ أزل كلمة المرور أولًا."),
 "split-pdf": ("أدخل نطاقًا واحدًا أو أكثر من الصفحات فيصبح كل نطاق ملف PDF مستقلًا. فمثلًا يحوّل <bdi>1-3, 4-6, 7-</bdi> مستندًا طويلًا إلى ثلاثة ملفات.",
  "اختر ملف PDF، واكتب النطاقات مفصولة بفواصل، ثم اضغط «تقسيم PDF». يحصل كل ملف على زر تنزيل خاص به.",
  "ترقيم الصفحات يبدأ من 1، وتعني <bdi>7-</bdi> من الصفحة 7 إلى النهاية. وتُنزَّل الملفات واحدًا واحدًا؛ فلا يوجد تنزيل بصيغة ZIP."),
 "extract-pdf-pages": ("تبني ملف PDF جديدًا يحتوي فقط على الصفحات التي تحددها، بالترتيب الذي تكتبه. وهذا مفيد لإرسال بضع صفحات من تقرير طويل.",
  "اختر ملف PDF، وأدخل الصفحات مثل <bdi>2, 5-7, 12</bdi>، ثم اضغط «استخراج الصفحات».",
  "الصفحة المكتوبة مرتين تظهر مرتين. ولا تنتقل الإشارات المرجعية وحقول النماذج من الملف الأصلي."),
 "rotate-pdf": ("تعدّل اتجاه الصفحات الجانبية أو المقلوبة لتصير بالوضع الصحيح. يُضاف التدوير إلى تدوير الصفحة الحالي ويُحفظ في ملف جديد، فلا يتغيّر ملفك الأصلي.",
  "اختر ملف PDF وزاوية التدوير. اترك خانة الصفحات فارغة لتدوير كل الصفحات، أو أدخل صفحات مثل <bdi>1, 3-5</bdi>.",
  "التدوير مع عقارب الساعة، ويُخزَّن في إعدادات الصفحة، لذا قد تعامله بعض برامج العرض أو نوافذ الطباعة بشكل مختلف عن صفحة أُعيد مسحها ضوئيًا."),
 "jpg-to-pdf": ("تضع كل صورة في صفحة مستقلة. اختر صفحة بحجم الصورة نفسه، أو A4 بهامش. وتُضمَّن الصور كما هي دون إعادة ضغطها.",
  "أضف صورك، واستخدم «أعلى» و«أسفل» لضبط الترتيب، واختر حجم الصفحة، ثم اضغط «إنشاء PDF».",
  "يُدعم JPEG وPNG فقط؛ حوّل الصيغ الأخرى أولًا بمحوّل WebP. والصور الكبيرة تنتج ملفات PDF كبيرة."),
 "pdf-to-images": ("ترسم كل صفحة بالدقة التي تختارها وتعطيك صورة لكل صفحة. وهذا مفيد لمشاركة صفحة في موقع لا يقبل PDF أو لوضع صفحة في شريحة عرض.",
  "اختر ملف PDF، وحدّد الصيغة والدقة، ثم اضغط «تحويل الصفحات». لكل صفحة زر تنزيل خاص بها.",
  "حتى 100 صفحة في المرة الواحدة. والدقة العالية جدًا على الصفحات الكبيرة تحتاج ذاكرة كبيرة وقد تفشل على الهواتف. ولا يمكن تحديد النص داخل الصور."),
 "compress-pdf": ("ترسم كل صفحة وتضغطها بصيغة JPEG بالجودة والدقة اللتين تحددهما، ثم تبني ملف PDF جديدًا من تلك الصور. وقد يقلّص هذا حجم الملفات الممسوحة ضوئيًا والغنية بالصور كثيرًا.",
  "اختر ملف PDF، واضبط الجودة والدقة، ثم اضغط «ضغط PDF». قارن الحجمين المعروضين، واحتفظ بالأصل إن لم تكن النتيجة أصغر.",
  "تتحول كل صفحة إلى صورة: فلا يمكن بعد ذلك تحديد النص أو البحث فيه، وتضيع الروابط وحقول النماذج، وتصير الرسومات المتجهة بكسلات. أما ملفات PDF النصية في معظمها فيكبر حجمها في الغالب ولا يصغر. والحد الأقصى 100 صفحة."),
 "text-diff-checker": ("الصق نسخة أصلية ونسخة معدَّلة، فيُعرض كل سطر على أنه دون تغيير أو مضاف (+) أو محذوف (-). وهذا مفيد لمراجعة التعديلات على مستند أو ملف إعدادات أو قائمة.",
  "الصق النص الأصلي في المربع الأول والنص المعدَّل في المربع الثاني، ثم اضغط «مقارنة». فعّل خيار المسافات لتجاهل المسافات في نهاية الأسطر.",
  "تعمل المقارنة على الأسطر كاملة، فيظهر تعديل كلمة واحدة على أنه سطر محذوف وسطر مضاف. ويُقتصر كل نص على نحو 2000 سطر."),
 "qr-code-generator": ("تحوّل رابطًا أو أي نص إلى رمز QR يمكنك تنزيله بصيغة PNG. يُرسم الرمز في متصفحك مع هامش هادئ بعرض أربع وحدات حوله ليقرأه الماسح بسهولة. ويُرمَّز النص بترميز UTF-8، ومع ذلك جرّب الرمز بهاتفك للتأكد من قراءة النص العربي.",
  "اكتب النص أو الصقه، واختر مستوى تصحيح الأخطاء (المستويات الأعلى تتحمل تلفًا أكبر لكنها تنتج رمزًا أكثف) والحجم، ثم اضغط «تنزيل PNG».",
  "تحمّل الصفحة مكتبة صغيرة مفتوحة المصدر من شبكة jsDelivr، لذا تحتاج إلى اتصال بالإنترنت. ويُقرَّب حجم الصورة بحيث تشغل كل وحدة عددًا صحيحًا من البكسلات. امسح الرمز بهاتفك قبل الطباعة."),
})
for slug in AR_SLUGS:
    name, short = AR[slug]
    about, how, limit = AR_TOOL[slug]
    cat = next(t[2] for t in TOOLS if t[0] == slug)
    rel = "".join(tile(x, f"{x}.html", AR[x][0], AR[x][1], cat_of[x]) for x in sorted([y for y in AR_SLUGS if y != slug], key=lambda y: cat_of[y] != cat)[:3])
    body = f'''<div class="wrap {CLS[cat]}"><nav class="crumbs" aria-label="مسار التنقل"><a href="../index.html">الرئيسية</a> / <a href="../index.html#{anchor(cat)}">{AR_CATS[cat]}</a> / <span aria-current="page">{name}</span></nav>
<div class="tool-head"><span class="badge" aria-hidden="true">{esc(BADGE[slug])}</span><div><h1>{name}</h1><p class="lead">{short}</p></div></div>{slot("banner")}
<div id="tool"><p>تحتاج هذه الأداة إلى تفعيل JavaScript في المتصفح.</p></div>{slot("inline")}
<div class="info"><section><h2>ماذا تفعل الأداة</h2><p>{about}</p></section><section><h2>طريقة الاستخدام</h2><p>{how}</p></section><section><h2>حدود يجب أن تعرفها</h2><p>{limit}</p></section></div>{slot("native")}
<section class="related"><h2>أدوات ذات صلة</h2><ul class="grid">{rel}</ul></section></div>'''
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "description": short, "inLanguage": "ar",
          "url": f"{SITE}/ar/tools/{slug}.html", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    page(f"ar/tools/{slug}.html", f"{name} | Toolora", f"{short} الأداة مجانية، وتعمل داخل متصفحك دون تسجيل.", body, ld, slug, lang="ar")
pages += [f"ar/tools/{s}.html" for s in AR_SLUGS]

open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{SITE}/{p.removesuffix('index.html')}</loc></url>\n" for p in pages) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open("ads.txt", "w").write("# Add the ads.txt line from your Adsterra account here once it is approved.\n")
NOTES = {
 "image-compressor": "JPEG and WebP output, smaller result, wrong file type, damaged file",
 "image-resizer": "Keep ratio, free resize, PNG transparency kept",
 "jpg-to-png": "Conversion, wrong file type",
 "png-to-jpg": "Transparent areas become white",
 "webp-converter": "WebP to WebP, WebP to PNG",
 "image-cropper": "Numeric crop, 1:1 ratio, mouse drag, wrong file type",
 "image-to-base64": "Prefix on and off, wrong file type",
 "image-color-picker": "Two pixel colours as HEX and RGB",
 "merge-pdf": "Merge, reorder, single file, damaged PDF, wrong file type",
 "split-pdf": "Ranges 1-2 and 4-",
 "extract-pdf-pages": "Page order 5, 1-2; invalid ranges",
 "rotate-pdf": "Overlapping pages rotate once; all pages at 270 degrees",
 "jpg-to-pdf": "Page size same as image, A4",
 "text-diff-checker": "Added and removed lines, identical texts, empty input",
 "pdf-to-images": "Only the message shown when PDF.js cannot load",
 "compress-pdf": "Only the message shown when PDF.js cannot load",
 "qr-code-generator": "Only the hidden canvas and the message shown when the library cannot load",
}
DEFAULT = "Sample input and output, clear, Arabic page; logic with valid, empty and invalid input (Node)"
NOT_TESTED = {"pdf-to-images", "compress-pdf", "qr-code-generator"}
rows = "".join(f"| {t[1]} | {NOTES.get(t[0], DEFAULT)} | {'Not tested' if t[0] in NOT_TESTED else 'Passed'} |\n" for t in TOOLS)
open("TEST-REPORT.md", "w").write("""# Test report

**Status: 27 of 30 tools were tested in headless Chromium on Linux, at 1280 px and 360 px width.** PDF to Images, Compress PDF and QR Code Generator were not tested, because their libraries cannot be loaded offline. No other browser and no real phone was used.

| Tool | What was tested | Result |
|---|---|---|
""" + rows + """
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
""")
