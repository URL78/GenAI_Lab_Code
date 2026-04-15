let storedTranscript = "";

// Helper function to call proxy
async function callOllama(prompt) {
  try {
    const response = await fetch("http://localhost:5000/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });

    const data = await response.json();
    return data.result;

  } catch (error) {
    console.error("Proxy call error:", error);
    return "Error generating response from LLM.";
  }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

  // Store transcript from content.js
  if (message.type === "TRANSCRIPT_UPDATE") {
    storedTranscript = message.data;
    return;
  }

  // Send transcript to popup
  if (message.type === "GET_TRANSCRIPT") {
    sendResponse({ data: storedTranscript });
    return true;
  }

  // Generate clarification questions
  if (message.type === "GENERATE_QUESTIONS") {

    (async () => {
      const prompt = `
You are a software requirements analyst.

Based on the following transcript, generate 5 clarification questions.

Transcript:
${storedTranscript}
`;

      const result = await callOllama(prompt);
      sendResponse({ questions: result });

    })();

    return true;
  }

  // Generate Functional & Non-Functional Requirements
  if (message.type === "GENERATE_REQUIREMENTS") {

    (async () => {
      const prompt = `
You are a senior system analyst.

Using the transcript and clarification answers below, generate:

1. Functional Requirements
2. Non-Functional Requirements

Transcript:
${storedTranscript}

Clarification Answers:
${message.answers}
`;

      const result = await callOllama(prompt);
      sendResponse({ requirements: result });

    })();

    return true;
  }

});