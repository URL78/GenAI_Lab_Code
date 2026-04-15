console.log("Stable caption extractor running...");

let transcript = "";

const observer = new MutationObserver(() => {

  const captions = document.querySelectorAll("div.ygicle.VbkSUe");

  if (captions.length === 0) return;

  // Google Meet shows full sentence progressively,
  // so we just take the LAST caption block.
  const latestCaption = captions[captions.length - 1].innerText.trim();

  if (!latestCaption) return;

  // Instead of appending, we replace transcript
  transcript = latestCaption;

  console.log("Current Caption:", transcript);

  chrome.runtime.sendMessage({
    type: "TRANSCRIPT_UPDATE",
    data: transcript
  });

});

observer.observe(document.body, {
  childList: true,
  subtree: true,
  characterData: true
});