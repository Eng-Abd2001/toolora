const AR_STR = {
  "Input": "الإدخال", "Output": "الناتج", "Generate": "توليد", "Copy": "نسخ", "Download": "تنزيل", "Clear": "مسح",
  "Nothing to copy": "لا يوجد ما يُنسخ", "Copied": "تم النسخ", "Nothing to save": "لا يوجد ما يُحفظ",
  "Paste or type here": "الصق نصك أو اكتبه هنا",
  "Words": "الكلمات", "Characters": "الأحرف", "Without spaces": "بدون مسافات", "Sentences": "الجمل",
  "Paragraphs": "الفقرات", "Reading time": "مدة القراءة (دقائق)", "Lines": "الأسطر", "Bytes (UTF-8)": "البايتات (UTF-8)",
  "Reverse by": "العكس حسب", "Words in each line": "كلمات كل سطر", "Line order": "ترتيب الأسطر",
  "Paste one item per line": "الصق عنصرًا واحدًا في كل سطر", "Ignore capitalisation": "تجاهل حالة الأحرف",
  "Trim spaces around lines": "حذف المسافات حول الأسطر", "Remove blank lines": "إزالة الأسطر الفارغة",
  "Length": "الطول", "Symbols": "الرموز", "How many": "العدد",
  "Select at least one character type.": "اختر نوعًا واحدًا على الأقل من الأحرف.",
  "Length must be a whole number from 8 to 128.": "يجب أن يكون الطول عددًا صحيحًا من 8 إلى 128.",
  "Enter a number from 1 to 100.": "أدخل عددًا من 1 إلى 100."
};

Object.assign(AR_STR, {
  "Convert to": "تحويل إلى", "Minimum": "الحد الأدنى", "Maximum": "الحد الأقصى", "No repeats": "بدون تكرار",
  "Fill in minimum, maximum and count.": "املأ الحد الأدنى والحد الأقصى والعدد.",
  "Minimum must not be greater than maximum.": "يجب ألا يتجاوز الحد الأدنى الحد الأقصى.",
  "Count must be from 1 to 1000.": "يجب أن يكون العدد من 1 إلى 1000.",
  "Choose from 1 to 20 paragraphs.": "اختر من 1 إلى 20 فقرة.",
  "Paste JSON here": "الصق JSON هنا", "Format": "التنسيق", "2 spaces": "مسافتان", "4 spaces": "4 مسافات", "Minify": "ضغط (إزالة المسافات)",
  "Direction": "الاتجاه", "Encode text to Base64": "ترميز النص إلى Base64", "Decode Base64 to text": "فك ترميز Base64 إلى نص",
  "This is not valid Base64 for UTF-8 text.": "هذا ليس نص Base64 صالحًا لنص بترميز UTF-8.",
  "Mode": "الوضع", "Encode value": "ترميز قيمة", "Encode full URL": "ترميز الرابط كاملًا", "Decode": "فك الترميز",
  "The input has a malformed % sequence or an unpaired surrogate character.": "يحتوي الإدخال على تسلسل % غير صالح أو رمز يونيكود غير مكتمل.",
  "Paste HTML here": "الصق HTML هنا", "Indent 2 spaces": "إزاحة بمسافتين", "Indent 4 spaces": "إزاحة بـ 4 مسافات", "Indent with tabs": "إزاحة بعلامات تبويب"
});
const AR_PAT = [
  [/^Cannot pick (\d+) different numbers from only (\d+) possible values\.$/, (a, b) => `عدد الأرقام المطلوبة (${a}) أكبر من عدد القيم الممكنة بدون تكرار (${b}).`],
  [/^Invalid JSON: (.*)$/, m => "JSON غير صالح: " + m]
];

