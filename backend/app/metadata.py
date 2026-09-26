from PIL import Image

def analyze(img:Image.Image):
 exif=img.getexif(); data={}
 for k,v in exif.items():
  try:data[str(k)]=str(v)[:300]
  except:pass
 software=data.get('305','')
 camera=bool(data.get('272') or data.get('271'))
 if software: summary='Software metadata present'; detail=f'Software tag: {software}'
 elif camera: summary='Camera metadata present'; detail=f'Make/model metadata detected: {data.get("271","")} {data.get("272","")}'.strip()
 else: summary='Limited metadata'; detail='No clear camera make/model or software tag was found. Missing metadata does not prove AI generation.'
 return {'summary':summary,'detail':detail,'fields':data,'camera_metadata':camera,'software_metadata':bool(software)}
