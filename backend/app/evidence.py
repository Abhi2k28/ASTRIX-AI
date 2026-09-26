def build(det,meta,forensic,manip):
 ev=[]; ai=det.get('ai_score');
 if ai is not None:
  if ai>=0.8: ev.append({'severity':'high','title':'AI detector found a strong synthetic signal','description':det['message'],'source':'AI detector'})
  elif ai>=0.6: ev.append({'severity':'medium','title':'AI detector found a moderate synthetic signal','description':det['message'],'source':'AI detector'})
  else: ev.append({'severity':'info','title':'AI detector did not find a strong synthetic signal','description':det['message'],'source':'AI detector'})
 if meta.get('software_metadata'): ev.append({'severity':'medium','title':'Software metadata is present','description':meta['detail'],'source':'EXIF'})
 elif meta.get('camera_metadata'): ev.append({'severity':'info','title':'Camera metadata is present','description':meta['detail'],'source':'EXIF'})
 else: ev.append({'severity':'info','title':'Camera metadata is unavailable','description':meta['detail'],'source':'EXIF'})
 if forensic['local_noise_variation']>1.8: ev.append({'severity':'medium','title':'Local noise variation detected','description':'Noise statistics vary across the image; this is supporting forensic evidence and can also occur after editing or compression.','source':'Forensics'})
 else: ev.append({'severity':'info','title':'Noise variation is not strongly anomalous','description':'No strong local noise inconsistency was detected by this simple forensic signal.','source':'Forensics'})
 if manip['ela_mean']>7: ev.append({'severity':'medium','title':'Compression/editing inconsistency detected','description':manip['detail'],'source':'Manipulation'})
 else: ev.append({'severity':'info','title':'No strong ELA inconsistency detected','description':manip['detail'],'source':'Manipulation'})
 # Conservative evidence score, explicitly not probability.
 score=0
 if ai is not None: score += ai*70
 score += min(15, max(0, (forensic['local_noise_variation']-1)*7))
 score += 10 if manip['ela_mean']>7 else 0
 score += 5 if meta.get('software_metadata') else 0
 score=max(0,min(100,round(score)))
 if ai is None: verdict='INCONCLUSIVE'; cls='neutral'; explanation='The AI detector was unavailable, so ASTRIX cannot make a model-backed authenticity assessment.'
 elif ai>=0.72: verdict='LIKELY AI-GENERATED'; cls='bad'; explanation='The detector found a strong synthetic signal, supported by the forensic evidence shown below.'
 elif ai<=0.28 and manip['ela_mean']<=7: verdict='LIKELY AUTHENTIC'; cls='good'; explanation='The detector found a stronger authentic signal and the supporting forensic checks did not show strong manipulation evidence.'
 elif manip['ela_mean']>10: verdict='LIKELY MANIPULATED'; cls='warn'; explanation='The image shows a strong conventional editing/compression inconsistency; AI generation itself is not established.'
 else: verdict='INCONCLUSIVE'; cls='neutral'; explanation='The available evidence is mixed or not strong enough for a confident classification.'
 return verdict,cls,explanation,score,ev
