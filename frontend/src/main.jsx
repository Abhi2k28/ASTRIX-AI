import React,{useRef,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Upload,ShieldCheck,ScanSearch,FileCheck2,Download,RotateCcw,AlertTriangle,CheckCircle2,Info,Image as ImageIcon,ChevronRight,Video,Mic} from 'lucide-react';
import './style.css';

const API='http://127.0.0.1:8000';

function App(){
 const input=useRef(); const [file,setFile]=useState(null); const [preview,setPreview]=useState(''); const [drag,setDrag]=useState(false); const [loading,setLoading]=useState(false); const [stage,setStage]=useState(''); const [result,setResult]=useState(null); const [error,setError]=useState('');
 const stages=['Validating image','Running AI-generation detector','Analyzing metadata & provenance','Running digital forensics','Building evidence map','Preparing assessment'];
 const choose=f=>{setError('');setResult(null);if(!f)return; if(!f.type.startsWith('image/'))return setError('Please select a JPG, JPEG, PNG or WEBP image.'); if(f.size>15*1024*1024)return setError('Image is larger than 15 MB.'); setFile(f);setPreview(URL.createObjectURL(f));};
 const analyze=async()=>{if(!file)return;setLoading(true);setError('');setResult(null);let timer=setInterval(()=>setStage(stages[Math.floor(Math.random()*stages.length)]),650);try{const fd=new FormData();fd.append('file',file);const r=await fetch(`${API}/api/analyze/image`,{method:'POST',body:fd});const data=await r.json();if(!r.ok)throw new Error(data.detail||'Analysis failed');setResult(data);}catch(e){setError(e.message||'Could not connect to ASTRIX backend.');}finally{clearInterval(timer);setStage('');setLoading(false);}};
 const reset=()=>{setFile(null);setPreview('');setResult(null);setError('');};
 const verdict=result?.verdict; const verdictClass=verdict?.includes('AI-GENERATED')?'bad':verdict?.includes('MANIPULATED')?'warn':verdict?.includes('AUTHENTIC')?'good':'neutral';

 return <div className="app">
  <header>
   <div className="brand">
    <div className="logo">A</div>
    <div>
     <b>ASTRIX AI</b>
     <span>Multimodal Authenticity Intelligence</span>
    </div>
   </div>
   <nav>
    <a href="#analyze">Analyze</a>
    <a href="#how">How it works</a>
    <a href="#about">About</a>
   </nav>
  </header>

  <main>
   <section className="hero">
    <div className="eyebrow"><ShieldCheck size={15}/> EVIDENCE-BASED MEDIA AUTHENTICITY</div>
    <h1>Can you trust<br/><em>what you see?</em></h1>
    <p>Analyze an image for signs of AI generation, manipulation, metadata anomalies and digital inconsistencies — with evidence you can inspect.</p>
   </section>

   <section id="analyze" className="panel">
    {!result && <>
     <div className="panel-head">
      <div>
       <span className="kicker">IMAGE ANALYZER</span>
       <h2>Upload an image</h2>
       <p>JPG, JPEG, PNG or WEBP · Maximum 15 MB</p>
      </div>
      <div className="status-pill"><span/> Local analysis</div>
     </div>

     <div
      className={`drop ${drag?'drag':''}`}
      onDragOver={e=>{e.preventDefault();setDrag(true)}}
      onDragLeave={()=>setDrag(false)}
      onDrop={e=>{e.preventDefault();setDrag(false);choose(e.dataTransfer.files[0])}}
      onClick={()=>input.current.click()}
     >
      <input
       ref={input}
       type="file"
       accept="image/jpeg,image/png,image/webp"
       hidden
       onChange={e=>choose(e.target.files[0])}
      />

      {preview
       ? <img src={preview} className="preview"/>
       : <>
          <div className="upload-icon"><Upload/></div>
          <strong>Drop your image here</strong>
          <span>or click to browse</span>
         </>
      }
     </div>

     {file&&
      <div className="file-row">
       <div>
        <ImageIcon size={18}/>
        <div>
         <b>{file.name}</b>
         <small>{(file.size/1024/1024).toFixed(2)} MB</small>
        </div>
       </div>
       <button className="ghost" onClick={e=>{e.stopPropagation();reset()}}>Remove</button>
      </div>
     }

     {error&&
      <div className="error">
       <AlertTriangle size={18}/>
       {error}
      </div>
     }

     {loading&&
      <div className="progress">
       <div className="spinner"/>
       <div>
        <b>ASTRIX is analyzing your image</b>
        <span>{stage}</span>
       </div>
      </div>
     }

     <button className="primary" disabled={!file||loading} onClick={analyze}>
      {loading?'Analyzing…':'Analyze Image'}
      <ChevronRight size={18}/>
     </button>

     <div className="privacy">
      <ShieldCheck size={15}/>
      Images are processed temporarily by this local demo server and removed after analysis.
     </div>
    </>}

    {result&&<Result data={result} preview={preview} onReset={reset}/>}
   </section>

   <section id="how" className="three">
    <Feature
     icon={<ScanSearch/>}
     title="AI detection"
     text="A pretrained vision classifier evaluates the image for synthetic-generation signals."
    />

    <Feature
     icon={<FileCheck2/>}
     title="Digital forensics"
     text="Metadata, compression, noise, frequency and manipulation signals provide supporting evidence."
    />

    <Feature
     icon={<ShieldCheck/>}
     title="Explainable result"
     text="ASTRIX separates strong evidence from weak or missing signals instead of inventing certainty."
    />
   </section>

   {/* MULTIMODAL ROADMAP */}
   <section className="multimodal-roadmap">
    <div className="roadmap-heading">
     <span className="kicker">MULTIMODAL INTELLIGENCE</span>
     <h2>More media intelligence is coming.</h2>
     <p>ASTRIX is expanding beyond image authenticity analysis.</p>
    </div>

    <div className="roadmap-grid">

     <div className="roadmap-card">
      <div className="roadmap-icon">
       <Video/>
      </div>

      <div>
       <div className="roadmap-title">
        <h3>VIDEO INTELLIGENCE</h3>
        <span>COMING SOON</span>
       </div>

       <p>
        Analyze videos for AI-generated frames, face manipulation,
        temporal inconsistencies and synthetic-media signals.
       </p>
      </div>
     </div>

     <div className="roadmap-card">
      <div className="roadmap-icon">
       <Mic/>
      </div>

      <div>
       <div className="roadmap-title">
        <h3>AUDIO INTELLIGENCE</h3>
        <span>COMING SOON</span>
       </div>

       <p>
        Analyze audio for AI-generated voices, synthetic speech patterns,
        voice manipulation and authenticity signals.
       </p>
      </div>
     </div>

    </div>
   </section>

   <section id="about" className="about">
    <span className="kicker">DESIGNED FOR RESPONSIBLE AUTHENTICITY ANALYSIS</span>
    <h2>One image. Multiple lines of evidence.</h2>
    <p>No automated detector is perfect. ASTRIX reports a reasoned assessment and exposes limitations so the user can understand what was actually observed.</p>
   </section>
  </main>

  <footer>
   ASTRIX AI · Hackathon prototype · Image authenticity analysis
  </footer>
 </div>
}

