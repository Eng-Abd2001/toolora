const PDFLIB = "https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js";
const PDFJS = "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js";
const PDFJS_WORKER = "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js";
const loaded = {};
const loadScript = src => loaded[src] || (loaded[src] = new Promise((ok, no) => {
  const s = document.createElement("script");
  s.src = src; s.onload = ok;
  s.onerror = () => { delete loaded[src]; no(new Error("A required library could not be loaded. Check your connection and reload the page.")); };
  document.head.append(s);
}));
const needLib = () => loadScript(PDFLIB);
const needJs = async () => { await loadScript(PDFJS); pdfjsLib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER; };
const isPdf = f => f.type === "application/pdf" || /\.pdf$/i.test(f.name);
const isJpgPng = f => f.type === "image/jpeg" || f.type === "image/png";
const baseName = f => f.name.replace(/\.[^.]+$/, "");
const pdfBlob = bytes => new Blob([bytes], { type: "application/pdf" });
const toBlob = (c, type, q) => new Promise(r => c.toBlob(r, type, q));
const openPdf = async f => {
  try { return await PDFLib.PDFDocument.load(await f.arrayBuffer()); }
  catch (e) { throw new Error(f.name + " could not be opened. It may be damaged or password-protected."); }
};
const ranges = (text, total) => {
  const out = text.split(",").map(s => s.trim()).filter(Boolean).map(tok => {
    const m = tok.match(/^(\d+)?\s*(-)?\s*(\d+)?$/);
    if (!m || (!m[1] && !m[3])) throw new Error("“" + tok + "” is not a valid page or range. Use a format such as 1-3, 5, 8-.");
    const a = m[1] ? +m[1] : 1, b = m[2] ? (m[3] ? +m[3] : total) : a;
    if (a < 1 || b > total || a > b) throw new Error("“" + tok + "” is outside this PDF, which has " + total + " pages.");
    return [a, b];
  });
  if (!out.length) throw new Error("Enter at least one page or range, for example 1-3, 5.");
  return out;
};
const span = (a, b) => Array.from({ length: b - a + 1 }, (_, i) => a - 1 + i);
const copyInto = async (out, src, idx) => (await out.copyPages(src, idx)).forEach(p => out.addPage(p));

const renderPages = async (file, scale, each) => {
  await needJs();
  let doc;
  try { doc = await pdfjsLib.getDocument({ data: await file.arrayBuffer() }).promise; }
  catch (e) { throw new Error(file.name + " could not be opened. It may be damaged or password-protected."); }
  if (doc.numPages > 100) throw new Error("This PDF has " + doc.numPages + " pages. The limit is 100 per run.");
  for (let p = 1; p <= doc.numPages; p++) {
    const page = await doc.getPage(p), vp = page.getViewport({ scale });
    if (vp.width * vp.height > 6e7) throw new Error("Page " + p + " is too large at this resolution. Choose a lower resolution.");
    const c = document.createElement("canvas");
    c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
    const ctx = c.getContext("2d");
    ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, c.width, c.height);
    await page.render({ canvasContext: ctx, viewport: vp }).promise;
    await each(c, p, doc.numPages, page.getViewport({ scale: 1 }));
    c.width = c.height = 0;
  }
};

