from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path

def make_report(out,analysis):
 styles=getSampleStyleSheet(); doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42); story=[]
 story += [Paragraph('ASTRIX AI',styles['Title']),Paragraph('Multimodal Authenticity Intelligence — Image Analysis Report',styles['Heading2']),Spacer(1,14)]
 story += [Paragraph(f"Assessment: <b>{analysis['verdict']}</b>",styles['Heading1']),Paragraph(analysis['verdict_explanation'],styles['BodyText']),Spacer(1,10)]
 rows=[['Analysis ID',analysis['analysis_id']],['Filename',analysis['filename']],['SHA-256',analysis['file_hash']],['Evidence score',str(analysis['evidence_score'])+'/100'],['Detector',analysis['detector'].get('message','')],['Metadata',analysis['metadata']['detail']],['Forensics',analysis['forensics']['summary']],['Manipulation',analysis['manipulation']['summary']]]
 t=Table(rows,colWidths=[115,380]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.HexColor('#eee9e2')),('GRID',(0,0),(-1,-1),.4,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP'),('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),9),('PADDING',(0,0),(-1,-1),7)]));story += [t,Spacer(1,16),Paragraph('Evidence',styles['Heading2'])]
 for e in analysis['evidence']: story.append(Paragraph(f"<b>{e['severity'].upper()} — {e['title']}</b><br/>{e['description']} <font color='#666'>({e['source']})</font>",styles['BodyText']));story.append(Spacer(1,7))
 story += [Spacer(1,10),Paragraph('Limitations',styles['Heading2']),Paragraph('Automated authenticity detection is not perfect. This report is an evidence-based technical assessment, not a guarantee of origin. Missing metadata does not prove AI generation, and forensic heuristics can be affected by compression, resizing and editing.',styles['BodyText'])]
 doc.build(story)
