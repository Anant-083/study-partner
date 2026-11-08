"""Quantized MiniLM inference without importing PyTorch. No runtime downloads."""
from pathlib import Path
import threading
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

class MiniLM:
    def __init__(self, directory):
        directory=Path(directory)
        self.tokenizer=Tokenizer.from_file(str(directory/'tokenizer.json'))
        self.tokenizer.enable_truncation(max_length=256)
        self.tokenizer.enable_padding(pad_id=0,pad_token='[PAD]')
        options=ort.SessionOptions()
        options.intra_op_num_threads=1
        options.inter_op_num_threads=1
        options.enable_cpu_mem_arena=False
        self.session=ort.InferenceSession(str(directory/'model_quantized.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
        self.lock=threading.Lock()

    def encode(self,texts,normalize_embeddings=True):
        single=isinstance(texts,str)
        if single: texts=[texts]
        results=[]
        with self.lock:
            for start in range(0,len(texts),4):
                tokens=self.tokenizer.encode_batch(texts[start:start+4])
                inputs={'input_ids':np.array([t.ids for t in tokens],dtype=np.int64),
                        'attention_mask':np.array([t.attention_mask for t in tokens],dtype=np.int64),
                        'token_type_ids':np.array([t.type_ids for t in tokens],dtype=np.int64)}
                output=self.session.run(None,{i.name:inputs[i.name] for i in self.session.get_inputs()})[0]
                mask=inputs['attention_mask'][...,None]
                vectors=(output*mask).sum(axis=1)/np.maximum(mask.sum(axis=1),1) if output.ndim==3 else output
                if normalize_embeddings: vectors=vectors/np.maximum(np.linalg.norm(vectors,axis=1,keepdims=True),1e-12)
                results.extend(vectors.astype(np.float32))
        result=np.array(results,dtype=np.float32)
        return result[0] if single else result
