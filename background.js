console.log("Extension started");

let activeTab = null;
let startTime = Date.now();

function getDomain(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return "unknown";
  }
}

function recordTime() {
  if (!activeTab) return;

  const duration = Date.now() - startTime;

  console.log("Recording:", activeTab, duration);


  fetch("http://127.0.0.1:8000/track", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      domain: activeTab,
      duration: duration
    })
  });

  startTime = Date.now();
}

chrome.tabs.onActivated.addListener(async (activeInfo) => {
  const tab = await chrome.tabs.get(activeInfo.tabId);
  recordTime();
  activeTab = getDomain(tab.url);
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (tab.active && changeInfo.status === "complete") {
    recordTime();
    activeTab = getDomain(tab.url);
  }
});
