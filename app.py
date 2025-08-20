import streamlit as st
import json
import os
import fitz  # PyMuPDF
from io import StringIO

DATA_FILE = "knowledge_data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        knowledge_entries = json.load(f)
else:
    knowledge_entries = []

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(knowledge_entries, f, indent=4)

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

st.set_page_config(page_title="Multi-Module Knowledge App", layout="wide")
st.title("📘 Multi-Module Knowledge App")

tab1, tab2, tab3 = st.tabs(["📚 Knowledge Management", "📄 Document Upload & View", "❓ FAQs"])

with tab1:
    st.header("➕ Add New Knowledge Entry")
    title = st.text_input("Title")
    content = st.text_area("Content")
    if st.button("Add Entry"):
        if title and content:
            knowledge_entries.append({"title": title, "content": content})
            save_data()
            st.success("Entry added successfully!")
        else:
            st.error("Please provide both title and content.")

    st.header("🔍 Search Knowledge")
    search_query = st.text_input("Search by keyword")
    if search_query:
        results = [entry for entry in knowledge_entries if search_query.lower() in entry["title"].lower() or search_query.lower() in entry["content"].lower()]
        st.subheader(f"Search Results for '{search_query}':")
        for entry in results:
            st.markdown(f"### {entry['title']}")
            st.markdown(entry['content'])
        if not results:
            st.info("No matching entries found.")

    st.header("📖 All Knowledge Entries")
    for entry in knowledge_entries:
        st.markdown(f"### {entry['title']}")
        st.markdown(entry['content'])

with tab2:
    st.header("📄 Upload and View Document")
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    if uploaded_file:
        st.subheader("📃 Document Content")
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
            st.text_area("Extracted Text", text, height=400)
        elif uploaded_file.type == "text/plain":
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text = stringio.read()
            st.text_area("File Content", text, height=400)

with tab3:
    st.header("❓ Frequently Asked Questions")
    faqs = [
        {"question": "What is this app for?", "answer": "This app helps you manage knowledge entries, view documents, and access FAQs."},
        {"question": "How do I add a knowledge entry?", "answer": "Go to the Knowledge Management tab and fill in the title and content."},
        {"question": "What file types can I upload?", "answer": "You can upload PDF and TXT files in the Document Upload tab."},
        {"question": "Can I share this app with others?", "answer": "Yes, you can deploy it using Streamlit Cloud and share the URL."}
    ]
    for faq in faqs:
        st.markdown(f"**Q: {faq['question']}**")
        st.markdown(f"A: {faq['answer']}")
        st.markdown("---")
