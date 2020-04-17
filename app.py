from flask import Flask, request, jsonify,url_for
import json
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/hello')
def home():
    return jsonify({'msg': 'Hello'})


@app.route('/api/short_url', methods=['GET', 'POST'])
def short_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json', 'r') as urls_file:
                urls = json.loads(urls_file.read())
        if request.json['code'] in urls.keys():
            return jsonify({'msg': 'That short name is already taken'}), 201
        if 'url' in request.json.keys():
            urls[request.json['code']] = {
                'url': request.json['url'], 'emailid': request.json['email']}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        return jsonify({'msg': 'Data added successfully'}), 200
    else:
        return jsonify({'msg': 'API is WORKING'}), 200


@app.route('/api/short_file_url', methods=['GET', 'POST'])
def short_file_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json', 'r') as urls_file:
                urls = json.loads(urls_file.read())
        if request.form['code'] in urls.keys():
            return jsonify({'msg': 'That short name is already taken', 'status': 201})
        else:
            f = request.files['file']
            full_name = request.form['code']+"_"+secure_filename(f.filename)
            f.save(os.path.dirname(os.path.abspath(__file__)) +
                   '\\static'+'\\uploaded_files'+'\\'+full_name)
            urls[request.form['code']] = {
                'file': full_name, 'emailid': request.form['email']}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        return jsonify({'msg': 'Data added successfully', 'status': 200})
    else:
        return jsonify({'msg': 'API is WORKING', 'status': 200})


@app.route('/api/get_short_urls/<string:email>', methods=['GET'])
def get_short_urls(email: str):
    urls = {}
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as urls_file:
            urls = json.loads(urls_file.read())
        finaldata = {}
        for key, value in enumerate(urls):
            if urls[value]['emailid'] == email:
                if 'url' in urls[value]:
                    if 'http' in urls[value]['url'] or 'https' in urls[value]['url']:
                        finaldata[value] = urls[value]['url']
                    else:
                        finaldata[value] = "https://"+urls[value]['url']
        return jsonify({'message': finaldata})
    return jsonify({'message': 'No Data'})


@app.route('/api/get_file_urls/<string:email>', methods=['GET'])
def get_file_urls(email: str):
    urls = {}
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as urls_file:
            urls = json.loads(urls_file.read())
        finaldata = {}
        for key, value in enumerate(urls):
            if urls[value]['emailid'] == email:
                if 'file' in urls[value]:
                    finaldata[value] = url_for('static',filename='uploaded_files/'+urls[value]['file'],_external=True)
        return jsonify({'message': finaldata})
    return jsonify({'message': 'No Data'})

@app.route('/api/delete_url/<string:code>', methods=['DELETE'])
def delete_url(code: str):
    urls = {}
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as urls_file:
            urls = json.loads(urls_file.read())
        for element in urls:
            if code in element:
                del urls[code]
                break
        if(len(urls)==0):
            os.remove("urls.json")
        else:
            with open('urls.json', 'w') as urls_file:
                json.dump(urls, urls_file)
        return jsonify({'message':'Data Deleted Successfully','status': 200})
    return jsonify({'message': 'Could not delete', 'status': 500})
@app.route('/api/delete_file/<string:code>', methods=['DELETE'])
def delete_file(code: str):
    urls = {}
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as urls_file:
            urls = json.loads(urls_file.read())
        for element,value in enumerate(urls):
            if code in value:
                if 'file' in urls[value]:
                    os.remove(os.path.dirname(os.path.abspath(__file__)) +'\\static'+'\\uploaded_files'+'\\'+urls[value]['file'])
                    del urls[code]
                    break
        if(len(urls)==0):
            os.remove("urls.json")
        else:
            with open('urls.json', 'w') as urls_file:
                json.dump(urls, urls_file)
        return jsonify({'message':'Data Deleted Successfully','status': 200})
    return jsonify({'message': 'Could not delete', 'status': 500})
