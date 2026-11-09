const CUSTOM_TOOLS = {};
const q1 = (s, r = document) => r.querySelector(s);
const kb = n => n < 1048576 ? (n / 1024).toFixed(n < 10240 ? 1 : 0) + " KB" : (n / 1048576).toFixed(1) + " MB";
const MIME = { png: "image/png", jpeg: "image/jpeg", webp: "image/webp" };
const KEY = { "image/png": "png", "image/jpeg": "jpeg", "image/webp": "webp" };
const EXT = { png: "png", jpeg: "jpg", webp: "webp" };
const LABEL = { same: "Same as original", png: "PNG", jpeg: "JPEG", webp: "WebP" };

const dropZone = (root, onFiles) => {
  const drop = q1(".drop", root), input = q1("input", drop);
  input.addEventListener("change", () => { onFiles([...input.files]); input.value = ""; });
  ["dragenter", "dragover"].forEach(e => drop.addEventListener(e, ev => { ev.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach(e => drop.addEventListener(e, ev => { ev.preventDefault(); drop.classList.remove("over"); }));
  drop.addEventListener("drop", ev => onFiles([...ev.dataTransfer.files]));
};
const copyButton = (btn, getText) => btn.addEventListener("click", async () => {
  const old = btn.textContent;
  try { await navigator.clipboard.writeText(getText()); btn.textContent = "Copied"; } catch (e) { btn.textContent = "Copy failed"; }
  setTimeout(() => { btn.textContent = old; }, 1400);
});

const convert = async (file, o) => {
  let bmp;
  try { bmp = await createImageBitmap(file); } catch (e) { throw new Error("This file could not be read as an image. It may be damaged."); }
  let w = bmp.width, h = bmp.height;
  if (o.w || o.h) {
    if (o.keep) { const s = Math.min(o.w ? o.w / w : Infinity, o.h ? o.h / h : Infinity); w = Math.round(w * s); h = Math.round(h * s); }
    else { w = o.w || w; h = o.h || h; }
  }
  if (!w || !h || w > 16384 || h > 16384 || w * h > 1e8) { bmp.close(); throw new Error("The output size is too large for the browser. Use smaller dimensions."); }
  const key = o.fmt === "same" ? KEY[file.type] : o.fmt;
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  const ctx = c.getContext("2d");
  if (key === "jpeg") { ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, w, h); }
  ctx.imageSmoothingQuality = "high";
  ctx.drawImage(bmp, 0, 0, w, h);
  bmp.close();
  const blob = await new Promise(r => c.toBlob(r, MIME[key], o.q));
  if (!blob || blob.type !== MIME[key]) throw new Error("Your browser cannot save " + LABEL[key] + " files. Try another browser.");
  return { blob, w, h, key, url: URL.createObjectURL(blob) };
};

const imageConverter = cfg => mount => {
  mount.className = "tool";
  mount.innerHTML = `<div class="opts">
${cfg.formats.length > 1 ? `<label>Output format<select id="i-fmt">${cfg.formats.map(f => `<option value="${f}">${LABEL[f]}</option>`).join("")}</select></label>` : ""}
${cfg.quality ? `<label><span>Quality <output id="i-qv">${cfg.quality}</output>%</span><input id="i-q" type="range" min="10" max="100" value="${cfg.quality}"></label>` : ""}
${cfg.resize ? `<label>Width (px)<input id="i-w" type="number" min="1" max="16384" placeholder="auto"></label><label>Height (px)<input id="i-h" type="number" min="1" max="16384" placeholder="auto"></label><label class="chk"><input id="i-keep" type="checkbox" checked>&nbsp;Keep aspect ratio</label>` : ""}
</div>
<label class="drop"><input type="file" accept="${cfg.accept}" multiple>Drop images here or choose files<small>${cfg.hint}. Settings apply to the files you add next.</small></label>
<p class="err" role="alert" hidden></p><ul class="files"></ul>`;
  const list = q1(".files", mount), err = q1(".err", mount), val = id => q1(id, mount);
  let urls = [];
  const slider = val("#i-q");
  if (slider) slider.addEventListener("input", () => { val("#i-qv").textContent = slider.value; });
  dropZone(mount, async files => {
    urls.forEach(u => URL.revokeObjectURL(u));
    urls = [];
    list.replaceChildren();
    err.hidden = true;
    const o = {
      fmt: val("#i-fmt") ? val("#i-fmt").value : cfg.formats[0],
      q: slider ? slider.value / 100 : 0.92,
      w: val("#i-w") ? val("#i-w").valueAsNumber || 0 : 0,
      h: val("#i-h") ? val("#i-h").valueAsNumber || 0 : 0,
      keep: val("#i-keep") ? val("#i-keep").checked : false
    };
    for (const [i, file] of files.entries()) {
      const li = document.createElement("li"), name = document.createElement("span"), status = document.createElement("span");
      name.className = "n"; status.className = "s";
      name.textContent = file.name;
      li.append(name, status);
      list.append(li);
      if (!cfg.accept.split(",").includes(file.type)) { status.textContent = "Skipped: " + (file.type || "unknown file type") + " is not supported here."; continue; }
      status.textContent = "Processing " + (i + 1) + " of " + files.length + "…";
      try {
        const r = await convert(file, o);
        urls.push(r.url);
        const pct = Math.round((r.blob.size / file.size - 1) * 100);
        status.textContent = kb(file.size) + " to " + kb(r.blob.size) + " (" + (pct > 0 ? "+" : "") + pct + "%), " + r.w + "×" + r.h + " px";
        const a = document.createElement("a");
        a.className = "btn alt"; a.href = r.url; a.textContent = "Download";
        a.download = file.name.replace(/\.[^.]+$/, "") + cfg.suffix + "." + EXT[r.key];
        li.append(a);
      } catch (e) { status.textContent = e.message; }
    }
  });
};
const STD = "image/jpeg,image/png,image/webp";
CUSTOM_TOOLS["image-compressor"] = imageConverter({ accept: STD, hint: "JPEG, PNG or WebP", formats: ["jpeg", "webp"], quality: 75, suffix: "-compressed" });
CUSTOM_TOOLS["image-resizer"] = imageConverter({ accept: STD, hint: "JPEG, PNG or WebP", formats: ["same", "png", "jpeg", "webp"], quality: 90, resize: true, suffix: "-resized" });
CUSTOM_TOOLS["jpg-to-png"] = imageConverter({ accept: "image/jpeg", hint: "JPEG files", formats: ["png"], suffix: "" });
CUSTOM_TOOLS["png-to-jpg"] = imageConverter({ accept: "image/png", hint: "PNG files", formats: ["jpeg"], quality: 90, suffix: "" });
CUSTOM_TOOLS["webp-converter"] = imageConverter({ accept: STD, hint: "WebP, JPEG or PNG", formats: ["webp", "jpeg", "png"], quality: 85, suffix: "" });

CUSTOM_TOOLS["image-to-base64"] = mount => {
  mount.className = "tool";
  mount.innerHTML = `<div class="opts"><label class="chk"><input id="b-pre" type="checkbox" checked>&nbsp;Include the data:image prefix</label></div>
<label class="drop"><input type="file" accept="image/*">Drop an image here or choose a file<small>Up to 5 MB</small></label>
<p class="err" role="alert" hidden></p>
<div id="b-res" hidden><img class="prev" alt="Preview of the chosen image"><label>Base64 output<textarea id="b-t" readonly></textarea></label><div class="bar"><button class="btn" id="b-copy" type="button">Copy</button></div></div>`;
  const err = q1(".err", mount), box = q1("#b-res", mount), t = q1("#b-t", mount), pre = q1("#b-pre", mount);
  let data = "";
  const show = () => { t.value = pre.checked ? data : data.slice(data.indexOf(",") + 1); };
  pre.addEventListener("change", () => data && show());
  copyButton(q1("#b-copy", mount), () => t.value);
  dropZone(mount, files => {
    const f = files[0];
    err.hidden = true;
    if (!f) return;
    const fail = m => { err.textContent = m; err.hidden = false; box.hidden = true; };
    if (!f.type.startsWith("image/")) return fail(f.name + " is not an image file.");
    if (f.size > 5 * 1048576) return fail("This image is " + kb(f.size) + ". The limit is 5 MB.");
    const rd = new FileReader();
    rd.onerror = () => fail("The file could not be read.");
    rd.onload = () => { data = rd.result; q1(".prev", mount).src = data; show(); box.hidden = false; };
    rd.readAsDataURL(f);
  });
};

CUSTOM_TOOLS["image-color-picker"] = mount => {
  mount.className = "tool";
  mount.innerHTML = `<label class="drop"><input type="file" accept="image/*">Drop an image here or choose a file<small>Then click or tap the colour you want</small></label>
<p class="err" role="alert" hidden></p>
<div id="c-res" hidden><canvas id="c-cv" aria-label="Chosen image. Click or tap to pick a colour."></canvas>
<div class="picked"><span id="c-sw" class="sw"></span><div><div>HEX <output id="c-hex">-</output> <button class="btn alt" id="c-ch" type="button">Copy</button></div><div>RGB <output id="c-rgb">-</output> <button class="btn alt" id="c-cr" type="button">Copy</button></div></div></div></div>`;
  const err = q1(".err", mount), cv = q1("#c-cv", mount), hex = q1("#c-hex", mount), rgb = q1("#c-rgb", mount);
  copyButton(q1("#c-ch", mount), () => hex.textContent);
  copyButton(q1("#c-cr", mount), () => rgb.textContent);
  dropZone(mount, async files => {
    const f = files[0];
    err.hidden = true;
    if (!f) return;
    if (!f.type.startsWith("image/")) { err.textContent = f.name + " is not an image file."; err.hidden = false; return; }
    try {
      const bmp = await createImageBitmap(f), s = Math.min(1, 1600 / Math.max(bmp.width, bmp.height));
      cv.width = Math.round(bmp.width * s); cv.height = Math.round(bmp.height * s);
      cv.getContext("2d", { willReadFrequently: true }).drawImage(bmp, 0, 0, cv.width, cv.height);
      bmp.close();
      q1("#c-res", mount).hidden = false;
    } catch (e) { err.textContent = "This file could not be read as an image."; err.hidden = false; }
  });
  cv.addEventListener("pointerdown", e => {
    const r = cv.getBoundingClientRect();
    const x = Math.min(cv.width - 1, Math.floor((e.clientX - r.left) * cv.width / r.width));
    const y = Math.min(cv.height - 1, Math.floor((e.clientY - r.top) * cv.height / r.height));
    const [R, G, B, A] = cv.getContext("2d").getImageData(x, y, 1, 1).data;
    if (!A) { hex.textContent = "transparent"; rgb.textContent = "-"; return; }
    hex.textContent = "#" + [R, G, B].map(v => v.toString(16).padStart(2, "0")).join("").toUpperCase();
    rgb.textContent = `rgb(${R}, ${G}, ${B})`;
    q1("#c-sw", mount).style.background = hex.textContent;
  });
};

CUSTOM_TOOLS["text-diff-checker"] = mount => {
  mount.className = "tool";
  mount.innerHTML = `<div class="opts"><label class="chk"><input id="d-ws" type="checkbox">&nbsp;Ignore spaces at the end of lines</label></div>
<div class="io"><label>Original<textarea id="d-a" spellcheck="false" placeholder="Paste the original text"></textarea></label><label>Changed<textarea id="d-b" spellcheck="false" placeholder="Paste the changed text"></textarea></label></div>
<p class="err" role="alert" hidden></p>
<div class="bar"><button class="btn" id="d-run" type="button">Compare</button><button class="btn alt" id="d-clear" type="button">Clear</button></div>
<div class="diff" id="d-out" aria-live="polite" hidden></div>`;
  const A = q1("#d-a", mount), B = q1("#d-b", mount), out = q1("#d-out", mount), err = q1(".err", mount);
  q1("#d-clear", mount).addEventListener("click", () => { A.value = B.value = ""; out.hidden = err.hidden = true; });
  q1("#d-run", mount).addEventListener("click", () => {
    err.hidden = true;
    if (!A.value && !B.value) { err.textContent = "Enter text in at least one box."; err.hidden = false; return; }
    const a = A.value.split("\n"), b = B.value.split("\n"), n = a.length, m = b.length;
    if (n * m > 4e6) { err.textContent = "These texts are too long to compare. Keep each under about 2,000 lines."; err.hidden = false; return; }
    const norm = l => q1("#d-ws", mount).checked ? l.trimEnd() : l, ka = a.map(norm), kb2 = b.map(norm);
    const W = m + 1, dp = new Uint16Array((n + 1) * W);
    for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--)
      dp[i * W + j] = ka[i] === kb2[j] ? dp[(i + 1) * W + j + 1] + 1 : Math.max(dp[(i + 1) * W + j], dp[i * W + j + 1]);
    const rows = [];
    let i = 0, j = 0;
    while (i < n && j < m) {
      if (ka[i] === kb2[j]) { rows.push(["same", b[j]]); i++; j++; }
      else if (dp[(i + 1) * W + j] >= dp[i * W + j + 1]) rows.push(["del", a[i++]]);
      else rows.push(["add", b[j++]]);
    }
    while (i < n) rows.push(["del", a[i++]]);
    while (j < m) rows.push(["add", b[j++]]);
    const added = rows.filter(r => r[0] === "add").length, removed = rows.filter(r => r[0] === "del").length;
    const sum = document.createElement("p");
    sum.textContent = added || removed ? added + " added, " + removed + " removed" : "The two texts are identical.";
    out.replaceChildren(sum, ...rows.map(([k, text]) => {
      const d = document.createElement("div");
      d.className = k;
      d.translate = false;
      d.textContent = (k === "add" ? "+ " : k === "del" ? "- " : "  ") + text;
      return d;
    }));
    out.hidden = false;
  });
};

CUSTOM_TOOLS["qr-code-generator"] = mount => {
  mount.className = "tool";
  mount.innerHTML = `<div class="opts"><label>Error correction<select id="q-ec"><option value="L">Low</option><option value="M" selected>Medium</option><option value="Q">Quartile</option><option value="H">High</option></select></label>
<label>Size (px)<input id="q-sz" type="number" value="320" min="128" max="1024"></label></div>
<div class="io one"><label>Text or URL<textarea id="q-t" spellcheck="false" placeholder="https://example.com" style="min-height:90px"></textarea></label></div>
<p class="err" role="alert" hidden></p>
<canvas id="q-cv" aria-label="Generated QR code" hidden></canvas>
<div class="bar"><button class="btn" id="q-dl" type="button">Download PNG</button></div>`;
  const t = q1("#q-t", mount), cv = q1("#q-cv", mount), err = q1(".err", mount);
  let lib;
  const load = () => lib || (lib = new Promise((ok, no) => {
    const s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.js";
    s.onload = () => { qrcode.stringToBytes = str => Array.from(new TextEncoder().encode(str)); ok(); };
    s.onerror = () => { lib = null; no(new Error("The QR library could not be loaded. Check your connection and reload the page.")); };
    document.head.append(s);
  }));
  const draw = async () => {
    err.hidden = true;
    if (!t.value) { cv.hidden = true; return; }
    const size = q1("#q-sz", mount).valueAsNumber;
    try {
      if (!(size >= 128 && size <= 1024)) throw new Error("Size must be from 128 to 1024 pixels.");
      await load();
      const qr = qrcode(0, q1("#q-ec", mount).value);
      try { qr.addData(t.value); qr.make(); } catch (e) { throw new Error("This text is too long for a QR code at this error-correction level."); }
      const n = qr.getModuleCount(), cell = Math.max(1, Math.floor(size / (n + 8))), full = cell * (n + 8);
      cv.width = cv.height = full;
      const ctx = cv.getContext("2d");
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, full, full);
      ctx.fillStyle = "#000";
      for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (qr.isDark(r, c)) ctx.fillRect((c + 4) * cell, (r + 4) * cell, cell, cell);
      cv.hidden = false;
    } catch (e) { cv.hidden = true; err.textContent = e.message; err.hidden = false; }
  };
  mount.addEventListener("input", draw);
  q1("#q-dl", mount).addEventListener("click", () => {
    if (cv.hidden) { err.textContent = "Enter some text first."; err.hidden = false; return; }
    cv.toBlob(b => {
      const url = URL.createObjectURL(b);
      Object.assign(document.createElement("a"), { href: url, download: "qr-code.png" }).click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
  });
};

CUSTOM_TOOLS["image-cropper"] = mount => {
  mount.className = "tool";
  mount.innerHTML = `<div class="opts"><label>Aspect ratio<select id="k-ar"><option value="0">Free</option><option value="1">1:1</option><option value="1.3333">4:3</option><option value="1.5">3:2</option><option value="1.7778">16:9</option></select></label>
<label>Output format<select id="k-fmt"><option value="png">PNG</option><option value="jpeg">JPEG</option><option value="webp">WebP</option></select></label></div>
<label class="drop"><input type="file" accept="image/jpeg,image/png,image/webp">Drop an image here or choose a file<small>Then drag on the image to select the area to keep</small></label>
<p class="err" role="alert" hidden></p>
<div id="k-res" hidden><canvas id="k-cv" aria-label="Chosen image. Drag to select the crop area."></canvas>
<div class="opts"><label>X<input id="k-x" type="number" min="0"></label><label>Y<input id="k-y" type="number" min="0"></label><label>Width<input id="k-w" type="number" min="1"></label><label>Height<input id="k-h" type="number" min="1"></label></div>
<div class="bar"><button class="btn" id="k-go" type="button">Crop and download</button></div></div>`;
  const f = id => q1("#k-" + id, mount), cv = f("cv"), ctx = cv.getContext("2d"), err = q1(".err", mount);
  let bmp = null, s = 1, sel = null, drag = null, base = "image";
  const ratio = () => +f("ar").value;
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const draw = () => {
    ctx.drawImage(bmp, 0, 0, cv.width, cv.height);
    ctx.fillStyle = "rgba(0,0,0,.5)";
    ctx.fillRect(0, 0, cv.width, sel.y);
    ctx.fillRect(0, sel.y + sel.h, cv.width, cv.height - sel.y - sel.h);
    ctx.fillRect(0, sel.y, sel.x, sel.h);
    ctx.fillRect(sel.x + sel.w, sel.y, cv.width - sel.x - sel.w, sel.h);
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 2;
    ctx.strokeRect(sel.x, sel.y, sel.w, sel.h);
    [["x", sel.x], ["y", sel.y], ["w", sel.w], ["h", sel.h]].forEach(([k, v]) => { f(k).value = Math.round(v / s); });
  };
  const fit = () => {
    const r = ratio();
    if (!r) return;
    sel.h = sel.w / r;
    if (sel.y + sel.h > cv.height) { sel.h = cv.height - sel.y; sel.w = sel.h * r; }
  };
  const pos = e => {
    const b = cv.getBoundingClientRect();
    return [clamp((e.clientX - b.left) * cv.width / b.width, 0, cv.width), clamp((e.clientY - b.top) * cv.height / b.height, 0, cv.height)];
  };
  f("ar").addEventListener("change", () => { if (bmp) { fit(); draw(); } });
  mount.addEventListener("input", e => {
    if (!bmp || e.target.type !== "number") return;
    let [x, y, w, h] = ["x", "y", "w", "h"].map(k => (+f(k).value || 0) * s);
    if (ratio()) { if (e.target.id === "k-h") w = h * ratio(); else h = w / ratio(); }
    x = clamp(x, 0, cv.width - 1); y = clamp(y, 0, cv.height - 1);
    sel = { x, y, w: clamp(w, 1, cv.width - x), h: clamp(h, 1, cv.height - y) };
    draw();
  });
  cv.addEventListener("pointerdown", e => {
    if (!bmp) return;
    const [px, py] = pos(e);
    cv.setPointerCapture(e.pointerId);
    drag = px > sel.x && px < sel.x + sel.w && py > sel.y && py < sel.y + sel.h ? { move: true, dx: px - sel.x, dy: py - sel.y } : { ax: px, ay: py };
  });
  cv.addEventListener("pointermove", e => {
    if (!drag) return;
    const [px, py] = pos(e);
    if (drag.move) { sel.x = clamp(px - drag.dx, 0, cv.width - sel.w); sel.y = clamp(py - drag.dy, 0, cv.height - sel.h); }
    else {
      let w = Math.min(Math.abs(px - drag.ax), px < drag.ax ? drag.ax : cv.width - drag.ax);
      let h = Math.min(Math.abs(py - drag.ay), py < drag.ay ? drag.ay : cv.height - drag.ay);
      const r = ratio();
      if (r) { if (w / h > r) w = h * r; else h = w / r; }
      sel = { x: px < drag.ax ? drag.ax - w : drag.ax, y: py < drag.ay ? drag.ay - h : drag.ay, w: Math.max(1, w), h: Math.max(1, h) };
    }
    draw();
  });
  ["pointerup", "pointercancel"].forEach(t => cv.addEventListener(t, () => { drag = null; }));
  dropZone(mount, async files => {
    const file = files[0];
    err.hidden = true;
    if (!file) return;
    const fail = m => { err.textContent = m; err.hidden = false; };
    if (!KEY[file.type]) return fail(file.name + " is not a JPEG, PNG or WebP image.");
    try { if (bmp) bmp.close(); bmp = await createImageBitmap(file); } catch (e) { bmp = null; return fail("This file could not be read as an image."); }
    base = file.name.replace(/\.[^.]+$/, "");
    cv.width = Math.min(bmp.width, 900);
    s = cv.width / bmp.width;
    cv.height = Math.round(bmp.height * s);
    sel = { x: cv.width * .1, y: cv.height * .1, w: cv.width * .8, h: cv.height * .8 };
    fit();
    q1("#k-res", mount).hidden = false;
    draw();
  });
  f("go").addEventListener("click", async () => {
    err.hidden = true;
    if (!bmp) return;
    const x = Math.round(sel.x / s), y = Math.round(sel.y / s);
    const w = Math.max(1, Math.min(Math.round(sel.w / s), bmp.width - x)), h = Math.max(1, Math.min(Math.round(sel.h / s), bmp.height - y));
    const key = f("fmt").value, c = document.createElement("canvas");
    c.width = w; c.height = h;
    const g = c.getContext("2d");
    if (key === "jpeg") { g.fillStyle = "#fff"; g.fillRect(0, 0, w, h); }
    g.drawImage(bmp, x, y, w, h, 0, 0, w, h);
    const blob = await new Promise(r => c.toBlob(r, MIME[key], 0.92));
    if (!blob || blob.type !== MIME[key]) { err.textContent = "Your browser cannot save " + LABEL[key] + " files. Try another format."; err.hidden = false; return; }
    const url = URL.createObjectURL(blob);
    Object.assign(document.createElement("a"), { href: url, download: base + "-cropped." + EXT[key] }).click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
};
