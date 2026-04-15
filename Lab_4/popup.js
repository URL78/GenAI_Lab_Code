document.addEventListener("DOMContentLoaded", () => {

  const transcriptBox = document.getElementById("transcript");
  const questionsBox = document.getElementById("questions");
  const answersContainer = document.getElementById("answersContainer");
  const finalOutput = document.getElementById("finalOutput");

  const generateQuestionsBtn = document.getElementById("generateQuestions");
  const generateFRNFRBtn = document.getElementById("generateFRNFR");

  // Load transcript
  chrome.runtime.sendMessage({ type: "GET_TRANSCRIPT" }, (response) => {
    if (response && response.data) {
      transcriptBox.value = response.data;
    }
  });

  // Generate clarification questions
  generateQuestionsBtn.addEventListener("click", () => {

    questionsBox.value = "Generating questions...";
    answersContainer.innerHTML = "";

    chrome.runtime.sendMessage(
      { type: "GENERATE_QUESTIONS" },
      (response) => {

        if (!response || !response.questions) {
          questionsBox.value = "Error generating questions.";
          return;
        }

        questionsBox.value = response.questions;
        renderAnswerFields(response.questions);
      }
    );
  });

  function renderAnswerFields(text) {

    const lines = text
      .split("\n")
      .filter(line => line.trim() !== "");

    answersContainer.innerHTML = "";

    lines.forEach((line, index) => {

      const wrapper = document.createElement("div");
      wrapper.style.marginBottom = "10px";

      const label = document.createElement("label");
      label.innerText = line;

      const textarea = document.createElement("textarea");
      textarea.rows = 2;
      textarea.style.width = "100%";
      textarea.className = "answerField";

      wrapper.appendChild(label);
      wrapper.appendChild(textarea);

      answersContainer.appendChild(wrapper);
    });
  }

  // Generate FR & NFR
  generateFRNFRBtn.addEventListener("click", () => {

    const answerFields = document.querySelectorAll(".answerField");

    let compiledAnswers = "";

    answerFields.forEach((field, index) => {
      compiledAnswers += `Answer ${index + 1}: ${field.value}\n`;
    });

    finalOutput.value = "Generating requirements...";

    chrome.runtime.sendMessage(
      {
        type: "GENERATE_REQUIREMENTS",
        answers: compiledAnswers
      },
      (response) => {

        if (!response || !response.requirements) {
          finalOutput.value = "Error generating requirements.";
          return;
        }

        finalOutput.value = response.requirements;
      }
    );
  });

});