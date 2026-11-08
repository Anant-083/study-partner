from pathlib import Path
from urllib.request import urlretrieve
p=Path(__file__).parent/'models'/'minilm-onnx'
p.mkdir(parents=True,exist_ok=True)
base='https://huggingface.co/Xenova/all-MiniLM-L6-v2/resolve/main/'
for remote,name in [('tokenizer.json','tokenizer.json'),('config.json','config.json'),('onnx/model_quantized.onnx','model_quantized.onnx')]:
    print('Downloading '+name,flush=True)
    urlretrieve(base+remote,p/name)
print('Model ready',flush=True)
