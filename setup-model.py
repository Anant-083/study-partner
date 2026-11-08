"""One-time, explicitly online model provisioning. Runtime never downloads."""
import os
from pathlib import Path
os.environ.pop('HF_HUB_OFFLINE', None)
os.environ.pop('TRANSFORMERS_OFFLINE', None)
os.environ['HF_HOME'] = str(Path(__file__).parent/'models'/'cache')
from sentence_transformers import SentenceTransformer
target = Path(__file__).parent/'models'/'minilm'
print('Downloading MiniLM from Hugging Face...', flush=True)
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2').save(str(target))
print('Ready for offline document search.', flush=True)
