from flask import Flask, request, jsonify
import whisper
import requests
import os
import difflib

app = Flask(__name__)

# Load Whisper
whisper_model = whisper.load_model("base")

# Ollama Config
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

previous_requirements = ""
iteration_count = 0

# -----------------------------
# Helper: Call LLM
# -----------------------------
def call_llm(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    return response.json()["response"]

# -----------------------------
# Helper: Stability Check
# -----------------------------
def calculate_stability(old, new):
    if not old:
        return 0
    similarity = difflib.SequenceMatcher(None, old, new).ratio()
    return round(similarity * 100, 2)

# -----------------------------
# Initial Processing
# -----------------------------
@app.route("/process", methods=["POST"])
def process_audio():
    global previous_requirements, iteration_count

    audio_file = request.files["audio"]
    audio_path = "temp.wav"
    audio_file.save(audio_path)

    result = whisper_model.transcribe(audio_path)
    transcript = result["text"]

    os.remove(audio_path)

    iteration_count = 1

    prompt = f"""
You are a senior software requirements engineer.

From the transcript below:

1. Generate FUNCTIONAL REQUIREMENTS separately.
2. Generate NON-FUNCTIONAL REQUIREMENTS separately.
3. Identify ambiguities.
4. Ask clarification questions to remove ambiguity.

Transcript:
{transcript}

Return format:

FUNCTIONAL REQUIREMENTS:
- ...

NON-FUNCTIONAL REQUIREMENTS:
- ...

CLARIFICATION QUESTIONS:
1. ...
2. ...
"""

    output = call_llm(prompt)
    previous_requirements = output

    return jsonify({
        "transcript": transcript,
        "requirements": output,
        "stability": 0,
        "iteration": iteration_count
    })

# -----------------------------
# Refinement Loop
# -----------------------------
@app.route("/refine", methods=["POST"])
def refine():
    global previous_requirements, iteration_count

    answers = request.json["answers"]

    iteration_count += 1

    prompt = f"""
You are refining software requirements.

Previous Requirements:
{previous_requirements}

User Clarifications:
{answers}

1. Regenerate refined FUNCTIONAL REQUIREMENTS.
2. Regenerate refined NON-FUNCTIONAL REQUIREMENTS.
3. Ask further clarification questions ONLY if needed.
4. If requirements are stable, say: "NO FURTHER CLARIFICATIONS NEEDED"

Return same structured format.
"""

    new_output = call_llm(prompt)

    stability_score = calculate_stability(previous_requirements, new_output)

    previous_requirements = new_output

    return jsonify({
        "requirements": new_output,
        "stability": stability_score,
        "iteration": iteration_count
    })

if __name__ == "__main__":
    app.run(debug=True)
