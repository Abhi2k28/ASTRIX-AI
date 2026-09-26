import cv2,numpy as np
from PIL import Image

def analyze(img:Image.Image):
 arr=np.array(img.convert('RGB')); gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY)
 # JPEG ELA only when image can be encoded. This is a supporting signal.
 ok,enc=cv2.imencode('.jpg',cv2.cvtColor(arr,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,90])
 if ok:
  rec=cv2.imdecode(enc,cv2.IMREAD_COLOR); diff=cv2.absdiff(cv2.cvtColor(arr,cv2.COLOR_RGB2BGR),rec); ela=float(np.mean(diff))
 else: ela=0.0
 edges=cv2.Canny(gray,80,160); edge_density=float(np.mean(edges>0))
 if ela>7: summary='Potential compression/editing inconsistency'; detail=f'ELA difference is {ela:.2f}; this is a supporting manipulation signal only.'
 else: summary='No strong conventional editing signal'; detail=f'ELA difference is {ela:.2f}; no strong compression inconsistency was detected by this simple test.'
 return {'summary':summary,'detail':detail,'ela_mean':round(ela,3),'edge_density':round(edge_density,4)}
