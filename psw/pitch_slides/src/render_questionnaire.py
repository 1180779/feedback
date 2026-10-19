"""Convert the editable questionnaire to a printable PDF source. Standard library only."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'kwestionariusz-wyboru-silnika.md').read_text()

def escape(value):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(replacements.get(c, c) for c in value)

def inline(value):
    pieces = []
    pattern = r'(\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*|`[^`]+`)'
    for item in re.split(pattern, value):
        if item.startswith('[') and '](' in item:
            label, url = item[1:].split('](', 1)
            pieces.append(r'\href{' + url[:-1].replace('%', r'\%') + '}{' + escape(label) + '}')
        elif item.startswith('**'):
            pieces.append(r'\textbf{' + escape(item[2:-2]) + '}')
        elif item.startswith('`'):
            pieces.append(r'\texttt{' + escape(item[1:-1]) + '}')
        else:
            pieces.append(escape(item))
    return ''.join(pieces)

out = [r'''\documentclass[10pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Lato}
\usepackage[margin=18mm,headheight=15pt]{geometry}
\usepackage{xcolor,hyperref,longtable,array,booktabs,fancyhdr,enumitem,titlesec}
\definecolor{accent}{HTML}{176E72}
\definecolor{ink}{HTML}{202D3A}
\hypersetup{colorlinks=true,urlcolor=accent,linkcolor=accent,pdftitle={Feedback — kwestionariusz wyboru silnika}}
\color{ink}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\setlength{\emergencystretch}{3em}
\renewcommand{\arraystretch}{1.3}
\setlist[itemize]{leftmargin=*,nosep}
\titleformat{\section}{\Large\bfseries\color{accent}}{}{0pt}{}
\titleformat{\subsection}{\large\bfseries}{}{0pt}{}
\pagestyle{fancy}\fancyhf{}
\lhead{\small FEEDBACK / WYBÓR TECHNOLOGII}
\rhead{\small DECYZJA OTWARTA}
\cfoot{\small\thepage}
\begin{document}
''']
lines = source.splitlines()
i = 0
in_list = False
while i < len(lines):
    line = lines[i]
    if in_list and not line.startswith('- '):
        out.append(r'\end{itemize}'); in_list = False
    if line.startswith('|'):
        table = []
        while i < len(lines) and lines[i].startswith('|'):
            row = [c.strip() for c in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r'[-: ]+', c) for c in row): table.append(row)
            i += 1
        count = len(table[0])
        widths = [1 / count] * count
        if count == 5: widths = [.12,.19,.22,.29,.18]
        if count == 8: widths = [.08,.055,.055,.12,.19,.19,.15,.16]
        if count == 5 and table[0][0] == 'Co sprawdzamy': widths = [.4,.15,.15,.15,.15]
        # Subtract inter-column padding from total available width.
        columns = ''.join('>{\\raggedright\\arraybackslash}p{'+f'{(174-(count*4))*v:.2f}'+'mm}' for v in widths)
        out.append(r'{\scriptsize\setlength{\tabcolsep}{2mm}\begin{longtable}{'+columns+'}')
        out.append(r'\toprule ' + ' & '.join(r'\textbf{'+inline(c)+'}' for c in table[0]) + r' \\ \midrule\endhead')
        for row in table[1:]:out.append(' & '.join(inline(c) for c in row) + r' \\ \addlinespace[2pt]')
        out.append(r'\bottomrule\end{longtable}}')
        continue
    if line.startswith('# '):
        out.append(r'{\Huge\bfseries '+inline(line[2:])+r'\par}\vspace{3mm}')
    elif line.startswith('## '):
        title = line[3:]
        if title.startswith(('Karty silników','Wspólna próba','Źródła')):out.append(r'\clearpage')
        out.append(r'\section*{'+inline(title)+'}')
    elif line.startswith('### '):out.append(r'\subsection*{'+inline(line[4:])+'}')
    elif line.startswith('- '):
        if not in_list:out.append(r'\begin{itemize}');in_list = True
        out.append(r'\item '+inline(line[2:]))
    elif not line:out.append('\n')
    else:out.append(inline(line)+'\n')
    i += 1
if in_list:out.append(r'\end{itemize}')
out.append(r'\end{document}')
(ROOT/'src'/'kwestionariusz.tex').write_text('\n'.join(out))
print('Generated src/kwestionariusz.tex')
