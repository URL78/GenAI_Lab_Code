import streamlit as st
import requests
import zlib
import base64
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

st.set_page_config(page_title="Activity Diagram Generator", layout="wide")

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
# Encode PlantUML
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


def plantuml_url(code):

    encoded = encode_plantuml(code)

    return f"https://www.plantuml.com/plantuml/png/{encoded}"


# -----------------------------
# Extract UML
# -----------------------------
def extract_uml(text):

    pattern = r"@startuml[\s\S]*?@enduml"

    match = re.search(pattern, text)

    if match:
        return match.group()

    # fallback wrap
    return f"@startuml\n{text}\n@enduml"


# -----------------------------
# Generate Requirements
# -----------------------------
def generate_requirements(transcript):

    prompt = f"""
You are a software requirements engineer.

Extract requirements.

Return format:

FUNCTIONAL REQUIREMENTS
- FR-01
- FR-02

NON FUNCTIONAL REQUIREMENTS
- NFR-01
- NFR-02

Transcript:
{transcript}
"""

    return call_llm(prompt)


# -----------------------------
# Generate User Stories
# -----------------------------
def generate_user_stories(requirements):

    prompt = f"""
You are an Agile analyst.

Convert the requirements into workflow-friendly user stories.

Requirements:
{requirements}

Generate 6 user stories.

Format strictly:

Story 1:
Actor:
Action:
System Response:
Validation:

Story 2:
Actor:
Action:
System Response:
Validation:

Focus on workflow steps so they can easily convert into activity diagrams.
"""

    return call_llm(prompt)


# -----------------------------
# Generate Activity Diagram
# -----------------------------
def generate_activity_diagram(stories):

    prompt = f"""
You are a software architect.

Create a PlantUML ACTIVITY DIAGRAM from the workflow.

Workflow:
{stories}

Rules:

- Must start with @startuml
- Must end with @enduml
- Use start and stop
- Include validation decisions
- Include yes/no branches
- Include alternate flows

Example syntax:

@startuml
start
:User login;

if (Credentials valid?) then (Yes)
  :Upload resume;

  if (File format valid?) then (Yes)
    :Analyze resume;
    :Generate score;
  else (No)
    :Reject file;
  endif

else (No)
  :Show login error;
endif

stop
@enduml
"""

    raw = call_llm(prompt)

    uml = extract_uml(raw)

    return uml


# -----------------------------
# UI
# -----------------------------
st.title("AI Activity Diagram Generator")

transcript = st.text_area("Enter Transcript")


if st.button("Generate Requirements"):

    req = generate_requirements(transcript)

    st.session_state["req"] = req


if "req" in st.session_state:

    st.subheader("Requirements")

    st.write(st.session_state["req"])

    if st.button("Generate User Stories"):

        stories = generate_user_stories(st.session_state["req"])

        st.session_state["stories"] = stories


if "stories" in st.session_state:

    st.subheader("User Stories")

    st.write(st.session_state["stories"])

    if st.button("Generate Activity Diagram"):

        uml = generate_activity_diagram(st.session_state["stories"])

        st.session_state["uml"] = uml


if "uml" in st.session_state:

    st.header("Activity Diagram")

    url = plantuml_url(st.session_state["uml"])

    st.image(url, use_container_width=True)