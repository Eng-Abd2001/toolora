const rnd = n => { const lim = 2 ** 32 - (2 ** 32 % n); let x; do { x = crypto.getRandomValues(new Uint32Array(1))[0]; } while (x >= lim); return x % n; };
const count = s => Array.from(s).length;
const wordsOf = t => t.toLowerCase().match(/[\p{L}\p{N}]+/gu) || [];
const sel = (id, label, choices) => ({ id, label, type: "select", choices });
const num = (id, label, value, min, max) => ({ id, label, type: "number", value, min, max });
const chk = (id, label, value = true) => ({ id, label, type: "check", value });
const LOREM = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur".split(" ");
const sentence = () => { const w = Array.from({ length: 8 + rnd(8) }, () => LOREM[rnd(LOREM.length)]); return w[0][0].toUpperCase() + w.join(" ").slice(1) + "."; };
const uuid = () => crypto.randomUUID ? crypto.randomUUID() :
  "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, c => { const r = rnd(16); return (c === "x" ? r : (r & 3) | 8).toString(16); });

const TOOLS = {
  "word-counter": {
    stats: t => {
      const w = t.trim() ? t.trim().split(/\s+/).length : 0;
      return [["Words", w], ["Characters", count(t)], ["Without spaces", count(t.replace(/\s/g, ""))],
        ["Sentences", t.split(/[.!?؟]+(?:\s|$)/).filter(s => s.trim()).length],
        ["Paragraphs", t.split(/\n\s*\n/).filter(p => p.trim()).length],
        ["Reading time", (w ? Math.max(1, Math.round(w / 238)) : 0) + " min"]];
    }
  },
  "character-counter": {
    stats: t => [["Characters", count(t)], ["Without spaces", count(t.replace(/\s/g, ""))],
      ["Lines", t ? t.split("\n").length : 0], ["Bytes (UTF-8)", new TextEncoder().encode(t).length]]
  },
  "case-converter": {
    opts: [sel("mode", "Convert to", [["upper", "UPPERCASE"], ["lower", "lowercase"], ["title", "Title Case"], ["sentence", "Sentence case"], ["camel", "camelCase"], ["snake", "snake_case"], ["kebab", "kebab-case"]])],
    run: (t, o) => ({
      upper: t => t.toUpperCase(),
      lower: t => t.toLowerCase(),
      title: t => t.toLowerCase().replace(/(^|[\s\-(])(\p{L})/gu, (m, a, b) => a + b.toUpperCase()),
      sentence: t => t.toLowerCase().replace(/(^\s*|[.!?]\s+)(\p{L})/gu, (m, a, b) => a + b.toUpperCase()),
      camel: t => wordsOf(t).map((w, i) => i ? w[0].toUpperCase() + w.slice(1) : w).join(""),
      snake: t => wordsOf(t).join("_"),
      kebab: t => wordsOf(t).join("-")
    })[o.mode](t)
  },
  "remove-duplicate-lines": {
    hint: "Paste one item per line",
    opts: [chk("ignoreCase", "Ignore capitalisation", false), chk("trim", "Trim spaces around lines"), chk("dropEmpty", "Remove blank lines", false)],
    run: (t, o) => {
      const seen = new Set();
      return t.split(/\r?\n/).map(l => o.trim ? l.trim() : l).filter(l => {
        if (o.dropEmpty && !l.trim()) return false;
        const key = o.ignoreCase ? l.toLowerCase() : l;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      }).join("\n");
    }
  },
  "text-reverser": {
    opts: [sel("mode", "Reverse by", [["chars", "Characters"], ["words", "Words in each line"], ["lines", "Line order"]])],
    run: (t, o) => ({
      chars: t => Array.from(t).reverse().join(""),
      words: t => t.split("\n").map(l => l.trim().split(/\s+/).reverse().join(" ")).join("\n"),
      lines: t => t.split("\n").reverse().join("\n")
    })[o.mode](t)
  },
  "password-generator": {
    gen: true,
    opts: [num("length", "Length", 16, 8, 128), chk("upper", "A–Z"), chk("lower", "a–z"), chk("digits", "0–9"), chk("symbols", "Symbols")],
    run: (_, o) => {
      const sets = [["upper", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"], ["lower", "abcdefghijklmnopqrstuvwxyz"], ["digits", "0123456789"], ["symbols", "!@#$%^&*()-_=+[]{};:,.?"]]
        .filter(s => o[s[0]]).map(s => s[1]);
      if (!sets.length) throw new Error("Select at least one character type.");
      if (!(o.length >= 8 && o.length <= 128)) throw new Error("Length must be a whole number from 8 to 128.");
      const all = sets.join("");
      const out = sets.map(s => s[rnd(s.length)]);
      while (out.length < o.length) out.push(all[rnd(all.length)]);
      for (let i = out.length - 1; i > 0; i--) { const j = rnd(i + 1); [out[i], out[j]] = [out[j], out[i]]; }
      return out.join("");
    }
  },
  "uuid-generator": {
    gen: true,
    opts: [num("count", "How many", 5, 1, 100)],
    run: (_, o) => {
      if (!(o.count >= 1 && o.count <= 100)) throw new Error("Enter a number from 1 to 100.");
      return Array.from({ length: o.count }, uuid).join("\n");
    }
  },
  "random-number-generator": {
    gen: true,
    opts: [num("min", "Minimum", 1, -1e9, 1e9), num("max", "Maximum", 100, -1e9, 1e9), num("count", "How many", 5, 1, 1000), chk("unique", "No repeats", false)],
    run: (_, o) => {
      const a = Math.ceil(o.min), b = Math.floor(o.max);
      if (![a, b, o.count].every(Number.isFinite)) throw new Error("Fill in minimum, maximum and count.");
      if (a > b) throw new Error("Minimum must not be greater than maximum.");
      if (!(o.count >= 1 && o.count <= 1000)) throw new Error("Count must be from 1 to 1000.");
      const span = b - a + 1;
      if (span > 2 ** 32) throw new Error("The range is too large. Keep maximum minus minimum below 4 billion.");
      if (o.unique && o.count > span) throw new Error("Cannot pick " + o.count + " different numbers from only " + span + " possible values.");
      const out = [], seen = new Set();
      while (out.length < o.count) {
        const v = a + rnd(span);
        if (o.unique) { if (seen.has(v)) continue; seen.add(v); }
        out.push(v);
      }
      return out.join("\n");
    }
  },
  "lorem-ipsum-generator": {
    gen: true,
    opts: [num("paragraphs", "Paragraphs", 3, 1, 20)],
    run: (_, o) => {
      if (!(o.paragraphs >= 1 && o.paragraphs <= 20)) throw new Error("Choose from 1 to 20 paragraphs.");
      return Array.from({ length: o.paragraphs }, (_, p) =>
        (p ? "" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. ") + Array.from({ length: 3 + rnd(3) }, sentence).join(" ")).join("\n\n");
    }
  },
  "json-formatter": {
    ext: "json", hint: "Paste JSON here",
    opts: [sel("indent", "Format", [["2", "2 spaces"], ["4", "4 spaces"], ["min", "Minify"]])],
    run: (t, o) => {
      if (!t.trim()) return "";
      let v;
      try { v = JSON.parse(t); } catch (e) { throw new Error("Invalid JSON: " + e.message); }
      return JSON.stringify(v, null, o.indent === "min" ? 0 : +o.indent);
    }
  },
  "base64-encoder-decoder": {
    opts: [sel("mode", "Direction", [["encode", "Encode text to Base64"], ["decode", "Decode Base64 to text"]])],
    run: (t, o) => {
      if (!t) return "";
      if (o.mode === "encode") {
        let s = "";
        new TextEncoder().encode(t).forEach(b => s += String.fromCharCode(b));
        return btoa(s);
      }
      try {
        const bin = atob(t.replace(/\s/g, "").replace(/-/g, "+").replace(/_/g, "/"));
        return new TextDecoder("utf-8", { fatal: true }).decode(Uint8Array.from(bin, c => c.charCodeAt(0)));
      } catch (e) { throw new Error("This is not valid Base64 for UTF-8 text."); }
    }
  },
  "url-encoder-decoder": {
    opts: [sel("mode", "Mode", [["value", "Encode value"], ["url", "Encode full URL"], ["decode", "Decode"]])],
    run: (t, o) => {
      try { return ({ value: encodeURIComponent, url: encodeURI, decode: decodeURIComponent })[o.mode](t); }
      catch (e) { throw new Error("The input has a malformed % sequence or an unpaired surrogate character."); }
    }
  }
};

TOOLS["html-formatter"] = {
  ext: "html", hint: "Paste HTML here",
  opts: [sel("mode", "Format", [["2", "Indent 2 spaces"], ["4", "Indent 4 spaces"], ["tab", "Indent with tabs"], ["min", "Minify"]])],
  run: (t, o) => {
    if (!t.trim()) return "";
    if (o.mode === "min") return t.replace(/<!--[\s\S]*?-->/g, "").replace(/>\s+</g, "><").replace(/\s{2,}/g, " ").trim();
    const unit = o.mode === "tab" ? "\t" : " ".repeat(+o.mode);
    const VOID = /^<(area|base|br|col|embed|hr|img|input|link|meta|source|track|wbr)\b/i;
    let depth = 0;
    return t.replace(/>\s+</g, "><").split(/(<[^>]+>)/).map(s => s.trim()).filter(Boolean).map(tok => {
      if (tok.startsWith("</")) depth = Math.max(0, depth - 1);
      const line = unit.repeat(depth) + tok;
      if (/^<[a-z]/i.test(tok) && !tok.endsWith("/>") && !VOID.test(tok)) depth++;
      return line;
    }).join("\n");
  }
};
