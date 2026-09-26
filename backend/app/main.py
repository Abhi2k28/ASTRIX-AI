from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from PIL import Image
import tempfile,os,hashlib,uuid,time
from .model import detector_status,predict
from .metadata import analyze as metadata_analyze
from .forensics import analyze as forensic_analyze,heatmap
from .manipulation import analyze as manipulation_analyze
from .evidence import build
from .report import make_report

app=FastAPI(title='ASTRIX AI API',version='0.1.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
REPORT_DIR=Path(__file__).resolve().parents[2]/'reports';REPORT_DIR.mkdir(exist_ok=True)
MAX=15*1024*1024

def save_bytes(data,suffix):
 fd,path=tempfile.mkstemp(suffix=suffix);os.close(fd);Path(path).write_bytes(data);return Path(path)

@app.get('/api/health')
def health(): return {'status':'ok','service':'ASTRIX AI','detector':detector_status()}

@app.post('/api/analyze/image')
async def analyze_image(file:UploadFile=File(...)):
 if not file.content_type or not file.content_type.startswith('image/'): raise HTTPException(400,'Please upload an image file.')
 data=await file.read()
 if len(data)>MAX: raise HTTPException(413,'Image exceeds 15 MB limit.')
 suffix=Path(file.filename or '').suffix.lower() or '.jpg'; path=save_bytes(data,suffix); started=time.perf_counter(); aid='ASTRIX-'+uuid.uuid4().hex[:10].upper(); sha=hashlib.sha256(data).hexdigest()
 try:
  try: img=Image.open(path); img.load(); img=img.convert('RGB')
  except Exception: raise HTTPException(400,'Unable to decode this image.')
  det=predict(img); meta=metadata_analyze(img); forensic=forensic_analyze(img); manip=manipulation_analyze(img); verdict,cls,explanation,score,ev=build(det,meta,forensic,manip); hm=heatmap(img)
  result={'analysis_id':aid,'filename':file.filename,'file_hash':sha,'verdict':verdict,'verdict_class':cls,'verdict_explanation':explanation,'evidence_score':score,'detector':det,'metadata':meta,'forensics':{'summary':'Forensic signals analyzed','detail':f"Noise σ {forensic['noise_std']}; frequency ratio {forensic['frequency_ratio']}; local noise variation {forensic['local_noise_variation']}.",'signals':forensic},'manipulation':manip,'evidence':ev,'heatmap':{'available':bool(hm),'overlay_base64':hm},'processing_time_ms':round((time.perf_counter()-started)*1000,1),'limitations':['The detector was trained on a specific dataset and may not generalize to unseen generators.','Evidence score is not a calibrated probability.','Compression, resizing, screenshots and editing can affect forensic signals.']}
  make_report(REPORT_DIR/f'{aid}.pdf',result);return result
 finally: path.unlink(missing_ok=True)

@app.get('/api/report/{analysis_id}')
def report(analysis_id:str):
 p=REPORT_DIR/f'{analysis_id}.pdf'
 if not p.exists(): raise HTTPException(404,'Report not found')
 from fastapi.responses import FileResponse
 return FileResponse(p,media_type='application/pdf',filename=f'{analysis_id}.pdf')
