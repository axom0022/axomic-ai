import torch
import torch.nn as nn
import math

class axomicmodel(nn.Module):
    def __init__(self, vocab=256, embed=256, heads=8, layers=6, maxlen=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab, embed)
        self.pos = self.posenc(maxlen, embed)
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(embed, heads, dim_feedforward=1024, dropout=0.1),
            num_layers=layers
        )
        self.decoder = nn.Linear(embed, vocab)
        self.maxlen = maxlen
        self.vocab = vocab
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)

    def posenc(self, length, dim):
        pe = torch.zeros(length, dim)
        pos = torch.arange(0, length).unsqueeze(1)
        div = torch.exp(torch.arange(0, dim, 2) * -(math.log(10000.0) / dim))
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        return pe.unsqueeze(0)

    def forward(self, x, mask=None):
        seqlen = x.size(1)
        x = self.embedding(x) + self.pos[:, :seqlen, :].to(x.device)
        x = self.encoder(x, src_key_padding_mask=mask)
        return self.decoder(x)

    def generate(self, prompt, maxnew=100):
        self.eval()
        return "Echo: " + prompt

    def load(self, path):
        self.load_state_dict(torch.load(path, map_location=self.device))

    def save(self, path):
        torch.save(self.state_dict(), path)
