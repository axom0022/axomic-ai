import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

char2idx = {chr(i): i-32 for i in range(32, 127)}
char2idx['<PAD>'] = 0
idx2char = {v: k for k, v in char2idx.items()}
vocabsize = 256

class textdataset(Dataset):
    def __init__(self, texts, maxlen=128):
        self.texts = texts
        self.maxlen = maxlen

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx][:self.maxlen]
        indices = [char2idx.get(c, 0) for c in text]
        if len(indices) < self.maxlen:
            indices += [0] * (self.maxlen - len(indices))
        return torch.tensor(indices, dtype=torch.long)

def trainmodel(model, dataset, epochs=1, batchsize=4, lr=1e-3):
    if len(dataset) < 2:
        return
    traindata = textdataset(dataset)
    dataloader = DataLoader(traindata, batch_size=min(batchsize, len(dataset)), shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    model.train()
    for epoch in range(epochs):
        total = 0
        for batch in dataloader:
            batch = batch.to(model.device)
            inp = batch[:, :-1]
            tgt = batch[:, 1:]
            mask = (inp == 0)
            out = model(inp, mask)
            loss = criterion(out.reshape(-1, model.vocab), tgt.reshape(-1))
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            total += loss.item()
    model.eval()