Object.assign(AR_STR, {
  "Output format": "صيغة الإخراج", "Same as original": "نفس صيغة الأصل", "Quality": "الجودة", "Width (px)": "العرض (بكسل)", "Height (px)": "الارتفاع (بكسل)",
  "auto": "تلقائي", "Keep aspect ratio": "الحفاظ على النسبة", "Drop images here or choose files": "أسقط الصور هنا أو اختر ملفات",
  "JPEG, PNG or WebP": "JPEG أو PNG أو WebP", "JPEG files": "ملفات JPEG", "PNG files": "ملفات PNG", "WebP, JPEG or PNG": "WebP أو JPEG أو PNG",
  "unknown file type": "غير معروف",
  "This file could not be read as an image. It may be damaged.": "تعذّرت قراءة هذا الملف كصورة. ربما هو تالف.",
  "This file could not be read as an image.": "تعذّرت قراءة هذا الملف كصورة.",
  "The output size is too large for the browser. Use smaller dimensions.": "حجم الإخراج أكبر مما يحتمله المتصفح. استخدم أبعادًا أصغر.",
  "Include the data:image prefix": "تضمين البادئة data:image", "Drop an image here or choose a file": "أسقط صورة هنا أو اختر ملفًا",
  "Up to 5 MB": "حتى 5 ميغابايت", "Base64 output": "ناتج Base64", "Preview of the chosen image": "معاينة الصورة المختارة",
  "The file could not be read.": "تعذّرت قراءة الملف.", "Copy failed": "تعذّر النسخ",
  "Then click or tap the colour you want": "ثم انقر أو المس اللون الذي تريده",
  "Chosen image. Click or tap to pick a colour.": "الصورة المختارة. انقر أو المس لالتقاط لون.", "transparent": "شفاف",
  "Aspect ratio": "نسبة العرض إلى الارتفاع", "Free": "حرة", "Width": "العرض", "Height": "الارتفاع",
  "Then drag on the image to select the area to keep": "ثم اسحب على الصورة لتحديد المنطقة التي تريد الإبقاء عليها",
  "Chosen image. Drag to select the crop area.": "الصورة المختارة. اسحب لتحديد منطقة القص.", "Crop and download": "قص وتنزيل"
});
AR_PAT.push(
  [/^Skipped: (.*) is not supported here\.$/, t => `تم التخطي: النوع ${T(t)} غير مدعوم هنا.`],
  [/^Processing (\d+) of (\d+)…$/, (a, b) => `جارٍ المعالجة (${a} من ${b})…`],
  [/^(.+) to (.+) \(([+-]?\d+)%\), (\d+)×(\d+) px$/, (a, b, c, w, h) => `${a} إلى ${b} (\u200E${c}%)، ${w}×${h} بكسل`],
  [/^Your browser cannot save (.*) files\. Try another (browser|format)\.$/, (l, k) => `لا يستطيع متصفحك حفظ ملفات ${l}. جرّب ${k === "browser" ? "متصفحًا آخر" : "صيغة أخرى"}.`],
  [/^(.*) is not a JPEG, PNG or WebP image\.$/, f => `الملف ${f} ليس صورة JPEG أو PNG أو WebP.`],
  [/^(.*) is not an image file\.$/, f => `الملف ${f} ليس ملف صورة.`],
  [/^This image is (.*)\. The limit is 5 MB\.$/, s => `حجم هذه الصورة ${s}، والحد الأقصى 5 ميغابايت.`],
  [/^(.*)\. Settings apply to the files you add next\.$/, h => `${T(h)}. تُطبَّق الإعدادات على الملفات التي تضيفها لاحقًا.`]
);
const T = s => {
  if (AR_STR[s]) return AR_STR[s];
  for (const [re, fn] of AR_PAT) { const m = s.match(re); if (m) return fn(...m.slice(1)); }
  return s;
};
const observeAr = root => {
  const attrs = ["placeholder", "aria-label", "alt"];
  const run = node => {
    const w = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentElement && n.parentElement.closest("[translate=no]") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    for (let n; (n = w.nextNode());) {
      const t = n.nodeValue.trim(), r = t && T(t);
      if (r && r !== t) n.nodeValue = n.nodeValue.replace(t, () => r);
    }
    node.querySelectorAll("[placeholder],[aria-label],[alt]").forEach(e => attrs.forEach(a => {
      const v = e.getAttribute(a);
      if (v && T(v) !== v) e.setAttribute(a, T(v));
    }));
  };
  run(root);
  new MutationObserver(ms => ms.forEach(m => {
    if (m.type === "characterData") run(m.target.parentNode);
    m.addedNodes.forEach(n => run(n.nodeType === 1 ? n : n.parentNode));
  })).observe(root, { childList: true, characterData: true, subtree: true });
};