function Feature({icon,title,text}){
 return <div className="feature">
  <div className="ficon">{icon}</div>
  <h3>{title}</h3>
  <p>{text}</p>
 </div>
}

function Result({data,preview,onReset}){
 return <div className="result">

  <div className="result-top">
   <div>
    <span className="kicker">ANALYSIS COMPLETE</span>
    <h2>Authenticity assessment</h2>
   </div>

   <button className="ghost" onClick={onReset}>
    <RotateCcw size={16}/>
    New analysis
   </button>
  </div>

  <div className="verdict-grid">

   <div className={`verdict ${data.verdict_class}`}>
    <div className="verdict-icon">
     {data.verdict_class==='good'
      ? <CheckCircle2/>
      : data.verdict_class==='bad'
      ? <AlertTriangle/>
      : <Info/>
     }
    </div>

    <div>
     <small>ASTRIX ASSESSMENT</small>
     <strong>{data.verdict}</strong>
     <span>{data.verdict_explanation}</span>
    </div>
   </div>

   <div className="score">
    <small>Evidence score</small>
    <b>{data.evidence_score}<i>/100</i></b>
    <div className="bar">
     <span style={{width:`${data.evidence_score}%`}}/>
    </div>
    <small>Not a calibrated probability.</small>
   </div>

  </div>

  <div className="result-columns">

   <div className="image-card">
    <img src={preview}/>
    <div>
     <span>SHA-256</span>
     <code>{data.file_hash.slice(0,18)}…</code>
    </div>
   </div>

   <div className="evidence">
    <h3>Why ASTRIX reached this result</h3>

    {data.evidence.map((e,i)=>
     <div className="eitem" key={i}>
      <span className={`dot ${e.severity}`}/>
      <div>
       <b>{e.title}</b>
       <p>{e.description}</p>
      </div>
      <small>{e.source}</small>
     </div>
    )}

   </div>
  </div>

  <div className="cards">
   <Card title="AI detector" value={data.detector.label} detail={data.detector.message}/>
   <Card title="Metadata & provenance" value={data.metadata.summary} detail={data.metadata.detail}/>
   <Card title="Digital forensics" value={data.forensics.summary} detail={data.forensics.detail}/>
   <Card title="Manipulation analysis" value={data.manipulation.summary} detail={data.manipulation.detail}/>
  </div>

  <div className="limitations">
   <Info size={17}/>
   <div>
    <b>Important limitation</b>
    <p>{data.limitations.join(' ')}</p>
   </div>
  </div>

  {data.heatmap?.available&&
   <div className="heatmap">
    <h3>Forensic visualization</h3>
    <p>Highlighted regions indicate where supporting forensic signals were concentrated. They are not proof by themselves.</p>
    <img src={`data:image/png;base64,${data.heatmap.overlay_base64}`}/>
   </div>
  }

  <a
   className="download"
   href={`${API}/api/report/${data.analysis_id}`}
   target="_blank"
   rel="noreferrer"
  >
   <Download size={17}/>
   Open analysis report
   <ChevronRight size={17}/>
  </a>

 </div>
}

function Card({title,value,detail}){
 return <div className="card">
  <span>{title}</span>
  <b>{value}</b>
  <p>{detail}</p>
 </div>
}

createRoot(document.getElementById('root')).render(<App/>);