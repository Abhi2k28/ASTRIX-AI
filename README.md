# ASTRIX AI — Multimodal Authenticity Intelligence

A hackathon-ready image authenticity analyzer built from the original TruthLens prototype. The current implementation focuses on images and provides a real pretrained AI-image classifier plus supporting metadata, forensic, manipulation and explainability modules.

## What is included
- Professional image-first React UI
- FastAPI backend
- Pretrained AI-generated-image detector: `delpot/steganograph-ia-detector`
- EXIF/metadata inspection
- Noise and frequency forensic signals
- JPEG/ELA supporting manipulation signal
- Evidence engine with conservative verdicts
- Suspicious-region visualization
- SHA-256 file hash and analysis ID
- PDF analysis report
- Health endpoint
- Input validation and temporary-file cleanup
- Clear limitations and no fake probability claims

The selected detector is a ViT classifier. Its model card reports 92.3% accuracy on its own 15,000-image balanced test set, with 1.4% false-positive rate on that test set; those are the model author's reported benchmark figures and should not be presented as ASTRIX's own benchmark. The model card also notes limited generalization to unseen generators. See the model documentation before relying on it. Hugging Face documents `AutoImageProcessor` and `AutoModelForImageClassification` as the standard APIs for loading compatible image classifiers.

## Windows setup

### 1. Install prerequisites
- Python 3.11 recommended
- Node.js 20+ recommended

### 2. Backend
Open PowerShell in `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

On the first analysis, Transformers downloads the detector model from Hugging Face. Internet is required for that first model download unless the model is already cached.

### 3. Frontend
Open a second PowerShell in `frontend`:

```powershell
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

## Important
The application is an engineering prototype, not a guarantee of image origin. Missing EXIF does not mean an image is AI-generated. ELA, noise and frequency signals are supporting forensic evidence, not standalone AI detectors. The evidence score is deliberately labelled as an evidence score, not a probability.

## Next benchmark work
Build a held-out dataset containing genuine camera images, AI-generated images from multiple generators and manipulated images. Report accuracy, precision, recall, F1, false-positive rate, false-negative rate and a confusion matrix. Do not tune and test on the same images.

## Future ASTRIX roadmap
Image → Video → Audio → Multimodal media authenticity intelligence.
