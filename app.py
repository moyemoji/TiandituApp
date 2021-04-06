#!/usr/bin/env python
# -* coding: utf-8 -*-
import os
from flask import Flask, render_template, request, make_response, send_from_directory, send_file
import exts

 
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def main():
    return render_template("Tianditu.html")

@app.route('/image', methods=["POST"])
def getImage():
    tl_lng = request.form.get('tl_lng')
    tl_lat = request.form.get('tl_lat')
    br_lng = request.form.get('br_lng')
    br_lat = request.form.get('br_lat')
    zoom = request.form.get('zoom')
    filename = exts.downloadImage(tl_lng, tl_lat, br_lng, br_lat, zoom)
    return filename

@app.route('/download/<path:filename>', methods=['GET'])
def downloadImage(filename):
    result_path = os.path.join("merge/tiff", filename)
    response = make_response(send_file(result_path, mimetype='image/tiff', as_attachment=True))
    response.headers['filename'] = filename.encode('utf-8')
    return response

    
if __name__ == '__main__':
    app.run()