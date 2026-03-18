import re

# Read the CV body HTML
with open('/tmp/cv_body.html', 'r') as f:
    cv_body = f.read()

# Remove the first h1 (name), the subtitle lines, and the first hr + contact block
# We'll put those in the hero section instead
# Remove everything up to and including the first <hr /> after contact details
# The CV body starts with <h1>Dr Anjana...</h1> then <p><strong>Senior...
# We want to strip out the header portion through the first <hr /> after ORCID

# Find the position after the second <hr /> (first is after JCU line, second is after ORCID)
hrs = [m.start() for m in re.finditer(r'<hr\s*/?>', cv_body)]
if len(hrs) >= 2:
    # Start CV content after the second <hr>
    match = re.search(r'<hr\s*/?>', cv_body[hrs[1]:])
    cut_pos = hrs[1] + match.end()
    cv_content = cv_body[cut_pos:].strip()
else:
    cv_content = cv_body

# Also remove the Referees section
cv_content = re.sub(r'<h2[^>]*id="referees"[^>]*>.*?</h2>\s*<table>.*?</table>', '', cv_content, flags=re.DOTALL)
# Remove "Last updated" line
cv_content = re.sub(r'<p><em>Last updated:.*?</em></p>', '', cv_content)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dr Anjana C. Karawita — Veterinary Pathologist &amp; Genomics Researcher</title>
<meta name="description" content="Dr Anjana C. Karawita — Senior Research Scientist and Veterinary Pathologist at CSIRO ACDP, specialising in veterinary pathology, genomics, and emerging infectious diseases.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 15px; line-height: 1.6; color: #2c3e50;
    margin: 0; padding: 0; background: #f8f9fa;
  }}

  /* ─── Hero banner ─── */
  .hero {{
    background: linear-gradient(135deg, #1b2a4a 0%, #2c5282 100%);
    color: #fff; padding: 50px 20px 40px; text-align: center;
  }}
  .hero-inner {{ max-width: 700px; margin: 0 auto; }}
  .avatar {{
    width: 150px; height: 150px; border-radius: 50%;
    border: 4px solid rgba(255,255,255,0.3);
    object-fit: cover; margin-bottom: 18px;
    background: rgba(255,255,255,0.15);
  }}
  .avatar-placeholder {{
    width: 150px; height: 150px; border-radius: 50%;
    border: 4px solid rgba(255,255,255,0.3);
    margin: 0 auto 18px; display: flex; align-items: center;
    justify-content: center; font-size: 54px; font-weight: 300;
    background: rgba(255,255,255,0.12); color: rgba(255,255,255,0.8);
  }}
  .hero h1 {{ font-size: 2rem; font-weight: 700; margin: 0 0 6px; letter-spacing: -0.5px; }}
  .hero .subtitle {{ font-size: 1.05rem; font-weight: 400; opacity: 0.9; margin: 0 0 4px; }}
  .hero .affiliation {{ font-size: 0.9rem; opacity: 0.7; margin: 0 0 18px; }}
  .hero-links {{ display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }}
  .hero-links a {{
    color: #fff; text-decoration: none; font-size: 0.85rem;
    padding: 6px 14px; border: 1px solid rgba(255,255,255,0.35);
    border-radius: 20px; transition: all 0.2s;
  }}
  .hero-links a:hover {{ background: rgba(255,255,255,0.15); border-color: rgba(255,255,255,0.6); }}

  /* ─── Main content ─── */
  .content {{
    max-width: 820px; margin: 0 auto; padding: 30px 24px 60px;
    background: #fff; min-height: 100vh;
  }}
  @media (min-width: 860px) {{
    .content {{ box-shadow: 0 0 30px rgba(0,0,0,0.06); margin-top: -20px; border-radius: 8px 8px 0 0; position: relative; z-index: 1; }}
  }}

  /* ─── Typography ─── */
  h2 {{
    font-size: 1.25rem; color: #1b2a4a; font-weight: 600;
    border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;
    margin: 32px 0 14px;
  }}
  h3 {{
    font-size: 1.05rem; color: #2d3748; font-weight: 600;
    margin: 18px 0 8px;
  }}
  p {{ margin: 6px 0; }}
  a {{ color: #2b6cb0; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  strong {{ color: #1a202c; }}
  em {{ color: #718096; }}

  /* ─── Tables ─── */
  table {{
    border-collapse: collapse; width: 100%; margin: 10px 0;
    font-size: 0.88rem;
  }}
  th, td {{
    border: 1px solid #e2e8f0; padding: 7px 10px; text-align: left; vertical-align: top;
  }}
  th {{ background: #edf2f7; font-weight: 600; color: #2d3748; }}

  /* ─── Lists ─── */
  ul, ol {{ margin: 6px 0; padding-left: 22px; }}
  li {{ margin-bottom: 4px; }}

  hr {{ border: none; border-top: 1px solid #e2e8f0; margin: 24px 0; }}

  /* ─── Footer ─── */
  .footer {{
    text-align: center; padding: 20px; font-size: 0.8rem; color: #a0aec0;
    background: #f8f9fa;
  }}

  /* ─── Print ─── */
  @media print {{
    .hero {{ background: #1b2a4a !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; padding: 30px 20px; }}
    .content {{ box-shadow: none; margin-top: 0; padding: 20px; }}
    body {{ font-size: 10pt; background: #fff; }}
    h2 {{ font-size: 13pt; margin-top: 18px; }}
    h3 {{ font-size: 11pt; }}
    table {{ font-size: 9pt; }}
    @page {{ margin: 1.5cm; size: A4; }}
  }}
</style>
</head>
<body>

<!-- Hero Section -->
<header class="hero">
  <div class="hero-inner">
    <!-- Replace the placeholder below with: <img src="photo.jpg" alt="Dr Anjana C. Karawita" class="avatar"> -->
    <div class="avatar-placeholder">AK</div>
    <h1>Dr Anjana C. Karawita</h1>
    <p class="subtitle">Senior Research Scientist &middot; Veterinary Pathologist</p>
    <p class="affiliation">Australian Centre for Disease Preparedness (ACDP), CSIRO, Geelong<br>
    Adjunct Senior Research Fellow, James Cook University</p>
    <nav class="hero-links">
      <a href="mailto:anjana.karawita@csiro.au">Email</a>
      <a href="https://scholar.google.com.au/citations?user=czgmpIAAAAAJ&hl=en" target="_blank" rel="noopener">Google Scholar</a>
      <a href="https://orcid.org/0000-0003-0271-0180" target="_blank" rel="noopener">ORCID</a>
      <a href="https://www.linkedin.com/in/anjana-karawita-phd-53a54628/" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://people.csiro.au/K/A/anjana-karawita" target="_blank" rel="noopener">CSIRO Profile</a>
    </nav>
  </div>
</header>

<!-- CV Content -->
<main class="content">
{cv_content}
</main>

<footer class="footer">
  &copy; 2026 Dr Anjana C. Karawita
</footer>

</body>
</html>
'''

with open('/home/ackarawita/projects/karawita-site/index.html', 'w') as f:
    f.write(html)
print("Site built successfully")
