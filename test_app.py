import os, tempfile
os.environ['STUDY_DATA'] = tempfile.mkdtemp()
from app import app, db, verified

def test_quote_verification():
    with db() as c:
        c.execute("INSERT OR REPLACE INTO files VALUES('f','owner','notes.txt','txt')")
        c.execute("INSERT OR REPLACE INTO pages VALUES('f',1,'Water moves through the membrane.')")
        good={'file':'f','page':1,'quote':'Water moves'}
        assert len(verified(c,'owner',['f'],[good])) == 1
        assert not verified(c,'stranger',['f'],[good])
        assert not verified(c,'owner',[],[good])
        assert not verified(c,'owner',['f'],[dict(good,quote='Invented fact')])
        assert not verified(c,'owner',['f'],[dict(good,page=2)])

def test_auth_and_private_sources():
    client=app.test_client()
    assert client.get('/api/files').status_code==401
    assert client.post('/api/auth/signup',json={}).status_code==403
    token=client.get('/api/session').json['csrf']
    r=client.post('/api/auth/signup',headers={'X-CSRF-Token':token},json={'name':'student','password':'a-long-test-password'})
    assert r.status_code==200
    assert client.get('/api/source/f/1').status_code==404
    assert client.get('/api/original/f').status_code==404
    assert client.get('/api/files').json==[]
