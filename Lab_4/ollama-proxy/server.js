const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

app.post("/generate", async (req, res) => {
  try {
    const { prompt } = req.body;

    console.log("Prompt received:", prompt);

    const response = await fetch("http://127.0.0.1:11434/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "llama3.2:latest",
        prompt: prompt,
        stream: false
      })
    });

    const data = await response.json();

    console.log("Ollama response:", data.response);

    res.json({ result: data.response });

  } catch (error) {
    console.error("Server error:", error);
    res.status(500).json({ error: "Failed to generate from Ollama" });
  }
});

app.listen(5000, () => {
  console.log("✅ Proxy server running at http://localhost:5000");
});