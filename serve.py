import os
from waitress import serve
from app import app
serve(app, host='0.0.0.0' if os.environ.get('RENDER') else '127.0.0.1', port=int(os.environ.get('PORT','5000')), threads=4)
