# Deribit Max Gamma Exposure (GEX)

Python script that fetches options data from Deribit and computes gamma exposure (GEX) across all strikes.

Output:
- Spot price
- Strikes with highest absolute GEX above and below spot
- Total net GEX : 
  - Positive -> mean reverting regime (dealers long gamma)
  - Negative -> trend chasing regime (dealers short gamma)
- Total absolute GEX : mass of dealer flow

---

Original GEX paper by SqueezeMetrics: [white_paper.pdf](https://squeezemetrics.com/download/white_paper.pdf)

---

## Setup

```bash
git clone https://github.com/perpgreed/deribit-gex.git
cd deribit-gex
pip install -r requirements.txt
