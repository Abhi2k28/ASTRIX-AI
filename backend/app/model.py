from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from .config import MODEL_ID

_processor=None
_model=None
_error=None

def load_model():
 global _processor,_model,_error
 if _model is not None:return
 try:
  _processor=AutoImageProcessor.from_pretrained(MODEL_ID)
  _model=AutoModelForImageClassification.from_pretrained(MODEL_ID)
  _model.eval(); _error=None
 except Exception as e:
  _error=str(e)

def detector_status():
 load_model(); return {'loaded':_model is not None,'model_id':MODEL_ID,'error':_error}

def predict(image:Image.Image):
 load_model()
 if _model is None:
  return {'available':False,'label':'unavailable','ai_score':None,'real_score':None,'message':'AI detector could not be loaded. See backend error log.','error':_error}
 with torch.no_grad():
  inputs=_processor(image.convert('RGB'),return_tensors='pt')
  logits=_model(**inputs).logits
  probs=torch.softmax(logits,dim=-1)[0]
 labels=_model.config.id2label
 pairs=[(labels.get(i,str(i)).lower(),float(probs[i])) for i in range(len(probs))]
 ai=next((s for l,s in pairs if 'fake' in l or 'ai' in l or 'generated' in l or 'synthetic' in l),None)
 real=next((s for l,s in pairs if 'real' in l or 'authentic' in l or 'human' in l),None)
 if ai is None or real is None:
  idx=int(torch.argmax(probs)); pred=labels.get(idx,str(idx)).lower(); ai=float(probs[idx]) if any(x in pred for x in ['fake','ai','generated','synthetic']) else 1-float(probs[idx]); real=1-ai
 return {'available':True,'label':'likely_ai' if ai>=0.5 else 'likely_real','ai_score':round(ai,4),'real_score':round(real,4),'message':f'Model output: {"synthetic" if ai>=0.5 else "authentic"} signal {max(ai,real)*100:.1f}%','model_id':MODEL_ID,'raw_labels':labels}
