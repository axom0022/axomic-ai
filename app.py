from flask import Flask, render_template, request, jsonify
import os
from axomicai import axomicai

app = Flask(__name__)
ai = axomicai()
if os.path.exists('axomic_weights.pt'):
    ai.loadmodel('axomic_weights.pt')
else:
    print("No weights found. Use manager to train or import.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    response = ai.chat(prompt)
    return jsonify({'response': response})

@app.route('/trainfile', methods=['POST'])
def trainfile():
    data = request.get_json()
    path = data.get('path', '')
    epochs = int(data.get('epochs', 1))
    batch = int(data.get('batch', 4))
    lr = float(data.get('lr', 1e-3))
    if not path or not os.path.exists(path):
        return jsonify({'error': 'Invalid path'}), 400
    ai.trainfromfile(path, epochs, batch, lr)
    ai.exportmodel('axomic_weights.pt')
    return jsonify({'status': 'success'})

@app.route('/trainurl', methods=['POST'])
def trainurl():
    data = request.get_json()
    url = data.get('url', '')
    epochs = int(data.get('epochs', 1))
    batch = int(data.get('batch', 4))
    lr = float(data.get('lr', 1e-3))
    if not url:
        return jsonify({'error': 'No url'}), 400
    ai.trainfromurl(url, epochs, batch, lr)
    ai.exportmodel('axomic_weights.pt')
    return jsonify({'status': 'success'})

@app.route('/trainfilestream', methods=['POST'])
def trainfilestream():
    data = request.get_json()
    path = data.get('path', '')
    epochs = int(data.get('epochs', 1))
    batch = int(data.get('batch', 4))
    lr = float(data.get('lr', 1e-3))
    chunksize = int(data.get('chunksize', 200))
    if not path or not os.path.exists(path):
        return jsonify({'error': 'Invalid path'}), 400
    ai.trainfromfilestream(path, epochs, batch, lr, chunksize)
    ai.exportmodel('axomic_weights.pt')
    return jsonify({'status': 'success'})

@app.route('/trainurlstream', methods=['POST'])
def trainurlstream():
    data = request.get_json()
    url = data.get('url', '')
    epochs = int(data.get('epochs', 1))
    batch = int(data.get('batch', 4))
    lr = float(data.get('lr', 1e-3))
    chunksize = int(data.get('chunksize', 200))
    if not url:
        return jsonify({'error': 'No url'}), 400
    ai.trainfromurlstream(url, epochs, batch, lr, chunksize)
    ai.exportmodel('axomic_weights.pt')
    return jsonify({'status': 'success'})

@app.route('/undo', methods=['POST'])
def undo():
    if ai.undo():
        ai.exportmodel('axomic_weights.pt')
        return jsonify({'status': 'undone'})
    return jsonify({'error': 'No undo'}), 400

@app.route('/redo', methods=['POST'])
def redo():
    if ai.redo():
        ai.exportmodel('axomic_weights.pt')
        return jsonify({'status': 'redone'})
    return jsonify({'error': 'No redo'}), 400

@app.route('/export', methods=['POST'])
def export():
    data = request.get_json()
    path = data.get('path', 'exported_model.pt')
    ai.exportmodel(path)
    return jsonify({'status': 'exported', 'path': path})

@app.route('/import', methods=['POST'])
def importmodel():
    data = request.get_json()
    path = data.get('path', '')
    if not path or not os.path.exists(path):
        return jsonify({'error': 'Invalid path'}), 400
    ai.loadmodel(path)
    ai.exportmodel('axomic_weights.pt')
    return jsonify({'status': 'imported'})

@app.route('/generate/code', methods=['POST'])
def gen_code():
    return jsonify({'result': 'Code gen not available'})

@app.route('/generate/image', methods=['POST'])
def gen_image():
    return jsonify({'error': 'Image gen not supported'}), 501

@app.route('/generate/audio', methods=['POST'])
def gen_audio():
    return jsonify({'error': 'Audio gen not supported'}), 501

@app.route('/generate/video', methods=['POST'])
def gen_video():
    return jsonify({'error': 'Video gen not supported'}), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
