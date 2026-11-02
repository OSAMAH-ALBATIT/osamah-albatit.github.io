"""Formal one-page-ish CV (A4) in Arabic and English, printed to PDF with headless Edge."""
import shutil, subprocess, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent
HERE = SITE / 'tools' / 'build'; HERE.mkdir(exist_ok=True)
for f in ['photo.jpg', 'logo-mark.png']:
    shutil.copy(SITE / f, HERE / f)

CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:%(font)s;color:#1C1C22;font-size:%(fs)s;line-height:%(lh)s;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:296.5mm;overflow:hidden;display:grid;grid-template-columns:64mm 1fr}
aside{background:linear-gradient(180deg,#1C1C22 0%%,#2A1A20 70%%,#500016 100%%);color:#F5F5F5;padding:14mm 8mm}
main{padding:12mm 11mm 8mm}
.ph{width:36mm;height:36mm;border-radius:6mm;overflow:hidden;border:1.2mm solid #D3C7A6;margin:0 auto 5mm}
.ph img{width:100%%;height:100%%;object-fit:cover}
.mark{display:block;width:16mm;margin:0 auto 6mm;opacity:.95}
aside h3{font-size:9.5pt;letter-spacing:.06em;color:#D3C7A6;margin:6mm 0 2.2mm;padding-bottom:1.4mm;border-bottom:.3mm solid rgba(211,199,166,.35)}
aside p,aside li{font-size:9pt;color:#E8E3D8}
aside ul{list-style:none;display:grid;gap:1.6mm}
.ct li{display:flex;gap:2mm;align-items:center;word-break:break-all}
.ct b{color:#D3C7A6;font-weight:700;min-width:14mm}
.chips{display:flex;flex-wrap:wrap;gap:1.4mm}
.chips span{font-size:8pt;padding:.6mm 2.2mm;border-radius:3mm;background:rgba(211,199,166,.14);border:.25mm solid rgba(211,199,166,.35);color:#F5F5F5}
.lg li{display:flex;justify-content:space-between}
.lg em{font-style:normal;color:#D3C7A6}
header h1{font-size:25pt;line-height:1.1;color:#1C1C22}
header .role{font-size:12pt;color:#800020;font-weight:700;margin:1.5mm 0 4mm}
header .bar{height:.9mm;width:30mm;background:linear-gradient(90deg,#800020,#D3C7A6);border-radius:1mm;margin-bottom:5mm}
html[dir=rtl] header .bar{background:linear-gradient(270deg,#800020,#D3C7A6)}
h2{font-size:11.5pt;color:#800020;margin:5mm 0 2.4mm;display:flex;align-items:center;gap:2mm}
h2::after{content:"";flex:1;height:.3mm;background:#E4DCC8}
.sum{color:#39313A}
.job{margin-bottom:3.4mm;break-inside:avoid}
.job .top{display:flex;justify-content:space-between;align-items:baseline;gap:3mm}
.job h4{font-size:10.6pt}
.job .at{color:#800020;font-weight:700;font-size:9.6pt}
.job .when{font-size:8.6pt;color:#6B6470;white-space:nowrap}
.job ul{margin-top:1mm;padding-inline-start:4.5mm;color:#39313A}
.job li{margin:.4mm 0}
.pr{display:grid;grid-template-columns:1fr 1fr;gap:2.6mm 5mm}
.pr div{break-inside:avoid}
.pr h5{font-size:9.8pt}
.pr p{font-size:8.8pt;color:#39313A}
.pr small{display:block;font-size:7.8pt;color:#800020;margin-top:.4mm}
.pr i{font-style:normal;font-size:7.6pt;color:#6B6470}
.eda b{display:block;font-size:9.4pt;color:#F5F5F5}
.eda p{font-size:8.6pt;color:#D3C7A6;margin-top:.6mm}
.ed h4{font-size:10.4pt}
.ed p{color:#39313A;font-size:9.4pt}
"""

def build(d):
    rtl = d['dir'] == 'rtl'
    font = "'Tajawal',sans-serif" if rtl else "'Inter','Tajawal',sans-serif"
    jobs = ''.join(f"""<div class="job"><div class="top"><h4>{t}</h4><span class="when">{w2}</span></div><div class="at">{w}</div><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div>""" for t, w, w2, items in d['jobs'])
    prs = ''.join(f"""<div><h5>{h} <i>{tag}</i></h5><p>{p}</p><small>{tech}</small></div>""" for h, tag, p, tech in d['projects'])
    skills = ''.join(f'<span>{x}</span>' for x in d['skills'])
    langs = ''.join(f'<li><span>{a}</span><em>{b}</em></li>' for a, b in d['langs'])
    return f"""<!doctype html><html lang="{d['lang']}" dir="{d['dir']}"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>{CSS % {'font': font, 'fs': '10.4pt' if rtl else '9.4pt', 'lh': '1.55' if rtl else '1.45'}}</style></head><body><div class="page">
<aside>
  <div class="ph"><img src="photo.jpg"></div>
  <img class="mark" src="logo-mark.png">
  <h3>{d['t_contact']}</h3>
  <ul class="ct"><li><b>{d['l_mail']}</b>batitcr7@gmail.com</li><li><b>{d['l_phone']}</b><span dir="ltr">+90 534 606 86 80</span></li><li><b>{d['l_web']}</b>osamah-cv.web.app</li></ul>
  <h3>{d['t_skills']}</h3><div class="chips">{skills}</div>
  <h3>{d['t_langs']}</h3><ul class="lg">{langs}</ul>
  <h3>{d['t_edu']}</h3><div class="eda"><b>{d['degree']}</b><p>{d['uni']}</p></div>
</aside>
<main>
  <header><h1>{d['name']}</h1><div class="role">{d['role']}</div><div class="bar"></div></header>
  <h2>{d['t_sum']}</h2><p class="sum">{d['summary']}</p>
  <h2>{d['t_exp']}</h2>{jobs}
  <h2>{d['t_proj']}</h2><div class="pr">{prs}</div>
</main></div></body></html>"""

AR = dict(lang='ar', dir='rtl', name='أسامة محمد', role='مهندس برمجيات · مطوّر مواقع وأنظمة وتطبيقات',
  t_contact='التواصل', l_mail='البريد', l_phone='الجوال', l_web='الموقع', t_skills='المهارات', t_langs='اللغات',
  t_sum='نبذة', t_exp='الخبرات العملية', t_proj='أبرز الأعمال', t_edu='المؤهل العلمي',
  summary='هندسة برمجيات تجمع بين الخبرة التقنية والحس الإداري، لبناء حلول رقمية متكاملة من مواقع وأنظمة وتطبيقات ومنصات، تخدم أهداف الجهات وترفع كفاءة أعمالها، بمعايير عالية في الجودة والأداء وتجربة المستخدم.',
  jobs=[
    ('مهندس برمجيات ومساند إداري', 'شركة ساس لخدمات الأعمال', 'حاليًا', ['تطوير الموقع الرسمي للشركة وصيانته وتحديث محتواه.', 'بناء أنظمة داخلية للحضور والانصراف وإدارة العقود وبطاقات الموظفين.', 'المساندة الإدارية في الأعمال اليومية والملفات والتقارير.']),
    ('مشاريع خاصة', 'لعدة جهات', 'مستمر', ['تنفيذ أنظمة ومنصات ومواقع حسب احتياج كل جهة، من تحليل المتطلبات حتى التسليم والدعم.', 'إعداد الدراسة البرمجية والتنفيذية لنظام إداري ومالي.']),
    ('مساند إداري', 'جهات خاصة', 'مستمر', ['متابعة الحسابات والميزانيات، وإعداد التقارير ومحاضر الاجتماعات والتقييمات.']),
    ('عمل حر', 'مستقل', 'مستمر', ['تصميم وتطوير مواقع وتطبيقات، وتصاميم إعلانية وهويات بصرية، ومونتاج فيديوهات للسوشال ميديا.']),
  ],
  projects=[
    ('منصة الدكتور أحمد البتيت', '· albatit.com', 'منصة محتوى إسلامي متكاملة بلوحة تحكم إدارية كاملة.', 'Laravel · PHP · MySQL · Tailwind CSS'),
    ('موقع شركة ساس', '· sascc.co', 'تطوير الموقع الرسمي للشركة وتحديثه.', 'Laravel · PHP · MySQL'),
    ('نظام الحضور والانصراف', '· ساس', 'نظام موارد بشرية لعرض حضور الموظفين وإجازاتهم.', 'PHP · JavaScript'),
    ('نظام إدارة العقود', '· ساس', 'إدارة عقود مزودي الخدمات مع تنبيهات الانتهاء.', 'JavaScript · Python'),
    ('النظام العائلي', '· خاص', 'إدارة المالية والمهام بلوحة بيانات وتقارير وإشعارات.', 'React · Node.js · Express · MySQL'),
    ('لمّة — منصة ألعاب جماعية', '', 'ثلاث ألعاب جماعية أونلاين أو على جوال واحد، بثلاث لغات.', 'Node.js · WebSocket · PWA'),
    ('VulnScan AI', '· مشروع التخرج', 'فحص ثغرات تطبيقات الويب وتحليل الكود مع مستشار ذكاء اصطناعي.', 'Python · FastAPI · React · Docker'),
    ('متجر رياضي إلكتروني', '· قيد التطوير', 'متجر بسلة وطلبات ولوحة تحكم.', 'Laravel · Livewire · Tailwind CSS'),
  ],
  skills=['Laravel', 'PHP', 'MySQL', 'JavaScript', 'React', 'Node.js', 'Python', 'FastAPI', 'Tailwind CSS', 'Docker', 'تصميم الأنظمة', 'قواعد البيانات', 'الذكاء الاصطناعي', 'التصميم الجرافيكي', 'المونتاج والموشن', 'Microsoft Office'],
  langs=[('العربية', 'اللغة الأم'), ('الإنجليزية', 'جيد جدًا'), ('التركية', 'جيد جدًا')],
  degree='بكالوريوس هندسة البرمجيات (قيد الدراسة)', uni='جامعة نيشانتاشي — إسطنبول، تركيا')

EN = dict(lang='en', dir='ltr', name='Osamah Mohammed', role='Software Engineer · Web, Systems & App Developer',
  t_contact='Contact', l_mail='Email', l_phone='Phone', l_web='Web', t_skills='Skills', t_langs='Languages',
  t_sum='Profile', t_exp='Experience', t_proj='Selected work', t_edu='Education',
  summary='Software engineering that combines technical expertise with administrative insight to build complete digital solutions (websites, systems, apps and platforms) that serve an organisation\'s goals, held to high standards of quality, performance and user experience.',
  jobs=[
    ('Software Engineer & Admin Support Specialist', 'SAS Business Services', 'Present', ['Develop, maintain and update the company website.', 'Built internal attendance, contracts and staff ID card systems.', 'Administrative support for daily operations, files and reporting.']),
    ('Private Projects', 'Several organisations', 'Ongoing', ['Systems, platforms and websites tailored to each client, from analysis to handover.', 'Technical and execution study for an admin and finance system.']),
    ('Administrative Support Specialist', 'Private organisations', 'Ongoing', ['Follow-up on accounts and budgets; reports, meeting minutes and evaluations.']),
    ('Freelance', 'Independent', 'Ongoing', ['Websites and apps, ad design and visual identities, and video editing for social media.']),
  ],
  projects=[
    ('Dr. Ahmed Albatit Platform', '· albatit.com', 'A complete Islamic content platform with a full admin dashboard.', 'Laravel · PHP · MySQL · Tailwind CSS'),
    ('SAS website', '· sascc.co', 'Development and updates of the corporate website.', 'Laravel · PHP · MySQL'),
    ('Attendance System', '· SAS', 'An HR system showing employee attendance and leave.', 'PHP · JavaScript'),
    ('Contracts Management System', '· SAS', 'Service-provider contracts with expiry alerts.', 'JavaScript · Python'),
    ('Family System', '· private', 'Finances and tasks with a dashboard, reports and notifications.', 'React · Node.js · Express · MySQL'),
    ('Lamma — party games', '', 'Three party games, online or on one phone, in three languages.', 'Node.js · WebSocket · PWA'),
    ('VulnScan AI', '· graduation project', 'Web vulnerability scanning and code analysis with an AI advisor.', 'Python · FastAPI · React · Docker'),
    ('Sports e-commerce store', '· in progress', 'A store with cart, orders and an admin panel.', 'Laravel · Livewire · Tailwind CSS'),
  ],
  skills=['Laravel', 'PHP', 'MySQL', 'JavaScript', 'React', 'Node.js', 'Python', 'FastAPI', 'Tailwind CSS', 'Docker', 'System design', 'Databases', 'AI', 'Graphic design', 'Video & motion', 'Microsoft Office'],
  langs=[('Arabic', 'Native'), ('English', 'Very good'), ('Turkish', 'Very good')],
  degree='B.Sc. Software Engineering (in progress)', uni='Nişantaşı University — Istanbul, Türkiye')

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
for d, out in [(AR, 'cv-ar'), (EN, 'cv-en')]:
    (HERE / f'{out}.html').write_text(build(d), encoding='utf-8')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=6000',
                    f'--print-to-pdf={SITE / (out + ".pdf")}', (HERE / f'{out}.html').as_uri()], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('done')
