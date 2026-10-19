"""Recover two supplied Figma Make components and freeze their SVG artwork.

No AI image recreation. Geometry/colors come from the archived source; motion
is sampled at idle or the first held parry keyframe (25% of the 1.6s cycle).
"""
from pathlib import Path
from zipfile import ZipFile
import json,re,hashlib,xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'assets'/'figma-characters';DEST.mkdir(exist_ok=True)
ARCHIVE=ROOT.parent/'Feedback mockup.make'
targets={'src/app/pages/CharacterShowcase.tsx','src/app/components/game/PixelEnemy.tsx'}
files={}
with ZipFile(ARCHIVE) as z:data=json.loads(z.read('ai_chat.json'))
for thread in data['threads']:
 for message in thread['messages']:
  for part in message.get('parts',[]):
   if part.get('partType')!='tool-call-json-DO-NOT-USE-IN-PROD':continue
   call=json.loads(part['contentJson']);args=json.loads(call['argsJson']);path=args.get('path','').lstrip('/')
   if path not in targets:continue
   kind=call['toolName']
   if kind=='write_tool':files[path]=args['file_text']
   elif kind=='fast_apply_tool':
    assert '... existing code ...' not in args['change_str'], 'Cannot reconstruct abbreviated changes'
    files[path]=args['change_str']
   elif kind=='edit_tool':
    assert args['old_str'] in files[path], (path,'unapplied edit')
    files[path]=files[path].replace(args['old_str'],args['new_str'],1)
assert set(files)==targets
for path,source in files.items():(DEST/Path(path).name).write_text(source)

SVG='http://www.w3.org/2000/svg';E.register_namespace('',SVG)
def freeze(source,parry=False,enemy=False):
 # Select only the SVG component, not the surrounding UI.
 source=source[source.index('<motion.svg'):source.index('</motion.svg>')+len('</motion.svg>')]
 if not enemy:
  source=source.split('      {/* Jump swoosh lines */}')[0]+'</motion.svg>'
  if not parry:
   start=source.index('      {/* Sword - only visible during parry */}')
   end=source.index('      {/* Head */}',start)
   source=source[:start]+source[end:]
   start=source.index('      {/* Parry energy effect around sword - only during parry */}')
   source=source[:start]+'</motion.svg>'
 source=re.sub(r'\{/\*.*?\*/\}', '', source,flags=re.S)
 root=E.Element('{'+SVG+'}svg',{'viewBox':'0 0 48 56' if enemy else '0 0 72 64','width':'768' if enemy else '1152','height':'896' if enemy else '1024','fill':'none'})
 stack=[root]
 for token in re.findall(r'<[^>]+>',source,re.S):
  match=re.match(r'<(/?)(?:motion\.)?(svg|g|rect|ellipse)\b',token)
  if not match:continue
  closing,kind=match.groups()
  if kind=='svg':continue
  if closing:stack.pop();continue
  attrs=dict(re.findall(r'\b(x|y|width|height|cx|cy|rx|ry|fill|opacity)="([^"]+)"',token))
  if kind=='ellipse' and not enemy:attrs['opacity']='0.4'
  if kind=='g' and parry:
   if 'rotate: [0, -30, -30, 0]' in token:
    attrs['transform']='translate(0 -4) translate(18 30) rotate(-30) translate(-18 -30)'
   elif 'rotate: [0, 45, 45, 0]' in token:
    attrs['transform']='translate(0 -6) translate(49 30) rotate(45) translate(-49 -30)'
   elif 'rotate: [0, 45, 45, 45, 0]' in token:
    attrs['transform']='translate(0 -6) translate(49 30) rotate(45) scale(0.9) translate(-49 -30)'
    attrs['opacity']='0.4'
  if kind=='rect' and parry and attrs.get('fill')=='#ffffff':attrs['opacity']='0.4'
  el=E.SubElement(stack[-1],'{'+SVG+'}'+kind,attrs)
  if kind=='g':stack.append(el)
 assert len(stack)==1
 return E.tostring(root,encoding='unicode')
char=files['src/app/pages/CharacterShowcase.tsx'];enemy=files['src/app/components/game/PixelEnemy.tsx']
for name,src,p,e in [('player-idle',char,False,False),('player-parry',char,True,False),('enemy',enemy,False,True)]:
 svg=freeze(src,p,e);(DEST/(name+'.svg')).write_text(svg)
 print(name, 'primitives:',len(list(E.fromstring(svg).iter())))
(DEST/'PROVENANCE.md').write_text('''# Artwork recovered from the supplied Figma Make archive

Source: `Feedback mockup.make`, `ai_chat.json` file-write/edit history.

- `CharacterShowcase.tsx`: later character design, including the sword-parry animation.
- `PixelEnemy.tsx`: enemy used in the mockup scene.
- `player-idle.svg`: static neutral pose; conditional sword and parry VFX hidden as in the component.
- `player-parry.svg`: first held parry keyframe (25% of the source 1.6 s animation); arm and sword transforms preserved.
- `enemy.svg`: neutral frame of the source enemy, preserving its colors and geometry.

SVGs are extracted artwork, not newly generated illustrations. React UI and animation are omitted. The player canvas is widened from 64 to 72 units to avoid clipping the rotated sword. PNGs are transparent high-resolution renders for PowerPoint portability. The presentation does not imply these are final in-game assets or a functioning game.
''')
