import os
import json
import zstandard as zstd
import requests
import csv
import xml.etree.ElementTree as et

def readfile(path):
    texts = []
    ext = os.path.splitext(path)[1].lower()
    if ext == '.txt':
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    texts.append(line)
    elif ext == '.jsonl':
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    txt = obj.get('text', '')
                    if txt:
                        texts.append(txt)
                except:
                    pass
    elif ext == '.zst':
        with open(path, 'rb') as f:
            dctx = zstd.ZstdDecompressor()
            reader = dctx.stream_reader(f)
            for line in reader:
                try:
                    line = line.decode('utf-8')
                    obj = json.loads(line)
                    txt = obj.get('text', '')
                    if txt:
                        texts.append(txt)
                except:
                    pass
    elif ext == '.csv':
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for cell in row:
                    if cell.strip():
                        texts.append(cell.strip())
    elif ext == '.xml':
        tree = et.parse(path)
        root = tree.getroot()
        for elem in root.iter():
            if elem.text and elem.text.strip():
                texts.append(elem.text.strip())
    elif ext == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        texts.append(item)
                    elif isinstance(item, dict):
                        for v in item.values():
                            if isinstance(v, str) and v.strip():
                                texts.append(v)
            elif isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, str) and v.strip():
                        texts.append(v)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    texts.append(line)
    return texts

def readurl(url):
    texts = []
    response = requests.get(url, stream=True)
    if url.endswith('.zst'):
        dctx = zstd.ZstdDecompressor()
        reader = dctx.stream_reader(response.raw)
        for line in reader:
            try:
                line = line.decode('utf-8')
                obj = json.loads(line)
                txt = obj.get('text', '')
                if txt:
                    texts.append(txt)
            except:
                pass
    elif url.endswith('.jsonl') or 'json' in response.headers.get('content-type', ''):
        for line in response.iter_lines():
            if line:
                try:
                    obj = json.loads(line)
                    txt = obj.get('text', '')
                    if txt:
                        texts.append(txt)
                except:
                    pass
    else:
        for line in response.iter_lines():
            if line:
                try:
                    txt = line.decode('utf-8').strip()
                    if txt:
                        texts.append(txt)
                except:
                    pass
    return texts

def readfilestream(path, chunksize=200):
    batch = []
    ext = os.path.splitext(path)[1].lower()
    if ext == '.zst':
        with open(path, 'rb') as f:
            dctx = zstd.ZstdDecompressor()
            reader = dctx.stream_reader(f)
            for line in reader:
                try:
                    line = line.decode('utf-8')
                    obj = json.loads(line)
                    txt = obj.get('text', '')
                    if txt:
                        batch.append(txt)
                        if len(batch) >= chunksize:
                            yield batch
                            batch = []
                except:
                    continue
    elif ext == '.jsonl':
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    txt = obj.get('text', '')
                    if txt:
                        batch.append(txt)
                        if len(batch) >= chunksize:
                            yield batch
                            batch = []
                except:
                    continue
    else:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    batch.append(line)
                    if len(batch) >= chunksize:
                        yield batch
                        batch = []
    if batch:
        yield batch

def readurlstream(url, chunksize=200):
    batch = []
    response = requests.get(url, stream=True)
    if url.endswith('.zst'):
        dctx = zstd.ZstdDecompressor()
        reader = dctx.stream_reader(response.raw)
        for line in reader:
            try:
                line = line.decode('utf-8')
                obj = json.loads(line)
                txt = obj.get('text', '')
                if txt:
                    batch.append(txt)
                    if len(batch) >= chunksize:
                        yield batch
                        batch = []
            except:
                continue
    elif url.endswith('.jsonl') or 'json' in response.headers.get('content-type', ''):
        for line in response.iter_lines():
            if line:
                try:
                    obj = json.loads(line)
                    txt = obj.get('text', '')
                    if txt:
                        batch.append(txt)
                        if len(batch) >= chunksize:
                            yield batch
                            batch = []
                except:
                    continue
    else:
        for line in response.iter_lines():
            if line:
                try:
                    txt = line.decode('utf-8').strip()
                    if txt:
                        batch.append(txt)
                        if len(batch) >= chunksize:
                            yield batch
                            batch = []
                except:
                    continue
    if batch:
        yield batch
