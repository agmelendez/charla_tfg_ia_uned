import json,re,sys,unicodedata
W='/tmp/w/'
def norm(s):
    s=unicodedata.normalize('NFC',s).lower()
    s=s.replace('“','"').replace('”','"').replace('’',"'").replace('®','')
    return re.sub(r'[\s­]+','',s)
src={}
for k,f in {'politica':'politica.txt','rediia':'rediia.txt','proifed':'proifed.txt','marco':'marco.txt','guia_est':'guia_est.txt','guia_doc':'guia_doc.txt','chatgpt':'chatgpt.txt'}.items():
    src[k]=[norm(p) for p in open(W+f,encoding='utf-8').read().split('\f')]
for k,f in {'euned_gus':'euned_gus.txt','informe_euned':'informe_euned.txt','euned_rev':'euned_rev.txt'}.items():
    src[k]=[norm(open(W+f,encoding='utf-8').read())]
import os
base=os.path.expanduser("~/mnt/0. Charla X Encuentro de Estudiantes de TFG/Bibliografía para las Charlas/pages.jsonl")
dec={}
for l in open(base):
    if '"AI Higher education survey 2026.pdf"' in l[:400]:
        p=json.loads(l); dec[p['page_number']]=p['clean_text']
src['dec']=[norm(dec.get(i,'')) for i in range(0,max(dec)+1)]
qs=json.load(open(W+'build/quotes.json'))
bad=0; out={}
for q in qs:
    n=norm(q['text']); pages=[i+1 for i,p in enumerate(src[q['src']]) if n in p]
    if q['src'] in('euned_gus','informe_euned','euned_rev'): pages=['sec'] if pages else []
    if q['src']=='dec': pages=[i for i,p in enumerate(src['dec']) if n in p]
    out[q['id']]=pages
    if not pages: bad+=1; print('NOT FOUND',q['id'],q['text'][:70])
print('total',len(qs),'notfound',bad)
json.dump(out,open(W+'build/quote_pages.json','w'))
print({k:v for k,v in out.items()})
# numeric facts DEC
nums={'61%':5,'31%':5,'22%':5,'20%':5,'19%':5,'66%':5,'73%':5,'29%':6,'60%':6,'15%':5,'43%':5,'45,398':3,'27,284':3,'18,114':3,'35 countries':3,'28%':7,'37%':8}
for k,pg in nums.items():
    print(k,pg,'OK' if k.lower() in dec.get(pg,'').lower() else 'MISSING')
