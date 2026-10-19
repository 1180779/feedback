"""Render this deck's native rectangles, ellipses, lines and text to PDF.

Reads the actual PPTX package. Uses local Pycairo; no network dependency.
Also checks text and shape bounds. Does not claim to be a general PPTX renderer.
"""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
import math
from io import BytesIO
import cairo

ROOT=Path(__file__).resolve().parents[1]
A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
P='{http://schemas.openxmlformats.org/presentationml/2006/main}'
R='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
REL='{http://schemas.openxmlformats.org/package/2006/relationships}'
UNIT=7620
z=ZipFile(ROOT/'feedback-pitch.pptx')
surface=cairo.PDFSurface(str(ROOT/'feedback-pitch.pdf'),960,540)
surface.set_metadata(cairo.PDF_METADATA_TITLE,'Feedback — koncepcja gry')
surface.set_metadata(cairo.PDF_METADATA_SUBJECT,'Pitch marketingowy, bez części technologicznej')
cr=cairo.Context(surface)
issues=[]

def color(node,fallback='FFFFFF'):
    if node is None:return None
    v=node.find(f'{A}solidFill/{A}srgbClr')
    if v is None:return None
    return v.get('val',fallback)
def set_color(c):cr.set_source_rgb(*(int(c[i:i+2],16)/255 for i in [0,2,4]))
def xf(node):
    t=node.find(A+'xfrm');o=t.find(A+'off');s=t.find(A+'ext')
    return tuple(int(v)/UNIT for v in [o.get('x'),o.get('y'),s.get('cx'),s.get('cy')])
def fillstroke(props):
    f=color(props); ln=props.find(A+'ln');s=color(ln)
    if f:set_color(f);cr.fill_preserve()
    if s:
        set_color(s);cr.set_line_width(int(ln.get('w','15240'))/UNIT);cr.stroke()
    else:cr.new_path()

def wrap(value,w):
    if not value:return ['']
    result=[];current=''
    for word in value.split(' '):
        trial=current+' '+word if current else word
        if current and cr.text_extents(trial).x_advance>w:
            result.append(current);current=word
        else:current=trial
    result.append(current)
    return result

for idx in range(1,10):
    cr.save();cr.scale(.6,.6)
    root=E.fromstring(z.read(f'ppt/slides/slide{idx}.xml'))
    rel=E.fromstring(z.read(f'ppt/slides/_rels/slide{idx}.xml.rels'))
    images={n.get('Id'):n.get('Target') for n in rel}
    tree=root.find(f'{P}cSld/{P}spTree')
    for item in tree:
        if item.tag==P+'sp':
            props=item.find(P+'spPr');x,y,w,h=xf(props)
            if x<0 or y<0 or x+w>1601 or y+h>901:issues.append((idx,'shape bounds',x,y,w,h))
            geom=props.find(A+'prstGeom').get('prst')
            cr.new_path()
            if geom=='ellipse':
                cr.save();cr.translate(x+w/2,y+h/2);cr.scale(w/2,h/2);cr.arc(0,0,1,0,math.tau);cr.restore()
            else:cr.rectangle(x,y,w,h)
            fillstroke(props)
            body=item.find(P+'txBody')
            if body is not None:
                ty=y
                for p in body.findall(A+'p'):
                    runs=p.findall(A+'r')
                    if not runs:continue
                    run=runs[0];rp=run.find(A+'rPr');size=int(rp.get('sz'))/60
                    cr.select_font_face('Lato',cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD if rp.get('b')=='1' else cairo.FONT_WEIGHT_NORMAL)
                    cr.set_font_size(size);ascent=cr.font_extents()[0]
                    text=''.join(n.text or '' for n in p.iter(A+'t'))
                    pp=p.find(A+'pPr');alignment=pp.get('algn','l') if pp is not None else 'l'
                    c=color(rp) or 'FFFFFF';set_color(c)
                    for line in wrap(text,w):
                        length=cr.text_extents(line).x_advance
                        if length>w+1:issues.append((idx,'word overflow',line))
                        dx=(w-length)/2 if alignment=='ctr' else (w-length if alignment=='r' else 0)
                        cr.move_to(x+dx,ty+ascent);cr.show_text(line)
                        ty+=size*1.1
                if ty>y+h+2:issues.append((idx,'text height',text,round(ty-y),h))
        elif item.tag==P+'cxnSp':
            props=item.find(P+'spPr');x,y,w,h=xf(props);t=props.find(A+'xfrm')
            x1,x2=(x+w,x) if t.get('flipH')=='1' else (x,x+w)
            y1,y2=(y+h,y) if t.get('flipV')=='1' else (y,y+h)
            ln=props.find(A+'ln');width=int(ln.get('w'))/UNIT;set_color(color(ln));cr.set_line_width(width);cr.set_line_cap(cairo.LINE_CAP_ROUND)
            dashed=ln.find(A+'prstDash') is not None
            cr.set_dash([width*2.5,width*2] if dashed else [])
            cr.move_to(x1,y1);cr.line_to(x2,y2);cr.stroke();cr.set_dash([])
            if ln.find(A+'tailEnd') is not None:
                angle=math.atan2(y2-y1,x2-x1);length=width*3.2;spread=width*1.5
                cr.move_to(x2,y2)
                cr.line_to(x2-length*math.cos(angle)+spread*math.sin(angle),y2-length*math.sin(angle)-spread*math.cos(angle))
                cr.line_to(x2-length*math.cos(angle)-spread*math.sin(angle),y2-length*math.sin(angle)+spread*math.cos(angle));cr.close_path();cr.fill()
        elif item.tag==P+'pic':
            x,y,w,h=xf(item.find(P+'spPr'))
            rid=item.find(f'{P}blipFill/{A}blip').get(R+'embed')
            filename=images[rid].removeprefix('../media/')
            im=cairo.ImageSurface.create_from_png(BytesIO(z.read('ppt/media/'+filename)))
            cr.save();cr.translate(x,y)
            if item.find(f'{P}spPr/{A}xfrm').get('flipH')=='1':
                cr.translate(w,0);cr.scale(-1,1)
            cr.scale(w/im.get_width(),h/im.get_height());cr.set_source_surface(im,0,0);cr.paint();cr.restore()
    cr.restore();surface.show_page()
surface.finish()
if issues:
    for issue in issues:print('CHECK:',issue)
    raise SystemExit('Resolve layout checks before delivery.')
print('Exported feedback-pitch.pdf; 9 pages; text and shape bounds passed.')
