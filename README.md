# Retail Multimodal Search Demo
**Jina jina-clip-v2 + Elasticsearch on Elastic Cloud**

---

## What this demo does

Lets you search a retail product catalogue by:
- **Text** — "blue running shoes for men"
- **Image** — upload a photo, find visually similar products
- **Hybrid** — combine both for the most precise results

The magic: Jina's `jina-clip-v2` model maps both text and images into the
same 1024-dimensional vector space, so a text query can match image
embeddings and vice versa.

---

## Prerequisites

| What | Where |
|---|---|
| Elastic Cloud account | https://cloud.elastic.co (free trial works) |
| Elastic Cloud ID | Deployment → Copy Cloud ID |
| Elastic API key | Kibana → Stack Management → API Keys → Create |

---

## Setup (one-time, ~10 min)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your credentials (or paste them into the sidebar in the app)
export ELASTIC_CLOUD_ID="your_cloud_id_here"
export ELASTIC_API_KEY="your_api_key_here"

# 3. Create the Elasticsearch index and Jina inference endpoint
python setup_index.py

# 4. Ingest products (200 products ≈ 5-10 min including image downloads)
python ingest.py --limit 200

# 5. Launch the app
streamlit run app.py
```

---

## File overview

```
setup_index.py   Creates the ES index (dense_vector, HNSW) and registers
                 the Jina inference endpoint on Elastic Inference Service.

ingest.py        Downloads a public fashion product dataset, fetches product
                 images, generates multimodal embeddings (text + image averaged),
                 and bulk-indexes into Elasticsearch.

app.py           Streamlit UI with three search tabs:
                   • Text search
                   • Image search
                   • Hybrid search (averaged embeddings)

requirements.txt Python dependencies.
```

---

## How the embeddings work

```
Product at ingest time:
  title + description  ──► Jina text tower  ──► 1024-dim vector
  product image        ──► Jina image tower ──► 1024-dim vector
                                                      │
                                             average + L2-normalise
                                                      │
                                             stored in dense_vector field

Query at search time:
  text query  ──► Jina text tower  ──┐
  image query ──► Jina image tower ──┴─ average (if hybrid) ──► kNN search
```

---

## Scaling up

- Increase `--limit` in `ingest.py` (full dataset: ~48 000 products)
- Bump `num_allocations` in `setup_index.py` for faster inference
- Add price / rating filters to `knn_search()` in `app.py`
- Enable hybrid BM25 + kNN with `"query": {"match": {...}}` alongside `"knn"`
  for improved recall on exact keyword matches

---

## Useful links

- [Elastic multimodal search docs](https://www.elastic.co/docs/solutions/search/multimodal-search)
- [Jina jina-clip-v2 model](https://jina.ai/news/jina-clip-v2/)
- [Elasticsearch kNN search](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html)
- [Elastic Inference Service](https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-elser.html)