const pdfTool = cfg => mount => {
  mount.className = "tool";
  mount.innerHTML = `${cfg.note ? `<p class="note">${cfg.note}</p>` : ""}<div class="opts">${cfg.opts || ""}</div>
<label class="drop"><input type="file" accept="${cfg.accept}"${cfg.multiple ? " multiple" : ""}>${cfg.multiple ? "Drop files here or choose files" : "Drop a file here or choose a file"}<small>${cfg.hint}</small></label>
<p class="err" role="alert" hidden></p><ul class="files queue"></ul>
<div class="bar"><button class="btn" id="go" type="button">${cfg.button}</button><button class="btn alt" id="clr" type="button">Clear</button></div><ul class="files out"></ul>`;
  const err = q1(".err", mount), queue = q1(".queue", mount), out = q1(".out", mount), go = q1("#go", mount);
  let files = [], urls = [];
  const fail = m => { err.textContent = m; err.hidden = false; };
  const clearOut = () => { urls.forEach(u => URL.revokeObjectURL(u)); urls = []; out.replaceChildren(); };
  mount.querySelectorAll("input[type=range]").forEach(r => r.addEventListener("input", () => { r.parentElement.querySelector("output").textContent = r.value; }));

  const renderQueue = () => queue.replaceChildren(...files.map((f, i) => {
    const li = document.createElement("li"), n = document.createElement("span"), s = document.createElement("span");
    n.className = "n"; s.className = "s"; n.textContent = f.name; s.textContent = kb(f.size);
    li.append(n, s);
    const btn = (text, fn, off) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "btn alt"; b.textContent = text; b.disabled = !!off;
      b.addEventListener("click", fn); li.append(b);
    };
    if (cfg.multiple) {
      btn("Up", () => { [files[i - 1], files[i]] = [files[i], files[i - 1]]; renderQueue(); }, i === 0);
      btn("Down", () => { [files[i + 1], files[i]] = [files[i], files[i + 1]]; renderQueue(); }, i === files.length - 1);
    }
    btn("Remove", () => { files.splice(i, 1); renderQueue(); });
    return li;
  }));

  dropZone(mount, picked => {
    err.hidden = true;
    const ok = picked.filter(cfg.test), bad = picked.filter(f => !cfg.test(f));
    if (bad.length) fail("Skipped " + bad.map(f => f.name).join(", ") + ": unsupported file type.");
    if (ok.length) { files = cfg.multiple ? files.concat(ok) : ok.slice(0, 1); renderQueue(); }
  });
  q1("#clr", mount).addEventListener("click", () => { files = []; renderQueue(); clearOut(); err.hidden = true; });

  const res = {
    row(name) {
      const li = document.createElement("li"), n = document.createElement("span"), s = document.createElement("span");
      n.className = "n"; s.className = "s"; n.textContent = name;
      li.append(n, s); out.append(li);
      return {
        status: t => { s.textContent = t; },
        download(blob, file) {
          const url = URL.createObjectURL(blob);
          urls.push(url);
          const a = document.createElement("a");
          a.className = "btn alt"; a.href = url; a.download = file; a.textContent = "Download";
          li.append(a);
        }
      };
    }
  };
  go.addEventListener("click", async () => {
    err.hidden = true; clearOut();
    if (!files.length) return fail(cfg.multiple ? "Add at least one file first." : "Choose a file first.");
    go.disabled = true;
    const o = Object.fromEntries([...mount.querySelectorAll("[data-o]")].map(e => [e.dataset.o, e.value]));
    try { await cfg.run(files, o, res); } catch (e) { fail(e.message); }
    go.disabled = false;
  });
};

const pagesField = (label, ph) => `<label>${label}<input data-o="pages" type="text" placeholder="${ph}" style="min-width:220px"></label>`;
const PDF_ONE = { accept: "application/pdf,.pdf", test: isPdf, hint: "One PDF file" };

CUSTOM_TOOLS["merge-pdf"] = pdfTool({
  accept: "application/pdf,.pdf", test: isPdf, multiple: true, hint: "Add two or more PDFs, then set their order", button: "Merge PDFs",
  run: async (files, o, res) => {
    if (files.length < 2) throw new Error("Add at least two PDF files to merge.");
    await needLib();
    const out = await PDFLib.PDFDocument.create(), row = res.row("merged.pdf");
    for (const [i, f] of files.entries()) {
      row.status("Adding file " + (i + 1) + " of " + files.length + "…");
      const src = await openPdf(f);
      await copyInto(out, src, src.getPageIndices());
    }
    const blob = pdfBlob(await out.save());
    row.status(out.getPageCount() + " pages, " + kb(blob.size));
    row.download(blob, "merged.pdf");
  }
});

CUSTOM_TOOLS["split-pdf"] = pdfTool({
  ...PDF_ONE, button: "Split PDF", opts: pagesField("Page ranges", "1-3, 4-6, 7-"),
  run: async ([f], o, res) => {
    await needLib();
    const src = await openPdf(f);
    for (const [a, b] of ranges(o.pages || "", src.getPageCount())) {
      const out = await PDFLib.PDFDocument.create();
      await copyInto(out, src, span(a, b));
      const blob = pdfBlob(await out.save()), name = baseName(f) + "-pages-" + a + (b > a ? "-" + b : "") + ".pdf", row = res.row(name);
      row.status((b - a + 1) + (b > a ? " pages, " : " page, ") + kb(blob.size));
      row.download(blob, name);
    }
  }
});

CUSTOM_TOOLS["extract-pdf-pages"] = pdfTool({
  ...PDF_ONE, button: "Extract pages", opts: pagesField("Pages to keep", "2, 5-7, 12"),
  run: async ([f], o, res) => {
    await needLib();
    const src = await openPdf(f), idx = ranges(o.pages || "", src.getPageCount()).flatMap(([a, b]) => span(a, b));
    const out = await PDFLib.PDFDocument.create();
    await copyInto(out, src, idx);
    const blob = pdfBlob(await out.save()), name = baseName(f) + "-extracted.pdf", row = res.row(name);
    row.status(idx.length + " pages, " + kb(blob.size));
    row.download(blob, name);
  }
});

