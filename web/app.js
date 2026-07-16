(() => {
  const $ = (id) => document.getElementById(id);

  const userIdEl = $("userId");
  const sessionIdEl = $("sessionId");
  const messageEl = $("message");
  const transcript = $("transcript");
  const emptyHint = $("emptyHint");
  const statusEl = $("status");
  const sendBtn = $("sendBtn");
  const form = $("chatForm");
  const clearBtn = $("clearSession");

  const LS_USER = "pgrag_user_id";
  const LS_SESSION = "pgrag_session_id";

  function uuid() {
    if (crypto.randomUUID) return crypto.randomUUID();
    return "sess-" + Math.random().toString(16).slice(2) + Date.now().toString(16);
  }

  function setStatus(text, isError = false) {
    statusEl.textContent = text;
    statusEl.classList.toggle("error", isError);
  }

  function ensureSession() {
    let sid = sessionIdEl.value.trim();
    if (!sid) {
      sid = uuid();
      sessionIdEl.value = sid;
      localStorage.setItem(LS_SESSION, sid);
    }
    return sid;
  }

  function formatCitations(citations) {
    if (!citations || !citations.length) return "Sources: (none)";
    const lines = citations.map((c) => {
      const id = c.ticker || c.name || "";
      return `- ${c.type}${id ? ":" + id : ""}`;
    });
    return "Sources:\n" + lines.join("\n");
  }

  function formatMood(mood) {
    if (!mood) return "Mood: —";
    if (mood.insufficient_signal || !mood.label) {
      return "Mood: not enough signal";
    }
    const conf = typeof mood.confidence === "number" ? mood.confidence.toFixed(2) : mood.confidence;
    return `Mood: ${mood.label} (${conf})`;
  }

  function appendUser(text) {
    if (emptyHint) emptyHint.remove();
    const wrap = document.createElement("div");
    wrap.className = "msg user";
    wrap.innerHTML = `<div class="who">You</div><div class="bubble"></div>`;
    wrap.querySelector(".bubble").textContent = text;
    transcript.appendChild(wrap);
    transcript.scrollTop = transcript.scrollHeight;
  }

  function appendBot(data) {
    if (emptyHint) emptyHint.remove();
    const wrap = document.createElement("div");
    wrap.className = "msg bot";
    const meta = document.createElement("div");
    meta.className = "meta" + (data.refused ? " refused" : "");
    meta.textContent = formatMood(data.mood) + "\n" + formatCitations(data.citations);
    if (data.refused) {
      meta.textContent += "\n(refused — no grounded portfolio data)";
    }
    wrap.innerHTML = `<div class="who">Bot</div><div class="bubble"></div>`;
    wrap.querySelector(".bubble").textContent = data.answer || "";
    wrap.appendChild(meta);
    transcript.appendChild(wrap);
    transcript.scrollTop = transcript.scrollHeight;
  }

  function clearTranscript() {
    transcript.innerHTML = "";
    const p = document.createElement("p");
    p.className = "empty";
    p.id = "emptyHint";
    p.textContent = "No messages yet. Ask about a holding, e.g. ADANIPOWER.";
    transcript.appendChild(p);
  }

  // restore identity
  userIdEl.value = localStorage.getItem(LS_USER) || "demo";
  sessionIdEl.value = localStorage.getItem(LS_SESSION) || uuid();

  userIdEl.addEventListener("change", () => {
    localStorage.setItem(LS_USER, userIdEl.value.trim());
  });
  sessionIdEl.addEventListener("change", () => {
    localStorage.setItem(LS_SESSION, sessionIdEl.value.trim());
  });

  clearBtn.addEventListener("click", () => {
    const sid = uuid();
    sessionIdEl.value = sid;
    localStorage.setItem(LS_SESSION, sid);
    clearTranscript();
    setStatus("idle — new session");
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userId = userIdEl.value.trim();
    const message = messageEl.value.trim();
    if (!userId) {
      setStatus("user_id is required", true);
      userIdEl.focus();
      return;
    }
    if (!message) {
      setStatus("message is required", true);
      messageEl.focus();
      return;
    }

    const sessionId = ensureSession();
    localStorage.setItem(LS_USER, userId);

    appendUser(message);
    messageEl.value = "";
    sendBtn.disabled = true;
    setStatus("thinking…");

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          session_id: sessionId,
          message,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        const detail = data.detail ? JSON.stringify(data.detail) : res.statusText;
        setStatus(`error ${res.status}: ${detail}`, true);
        return;
      }
      if (data.session_id && data.session_id !== sessionIdEl.value) {
        sessionIdEl.value = data.session_id;
        localStorage.setItem(LS_SESSION, data.session_id);
      }
      appendBot(data);
      setStatus(data.refused ? "idle (refused)" : "idle");
    } catch (err) {
      setStatus(`error: ${err.message || err}`, true);
    } finally {
      sendBtn.disabled = false;
      messageEl.focus();
    }
  });

  messageEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.requestSubmit();
    }
  });
})();
