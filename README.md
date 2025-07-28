# Deribit Max Gamma Exposure (GEX)

Python script that fetches options data from Deribit and identifies the strikes with the highest absolute gamma exposure (GEX) above and below the current spot price.

---

Original GEX paper by SqueezeMetrics: [white_paper.pdf](https://squeezemetrics.com/download/white_paper.pdf)

---

## Setup

```bash
git clone https://github.com/perpgreed/deribit-gex.git
cd deribit-gex
pip install -r requirements.txt