CUSTOM_TOOLS["rotate-pdf"] = pdfTool({
  ...PDF_ONE, button: "Rotate PDF",
  opts: `<label>Rotate clockwise by<select data-o="angle"><option value="90">90°</option><option value="180">180°</option><option value="270">270°</option></select></label>` + pagesField("Pages (empty = all)", "1, 3-5"),
  run: async ([f], o, res) => {
    await needLib();
    const src = await openPdf(f), pages = src.getPages();
    const idx = (o.pages || "").trim() ? ranges(o.pages, pages.length).flatMap(([a, b]) => span(a, b)) : span(1, pages.length);
    [...new Set(idx)].forEach(i => pages[i].setRotation(PDFLib.degrees((pages[i].getRotation().angle + +o.angle) % 360)));
    const blob = pdfBlob(await src.save()), name = baseName(f) + "-rotated.pdf", row = res.row(name);
    row.status(new Set(idx).size + " of " + pages.length + " pages rotated, " + kb(blob.size));
    row.download(blob, name);
  }
});

CUSTOM_TOOLS["jpg-to-pdf"] = pdfTool({
  accept: "image/jpeg,image/png", test: isJpgPng, multiple: true, hint: "JPEG or PNG images", button: "Create PDF",
  opts: `<label>Page size<select data-o="size"><option value="fit">Same as each image</option><option value="a4">A4 with margin</option></select></label>`,
  run: async (files, o, res) => {
    await needLib();
    const out = await PDFLib.PDFDocument.create(), row = res.row("images.pdf");
    for (const [i, f] of files.entries()) {
      row.status("Adding image " + (i + 1) + " of " + files.length + "…");
      let img;
      try {
        const bytes = await f.arrayBuffer();
        img = f.type === "image/png" ? await out.embedPng(bytes) : await out.embedJpg(bytes);
      } catch (e) { throw new Error(f.name + " could not be read as a valid " + (f.type === "image/png" ? "PNG" : "JPEG") + " image."); }
      if (o.size === "a4") {
        const W = 595.28, H = 841.89, s = Math.min((W - 72) / img.width, (H - 72) / img.height), w = img.width * s, h = img.height * s;
        out.addPage([W, H]).drawImage(img, { x: (W - w) / 2, y: (H - h) / 2, width: w, height: h });
      } else out.addPage([img.width, img.height]).drawImage(img, { x: 0, y: 0, width: img.width, height: img.height });
    }
    const blob = pdfBlob(await out.save());
    row.status(files.length + (files.length > 1 ? " pages, " : " page, ") + kb(blob.size));
    row.download(blob, "images.pdf");
  }
});

CUSTOM_TOOLS["pdf-to-images"] = pdfTool({
  ...PDF_ONE, button: "Convert pages",
  opts: `<label>Format<select data-o="fmt"><option value="png">PNG</option><option value="jpeg">JPEG</option></select></label><label>Resolution<select data-o="scale"><option value="1">Standard (1x)</option><option value="2" selected>High (2x)</option><option value="3">Very high (3x)</option></select></label>`,
  run: ([f], o, res) => renderPages(f, +o.scale, async (c, p) => {
    const png = o.fmt === "png", name = baseName(f) + "-page-" + p + (png ? ".png" : ".jpg");
    const blob = await toBlob(c, png ? "image/png" : "image/jpeg", 0.92), row = res.row(name);
    row.status(c.width + "×" + c.height + " px, " + kb(blob.size));
    row.download(blob, name);
  })
});

CUSTOM_TOOLS["compress-pdf"] = pdfTool({
  ...PDF_ONE, button: "Compress PDF",
  note: "This tool turns every page into an image and rebuilds the PDF. Scans and image-heavy files often shrink a lot, but text can no longer be selected or searched, and vector graphics lose sharpness. PDFs that are mostly text usually get larger.",
  opts: `<label><span>Image quality <output>60</output>%</span><input data-o="q" type="range" min="20" max="90" value="60"></label><label>Resolution<select data-o="dpi"><option value="72">72 dpi (smallest)</option><option value="110" selected>110 dpi</option><option value="150">150 dpi (sharper)</option></select></label>`,
  run: async ([f], o, res) => {
    await needLib();
    const out = await PDFLib.PDFDocument.create(), name = baseName(f) + "-compressed.pdf", row = res.row(name);
    await renderPages(f, +o.dpi / 72, async (c, p, n, size) => {
      row.status("Page " + p + " of " + n + "…");
      const img = await out.embedJpg(await (await toBlob(c, "image/jpeg", o.q / 100)).arrayBuffer());
      out.addPage([size.width, size.height]).drawImage(img, { x: 0, y: 0, width: size.width, height: size.height });
    });
    const blob = pdfBlob(await out.save());
    row.status(kb(f.size) + " to " + kb(blob.size) + (blob.size >= f.size ? ". The result is not smaller, so keep the original." : ""));
    row.download(blob, name);
  }
});
