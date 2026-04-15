import streamlit as st
import requests
import zlib
import base64
import re
import json

# -----------------------------
# CONFIG
# -----------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

st.set_page_config(page_title="UML Pipeline", layout="wide")

# -----------------------------
# LLM CALL
# -----------------------------
def call_llm(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )
    return response.json()["response"]

# -----------------------------
# CLEAN UML
# -----------------------------
def clean_uml(uml):
    return uml.strip()

# -----------------------------
# PlantUML Encoding
# -----------------------------
def encode_plantuml(uml_text):
    data = zlib.compress(uml_text.encode("utf-8"))
    compressed = data[2:-4]
    encoded = base64.b64encode(compressed).decode("ascii")

    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    result = ""

    for c in encoded:
        if c == "=":
            result += chars[0]
        else:
            idx = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".index(c)
            result += chars[idx]

    return result

def get_plantuml_url(code):
    return f"https://www.plantuml.com/plantuml/png/{encode_plantuml(code)}"

# -----------------------------
# Extract UML
# -----------------------------
def extract_uml(text):
    match = re.search(r"@startuml[\s\S]*?@enduml", text, re.IGNORECASE)
    return match.group() if match else f"@startuml\n{text}\n@enduml"

# -----------------------------
# GENERATE UML (BASE PAPER)
# -----------------------------
def generate_uml(transcript):

    prompt = f"""
Create a UML Class Diagram of the given exercise and give me the PlantUML code.

STRICT RULES:
- Use class keyword
- Define classes properly
- Do not output only arrows
- Use valid class diagram syntax

Example:
@startuml
class User {{
  name
}}
class Book {{
  title
}}
User --> Book
@enduml

{transcript}
"""

    return extract_uml(call_llm(prompt))

# -----------------------------
# SIZE METRICS (ROBUST)
# -----------------------------
def compute_size_metrics(uml):

    # classes
    class_pattern = r'^\s*class\s+["\w]+'
    classes = re.findall(class_pattern, uml, re.MULTILINE)

    # attributes
    attributes = re.findall(r'\w+\s*:\s*\w+', uml)

    # methods
    methods = re.findall(r'\w+\s*\(.*?\)', uml)

    # relationships
    relationships = re.findall(r'-->|<--|--|\*--|o--|\|--', uml)

    return {
        "classes": len(classes),
        "attributes": len(attributes),
        "methods": len(methods),
        "relationships": len(relationships)
    }

# -----------------------------
# QUALITY EVALUATION (LLM)
# -----------------------------
def evaluate_quality(transcript, uml):

    prompt = f"""
You are a UML expert.

Evaluate the UML diagram.

Return JSON:

{{
  "syntactic_quality": {{
    "summary": "",
    "issues": [],
    "error_count": 0
  }},
  "semantic_quality": {{
    "summary": "",
    "issues": [],
    "error_count": 0
  }},
  "pragmatic_quality": {{
    "summary": "",
    "issues": [],
    "error_count": 0
  }},
  "overall": {{
    "syntactic_errors": 0,
    "semantic_errors": 0,
    "pragmatic_errors": 0
  }}
}}

Requirements:
{transcript}

UML:
{uml}
"""

    res = call_llm(prompt)

    try:
        return json.loads(re.search(r"\{[\s\S]*\}", res).group())
    except:
        return {"error": res}

# -----------------------------
# UI
# -----------------------------
st.title("📊 UML Class Diagram Pipeline")

transcript = st.text_area("📝 Enter System Description")

# STEP 1
if st.button("1️⃣ Generate UML Code"):
    if transcript.strip():
        st.session_state["uml"] = generate_uml(transcript)
    else:
        st.warning("Please enter description")

# SHOW UML
if "uml" in st.session_state:

    st.subheader("🧾 UML Code")
    st.code(st.session_state["uml"])

    if st.button("2️⃣ Generate Class Diagram"):

        uml = clean_uml(st.session_state["uml"])
        st.session_state["diagram"] = get_plantuml_url(uml)

# SHOW DIAGRAM
if "diagram" in st.session_state:

    st.subheader("🖼️ Class Diagram")

    url = st.session_state["diagram"]

    try:
        st.image(url, use_container_width=True)
        st.markdown(f"[🔗 Open Diagram in Browser]({url})")
    except:
        st.error("Diagram rendering failed")
        st.code(st.session_state["uml"])

    if st.button("3️⃣ Evaluate"):

        uml = st.session_state["uml"]

        st.session_state["size"] = compute_size_metrics(uml)
        st.session_state["quality"] = evaluate_quality(transcript, uml)

# -----------------------------
# SHOW SIZE METRICS
# -----------------------------
if "size" in st.session_state:

    st.header("📏 Size Metrics (Accurate)")

    size = st.session_state["size"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Classes", size["classes"])
    col2.metric("Attributes", size["attributes"])
    col3.metric("Methods", size["methods"])
    col4.metric("Relationships", size["relationships"])

# -----------------------------
# SHOW QUALITY
# -----------------------------
if "quality" in st.session_state and "error" not in st.session_state["quality"]:

    data = st.session_state["quality"]

    st.header("📈 Quality Evaluation")

    st.subheader("🔧 Syntactic Quality")
    st.info(data["syntactic_quality"]["summary"])
    for i in data["syntactic_quality"]["issues"]:
        st.error(i)

    st.subheader("🧠 Semantic Quality")
    st.info(data["semantic_quality"]["summary"])
    for i in data["semantic_quality"]["issues"]:
        st.error(i)

    st.subheader("🎯 Pragmatic Quality")
    st.info(data["pragmatic_quality"]["summary"])
    for i in data["pragmatic_quality"]["issues"]:
        st.warning(i)

    st.subheader("📊 Overall")
    st.write(data["overall"])