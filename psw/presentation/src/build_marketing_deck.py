"""Build an editable PPTX pitch from project documents, using only Python stdlib.

Run from any directory. PDF is exported by export_pitch_pdf.py.
Diagrams and text are editable native PowerPoint shapes; original Figma artwork
is embedded as transparent PNGs. Source SVGs and provenance are retained.
"""
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZIP_DEFLATED
import math

ROOT = Path(__file__).resolve().parents[1]
W, H, UNIT = 1600, 900, 7620
BG='0D1120'; PANEL='171E31'; GRID='253149'; WHITE='F1F4FC'
MUTED='9FADC5'; CYAN='73E2CE'; VIOLET='A79AFF'; AMBER='FFB477'; RED='EC809B'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS=f'xmlns:a="{A}" xmlns:p="{P}" xmlns:r="{R}"'
slides=[]

def emu(v): return str(round(v*UNIT))
def col(c): return '<a:solidFill><a:srgbClr val="'+c+'"/></a:solidFill>'
def transform(x,y,w,h,rotation=0):
    rot=f' rot="{int(rotation*60000)}"' if rotation else ''
    return f'<a:xfrm{rot}><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'

class Slide:
    def __init__(self, section, title, note, tag=''):
        self.parts=[]; self.images=[]; self.counter=1;self.note=note;self.title=title
        slides.append(self)
        self.rect(0,0,W,H,BG)
        self.text(72,42,1200,30,section.upper(),19,CYAN,True)
        if title:self.text(72,105,1455,95,title,62,WHITE,True)
        self.line(72,839,1528,839,GRID,1)
        self.text(72,856,760,23,'FEEDBACK  /  KONCEPCJA GRY',17,MUTED)
        self.text(650,856,800,23,tag,17,MUTED,align='r')
        self.text(1465,853,63,27,f'{len(slides):02}',20,CYAN,True,align='r')
    def shape(self,x,y,w,h,kind='rect',fill=None,stroke=None,sw=2,rotation=0):
        self.counter+=1;i=self.counter
        props=transform(x,y,w,h,rotation)+f'<a:prstGeom prst="{kind}"><a:avLst/></a:prstGeom>'
        props+=col(fill) if fill else '<a:noFill/>'
        props+=f'<a:ln w="{int(sw*UNIT)}">{col(stroke)}</a:ln>' if stroke else '<a:ln><a:noFill/></a:ln>'
        self.parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Shape {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>{props}</p:spPr></p:sp>')
    def rect(self,x,y,w,h,fill,stroke=None,sw=2):self.shape(x,y,w,h,fill=fill,stroke=stroke,sw=sw)
    def circle(self,x,y,d,fill=None,stroke=None,sw=2):self.shape(x,y,d,d,'ellipse',fill,stroke,sw)
    def text(self,x,y,w,h,value,size=32,color=WHITE,bold=False,align='l'):
        self.counter+=1;i=self.counter
        paragraphs=[]
        for line in value.split('\n'):
            paragraphs.append(f'<a:p><a:pPr algn="{align}"><a:lnSpc><a:spcPct val="110000"/></a:lnSpc><a:spcAft><a:spcPts val="0"/></a:spcAft></a:pPr><a:r><a:rPr lang="pl-PL" sz="{round(size*60)}" b="{1 if bold else 0}" dirty="0">{col(color)}<a:latin typeface="Lato"/><a:ea typeface="Lato"/><a:cs typeface="Lato"/></a:rPr><a:t>{escape(line)}</a:t></a:r><a:endParaRPr lang="pl-PL" sz="{round(size*60)}"/></a:p>')
        props=transform(x,y,w,h)+'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln>'
        self.parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Text {i}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>{props}</p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"/><a:lstStyle/>{"".join(paragraphs)}</p:txBody></p:sp>')
    def line(self,x1,y1,x2,y2,color=CYAN,sw=4,arrow=False,dash=False):
        self.counter+=1;i=self.counter
        x,y=min(x1,x2),min(y1,y2);w,h=abs(x2-x1),abs(y2-y1)
        flip=(' flipH="1"' if x2<x1 else '')+(' flipV="1"' if y2<y1 else '')
        xf=f'<a:xfrm{flip}><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
        ln=f'<a:ln w="{int(sw*UNIT)}" cap="rnd">{col(color)}'+('<a:prstDash val="dash"/>' if dash else '')+('<a:tailEnd type="triangle" w="med" len="med"/>' if arrow else '')+'</a:ln>'
        self.parts.append(f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{i}" name="Line {i}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr>{xf}<a:prstGeom prst="line"><a:avLst/></a:prstGeom>{ln}</p:spPr></p:cxnSp>')
    def photo(self,x,y,w,h,name,flip=False):
        self.images.append(name);rid='img'+str(len(self.images));self.counter+=1;i=self.counter
        photo_transform=transform(x,y,w,h).replace('<a:xfrm>', '<a:xfrm flipH="1">') if flip else transform(x,y,w,h)
        self.parts.append(f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="{escape(name)}" descr="Grafika odzyskana z Feedback mockup.make; statyczny kadr makiety."/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr>{photo_transform}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    def pill(self,x,y,w,label,color=CYAN):
        self.rect(x,y,w,38,PANEL,color,1)
        self.text(x+14,y+7,w-28,26,label,18,color,True)
    def player(self,x,y,s=1,shield=False,left=False):
        # Match the original figure's head/feet placement without changing art.
        k=76/46
        pose='player-parry' if shield else 'player-idle'
        self.photo(x+(20-(40 if left else 32)*k)*s,y-10*k*s,72*k*s,64*k*s,
                   'figma-characters/'+pose+'.png',flip=left)
    def enemy(self,x,y,s=1,melee=False):
        # The supplied mockup has one enemy design; use it as a visual reference.
        self.photo(x-18*s,y-20*s,48*1.65*s,56*1.65*s,'figma-characters/enemy.png')
    def switch(self,x,y,s=1,active=False):
        c=CYAN if active else MUTED
        self.rect(x,y,28*s,44*s,PANEL,c,2*s)
        self.circle(x+7*s,y+9*s,14*s,c)
        self.rect(x-5*s,y+44*s,38*s,9*s,GRID)
    def platform(self,x,y,w,h=20):
        self.rect(x,y,w,h,GRID)
        self.rect(x,y,w,4,MUTED)
        for a in range(int(x)+20,int(x+w)-10,65):self.rect(a,y+10,18,4,PANEL)
    def sparks(self,x,y,r=50,c=CYAN):
        for a in [-65,-30,5,40,75,110,145,180,215]:
            t=math.radians(a)
            self.line(x+math.cos(t)*r,y+math.sin(t)*r,x+math.cos(t)*(r+15),y+math.sin(t)*(r+15),c,3)

# 1 — A hook, supported by a conceptual action drawing.
s=Slide('Pitch projektu','',
'''[0:00–0:30] Feedback opiera się na prostym pomyśle: siła przeciwnika może stać się naszym następnym ruchem. Parowanie pozwala odbijać pociski, pokonywać przeszkody i rozwiązywać zagadki. Przedstawiamy koncepcję gry na podstawie dokumentów projektu.
Ilustracja jest schematem koncepcyjnym przygotowanym do prezentacji, a nie zrzutem gry. Hasło jest propozycją redakcyjną.
Źródło: feedback/deadline_3/specyfikacja/specyfikacja.tex, Wprowadzenie i Opis gry.''',
'Schemat koncepcyjny')
s.text(72,165,850,150,'FEEDBACK',136,WHITE,True)
s.rect(76,312,112,7,CYAN)
s.text(72,355,800,190,'Siła przeciwnika.\nTwój następny ruch.',66,WHITE,True)
s.text(76,602,665,90,'Parowanie, które pozwala\nprzetrwać, poruszać się i odkrywać drogę.',30,MUTED)
s.pill(76,739,330,'KONCEPCJA GRY 2D')
for x in [1000,1120,1240,1360,1480]:s.line(x,250,x,760,GRID,1)
s.platform(933,701,563)
s.player(1125,475,2.5,True)
s.enemy(1410,552,1.9)
s.line(1390,576,1305,576,AMBER,7,True)
s.circle(1280,563,26,AMBER)
s.line(1220,482,1030,363,CYAN,7,True)
s.circle(1032,350,20,CYAN)
s.sparks(1175,560,120)
s.text(1000,770,470,32,'Ruch zaczyna się od parowania.',23,CYAN,align='r')

# 2 — Three applications of one mechanic.
s=Slide('01 / Obietnica gry','Każdy atak to okazja.',
'''[0:30–1:10] Jedna mechanika ma trzy zastosowania. Możemy oddać przeciwnikowi jego pocisk, przejąć pęd ataku fizycznego i użyć odbitego pocisku do uruchomienia elementu otoczenia. Przeciwnik jest zarówno zagrożeniem, jak i częścią rozwiązania. To opis projektowanej mechaniki, nie deklaracja ukończonej implementacji.
Źródło: specyfikacja.tex, trzy filary; req.tex, WF-03–WF-05 i WF-13.''',
'Schematy koncepcyjne')
cards=[(72,'01','Odbij pocisk','Wykorzystaj atak przeciwnika.',CYAN),(566,'02','Przejmij pęd','Dotrzyj dalej dzięki parowaniu.',VIOLET),(1060,'03','Otwórz drogę','Uruchom element otoczenia.',AMBER)]
for x,n,title,body,c in cards:
    s.rect(x,257,468,489,PANEL)
    s.text(x+30,280,100,42,n,28,c,True)
    s.text(x+30,593,410,58,title,42,WHITE,True)
    s.text(x+30,660,410,55,body,25,MUTED)
s.player(282,395,1.45,True,left=True);s.line(245,440,140,440,CYAN,7,True);s.circle(178,427,23,CYAN)
s.player(658,468,1.2,True,left=True);s.line(750,490,890,366,VIOLET,6,True);s.platform(853,392,111);s.player(879,318,.85)
s.switch(1403,391,1.5,True);s.line(1333,430,1200,430,AMBER,6,True);s.circle(1250,418,23,AMBER);s.rect(1154,392,22,96,GRID);s.rect(1149,371,35,9,CYAN)
s.text(72,782,1456,38,'Przeciwnik jest częścią zagadki.',30,CYAN,True)

# 3 — A clear three-frame puzzle storyboard.
s=Slide('02 / Przykład interakcji','Zagrożenie staje się rozwiązaniem.',
'''[1:10–1:55] Oto schemat jednej interakcji, a nie gotowy projekt poziomu. Po lewej przeciwnik wysyła pocisk w stronę gracza. W środku gracz paruje i odwraca jego kierunek. Po prawej odbity pocisk trafia przełącznik, który otwiera drzwi. Przełącznik reaguje na pocisk po odbiciu. Pozostaje przejść dalej. Ten przykład pokazuje połączenie obserwacji, timingu i zagadki.
Schemat nie ustala finalnego układu poziomów ani oprawy. Źródło: req.tex, WF-04 i WF-13.''',
'Storyboard koncepcyjny')
for idx,x in enumerate([72,566,1060]):
    s.rect(x,264,468,382,PANEL)
    s.text(x+26,283,415,38,['1  Sprowokuj','2  Sparuj','3  Przejdź'][idx],29,[AMBER,CYAN,VIOLET][idx],True)
    s.platform(x+25,560,418)
    s.enemy(x+42,483,.95)
    s.player(x+314,480,1,idx==1,left=True)
    s.switch(x+193,505,1,idx==2)
    s.rect(x+401,439,12,121,GRID)
    s.rect(x+390,424,35,12,CYAN if idx==2 else MUTED)
    if idx<2:s.rect(x+392,444,28,116,MUTED)
    else:
        for yy in [452,477,502,527]:s.line(x+402,yy,x+402,yy+11,CYAN,2)
    if idx==0:
        s.line(x+111,518,x+280,518,AMBER,5,True)
        s.circle(x+255,508,18,AMBER)
    elif idx==1:
        s.line(x+285,518,x+238,518,CYAN,5,True)
        s.circle(x+263,507,20,CYAN)
    else:
        s.line(x+354,600,x+424,600,VIOLET,5,True)
    s.text(x+26,679,419,92,[
        'Obserwujesz atak\ni wybierasz moment.',
        'Odbijasz pocisk\nw stronę przełącznika.',
        'Przełącznik otwiera drzwi.\nMożesz ruszyć dalej.'
    ][idx],29,WHITE)

# 4 — The second major interaction: movement through parry.
s=Slide('03 / Ruch','Sparuj. Wykorzystaj pęd.',
'''[1:55–2:30] Drugie zastosowanie parowania to ruch. Udane sparowanie ataku fizycznego może nadać postaci pęd i pozwolić dotrzeć na wyższą lub dalszą platformę. Gracz musi więc zaplanować nie tylko moment parowania, lecz także to, gdzie chce się znaleźć po nim.
Strzałki ilustrują ideę transferu pędu; nie przedstawiają pomiaru trajektorii ani ustalonego modelu fizyki. Źródło: req.tex, WF-05; specyfikacja.tex, Manipulacja fizyką i momentum.''',
'Schemat koncepcyjny')
s.rect(72,247,1040,530,PANEL)
s.platform(110,672,370)
s.platform(800,421,265)
s.enemy(241,570,1.55,melee=True)
s.player(410,537,1.6,True,left=True)
s.line(348,607,385,607,AMBER,5,True)
pts=[(487,570),(535,504),(590,445),(649,399),(710,370),(772,359),(833,366),(878,387)]
for i in range(len(pts)-1):s.line(*pts[i],*pts[i+1],VIOLET,5,arrow=i==len(pts)-2,dash=True)
s.player(925,328,1.2)
s.sparks(441,601,65)
s.text(125,711,600,39,'Atak → parowanie → zmiana ruchu',27,CYAN,True)
s.text(1160,320,370,100,'Twoja obrona\nwyznacza trasę.',41,WHITE,True)
s.text(1160,490,360,135,'Ten sam przycisk.\nNowe zastosowanie.\nInna droga przez poziom.',29,MUTED)

# 5 — Skill progression and fast retries.
s=Slide('04 / Doświadczenie gracza','Zobacz. Zaplanuj. Wykonaj.',
'''[2:30–3:05] Chcemy, żeby każdy poziom zaczynał się od zrozumienia sytuacji, a kończył płynnym wykonaniem. Pomyłka prowadzi do szybkiej kolejnej próby. Postęp wynika z poznania zasad, rozpoznawania ataków i doskonalenia własnego timingu. Nie pokazujemy tu obiecanego czasu przejścia ani wyników playtestów.
Źródło: specyfikacja.tex, Gameplay loop i Progression loop; req.tex, WF-11.''',
'Schemat pętli rozgrywki')
for x,n,title,body,c in [(72,'1','Obserwacja','Rozpoznajesz atak\ni układ przeszkód.',AMBER),(566,'2','Plan','Wybierasz moment\ni sposób użycia parry.',VIOLET),(1060,'3','Wykonanie','Łączysz refleks\nz rozwiązaniem zagadki.',CYAN)]:
    s.circle(x+126,272,180,None,c,3)
    s.text(x+126,307,180,110,n,86,c,True,align='ctr')
    s.text(x,496,468,60,title,44,WHITE,True,align='ctr')
    s.text(x,578,468,86,body,29,MUTED,align='ctr')
s.line(409,364,532,364,MUTED,4,True)
s.line(903,364,1026,364,MUTED,4,True)
s.line(1276,710,1276,755,CYAN,3)
s.line(1276,755,287,755,CYAN,3,True)
s.text(511,716,640,37,'Pomyłka → szybka kolejna próba',28,CYAN,True,align='ctr')

# 6 — Audience, based on stated design intent rather than invented market data.
s=Slide('05 / Dla kogo','Refleks spotyka łamigłówkę.',
'''[3:05–3:40] Projekt kierujemy do osób, które lubią wyzwania zręcznościowe i jednocześnie szukają logicznej satysfakcji ze zrozumienia poziomu. Punkt wspólny to frajda z opanowania jednej mechaniki i odkrywania jej kolejnych zastosowań. To grupa docelowa opisana w materiałach, a nie wynik przeprowadzonych badań rynku.
Źródło: specyfikacja.tex, Użytkownicy; deadline_1/value proposition canvas.pdf.''',
'Grupa docelowa z dokumentacji')
s.circle(160,261,440,None,VIOLET,4)
s.circle(482,261,440,None,CYAN,4)
s.text(213,441,300,66,'REFLEKS',49,VIOLET,True,align='ctr')
s.text(573,441,300,66,'ZAGADKI',49,CYAN,True,align='ctr')
s.circle(515,446,54,WHITE)
s.text(160,738,760,44,'Satysfakcja z opanowania mechaniki',28,WHITE,True,align='ctr')
for y,n,t,c in [(299,'01','Wyczucie właściwego momentu',VIOLET),(447,'02','Odkrywanie zależności',CYAN),(595,'03','Coraz płynniejsze przejścia',AMBER)]:
    s.text(1042,y,86,37,n,24,c,True)
    s.rect(1042,y+52,42,4,c)
    s.text(1114,y-2,389,105,t,35,WHITE,True)

# 7 — Actual user-supplied visual evidence.
s=Slide('06 / Pierwszy kierunek wizualny','',
'''[3:40–4:10] To jest istniejący mockup menu oraz oryginalna postać z dostarczonego pliku Figma Make. Po prawej widzimy neutralną pozę oraz klatkę animacji parowania mieczem. To statyczne kadry odzyskanych komponentów SVG, nie przerysowane postacie. Traktujemy go jako kierunek do dalszej rozmowy, nie jako zatwierdzoną oprawę całej gry. Etykieta wersji w obrazie należy do makiety i nie oznacza wydanej wersji gry.
Źródło grafiki: Feedback mockup.make, images/00131dcf29b7204da054f6a204fc6d419a773f8a. Oryginalny obraz menu, bez zmiany treści, zachowane proporcje. Postać: CharacterShowcase.tsx, neutralna poza i pierwszy utrzymany klucz parry. Źródła SVG zapisano w assets/figma-characters/.''',
'Oryginalny mockup • Figma Make')
s.title='Pierwszy obraz świata Feedback.'
s.rect(72,111,793,670,PANEL,GRID,1)
s.photo(82,121,773,652.21875,'figma-menu.png')
s.pill(931,146,306,'ISTNIEJĄCY MOCKUP',CYAN)
s.text(930,235,595,155,'Pierwszy obraz\nświata Feedback.',59,WHITE,True)
s.photo(929,439,225,200,'figma-characters/player-idle.png')
s.photo(1229,439,225,200,'figma-characters/player-parry.png')
s.text(929,659,225,40,'Spoczynek',25,MUTED,align='ctr')
s.text(1229,659,225,40,'Parowanie',25,MUTED,align='ctr')
s.text(933,731,580,57,'Postać i menu z istniejącej makiety',22,CYAN)

# 8 — Explicitly planned scope; no invented progress numbers or dates.
s=Slide('07 / Planowany prototyp','Jedna mechanika. Różne wyzwania.',
'''[4:10–4:45] Zapisany w specyfikacji zakres prototypu obejmuje co najmniej trzy poziomy, dwa typy przeciwników oraz trzy podstawowe akcje: ruch, skok i parowanie. To zakres planowany. Nie przedstawiamy tych liczb jako stanu ukończenia. Celem jest sprawdzenie, czy różne zastosowania parowania tworzą przyjemną grę.
Źródło: specyfikacja.tex, Cel projektu; req.tex, WF-01–WF-03, WF-07–WF-08 i WF-12. Aktualność zakresu pozostaje do potwierdzenia przez zespół, zgodnie z kwestionariuszem.''',
'Zakres zapisany w specyfikacji • plan')
for x,number,label,detail,c in [(72,'3','poziomy','Zagadki o rosnącej złożoności',CYAN),(566,'2','typy przeciwników','Atak dystansowy i fizyczny',AMBER),(1060,'3','podstawowe akcje','Ruch · skok · parowanie',VIOLET)]:
    s.rect(x,263,468,441,PANEL)
    s.text(x+29,282,400,211,number,178,c,True)
    s.text(x+30,515,408,68,label,40,WHITE,True)
    s.text(x+30,617,410,54,detail,25,MUTED)
s.text(76,752,1456,52,'Cel: sprawdzić, czy parowanie daje frajdę.',37,WHITE,True)

# 9 — A marketing close which does not invite people to play an unavailable build.
s=Slide('Feedback','',
'''[4:45–5:05] Kończymy pytaniem o najważniejszą obietnicę gry: jak wykorzystasz następny atak? Zapraszamy do pytań o koncepcję i uwag do proponowanych zastosowań parowania. Część technologiczna nie jest elementem tej wersji prezentacji. Hasło jest propozycją redakcyjną.
Zespół według dokumentów: Aleksander Bielicki, Radosław Głasek, Jakub Pączka, Michał Popkowicz, Filip Shramko, Kacper Trzciński.
Źródło koncepcji: specyfikacja.tex i req.tex. Brak deklaracji daty premiery, ceny, stanu ukończenia lub wyników testów.''',
'Schemat koncepcyjny')
s.text(72,162,1190,215,'Jak wykorzystasz\nnastępny atak?',89,WHITE,True)
s.text(78,450,780,53,'Pytania i uwagi do koncepcji',32,MUTED)
s.text(78,724,580,57,'FEEDBACK',53,CYAN,True)
s.platform(932,741,563)
s.enemy(1382,618,1.8)
s.player(1150,588,2,True)
s.line(1354,668,1296,668,AMBER,6,True)
s.circle(1283,655,25,AMBER)
s.line(1185,574,1039,485,CYAN,6,True)
s.sparks(1194,662,96)

# Minimal standards-compliant PPTX package, with native shapes and notes.
BASE_GROUP='<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
RELS_NS='http://schemas.openxmlformats.org/package/2006/relationships'
def rels(rows):
    return '<Relationships xmlns="'+RELS_NS+'">'+''.join(f'<Relationship Id="{i}" Type="{R}/{t}" Target="{target}"/>' for i,t,target in rows)+'</Relationships>'

def notes_xml(note):
    paragraphs=''.join('<a:p><a:r><a:rPr lang="pl-PL"/><a:t>'+escape(v)+'</a:t></a:r></a:p>' for v in note.split('\n'))
    return f'<p:notes {NS}><p:cSld><p:spTree>{BASE_GROUP}<p:sp><p:nvSpPr><p:cNvPr id="2" name="Notes Text"/><p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>{paragraphs}</p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>'

# Theme with all required color, font and format lists.
theme=f'''<a:theme xmlns:a="{A}" name="Feedback"><a:themeElements><a:clrScheme name="Feedback">
<a:dk1><a:srgbClr val="{BG}"/></a:dk1><a:lt1><a:srgbClr val="{WHITE}"/></a:lt1><a:dk2><a:srgbClr val="{PANEL}"/></a:dk2><a:lt2><a:srgbClr val="{MUTED}"/></a:lt2>
<a:accent1><a:srgbClr val="{CYAN}"/></a:accent1><a:accent2><a:srgbClr val="{VIOLET}"/></a:accent2><a:accent3><a:srgbClr val="{AMBER}"/></a:accent3><a:accent4><a:srgbClr val="{RED}"/></a:accent4><a:accent5><a:srgbClr val="{GRID}"/></a:accent5><a:accent6><a:srgbClr val="{MUTED}"/></a:accent6><a:hlink><a:srgbClr val="{CYAN}"/></a:hlink><a:folHlink><a:srgbClr val="{VIOLET}"/></a:folHlink></a:clrScheme>
<a:fontScheme name="Lato"><a:majorFont><a:latin typeface="Lato"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Lato"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>
<a:fmtScheme name="Feedback"><a:fillStyleLst>{('<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>')*3}</a:fillStyleLst><a:lnStyleLst>{('<a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>')*3}</a:lnStyleLst><a:effectStyleLst>{('<a:effectStyle><a:effectLst/></a:effectStyle>')*3}</a:effectStyleLst><a:bgFillStyleLst>{('<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>')*3}</a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>'''
clrmap='<p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/>'
files={}
files['_rels/.rels']=rels([('rId1','officeDocument','ppt/presentation.xml')])
files['ppt/presentation.xml']=f'<p:presentation {NS}><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="master"/></p:sldMasterIdLst><p:notesMasterIdLst><p:notesMasterId r:id="notesMaster"/></p:notesMasterIdLst><p:sldIdLst>'+''.join(f'<p:sldId id="{256+i}" r:id="slide{i}"/>' for i in range(1,len(slides)+1))+f'</p:sldIdLst><p:sldSz cx="{emu(W)}" cy="{emu(H)}" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle/></p:presentation>'
files['ppt/_rels/presentation.xml.rels']=rels([('master','slideMaster','slideMasters/slideMaster1.xml'),('notesMaster','notesMaster','notesMasters/notesMaster1.xml')]+[(f'slide{i}','slide',f'slides/slide{i}.xml') for i in range(1,len(slides)+1)])
files['ppt/theme/theme1.xml']=theme
files['ppt/slideMasters/slideMaster1.xml']=f'<p:sldMaster {NS}><p:cSld><p:spTree>{BASE_GROUP}</p:spTree></p:cSld>{clrmap}<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="layout"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>'
files['ppt/slideMasters/_rels/slideMaster1.xml.rels']=rels([('layout','slideLayout','../slideLayouts/slideLayout1.xml'),('theme','theme','../theme/theme1.xml')])
files['ppt/slideLayouts/slideLayout1.xml']=f'<p:sldLayout {NS} type="blank" preserve="1"><p:cSld name="Blank"><p:spTree>{BASE_GROUP}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>'
files['ppt/slideLayouts/_rels/slideLayout1.xml.rels']=rels([('master','slideMaster','../slideMasters/slideMaster1.xml')])
files['ppt/notesMasters/notesMaster1.xml']=f'<p:notesMaster {NS}><p:cSld><p:spTree>{BASE_GROUP}</p:spTree></p:cSld>{clrmap}<p:notesStyle/></p:notesMaster>'
files['ppt/notesMasters/_rels/notesMaster1.xml.rels']=rels([('theme','theme','../theme/theme1.xml')])
for idx,s in enumerate(slides,1):
    if any('figma-characters/' in name for name in s.images):
        s.note += '\nGrafika postaci/przeciwnika pochodzi z dostarczonego Figma Make (CharacterShowcase.tsx / PixelEnemy.tsx). Statyczne klatki SVG; schematy interakcji są opracowaniem do prezentacji. Jednego wzoru przeciwnika użyto ilustracyjnie, bez ustalania wyglądu poszczególnych typów.'
    files[f'ppt/slides/slide{idx}.xml']=f'<p:sld {NS}><p:cSld name="{escape(s.title or "Feedback")}"><p:spTree>{BASE_GROUP}{"".join(s.parts)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
    rows=[('layout','slideLayout','../slideLayouts/slideLayout1.xml'),('notes','notesSlide',f'../notesSlides/notesSlide{idx}.xml')]
    rows += [('img'+str(n),'image','../media/'+name) for n,name in enumerate(s.images,1)]
    files[f'ppt/slides/_rels/slide{idx}.xml.rels']=rels(rows)
    files[f'ppt/notesSlides/notesSlide{idx}.xml']=notes_xml(s.note)
    files[f'ppt/notesSlides/_rels/notesSlide{idx}.xml.rels']=rels([('master','notesMaster','../notesMasters/notesMaster1.xml'),('slide','slide',f'../slides/slide{idx}.xml')])
content_types={'ppt/presentation.xml':'presentationml.presentation','ppt/slideMasters/slideMaster1.xml':'presentationml.slideMaster','ppt/slideLayouts/slideLayout1.xml':'presentationml.slideLayout','ppt/notesMasters/notesMaster1.xml':'presentationml.notesMaster','ppt/theme/theme1.xml':'theme'}
for i in range(1,len(slides)+1):
    content_types[f'ppt/slides/slide{i}.xml']='presentationml.slide'
    content_types[f'ppt/notesSlides/notesSlide{i}.xml']='presentationml.notesSlide'
files['[Content_Types].xml']='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>'+''.join(f'<Override PartName="/{name}" ContentType="application/vnd.openxmlformats-officedocument.{ctype}+xml"/>' for name,ctype in content_types.items())+'</Types>'
output=ROOT/'feedback-pitch.pptx'
with ZipFile(output,'w',ZIP_DEFLATED) as z:
    for name,data in files.items():z.writestr(name,'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+data)
    for name in sorted({name for slide in slides for name in slide.images}):
        z.write(ROOT/'assets'/name,'ppt/media/'+name)
notes=['# Feedback — notatki prelegenta','\nWersja marketingowa, bez części technologicznej. 9 slajdów, około 5 minut. Czasy są propozycją tempa wystąpienia. Schematy i hasła są redakcyjnym opracowaniem dokumentacji; nie przedstawiają działającego prototypu.\n']
for idx,s in enumerate(slides,1):notes.extend([f'## {idx}. {s.title or "Feedback"}',s.note,''])
(ROOT/'notatki-prelegenta.md').write_text('\n\n'.join(notes))
print(f'Created {output} ({len(slides)} slides, native shapes and speaker notes)')
