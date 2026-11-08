# Study Partner

A Flask + vanilla JavaScript study workspace with local document search, verified source quotations, account-scoped chats and an installable PWA shell.

## Current status
Local MiniLM retrieval, TXT upload, citations, not-found responses and account isolation passed integration tests. Tesseract successfully read a generated test image. Three automated tests pass. The responsive interface includes multi-file upload, drag and drop, source selection, searchable history and tool-readiness indicators.

Supabase cloud tables and private storage have been created, with row-level ownership policies. A cross-account database access test passed. Cloud email login and storage code is included, but a full hosted signup/upload/chat flow and the Docker images have not yet been tested. No live Render deployment is claimed by this repository.

## Local setup
Use Python 3.12. From the repository folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup-model.py
.\.venv\Scripts\python.exe serve.py
```

Open http://127.0.0.1:5000. Create a local username/password account (password minimum 12 characters), upload documents, select sources and ask a question. Keep the server running. Initial installation and model download require internet; subsequent local processing does not.

Install Tesseract for images and scanned PDFs, then put it on PATH or set TESSERACT_CMD to its executable path. A project-local installation at tools/tesseract/tesseract.exe is detected automatically.

For non-strict mode, install Ollama, run `ollama pull llama3.2:3b` once, and keep `ollama serve` running. Ollama is contacted only at 127.0.0.1:11434. Downloaded models and third-party executables are deliberately excluded from GitHub.

## How answers work
PDF pages, PPTX slides, DOCX text/tables, TXT, Markdown and image OCR are extracted locally. MiniLM embeds overlapping 1,000-character chunks. Local mode stores text/vectors in SQLite and uses cosine similarity over the selected files.

Strict mode displays retrieved verbatim passages. Non-strict mode uses Ollama to select shorter exact quotations. Both modes verify that every displayed quote exists in extracted source text. They do not generate paraphrases. Empty results display "Not found in your documents".

Quote verification establishes textual presence, not relevance or semantic entailment. OCR can make transcription mistakes. Citations open extracted page/slide text with highlighting, not a native PDF/PowerPoint viewer. DOCX, TXT and Markdown use section 1 because they have no stable page layout in this extractor.

## Cloud mode: Supabase + Render
Set these environment variables (the .env.example file is a template, not automatically loaded):

- STUDY_MODE=cloud
- SUPABASE_URL: project URL
- SUPABASE_PUBLISHABLE_KEY: project publishable key; no service-role key is used
- SECRET_KEY: a random deployment secret
- HTTPS_ONLY=1
- PORT: assigned by the host

Cloud mode uses Supabase email/password Auth, private Storage, and owner-scoped Postgres tables: documents, passages and conversations. Tokens remain in server-side sessions. Sessions can expire on a restart; document data persists in Supabase. Configure Supabase email confirmation/site URLs for the eventual deployment URL. Google/GitHub OAuth provider setup is not included.

The Dockerfile installs MiniLM and Tesseract for Strict mode. Dockerfile.full additionally includes Ollama and provisions Llama 3.2 3B at build time. It requires substantially more memory and image storage; select hosting resources after testing. Both containers run Waitress and expose only the web app. These Docker builds are prepared but not validated on this machine.

Cloud mode requires internet. Installing the PWA does not install server-side models onto a phone. Local and cloud accounts are separate; automatic local-to-cloud sync and account migration are not implemented.

## Privacy and limits
No external AI inference API is used. Cloud mode does use Supabase APIs for authentication and storage. The service worker caches public interface assets only, never private documents or API responses. Local data is not encrypted at rest: protect the computer and data folder. Never commit data/, models/, tools/, .env files or logs.

File processing is synchronous, with a 25 MB upload limit, 300 PDF-page limit and compressed Office-file expansion limit. This prototype still needs processing isolation, abuse/rate limits, more format coverage, accessibility/browser QA, recovery flows and load testing before unrestricted public use.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The MiniLM integration test skips when the model is not installed. It uses isolated test data, not your uploaded files. Test coverage does not establish production readiness.
