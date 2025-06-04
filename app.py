import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.schema import SystemMessage, HumanMessage

# Simulated tools

@tool
def vector_search(query: str) -> str:
    """Simulated vector database search for regulatory/tax answers."""
    return "[Vector DB] Simulated result: Solar panels in TX use 5-year MACRS depreciation. [source: mock-chroma]"

@tool
def fetch_tax_document(code: str) -> str:
    """Simulates retrieving an IRS document by code."""
    return f"[IRS] Simulated: Document {code} explains MACRS for solar. [source: mock-irs]"

@tool
def get_case_law_summary(case_name: str) -> str:
    """Simulates a legal case summary lookup."""
    return f"[Legal DB] Simulated: In *{case_name}*, court upheld MACRS. [source: mock-caselaw]"

# Chat model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Streamlit UI
st.set_page_config(page_title="Echo AI", layout="centered")
st.title("🔗 Echo AI - Simulated Chatbot")

with st.form("qa_form"):
    question = st.text_area("Ask a tax/compliance question:", height=100, placeholder="e.g., What’s the depreciation for solar panels in Texas?")
    submit = st.form_submit_button("Get Answer")

def summarize_outputs(q: str, outputs: list[str]) -> str:
    content = (
        "You are a research assistant. Use the data below to answer the user's question with inline citations.\n\n"
        f"Question: {q}\n\n"
        "Tool Outputs:\n" +
        "\n".join(f"- {o}" for o in outputs)
    )
    return llm([SystemMessage(content="Summarize into a GPT-style answer."), HumanMessage(content=content)]).content

if submit and question.strip():
    with st.spinner("Simulating tool calls..."):
        out1 = vector_search.run(question)
        out2 = fetch_tax_document.run("168")
        out3 = get_case_law_summary.run("SolarCo v. Texas")
        final_answer = summarize_outputs(question, [out1, out2, out3])
        st.markdown("### ✅ GPT-Formatted Answer")
        st.markdown(final_answer)
        st.markdown("---")
        st.markdown("**Sources:** All responses are simulated for demonstration.")