Object.assign(AR_STR, {
  "Drop files here or choose files": "أسقط الملفات هنا أو اختر ملفات", "Drop a file here or choose a file": "أسقط ملفًا هنا أو اختر ملفًا",
  "Add two or more PDFs, then set their order": "أضف ملفَّي PDF أو أكثر ثم رتّبها", "One PDF file": "ملف PDF واحد", "JPEG or PNG images": "صور JPEG أو PNG",
  "Merge PDFs": "دمج الملفات", "Split PDF": "تقسيم PDF", "Extract pages": "استخراج الصفحات", "Rotate PDF": "تدوير PDF",
  "Create PDF": "إنشاء PDF", "Convert pages": "تحويل الصفحات", "Compress PDF": "ضغط PDF", "Up": "أعلى", "Down": "أسفل", "Remove": "إزالة",
  "Page ranges": "نطاقات الصفحات", "Pages to keep": "الصفحات المراد إبقاؤها", "Rotate clockwise by": "التدوير مع عقارب الساعة بمقدار",
  "Pages (empty = all)": "الصفحات (فارغ = الكل)", "Page size": "حجم الصفحة", "Same as each image": "مطابق لكل صورة", "A4 with margin": "A4 بهامش",
  "Resolution": "الدقة", "Standard (1x)": "عادية (1x)", "High (2x)": "عالية (2x)", "Very high (3x)": "عالية جدًا (3x)", "Image quality": "جودة الصورة",
  "72 dpi (smallest)": "72 نقطة/بوصة (الأصغر)", "110 dpi": "110 نقاط/بوصة", "150 dpi (sharper)": "150 نقطة/بوصة (أوضح)",
  "Add at least two PDF files to merge.": "أضف ملفَّي PDF على الأقل للدمج.", "Add at least one file first.": "أضف ملفًا واحدًا على الأقل أولًا.",
  "Choose a file first.": "اختر ملفًا أولًا.", "Enter at least one page or range, for example 1-3, 5.": "أدخل صفحة أو نطاقًا واحدًا على الأقل، مثل 1-3, 5.",
  "A required library could not be loaded. Check your connection and reload the page.": "تعذّر تحميل مكتبة مطلوبة. تحقق من اتصالك وأعد تحميل الصفحة.",
  "This tool turns every page into an image and rebuilds the PDF. Scans and image-heavy files often shrink a lot, but text can no longer be selected or searched, and vector graphics lose sharpness. PDFs that are mostly text usually get larger.":
    "تحوّل هذه الأداة كل صفحة إلى صورة وتعيد بناء ملف PDF. غالبًا ما تنكمش الملفات الممسوحة ضوئيًا والغنية بالصور كثيرًا، لكن لا يمكن بعد ذلك تحديد النص أو البحث فيه، وتفقد الرسومات المتجهة حدّتها. أما ملفات PDF النصية في معظمها فيكبر حجمها عادةً.",
  "Ignore spaces at the end of lines": "تجاهل المسافات في نهاية الأسطر", "Original": "الأصل", "Changed": "المعدَّل",
  "Paste the original text": "الصق النص الأصلي", "Paste the changed text": "الصق النص المعدَّل", "Compare": "مقارنة",
  "Enter text in at least one box.": "أدخل نصًا في أحد المربعين على الأقل.",
  "These texts are too long to compare. Keep each under about 2,000 lines.": "النصان أطول من أن يُقارَنا. اجعل كل نص أقل من نحو 2000 سطر.",
  "The two texts are identical.": "النصان متطابقان.",
  "Error correction": "تصحيح الأخطاء", "Low": "منخفض", "Medium": "متوسط", "Quartile": "ربعي", "High": "عالٍ", "Size (px)": "الحجم (بكسل)",
  "Text or URL": "نص أو رابط", "Generated QR code": "رمز QR المُنشأ", "Download PNG": "تنزيل PNG",
  "The QR library could not be loaded. Check your connection and reload the page.": "تعذّر تحميل مكتبة رمز QR. تحقق من اتصالك وأعد تحميل الصفحة.",
  "Size must be from 128 to 1024 pixels.": "يجب أن يكون الحجم من 128 إلى 1024 بكسل.",
  "This text is too long for a QR code at this error-correction level.": "هذا النص أطول من أن يتسع في رمز QR بمستوى تصحيح الأخطاء هذا.",
  "Enter some text first.": "أدخل نصًا أولًا."
});
const arPages = n => n == 1 ? "صفحة واحدة" : n == 2 ? "صفحتان" : n <= 10 ? n + " صفحات" : n + " صفحة";
AR_PAT.push(
  [/^Adding file (\d+) of (\d+)…$/, (a, b) => `جارٍ إضافة الملف ${a} من ${b}…`],
  [/^Adding image (\d+) of (\d+)…$/, (a, b) => `جارٍ إضافة الصورة ${a} من ${b}…`],
  [/^Page (\d+) of (\d+)…$/, (a, b) => `الصفحة ${a} من ${b}…`],
  [/^(\d+) pages?, (.+)$/, (n, s) => `${arPages(+n)}، ${s}`],
  [/^(\d+) of (\d+) pages rotated, (.+)$/, (a, b, s) => `الصفحات المدوَّرة: ${a} من ${b}، ${s}`],
  [/^(\d[\d.]* [KM]B) to (\d[\d.]* [KM]B)(\. The result is not smaller, so keep the original\.)?$/, (a, b, m) => `${a} إلى ${b}${m ? ". النتيجة ليست أصغر، فاحتفظ بالملف الأصلي." : ""}`],
  [/^(\d+)×(\d+) px, (.+)$/, (w, h, s) => `${w}×${h} بكسل، ${s}`],
  [/^Skipped (.*): unsupported file type\.$/, f => `تم التخطي (${f}): نوع الملف غير مدعوم.`],
  [/^(.*) could not be opened\. It may be damaged or password-protected\.$/, f => `تعذّر فتح الملف ${f}. ربما هو تالف أو محمي بكلمة مرور.`],
  [/^“(.*)” is not a valid page or range\. Use a format such as 1-3, 5, 8-\.$/, t => `«${t}» ليست صفحة أو نطاقًا صالحًا. استخدم صيغة مثل 1-3, 5, 8-.`],
  [/^“(.*)” is outside this PDF, which has (\d+) pages\.$/, (t, n) => `«${t}» خارج حدود هذا الملف (عدد صفحاته ${n}).`],
  [/^(.*) could not be read as a valid (PNG|JPEG) image\.$/, (f, t) => `تعذّرت قراءة الملف ${f} كصورة ${t} صالحة.`],
  [/^This PDF has (\d+) pages\. The limit is 100 per run\.$/, n => `يحتوي هذا الملف على ${n} صفحة. الحد الأقصى 100 صفحة في المرة الواحدة.`],
  [/^Page (\d+) is too large at this resolution\. Choose a lower resolution\.$/, n => `الصفحة ${n} كبيرة جدًا بهذه الدقة. اختر دقة أقل.`],
  [/^(\d+) added, (\d+) removed$/, (a, b) => `المضاف: ${a}، المحذوف: ${b}`]
);

Object.assign(AR_STR, {
  "The range is too large. Keep maximum minus minimum below 4 billion.": "النطاق كبير جدًا. اجعل الفرق بين الحد الأقصى والحد الأدنى أقل من 4 مليارات."
});

Object.assign(AR_STR, {
  "UPPERCASE": "أحرف كبيرة (UPPERCASE)", "lowercase": "أحرف صغيرة (lowercase)",
  "Title Case": "أول كل كلمة كبير (Title Case)", "Sentence case": "أول الجملة كبير (Sentence case)"
});
