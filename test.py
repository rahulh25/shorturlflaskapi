import requests

r = requests.get('http://127.0.0.1/')
assert 'HomePage' in r.content, 'No homepage loaded'