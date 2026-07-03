import os
import torch
from modelcore import axomicmodel
from trainingcore import trainmodel
from datahandler import readfile, readurl, readfilestream, readurlstream
from generator import generate
import time

class axomicai:
    def __init__(self):
        self.model = axomicmodel()
        self.trained = False
        self.checkpointdir = 'checkpoints'
        os.makedirs(self.checkpointdir, exist_ok=True)
        self.history = []
        self.current = -1
        self.maxcheckpoints = 100

    def loadmodel(self, path):
        self.model.load(path)
        self.trained = True

    def exportmodel(self, path):
        self.model.save(path)

    def trainfromfile(self, filepath, epochs=1, batchsize=4, lr=1e-3):
        texts = readfile(filepath)
        if not texts:
            print("No text extracted from file")
            return
        self._train(texts, epochs, batchsize, lr)

    def trainfromurl(self, url, epochs=1, batchsize=4, lr=1e-3):
        texts = readurl(url)
        if not texts:
            print("No text extracted from url")
            return
        self._train(texts, epochs, batchsize, lr)

    def trainfromfilestream(self, filepath, epochs=1, batchsize=4, lr=1e-3, chunksize=200):
        for chunk in readfilestream(filepath, chunksize):
            self._train(chunk, epochs, batchsize, lr)

    def trainfromurlstream(self, url, epochs=1, batchsize=4, lr=1e-3, chunksize=200):
        for chunk in readurlstream(url, chunksize):
            self._train(chunk, epochs, batchsize, lr)

    def trainfromtexts(self, texts, epochs=1, batchsize=4, lr=1e-3):
        self._train(texts, epochs, batchsize, lr)

    def _train(self, texts, epochs, batchsize, lr):
        trainmodel(self.model, texts, epochs, batchsize, lr)
        self.trained = True
        self._savecheckpoint()

    def _savecheckpoint(self):
        ts = str(int(time.time()))
        fname = f'checkpoint_{ts}.pt'
        path = os.path.join(self.checkpointdir, fname)
        self.model.save(path)
        if self.current < len(self.history) - 1:
            self.history = self.history[:self.current+1]
        self.history.append(path)
        self.current += 1
        if len(self.history) > self.maxcheckpoints:
            old = self.history.pop(0)
            if os.path.exists(old):
                os.remove(old)
            self.current -= 1

    def undo(self):
        if self.current <= 0:
            print("No older checkpoint")
            return False
        self.current -= 1
        self._loadcurrent()
        return True

    def redo(self):
        if self.current >= len(self.history) - 1:
            print("No newer checkpoint")
            return False
        self.current += 1
        self._loadcurrent()
        return True

    def _loadcurrent(self):
        if self.current >= 0 and self.current < len(self.history):
            self.loadmodel(self.history[self.current])

    def chat(self, prompt):
        if not self.trained:
            return "Model not trained."
        return self.model.generate(prompt)

    def generatecode(self, prompt):
        return generate(prompt, "code")

    def generateaudio(self, prompt):
        return generate(prompt, "audio")

    def generatevideo(self, prompt):
        return generate(prompt, "video")

    def generateimage(self, prompt):
        return generate(prompt, "image")
