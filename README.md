<div align="center">

<a href="https://emrecancioglu.com">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg" />
  <img src="assets/hero-dark.svg" alt="Emre Çancıoğlu: Digitalization &amp; AI Supervisor. Bilingual résumé and cover letter built with LaTeX and Awesome-CV" width="100%" />
</picture>
</a>

**🇬🇧 English** · [🇹🇷 Türkçe](#-türkçe)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/stats-light.svg" />
  <img src="assets/stats-dark.svg" alt="9+ years experience · 3 manufacturing plants · 4 publications · 6 awards" width="100%" />
</picture>

<a href="resume.pdf"><img alt="Resume PDF" src="assets/badges/resume-pdf.svg"/></a>
<a href="resume_tr.pdf"><img alt="Özgeçmiş PDF" src="assets/badges/ozgecmis-pdf.svg"/></a>
<a href="https://emrecancioglu.com"><img alt="emrecancioglu.com" src="assets/badges/website.svg"/></a>

<img alt="LaTeX: XeTeX" src="assets/badges/latex.svg"/>
<a href="https://github.com/posquit0/Awesome-CV"><img alt="Template: Awesome-CV" src="assets/badges/template.svg"/></a>
<img alt="Languages: EN | TR" src="assets/badges/languages.svg"/>
<img alt="License: MIT" src="assets/badges/license.svg"/>

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg" />
  <img src="assets/divider-dark.svg" alt="" width="100%" />
</picture>

## 🇬🇧 English

A bilingual (EN / TR) **résumé and cover-letter** set built with LaTeX and the [Awesome-CV](https://github.com/posquit0/Awesome-CV) class. Content lives in small per-section files, so updating a single bullet point never means touching layout code.

### 📄 Documents

| Document | English | Türkçe |
|---|---|---|
| Résumé (3 pages) | [`resume.pdf`](resume.pdf) · [`resume.tex`](resume.tex) | [`resume_tr.pdf`](resume_tr.pdf) · [`resume_tr.tex`](resume_tr.tex) |
| Cover letter (1 page) | [`coverletter.pdf`](coverletter.pdf) · [`coverletter.tex`](coverletter.tex) | [`coverletter_tr.pdf`](coverletter_tr.pdf) · [`coverletter_tr.tex`](coverletter_tr.tex) |

### 👀 Preview

<table>
  <tr>
    <td align="center"><b>Résumé · EN</b><br/><a href="resume.pdf"><img src="assets/preview_resume_en.png" width="250" alt="Resume EN"/></a></td>
    <td align="center"><b>Résumé · TR</b><br/><a href="resume_tr.pdf"><img src="assets/preview_resume_tr.png" width="250" alt="Resume TR"/></a></td>
  </tr>
  <tr>
    <td align="center"><b>Cover letter · EN</b><br/><a href="coverletter.pdf"><img src="assets/preview_coverletter_en.png" width="250" alt="Cover letter EN"/></a></td>
    <td align="center"><b>Cover letter · TR</b><br/><a href="coverletter_tr.pdf"><img src="assets/preview_coverletter_tr.png" width="250" alt="Cover letter TR"/></a></td>
  </tr>
</table>

### 🗂 Repository structure

```text
├── resume.tex / resume_tr.tex              # entry points (EN / TR)
├── resume/        resume_tr/               # one file per section
│   ├── summary.tex  skills.tex  experience.tex
│   └── honors.tex  presentation.tex  certification.tex  education.tex  project.tex
├── coverletter.tex / coverletter_tr.tex    # cover-letter templates (EN / TR)
├── awesome-cv.cls                          # template class (not modified)
├── fonts/                                  # Source Sans 3, Roboto, FontAwesome
├── assets/                                 # README graphics (SVGs are generated)
└── scripts/build_readme_assets.py          # regenerates the animated SVGs
```

### 🔧 Build

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/build-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/build-light.svg" />
  <img src="assets/build-dark.svg" alt="Build: one .tex file per section → resume.tex → xelatex twice → resume.pdf" width="100%" />
</picture>

XeTeX is required (custom fonts). Compile **twice** so references resolve:

```sh
xelatex resume.tex      && xelatex resume.tex
xelatex resume_tr.tex   && xelatex resume_tr.tex
xelatex coverletter.tex && xelatex coverletter.tex
xelatex coverletter_tr.tex && xelatex coverletter_tr.tex
```

Or open the folder on [Overleaf](https://www.overleaf.com) and set the compiler to **XeLaTeX**.

> Personal images (`photo.png`, `ECANCIOGLU.png`) are git-ignored. Put your own `photo.png` next to the `.tex` files before compiling.

### ✍️ Using the cover letter as a template

Everything that must change per application is highlighted in **bold red** in the PDF:

| Placeholder | Where |
|---|---|
| `[Company Address]` / `[Şirket Adresi]` | recipient block |
| `[POSITION]` / `[POZİSYON]` | letter title, “Why Me?” section |
| `[COMPANY NAME]` / `[ŞİRKET ADI]` | “Why …?” heading and body |

Fill these in, recompile, and the red disappears only when the placeholders do. The `\ph{...}` macro (top of each cover-letter file) controls the highlight. To send a final version without red, replace its definition with `\newcommand{\ph}[1]{#1}`.

### 🇹🇷 Turkish typesetting note

The class renders some headings in small caps, which drops the dot of Turkish **İ**. The TR files override those styles and hand-type affected headings in dotted upper case (`DİJİTALLEŞME`, `MÜHENDİSİ`, …). Keep that in mind when adding new headings to Turkish files.

### 💡 Tips for bullet points

- Structure: **“Accomplished [X] as measured by [Y] by doing [Z].”**
- Start with strong verbs, keep every bullet to one or two lines, and avoid a last line with only one or two words.
- Only claim numbers you can source; scope team results as team results.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg" />
  <img src="assets/divider-dark.svg" alt="" width="100%" />
</picture>

## 🇹🇷 Türkçe

**LaTeX** ve [Awesome-CV](https://github.com/posquit0/Awesome-CV) sınıfıyla hazırlanmış, iki dilli (TR / EN) **özgeçmiş ve ön yazı** seti. İçerik bölüm bölüm ayrı dosyalarda tutulur; tek bir maddeyi güncellemek için düzen koduna dokunmak gerekmez.

### 📄 Belgeler

| Belge | Türkçe | English |
|---|---|---|
| Özgeçmiş (3 sayfa) | [`resume_tr.pdf`](resume_tr.pdf) · [`resume_tr.tex`](resume_tr.tex) | [`resume.pdf`](resume.pdf) · [`resume.tex`](resume.tex) |
| Ön yazı (1 sayfa) | [`coverletter_tr.pdf`](coverletter_tr.pdf) · [`coverletter_tr.tex`](coverletter_tr.tex) | [`coverletter.pdf`](coverletter.pdf) · [`coverletter.tex`](coverletter.tex) |

Önizlemeler yukarıdaki **Preview** bölümündedir.

### 🔧 Derleme

Özel yazı tipleri nedeniyle **XeLaTeX** gerekir. Çapraz başvuruların oturması için her dosyayı **iki kez** derleyin:

```sh
xelatex resume_tr.tex && xelatex resume_tr.tex
xelatex coverletter_tr.tex && xelatex coverletter_tr.tex
```

Overleaf kullanıyorsanız derleyiciyi **XeLaTeX** olarak seçin.

> Kişisel görseller (`photo.png`, `ECANCIOGLU.png`) `.gitignore` içindedir. Derlemeden önce kendi `photo.png` dosyanızı `.tex` dosyalarının yanına koyun.

### ✍️ Ön yazıyı şablon olarak kullanma

Her başvuruda değişmesi gereken yerler PDF'te **kalın kırmızı** görünür:

| Yer tutucu | Nerede |
|---|---|
| `[Şirket Adresi]` | alıcı bloğu |
| `[POZİSYON]` | mektup başlığı, “Neden Ben?” bölümü |
| `[ŞİRKET ADI]` | “Neden …?” başlığı ve metin |

Yer tutucuları doldurup yeniden derleyin. Kırmızı rengi tamamen kaldırmak isterseniz `\ph` makrosunu `\newcommand{\ph}[1]{#1}` olarak değiştirin.

### 🔤 Türkçe dizgi notu

Sınıf bazı başlıkları küçük büyük harfle (small caps) basar ve bu, Türkçe **İ** harfinin noktasını düşürür. TR dosyalarında bu stiller geçersiz kılınmış, ilgili başlıklar noktalı büyük harfle elle yazılmıştır (`DİJİTALLEŞME`, `MÜHENDİSİ` …). Türkçe dosyalara yeni başlık eklerken bunu unutmayın.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg" />
  <img src="assets/divider-dark.svg" alt="" width="100%" />
</picture>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/footer-light.svg" />
  <img src="assets/footer-dark.svg" alt="Typeset with XeLaTeX and Awesome-CV" width="100%" />
</picture>

**📜 License**: MIT · Template class: [Awesome-CV](https://github.com/posquit0/Awesome-CV) (LPPL / MIT)

<sub>README artwork is generated by <a href="scripts/build_readme_assets.py"><code>scripts/build_readme_assets.py</code></a>. To change the text, edit it there and run <code>python3 scripts/build_readme_assets.py</code>.</sub>

</div>
