(() => {
  const $ = s => document.querySelector(s);
  const ar = document.documentElement.lang === "ar";
  const tr = s => (ar ? T(s) : s);
  const val = v => ar && typeof v === "string" ? v.replace(/ min$/, "") : v;
  $("#theme").addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
  });

  const q = $("#q");
  if (q) q.addEventListener("input", () => {
    const term = q.value.trim().toLowerCase();
    let shown = 0;
    document.querySelectorAll("#tools .grid li").forEach(li => {
      const hit = li.textContent.toLowerCase().includes(term);
      li.hidden = !hit;
      shown += hit;
    });
    document.querySelectorAll("#tools .cat").forEach(s => { s.hidden = !s.querySelector("li:not([hidden])"); });
    $("#popular").hidden = term !== "";
    $("#none").hidden = shown > 0;
  });

  const name = document.body.dataset.tool, spec = TOOLS[name], mount = $("#tool");
  if (mount && CUSTOM_TOOLS[name]) { CUSTOM_TOOLS[name](mount); if (ar) observeAr(mount); return; }
  if (!spec || !mount) return;

  const field = o => {
    const id = "o-" + o.id;
    if (o.type === "select") return `<label>${tr(o.label)}<select id="${id}">${o.choices.map(c => `<option value="${c[0]}">${tr(c[1])}</option>`).join("")}</select></label>`;
    if (o.type === "number") return `<label>${tr(o.label)}<input id="${id}" type="number" value="${o.value}" min="${o.min}" max="${o.max}"></label>`;
    return `<label class="chk"><input id="${id}" type="checkbox"${o.value ? " checked" : ""}>&nbsp;${tr(o.label)}</label>`;
  };
  const opts = spec.opts || [], hasInput = !spec.gen;
  mount.className = "tool";
  mount.innerHTML = `<div class="opts">${opts.map(field).join("")}</div>
<div class="io${hasInput ? "" : " one"}">
${hasInput ? `<label>${tr("Input")}<textarea id="in" dir="auto" spellcheck="false" placeholder="${tr(spec.hint || "Paste or type here")}"></textarea></label>` : ""}
${spec.stats ? `<dl class="stats" id="stats"></dl>` : `<label>${tr("Output")}<textarea id="out" dir="auto" readonly></textarea></label>`}
</div>
<p class="err" role="alert" dir="auto" hidden></p>
<div class="bar">${spec.gen ? `<button class="btn" id="run" type="button">${tr("Generate")}</button>` : ""}${spec.stats ? "" : `<button class="btn${spec.gen ? " alt" : ""}" id="copy" type="button">${tr("Copy")}</button><button class="btn alt" id="save" type="button">${tr("Download")}</button>`}${hasInput ? `<button class="btn alt" id="clear" type="button">${tr("Clear")}</button>` : ""}</div>`;

  const inp = $("#in"), out = $("#out"), err = $(".err");
  const read = () => Object.fromEntries(opts.map(o => {
    const e = $("#o-" + o.id);
    return [o.id, o.type === "check" ? e.checked : o.type === "number" ? e.valueAsNumber : e.value];
  }));
  const run = () => {
    err.hidden = true;
    try {
      const text = inp ? inp.value : "";
      if (spec.stats) $("#stats").innerHTML = spec.stats(text).map(([k, v]) => `<div><dt>${tr(k)}</dt><dd>${val(v)}</dd></div>`).join("");
      else out.value = spec.run(text, read());
    } catch (e) {
      err.textContent = tr(e.message);
      err.hidden = false;
      if (out) out.value = "";
    }
  };
  const flash = (btn, msg) => { const old = btn.textContent; btn.textContent = tr(msg); setTimeout(() => { btn.textContent = old; }, 1400); };

  if (spec.gen) $("#run").addEventListener("click", run);
  else mount.addEventListener("input", run);

  const copy = $("#copy");
  if (copy) copy.addEventListener("click", async () => {
    if (!out.value) return flash(copy, "Nothing to copy");
    try { await navigator.clipboard.writeText(out.value); } catch (e) { out.select(); document.execCommand("copy"); }
    flash(copy, "Copied");
  });
  const save = $("#save");
  if (save) save.addEventListener("click", () => {
    if (!out.value) return flash(save, "Nothing to save");
    const url = URL.createObjectURL(new Blob([out.value], { type: "text/plain" }));
    Object.assign(document.createElement("a"), { href: url, download: name + "." + (spec.ext || "txt") }).click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  const clear = $("#clear");
  if (clear) clear.addEventListener("click", () => { inp.value = ""; run(); inp.focus(); });
  run();
})();
