import cv2, numpy as np
from PIL import Image

def clamp(x): return float(max(0,min(1,x)))

def analyze(img:Image.Image):
 arr=np.array(img.convert('RGB'))
 gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY)
 blur=float(cv2.Laplacian(gray,cv2.CV_64F).var())
 residual=gray.astype(np.float32)-cv2.GaussianBlur(gray,(5,5),0)
 noise=float(np.std(residual))
 fft=np.fft.fftshift(np.fft.fft2(gray.astype(np.float32)))
 mag=np.log1p(np.abs(fft)); h,w=gray.shape; yy,xx=np.ogrid[:h,:w]; r=np.sqrt((xx-w/2)**2+(yy-h/2)**2); high=mag[r>min(h,w)*0.25].mean(); low=mag[r<=min(h,w)*0.25].mean(); freq_ratio=float(high/(low+1e-6))
 # local noise inconsistency map
 small=cv2.resize(residual,(max(32,w//8),max(32,h//8)),interpolation=cv2.INTER_AREA)
 local=np.abs(small); score=float(np.std(local)/(np.mean(local)+1e-6));
 return {'blur_variance':round(blur,2),'noise_std':round(noise,3),'frequency_ratio':round(freq_ratio,3),'local_noise_variation':round(score,3),'notes':[
  'Noise statistics are supporting forensic evidence, not proof of AI generation.',
  'Frequency analysis can reveal unusual image statistics but is not a standalone classifier.'
 ]}

def heatmap(img:Image.Image):
 arr=np.array(img.convert('RGB')); gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY); residual=np.abs(gray.astype(np.float32)-cv2.GaussianBlur(gray,(5,5),0)); residual=cv2.normalize(residual,None,0,255,cv2.NORM_MINMAX).astype(np.uint8); residual=cv2.GaussianBlur(residual,(0,0),7); heat=cv2.applyColorMap(residual,cv2.COLORMAP_TURBO); overlay=cv2.addWeighted(cv2.cvtColor(arr,cv2.COLOR_RGB2BGR),0.62,heat,0.38,0); ok,buf=cv2.imencode('.png',overlay); import base64; return base64.b64encode(buf.tobytes()).decode() if ok else None
