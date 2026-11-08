"""Integration checks use real local MiniLM, isolated data, no external services."""
import io
import pytest
from app import app, MODEL_PATH

@pytest.mark.skipif(not (MODEL_PATH/'config.json').exists(), reason='Provision local MiniLM first')
def test_real_document_rag_and_isolation():
    import uuid
    c=app.test_client()
    token=c.get('/api/session').json['csrf']
    result=c.post('/api/auth/signup',json={'name':'test_'+uuid.uuid4().hex[:12],'password':'a-long-test-password'},headers={'X-CSRF-Token':token})
    assert result.status_code==200
    h={'X-CSRF-Token':result.json['csrf']}
    passage='Photosynthesis converts light energy into chemical energy. Chlorophyll absorbs sunlight in plant leaves.'
    r=c.post('/api/files',data={'file':(io.BytesIO(passage.encode()),'biology.txt')},headers=h)
    assert r.status_code==200,r.json
    fid=r.json['id']
    answer=c.post('/api/ask',json={'question':'What does photosynthesis convert?','files':[fid],'strict':True},headers=h)
    assert answer.status_code==200,answer.json
    citations=answer.json['messages'][0]['citations']
    assert citations and all(item['quote'] in passage for item in citations)
    assert c.get('/api/source/'+fid+'/1').json['text']==passage
    assert app.test_client().get('/api/source/'+fid+'/1').status_code==401
    absent=c.post('/api/ask',json={'question':'What is the postal code of the hotel in Madrid?','files':[fid],'strict':True},headers=h)
    assert absent.status_code==200
    assert absent.json['messages'][0]['answer']=='Not found in your documents'
    bad=c.post('/api/ask',json={'question':'Question','files':['not-owned'],'strict':True},headers=h)
    assert bad.status_code==403
