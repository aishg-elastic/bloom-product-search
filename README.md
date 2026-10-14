# 🌸 Bloom — Multimodal Product Catalog Search

A festive ecommerce demo app powered by **Jina omni multimodal embeddings** (`jina-embeddings-v5-omni-small`) on **Elastic Inference Service (EIS)**. Search by feeling, not just keywords.

Built and demoed live at **ElasticON 2026** 🎉

---

## ✨ What Makes This Special

Traditional search only matches keywords in text. Bloom uses Jina omni — a multimodal embedding model that understands both **images and text together**. This means:

- Search by **visual appearance** — colors, patterns, styles
- Find products from **image content** not mentioned in the description
- **Hybrid search** — BM25 keyword + kNN vector combined with RRF

---

## 🔍 Demo Queries

| Query | What it finds | Why it's impressive |
|-------|--------------|---------------------|
| `what should I wear for navratri night` | Garba chaniya choli, dandiya outfit | "navratri" not in description — found visually |
| `do you have leopard pattern shoes` | Animal print shoes | "leopard" removed from description — omni sees the pattern |
| `any items from elastic merch` | Graphic print t-shirt with Elastic logo | Elastic text only in the image — not in title or description |

---

## 🏗️ Architecture

```
Product Image + Description
        │
        ▼
jina-embeddings-v5-omni-small (EIS)
        │
        ▼
1024-dim multimodal embedding
        │
        ▼
Elasticsearch Index (omni-products)
  ├── embedding (dense_vector) — image + text combined
  └── description_semantic (semantic_text) — text only
        │
        ▼
Hybrid Search (RRF)
  ├── BM25 on description (keyword match)
  └── kNN on embedding (visual + semantic match)
```

---

## 🛠️ Prerequisites

- Elastic Cloud Hosted (ECH) 9.0+ cluster
- `jina-embeddings-v5-omni-small` enabled via Elastic Inference Service (EIS)
- Python 3.9+
- Streamlit

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/aishg-elastic/bloom-product-search
cd bloom-product-search

# Install dependencies
pip3 install streamlit pillow --break-system-packages

# Set environment variables
export ESCLUSTER="https://your-cluster.us-east-1.aws.found.io:443"
export ESKEY="your-api-key-here"
```

---

## 🗂️ Project Structure

```
bloom-product-search/
├── bloom_app.py          # Streamlit ecommerce app
├── ingest.py             # Product ingestion script
├── products.json         # Product catalog (23 items)
├── images/               # Product images (p001.jpg - p023.jpg)
└── README.md
```

---

## 🗄️ Step 1 — Create Elasticsearch Index

```json
PUT omni-products
{
  "mappings": {
    "properties": {
      "product_id": { "type": "keyword" },
      "name": { "type": "text" },
      "description": { "type": "text" },
      "description_semantic": {
        "type": "semantic_text",
        "inference_id": ".jina-embeddings-v5-omni-small"
      },
      "category": { "type": "keyword" },
      "color": { "type": "keyword" },
      "gender": { "type": "keyword" },
      "brand": { "type": "keyword" },
      "price_inr": { "type": "float" },
      "image": { "type": "keyword" },
      "embedding": {
        "type": "dense_vector",
        "dims": 1024,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}
```

---

## 📥 Step 2 — Ingest Products

```bash
python3 ingest.py
```

For each product the script:
1. Loads the image and description from `products.json`
2. Sends **both together** to `jina-embeddings-v5-omni-small` via EIS
3. Stores the 1024-dim embedding + all product fields in Elasticsearch

```python
# Image + text sent together to omni
payload = {
    "input": [{
        "content": [
            {"type": "image", "format": "base64", "value": f"data:image/jpeg;base64,{image_base64}"},
            {"type": "text", "value": product['description']}
        ]
    }]
}
```

---

## 🚀 Step 3 — Run the App

```bash
streamlit run bloom_app.py
```

Open `http://localhost:8501` in your browser.

---

## 💡 Two Embedding Fields Explained

| Field | Type | Input | Finds |
|-------|------|-------|-------|
| `embedding` | `dense_vector` | Image + Text | Visual patterns, logos, colors |
| `description_semantic` | `semantic_text` | Text only | Meaning, synonyms, context |

The `embedding` field is what makes Bloom special — it captures what the product **looks like**, not just what it says.

---

## 🌸 Product Catalog

23 products across tops, bottoms, outerwear, footwear, accessories and festive ethnic wear — including Navratri chaniya choli sets and dandiya outfits timed for the festive season.

---

## 🔧 Environment Variables

| Variable | Description |
|----------|-------------|
| `ESCLUSTER` | Your Elasticsearch cluster URL |
| `ESKEY` | Your Elasticsearch API key |

---

## 📚 Resources

- [Jina Embeddings v5 Omni](https://jina.ai/models/jina-embeddings-v5-omni-small/)
- [Elastic Inference Service](https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-elser.html)
- [semantic_text field type](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text-reference)
- [Reciprocal Rank Fusion](https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html)

---

## 🌸 Built With

- **Elasticsearch** — vector store + hybrid search
- **jina-embeddings-v5-omni-small** — multimodal embeddings via EIS
- **Streamlit** — frontend
- **Python** — ingestion pipeline

---

*Built for ElasticON 2026 — Navratri Edition 🎊*
