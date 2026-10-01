"""Apply Sara Abozeina site clean-up to the existing GitHub Pages site folder.
Run: python apply_site_update.py PATH_TO_REPOSITORY
Place the accompanying teaching-portfolio.html and assets/videos next to this script.
Only removes unsupported metrics and sample reviews. Certificates remain available.
"""
import pathlib,re,shutil,sys
source=pathlib.Path(__file__).resolve().parent
if len(sys.argv)!=2: raise SystemExit('Usage: python apply_site_update.py PATH_TO_SITE_REPOSITORY')
root=pathlib.Path(sys.argv[1]).resolve()
if not (root/'index.html').exists() or not (root/'ijazahs.html').exists(): raise SystemExit('Choose the quraan022.github.io repository folder (index.html and ijazahs.html required).')
shutil.copy2(source/'teaching-portfolio.html',root/'teaching-portfolio.html')
(root/'assets'/'videos').mkdir(parents=True,exist_ok=True)
for mp4 in (source/'assets'/'videos').glob('*.mp4'): shutil.copy2(mp4,root/'assets'/'videos'/mp4.name)
for p in root.glob('*.html'):
    s=p.read_text(encoding='utf-8'); old=s
    if p.name!='teaching-portfolio.html':
        s=s.replace('href="testimonials.html" data-en="Testimonials" data-ar="آراء الطالبات">Testimonials','href="teaching-portfolio.html" data-en="Teaching Portfolio" data-ar="نماذج الشرح">Teaching Portfolio')
        s=s.replace('href="qualifications.html#demo"','href="teaching-portfolio.html"')
    if p.name=='index.html':
        s,n=re.subn(r'<div class="hero-badges" aria-label="Academy highlights">.*?</div>\s*</div>\s*</section>', '</div></div></section>',s,flags=re.S)
        if n!=1: raise RuntimeError('Homepage metric section has changed; check source before applying.')
        s=re.sub(r'<section class="section">\s*<div class="container">\s*<div class="section-head center">\s*<span class="eyebrow" data-en="Student voices".*?</section>', '',s,flags=re.S)
        s=s.replace('href="qualifications.html" data-en="View Qualifications &amp; Demo"','href="teaching-portfolio.html" data-en="View Teaching Portfolio"')
        s=s.replace('PDQT Level One · 100%','PDQT Level One').replace('PDQT Level Two · 97%','PDQT Level Two').replace('شهادة المستوى الأول · ١٠٠٪','شهادة المستوى الأول').replace('شهادة المستوى الثاني · ٩٧٪','شهادة المستوى الثاني')
        s=s.replace('Replace placeholders with verified photos and certificates.','Professional teaching portfolio and credentials.').replace('تستبدل العناصر المؤقتة بصور وشهادات موثقة.','ملف نماذج الشرح والمؤهلات.')
    elif p.name=='qualifications.html':
        s=s.replace('<strong>100%</strong>','').replace('<strong>97%</strong>','')
        s=s.replace('href="#demo" data-en="Watch Teaching Demo"','href="teaching-portfolio.html" data-en="Watch Teaching Demo"')
        s=re.sub(r'<section class="section alt" id="demo">.*?</section>', '<section class="section alt" id="demo"><div class="container"><div class="section-head"><div><span class="eyebrow" data-en="Teaching demonstrations" data-ar="نماذج الشرح">Teaching demonstrations</span><h2 data-en="Explore the Teaching Portfolio" data-ar="شاهدي نماذج الشرح">Explore the Teaching Portfolio</h2></div></div><a class="btn btn-primary" href="teaching-portfolio.html" data-en="View Three Teaching Demos" data-ar="مشاهدة الديموهات الثلاثة">View Three Teaching Demos</a></div></section>',s,flags=re.S)
    elif p.name=='testimonials.html':
        s=re.sub(r'<main class="main">.*?</main>', '<main class="main"><section class="page-hero"><div class="container"><h1 data-en="Verified feedback" data-ar="آراء موثقة">Verified feedback</h1><p data-en="Student feedback will be published only after verification and permission." data-ar="ستنشر آراء الطالبات بعد التحقق منها والحصول على موافقة النشر.">Student feedback will be published only after verification and permission.</p><a class="btn btn-primary" href="teaching-portfolio.html" data-en="Teaching Portfolio" data-ar="نماذج الشرح">Teaching Portfolio</a></div></section></main>',s,flags=re.S)
    if s!=old: p.write_text(s,encoding='utf-8')
sp=root/'sitemap.xml'
if sp.exists():
    s=sp.read_text(encoding='utf-8').replace('https://quraan022.github.io/testimonials.html','https://quraan022.github.io/teaching-portfolio.html')
    sp.write_text(s,encoding='utf-8')
# The Ijazah page currently presents textual sanad records and no embedded Ijazah photos;
# do not remove the authentic PDQT certificate images (a separate category).
print('Done. Review locally and upload changed pages, teaching-portfolio.html, and assets/videos to GitHub.')
