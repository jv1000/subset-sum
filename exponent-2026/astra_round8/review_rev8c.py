"""Read-only PDF extraction/layout preparation for the preregistered rev8c review."""
from pathlib import Path
import pymupdf as fitz
from PIL import Image,ImageDraw
import json
OUT=Path(__file__).resolve().parent/'rev8c_review'
OUT.mkdir(exist_ok=True)
PDF=Path('D:/AIProjects/SubsetSum/preprint/Voitle_SubsetSum_certified-0.48758_2026-11-05_rev8c.pdf')
doc=fitz.open(PDF)
for i,p in enumerate(doc):
    (OUT/f'page_{i+1:02d}.txt').write_text(p.get_text(),encoding='utf-8')
(OUT/'full_text.txt').write_text('\n\n'.join(f'PAGE {i+1}\n'+p.get_text() for i,p in enumerate(doc)),encoding='utf-8')
for start in range(0,len(doc),4):
    sheet=Image.new('RGB',(1224,1654),'#dddddd'); draw=ImageDraw.Draw(sheet)
    for j in range(min(4,len(doc)-start)):
        pix=doc[start+j].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        im.thumbnail((600,790)); x=(j%2)*612; y=(j//2)*827+25
        sheet.paste(im,(x,y)); draw.text((x+10,y-20),f'Page {start+j+1}',fill='black')
    sheet.save(OUT/f'pages_{start+1:02d}_{min(start+4,len(doc)):02d}.png')
print(json.dumps({'pages':len(doc),'title':doc.metadata.get('title'),'output':str(OUT)}))
