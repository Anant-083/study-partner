"""Supervise the two local processes. Never exposes Ollama publicly."""
import os,subprocess,sys,time,signal
env=dict(os.environ,OLLAMA_HOST='127.0.0.1:11434',OLLAMA_NO_CLOUD='1')
ollama=subprocess.Popen(['ollama','serve'],env=env)
web=subprocess.Popen([sys.executable,'serve.py'],env=env)
def stop(*args):
    for p in (web,ollama):
        if p.poll() is None: p.terminate()
    for p in (web,ollama):
        try: p.wait(timeout=10)
        except subprocess.TimeoutExpired: p.kill()
signal.signal(signal.SIGTERM,stop)
signal.signal(signal.SIGINT,stop)
try:
    while web.poll() is None and ollama.poll() is None: time.sleep(1)
finally: stop()
sys.exit(web.returncode or ollama.returncode or 0)
