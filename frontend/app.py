import requests
import streamlit as st

from config import BACKEND_URL

API_BASE_URL = BACKEND_URL

st.set_page_config(page_title="Company Document Assistant", page_icon="💬")
st.title("Company Document Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Documents")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file is not None and st.button("Index this PDF"):
        with st.spinner("Indexing..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                resp = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                st.success(
                    f"Indexed {data['filename']}: "
                    f"{data['pages_indexed']} page(s), {data['chunks_indexed']} chunk(s)"
                )
            except requests.exceptions.ConnectionError:
                st.error("Could not reach the backend API. Is it running?")
            except requests.RequestException as e:
                detail = ""
                if e.response is not None:
                    try:
                        detail = e.response.json().get("detail", "")
                    except ValueError:
                        pass
                st.error(f"Upload failed: {detail or e}")


def render_sources(sources: list[dict]) -> None:
    if not sources:
        return
    with st.expander("Sources"):
        for s in sources:
            st.markdown(f"- {s['doc_name']}, p.{s['page_no']} (score={s['score']:.3f})")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        render_sources(message.get("sources", []))

query = st.chat_input("Ask a question about the company documents...")
if query:
    st.session_state.messages.append({"role": "user", "content": query, "sources": []})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")

        answer = ""
        sources: list[dict] = []
        try:
            resp = requests.post(f"{API_BASE_URL}/chat", json={"query": query}, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            answer = data["answer"]
            sources = data["sources"]
        except requests.exceptions.ConnectionError:
            answer = "Could not reach the backend API. Is it running? (`uvicorn api.main:app`)"
        except requests.RequestException as e:
            detail = ""
            if e.response is not None:
                try:
                    detail = e.response.json().get("detail", "")
                except ValueError:
                    pass
            answer = f"Request failed: {detail or e}"

        placeholder.markdown(answer)
        render_sources(sources)
        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
