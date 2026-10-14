import streamlit as st
import os
import json
import urllib.request
import urllib.error
from PIL import Image
import base64
from io import BytesIO

ESCLUSTER = os.environ.get('ESCLUSTER', '')
ESKEY = os.environ.get('ESKEY', '')
INFERENCE_ENDPOINT = ".jina-embeddings-v5-omni-small"
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

st.set_page_config(page_title="Bloom", page_icon="🌸", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #FFFFFF;
    color: #1A1A2E !important;
}

p, span, div, label, .stMarkdown, .stText {
    color: #1A1A2E !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #1A1A2E !important;
}

.stApp {
    background: #FFFFFF;
}

/* Hero banner */
.bloom-hero {
    background: linear-gradient(135deg, #FFF0F5 0%, #FFF8E7 40%, #F0F8FF 100%);
    border-radius: 24px;
    padding: 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    border: 1px solid #FFE4F0;
}

.bloom-hero::before {
    content: "🌸 ✨ 🎀 🌺 ⭐ 🌸 ✨ 🎀 🌺 ⭐ 🌸 ✨";
    position: absolute;
    top: 12px;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 18px;
    opacity: 0.5;
    letter-spacing: 8px;
}

.bloom-hero::after {
    content: "🌸 ✨ 🎀 🌺 ⭐ 🌸 ✨ 🎀 🌺 ⭐ 🌸 ✨";
    position: absolute;
    bottom: 12px;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 18px;
    opacity: 0.5;
    letter-spacing: 8px;
}

.bloom-title {
    font-family: 'Playfair Display', serif;
    font-size: 56px;
    font-weight: 600;
    color: #1A1A2E;
    text-align: center;
    margin: 0;
    letter-spacing: -1px;
}

.bloom-title span {
    color: #E91E8C;
}

.bloom-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    color: #666;
    text-align: center;
    margin-top: 8px;
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.bloom-badge {
    display: inline-block;
    background: linear-gradient(90deg, #E91E8C, #FF6B35);
    color: white;
    font-size: 11px;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Search bar */
.stTextInput input {
    border: 2px solid #FFB3D9 !important;
    border-radius: 50px !important;
    padding: 14px 24px !important;
    font-size: 16px !important;
    font-family: 'Inter', sans-serif !important;
    background: #FFF !important;
    color: #1A1A2E !important;
    box-shadow: 0 4px 20px rgba(233, 30, 140, 0.08) !important;
    transition: all 0.3s ease !important;
}

.stTextInput input::placeholder {
    color: #999 !important;
}

.stTextInput input[autocomplete] {
    autocomplete: off !important;
}

.stTextInput input:focus {
    border-color: #E91E8C !important;
    box-shadow: 0 4px 24px rgba(233, 30, 140, 0.2) !important;
}

/* Product card */
.product-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid #FFE4F0;
    transition: all 0.3s ease;
    height: 100%;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.product-card:hover {
    box-shadow: 0 12px 40px rgba(233, 30, 140, 0.15);
    transform: translateY(-4px);
    border-color: #FFB3D9;
}

.product-img-wrap {
    background: linear-gradient(135deg, #FFF0F5, #FFF8E7);
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 220px;
}

.product-info {
    padding: 16px;
}

.product-name {
    font-family: 'Playfair Display', serif;
    font-size: 15px;
    font-weight: 600;
    color: #1A1A2E;
    margin: 0 0 4px 0;
}

.product-desc {
    font-size: 12px;
    color: #888;
    margin: 0 0 10px 0;
    line-height: 1.5;
}

.product-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
}

.product-price {
    font-size: 18px;
    font-weight: 600;
    color: #E91E8C;
}

.product-gender {
    font-size: 11px;
    color: #999;
    background: #FFF0F5;
    padding: 3px 10px;
    border-radius: 20px;
}

.product-score {
    font-size: 11px;
    color: #aaa;
    margin-top: 6px;
}

.product-id {
    font-size: 10px;
    color: #bbb;
    font-family: monospace;
}

/* Section header */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    color: #1A1A2E;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #FFE4F0;
}

/* Filters */
.stSelectbox div {
    border-radius: 12px !important;
}

/* Festive banner */
.festive-banner {
    background: linear-gradient(90deg, #E91E8C, #FF6B35, #FFD700, #FF6B35, #E91E8C);
    background-size: 300% 100%;
    animation: festive 4s linear infinite;
    color: white;
    text-align: center;
    padding: 8px;
    font-size: 13px;
    font-weight: 500;
    border-radius: 8px;
    margin-bottom: 16px;
    letter-spacing: 1px;
}

@keyframes festive {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

/* Pill tags */
.pill {
    display: inline-block;
    background: #FFF0F5;
    color: #E91E8C;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px;
    border: 1px solid #FFB3D9;
}

/* Button */
.stButton button {
    background: linear-gradient(135deg, #E91E8C, #FF6B35) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 10px 32px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
}

.stButton button:hover {
    opacity: 0.9 !important;
    box-shadow: 0 8px 24px rgba(233, 30, 140, 0.3) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFDE7 !important;
}

[data-testid="stSidebar"] * {
    color: #1A1A2E !important;
}

[data-testid="stSidebar"] .stTextInput input {
    background: #FFFFFF !important;
    color: #1A1A2E !important;
    border: 1px solid #FFB3D9 !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #E91E8C, #FF6B35) !important;
    color: white !important;
}

/* Hide streamlit defaults */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Festive banner
st.markdown('<div class="festive-banner">🌸 FESTIVE SEASON SALE — Up to 40% off on selected items 🎀</div>', unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="bloom-hero">
    <h1 class="bloom-title">Bloo<span>m</span></h1>
    <p class="bloom-tagline">Discover fashion through AI — search by feeling, not just words</p>
</div>
""", unsafe_allow_html=True)

# Search bar
col_search, col_btn = st.columns([5, 1])
with col_search:
    query = st.text_input("", placeholder="🔍  Try: navratri outfit, elastic logo tshirt, blue outfit for men...", autocomplete="off")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("Search")

# Quick search pills
st.markdown("""
<div style="margin: -8px 0 20px 0;">
    <span style="font-size:12px; color:#999; margin-right:8px;">Try:</span>
    <span class="pill">elastic tshirt</span>
    <span class="pill">women's accessories</span>
    <span class="pill">blue outfit</span>
    <span class="pill">festive look</span>
    <span class="pill">casual wear</span>
</div>
""", unsafe_allow_html=True)

# Filters
with st.expander("🎛️ Filters", expanded=False):
    f1, f2, f3 = st.columns(3)
    with f1:
        gender_filter = st.selectbox("Gender", ["All", "Men's", "Women's", "Unisex"])
    with f2:
        category_filter = st.selectbox("Category", ["All", "tops", "bottoms", "outerwear", "accessories", "footwear"])
    with f3:
        top_k = 3

def get_embedding(query):
    payload = json.dumps({"input": [query]})
    req = urllib.request.Request(
        f"{ESCLUSTER}/_inference/embedding/{INFERENCE_ENDPOINT}",
        data=payload.encode(),
        headers={"Authorization": f"ApiKey {ESKEY}", "Content-Type": "application/json"},
        method="POST"
    )
    response = json.loads(urllib.request.urlopen(req).read().decode())
    return response["embeddings"][0]["embedding"]

def search_products(query_embedding, k):
    search_body = {
        "min_score": 0.55,
        "knn": {"field": "embedding", "query_vector": query_embedding, "k": k, "num_candidates": 50},
        "_source": ["product_id", "name", "description", "category", "color", "gender", "price_inr", "image", "brand"],
        "size": k
    }
    req = urllib.request.Request(
        f"{ESCLUSTER}/omni-products/_search",
        data=json.dumps(search_body).encode(),
        headers={"Authorization": f"ApiKey {ESKEY}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        response = json.loads(urllib.request.urlopen(req).read().decode())
        return response['hits']['hits']
    except urllib.error.HTTPError as e:
        st.error(f"Search error: {e.read().decode()}")
        return []

def load_image(filename):
    path = f"{IMAGES_DIR}/{filename}"
    if os.path.exists(path):
        return path  # Return path directly instead of PIL Image
    return None

if query or search_btn:
    if query:
        with st.spinner("✨ Finding your perfect match..."):
            try:
                query_embedding = get_embedding(query)
                hits = search_products(query_embedding, top_k)

                # Apply filters
                if gender_filter != "All":
                    hits = [h for h in hits if h['_source'].get('gender') == gender_filter]
                if category_filter != "All":
                    hits = [h for h in hits if h['_source'].get('category') == category_filter]

                if not hits:
                    st.info("No products found. Try a different search!")
                else:
                    st.markdown(f'<div class="section-header">✨ Showing results for "{query}"</div>', unsafe_allow_html=True)

                    cols = st.columns(5)
                    for i, hit in enumerate(hits):
                        src = hit['_source']
                        score = hit['_score']
                        img = load_image(src.get('image', ''))

                        with cols[i % 5]:
                            with st.container():
                                if img:
                                    st.image(img, use_container_width=True)
                                else:
                                    st.markdown("👕", unsafe_allow_html=True)

                                if src.get('brand'):
                                    st.markdown(f"<span style='font-size:10px;color:#E91E8C;font-weight:600;'>{src.get('brand','').upper()}</span>", unsafe_allow_html=True)
                                st.markdown(f"**{src['name']}**")
                                st.caption(f"{src['description'][:80]}...")
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.markdown(f"<span style='font-size:18px;font-weight:700;color:#E91E8C;'>₹{int(src['price_inr'])}</span>", unsafe_allow_html=True)
                                with c2:
                                    st.caption(src.get('gender', ''))
                                st.caption(f"Match: {score:.2%} · {src['product_id']}")

                                with st.expander("📋 View full details"):
                                    st.markdown(f"**{src['name']}**")
                                    st.markdown(f"_{src['description']}_")
                                    c1, c2 = st.columns(2)
                                    with c1:
                                        st.markdown(f"**Price:** ₹{int(src['price_inr'])}")
                                        st.markdown(f"**Category:** {src.get('category','').title()}")
                                        st.markdown(f"**Color:** {src.get('color','').title()}")
                                    with c2:
                                        st.markdown(f"**Gender:** {src.get('gender','')}")
                                        if src.get('brand'):
                                            st.markdown(f"**Brand:** {src.get('brand')}")
                                        st.markdown(f"**Product ID:** `{src['product_id']}`")
                                        st.markdown(f"**Match Score:** {score:.2%}")

            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.info("Enter a search query above!")

else:
    # Default landing — show all products
    st.markdown('<div class="section-header">🛍️ All Products</div>', unsafe_allow_html=True)
    
    try:
        req = urllib.request.Request(
            f"{ESCLUSTER}/omni-products/_search",
            data=json.dumps({"query": {"match_all": {}}, "size": 10, "_source": ["product_id", "name", "description", "price_inr", "image", "gender", "brand"]}).encode(),
            headers={"Authorization": f"ApiKey {ESKEY}", "Content-Type": "application/json"},
            method="POST"
        )
        response = json.loads(urllib.request.urlopen(req).read().decode())
        hits = response['hits']['hits']

        cols = st.columns(5)
        for i, hit in enumerate(hits):
            src = hit['_source']
            img = load_image(src.get('image', ''))
            with cols[i % 4]:
                if img:
                    st.image(img, use_container_width=True)
                if src.get('brand'):
                    st.markdown(f"<span style='font-size:10px;color:#E91E8C;font-weight:600;'>{src.get('brand','').upper()}</span>", unsafe_allow_html=True)
                st.markdown(f"**{src['name']}**")
                st.markdown(f"<span style='font-size:18px;font-weight:700;color:#E91E8C;'>₹{int(src['price_inr'])}</span>", unsafe_allow_html=True)
                st.caption(src.get('gender', ''))
    except Exception as e:
        st.info("Connect to your Elasticsearch cluster to see products.")

# Footer
st.markdown("""
<div style="text-align:center;padding:40px 0 20px 0;color:#ccc;font-size:12px;border-top:1px solid #FFE4F0;margin-top:40px;">
    🌸 Bloom — Powered by Jina omni multimodal search on Elastic &nbsp;|&nbsp; © 2026 Bloom Fashion
</div>
""", unsafe_allow_html=True)

# ── Floating Chat Assistant ──────────────────────────────────────────────────
st.markdown("""
<style>
.chat-fab {
    position: fixed;
    bottom: 28px;
    right: 28px;
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #E91E8C, #FF6B35);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 4px 20px rgba(233,30,140,0.4);
    cursor: pointer;
    z-index: 999;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%   { box-shadow: 0 4px 20px rgba(233,30,140,0.4); }
    50%  { box-shadow: 0 4px 32px rgba(233,30,140,0.7); }
    100% { box-shadow: 0 4px 20px rgba(233,30,140,0.4); }
}
.chat-window {
    background: white;
    border-radius: 20px;
    border: 1px solid #FFE4F0;
    padding: 20px;
    box-shadow: 0 8px 40px rgba(233,30,140,0.15);
}
.chat-msg-user {
    background: linear-gradient(135deg, #E91E8C, #FF6B35);
    color: white;
    padding: 10px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 6px 0;
    font-size: 14px;
    text-align: right;
}
.chat-msg-bot {
    background: #FFF0F5;
    color: #1A1A2E;
    padding: 10px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 6px 0;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# Chat state
if 'chat_open' not in st.session_state:
    st.session_state.chat_open = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# FAB button
st.markdown('<div class="chat-fab">🌸</div>', unsafe_allow_html=True)

with st.sidebar:
    st.divider()
    st.markdown("### 🌸 Bloom Assistant")
    st.caption("Ask me anything about our products!")

    # Chat history
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f'<div class="chat-msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-msg-bot">{msg["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    chat_input = st.text_input("Ask Bloom...", key="chat_input", placeholder="e.g. do you have blue shoes?")
    ask_btn = st.button("Ask 🌸", key="ask_btn")

    if ask_btn and chat_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": chat_input})

        try:
            # Get embedding for query
            req = urllib.request.Request(
                f"{ESCLUSTER}/_inference/embedding/.jina-embeddings-v5-omni-small",
                data=json.dumps({"input": [chat_input]}).encode(),
                headers={"Authorization": f"ApiKey {ESKEY}", "Content-Type": "application/json"},
                method="POST"
            )
            query_embedding = json.loads(urllib.request.urlopen(req).read().decode())["embeddings"][0]["embedding"]

            # Search products
            search_body = json.dumps({
                "retriever": {"rrf": {"retrievers": [
                    {"standard": {"query": {"match": {"description": chat_input}}}},
                    {"knn": {"field": "embedding", "query_vector": query_embedding, "k": 3, "num_candidates": 20}}
                ]}},
                "_source": ["product_id", "name", "price_inr", "gender", "color", "category", "description"],
                "size": 3
            })
            req = urllib.request.Request(
                f"{ESCLUSTER}/omni-products/_search",
                data=search_body.encode(),
                headers={"Authorization": f"ApiKey {ESKEY}", "Content-Type": "application/json"},
                method="POST"
            )
            results = json.loads(urllib.request.urlopen(req).read().decode())
            hits = results['hits']['hits']

            if hits:
                reply = f"I found {len(hits)} item(s) for you! 🛍️\n\n"
                for hit in hits:
                    src = hit['_source']
                    reply += f"**{src['name']}** — ₹{int(src['price_inr'])} ({src.get('gender','')})\n"
                reply += "\nSearch above to see the full results with images!"
            else:
                reply = "Hmm, I couldn't find anything matching that. Try different keywords! 🌸"

            st.session_state.chat_history.append({"role": "bot", "content": reply})

        except Exception as e:
            st.session_state.chat_history.append({"role": "bot", "content": "Sorry, something went wrong. Please try again! 🌸"})

        st.rerun()

    if st.button("Clear chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()
