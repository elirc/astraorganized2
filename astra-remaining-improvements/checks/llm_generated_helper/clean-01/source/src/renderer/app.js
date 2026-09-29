// Renderer logic. Talks to the main process only through the `window.api`
// bridge exposed by src/preload.js (getSettings, saveSettings, ask,
// onTranscript, onAnswerChunk). Audio helpers live in audio.js as `AudioUtil`.

// ---------- Elements ----------
const $ = (id) => document.getElementById(id);
const recordBtn = $("recordBtn");
const cancelBtn = $("cancelBtn");
const recordLabel = $("recordLabel");
const statusText = $("statusText");
const statusDot = $("statusDot");
const timerEl = $("timer");
const transcriptBox = $("transcriptBox");
const answerBox = $("answerBox");
const errorBox = $("errorBox");
const errorMsg = $("errorMsg");
const errorDismiss = $("errorDismiss");
const settingsBtn = $("settingsBtn");
const saveBtn = $("saveBtn");
const backBtn = $("backBtn");
const savedNote = $("savedNote");
const mainView = $("mainView");
const settingsView = $("settingsView");

const MAX_SECONDS = 120; // safety cap per clip
const TARGET_RATE = 16000; // SenseVoice-friendly sample rate
const READY_MSG =
  "Ready — press Record (or R) while the other person is speaking";

// ---------- State machine ----------
// idle -> starting -> recording -> transcribing -> generating -> idle
// Any failure returns to idle and surfaces the error in the error banner.
let state = "idle";

const STATE_UI = {
  idle: { dot: "dot", label: "Record", canRecord: true, canSettings: true },
  starting: {
    dot: "dot busy",
    label: "Starting…",
    canRecord: false,
    canSettings: false,
  },
  recording: {
    dot: "dot recording",
    label: "Stop & Answer",
    canRecord: true,
    canSettings: false,
  },
  transcribing: {
    dot: "dot busy",
    label: "Transcribing…",
    canRecord: false,
    canSettings: false,
  },
  generating: {
    dot: "dot busy",
    label: "Answering…",
    canRecord: false,
    canSettings: false,
  },
};

function setState(next, message) {
  state = next;
  const ui = STATE_UI[next];
  statusDot.className = ui.dot;
  recordLabel.textContent = ui.label;
  recordBtn.disabled = !ui.canRecord;
  recordBtn.classList.toggle("recording", next === "recording");
  recordBtn.setAttribute("aria-pressed", String(next === "recording"));
  settingsBtn.disabled = !ui.canSettings;
  cancelBtn.hidden = !["recording", "transcribing", "generating"].includes(
    next,
  );
  cancelBtn.disabled = false;
  if (typeof message === "string") statusText.textContent = message;
}

// ---------- Errors ----------
function showError(err) {
  const msg = String(err && err.message ? err.message : err).replace(
    /^Error invoking remote method 'ask':\s*(Error:)?\s*/,
    "",
  );
  errorMsg.textContent = msg;
  errorBox.hidden = false;
}

function clearError() {
  errorBox.hidden = true;
  errorMsg.textContent = "";
}

errorDismiss.addEventListener("click", () => {
  clearError();
  recordBtn.focus();
});

function friendlyCaptureError(err) {
  if (err && (err.name === "NotAllowedError" || err.name === "SecurityError")) {
    return new Error(
      "Audio capture was denied. Allow screen/audio recording for this app in Windows privacy settings, then try again.",
    );
  }
  if (err && err.name === "NotFoundError") {
    return new Error(
      "No capturable audio source was found. Make sure the call is playing audio on this PC.",
    );
  }
  return err;
}

function setPlaceholder(box, text) {
  box.textContent = "";
  const span = document.createElement("span");
  span.className = "placeholder";
  span.textContent = text;
  box.appendChild(span);
}

// ---------- Recording ----------
let stream = null;
let audioCtx = null;
let processor = null;
let chunks = [];
let sourceRate = 48000;
let recordStart = 0;
let timerInterval = null;

const CAP_LABEL = `${String(Math.floor(MAX_SECONDS / 60)).padStart(2, "0")}:${String(MAX_SECONDS % 60).padStart(2, "0")}`;

function fmtSeconds(s) {
  return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
}

async function startRecording() {
  if (state !== "idle") return;
  clearError();
  setState("starting", "Requesting system audio…");

  try {
    // getDisplayMedia is routed to system-audio loopback by the main process.
    stream = await navigator.mediaDevices.getDisplayMedia({
      video: true,
      audio: true,
    });

    const audioTracks = stream.getAudioTracks();
    if (audioTracks.length === 0) {
      throw new Error(
        "Could not capture system audio. Make sure audio is playing on this PC.",
      );
    }
    // The video track is required by the capture API but unused.
    stream.getVideoTracks().forEach((t) => t.stop());

    // If the OS/user ends the capture from outside the app, wrap up cleanly
    // instead of recording silence forever.
    audioTracks[0].addEventListener("ended", () => {
      if (state === "recording") stopRecording();
    });

    audioCtx = new AudioContext();
    sourceRate = audioCtx.sampleRate;
    const source = audioCtx.createMediaStreamSource(
      new MediaStream(audioTracks),
    );
    processor = audioCtx.createScriptProcessor(4096, 1, 1);
    chunks = [];
    processor.onaudioprocess = (e) => {
      chunks.push(new Float32Array(e.inputBuffer.getChannelData(0)));
    };
    source.connect(processor);
    processor.connect(audioCtx.destination); // required for onaudioprocess to fire
  } catch (err) {
    stopStream();
    setState("idle", READY_MSG);
    showError(friendlyCaptureError(err));
    return;
  }

  recordStart = Date.now();
  setState("recording", "Recording call audio…");
  timerEl.textContent = `00:00 / ${CAP_LABEL}`;
  timerInterval = setInterval(() => {
    const s = Math.floor((Date.now() - recordStart) / 1000);
    timerEl.textContent = `${fmtSeconds(Math.min(s, MAX_SECONDS))} / ${CAP_LABEL}`;
    if (s >= MAX_SECONDS) stopRecording(true);
  }, 250);
}

function stopStream() {
  if (processor) {
    try {
      processor.disconnect();
    } catch {}
    processor.onaudioprocess = null;
    processor = null;
  }
  if (audioCtx) {
    audioCtx.close().catch(() => {});
    audioCtx = null;
  }
  if (stream) {
    stream.getTracks().forEach((t) => t.stop());
    stream = null;
  }
  clearInterval(timerInterval);
  timerInterval = null;
  timerEl.textContent = "";
}

async function stopRecording(hitCap) {
  if (state !== "recording") return;
  setState(
    "transcribing",
    hitCap ? `Reached the ${CAP_LABEL} cap — transcribing…` : "Transcribing…",
  );
  stopStream();

  try {
    const samples = AudioUtil.mergeAndDownsample(
      chunks,
      sourceRate,
      TARGET_RATE,
    );
    chunks = [];
    if (samples.length < TARGET_RATE / 4) {
      throw new Error(
        "Recording was too short — hold Record while the question is being asked.",
      );
    }
    const wav = AudioUtil.encodeWav(samples, TARGET_RATE);

    setPlaceholder(transcriptBox, "Transcribing…");
    setPlaceholder(answerBox, "Waiting for transcript…");

    await window.api.ask(wav.buffer);
    flushAnswer(); // make sure the tail of the stream is rendered
    setState("idle", "Done — press Record (or R) for the next question");
  } catch (err) {
    chunks = [];
    showError(err);
    setState("idle", READY_MSG);
  }
}

function toggleRecord() {
  if (state === "idle") startRecording();
  else if (state === "recording") stopRecording();
  // starting / transcribing / generating: ignore — nothing valid to trigger.
}

recordBtn.addEventListener("click", toggleRecord);

// Keyboard shortcut: R toggles record/stop (ignored while typing in settings).
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !errorBox.hidden) {
    clearError();
    return;
  }
  if (e.key !== "r" && e.key !== "R") return;
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const t = e.target;
  if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA")) return;
  if (!settingsView.hidden) return;
  e.preventDefault();
  toggleRecord();
});

// ---------- Streaming answer display ----------
// Chunks are buffered and flushed once per animation frame so fast streams
// don't thrash layout. Auto-scroll only sticks while the user is at the
// bottom; scrolling up to re-read pauses it until they scroll back down.
let pendingAnswer = "";
let flushScheduled = false;
let stickToBottom = true;

answerBox.addEventListener("scroll", () => {
  stickToBottom =
    answerBox.scrollHeight - answerBox.scrollTop - answerBox.clientHeight < 24;
});

function flushAnswer() {
  flushScheduled = false;
  if (!pendingAnswer) return;
  if (answerBox.querySelector(".placeholder")) answerBox.textContent = "";
  answerBox.appendChild(document.createTextNode(pendingAnswer));
  pendingAnswer = "";
  if (stickToBottom) answerBox.scrollTop = answerBox.scrollHeight;
}

// ---------- Settings: secrets are write-only, revisions are explicit ----------
const fields = ["resume", "jobDescription"];
const secretFields = ["siliconflowKey", "deepseekKey"];
const reloadSettingsBtn = $("reloadSettingsBtn");
let savedNoteTimer = null;
let settingsRevision = null;
let settingsBaseline = null;
let settingsBusy = false;
let settingsNeedsReload = false;

function settingsDraft() {
  return {
    ...Object.fromEntries(fields.map((key) => [key, $(key).value])),
    alwaysOnTop: $("alwaysOnTop").checked,
    ...Object.fromEntries(
      secretFields.flatMap((key) => [
        [key, $(key).value],
        ["clear" + key, $("clear" + key).checked],
      ]),
    ),
  };
}
function settingsDirty() {
  return (
    settingsBaseline !== null &&
    JSON.stringify(settingsDraft()) !== JSON.stringify(settingsBaseline)
  );
}
function syncSettings() {
  for (const element of settingsView.querySelectorAll("input,textarea,button"))
    element.disabled = settingsBusy;
  saveBtn.disabled = settingsBusy || settingsNeedsReload || !settingsRevision;
  settingsBtn.disabled = settingsBusy || state !== "idle";
}
function acceptSettings(value) {
  settingsRevision = value.revision;
  settingsNeedsReload = false;
  for (const key of fields) $(key).value = value[key] ?? "";
  $("alwaysOnTop").checked = value.alwaysOnTop;
  for (const key of secretFields) {
    $(key).value = "";
    $("clear" + key).checked = false;
    $(key).placeholder = value.credentials[key]
      ? "Saved; leave blank to keep it"
      : "Enter a new credential";
    $(key + "Status").textContent = value.credentials[key]
      ? "A credential is saved. Its value is never returned to this screen."
      : "No credential is saved.";
  }
  settingsBaseline = settingsDraft();
}
async function openSettings() {
  if (settingsBusy || state !== "idle") return;
  if (
    !settingsView.hidden &&
    settingsDirty() &&
    !confirm("Discard the unsaved settings draft and reload accepted values?")
  )
    return;
  settingsBusy = true;
  syncSettings();
  try {
    acceptSettings(await window.api.getSettings());
    mainView.hidden = true;
    settingsView.hidden = false;
    savedNote.hidden = true;
    clearError();
  } catch (error) {
    showError(error);
  } finally {
    settingsBusy = false;
    syncSettings();
  }
  if (!settingsView.hidden) $("resume").focus();
}
settingsBtn.addEventListener("click", openSettings);
reloadSettingsBtn.addEventListener("click", openSettings);
backBtn.addEventListener("click", () => {
  if (
    settingsBusy ||
    (settingsDirty() && !confirm("Discard this unsaved settings draft?"))
  )
    return;
  for (const key of secretFields) {
    $(key).value = "";
    $("clear" + key).checked = false;
  }
  settingsBaseline = null;
  settingsView.hidden = true;
  mainView.hidden = false;
  savedNote.hidden = true;
  clearTimeout(savedNoteTimer);
  settingsBtn.focus();
});
saveBtn.addEventListener("click", async () => {
  if (settingsBusy || settingsNeedsReload || !settingsBaseline) return;
  const draft = settingsDraft();
  const changes = Object.fromEntries(
    [...fields, "alwaysOnTop"]
      .filter((key) => draft[key] !== settingsBaseline[key])
      .map((key) => [key, draft[key]]),
  );
  for (const key of secretFields) {
    if (draft["clear" + key]) changes[key] = "";
    else if (draft[key].trim()) changes[key] = draft[key].trim();
  }
  if (!Object.keys(changes).length) {
    savedNote.textContent = "No settings changed.";
    savedNote.hidden = false;
    return;
  }
  settingsBusy = true;
  syncSettings();
  clearError();
  try {
    const accepted = await window.api.saveSettings({
      revision: settingsRevision,
      changes,
    });
    acceptSettings(accepted);
    savedNote.textContent = "Settings saved.";
    savedNote.hidden = false;
    clearTimeout(savedNoteTimer);
    savedNoteTimer = setTimeout(() => {
      savedNote.hidden = true;
    }, 1500);
  } catch (error) {
    settingsNeedsReload = true;
    showError(
      new Error(
        `${error.message} Your draft remains here. Copy any changes you need, then reload accepted settings before another save.`,
      ),
    );
  } finally {
    settingsBusy = false;
    syncSettings();
  }
});

cancelBtn.addEventListener("click", async () => {
  if (state === "recording") {
    stopStream();
    chunks = [];
    setState("idle", "Recording discarded. Nothing was submitted.");
    return;
  }
  if (!["transcribing", "generating"].includes(state)) return;
  cancelBtn.disabled = true;
  statusText.textContent = "Cancelling the current request…";
  try {
    await window.api.cancelAsk();
  } catch (error) {
    showError(error);
    cancelBtn.disabled = false;
  }
});

// ---------- Bridge wiring & init ----------
if (window.api) {
  const unsubscribeTranscript = window.api.onTranscript((text) => {
    transcriptBox.textContent = text;
    pendingAnswer = "";
    stickToBottom = true;
    setPlaceholder(answerBox, "Generating…");
    if (state === "transcribing") setState("generating", "Generating answer…");
  });

  const unsubscribeAnswer = window.api.onAnswerChunk((chunk) => {
    pendingAnswer += chunk;
    if (!flushScheduled) {
      flushScheduled = true;
      requestAnimationFrame(flushAnswer);
    }
  });

  window.addEventListener("beforeunload", () => {
    stopStream();
    unsubscribeTranscript();
    unsubscribeAnswer();
    window.api.cancelAsk().catch(() => {});
  });

  // First run: nudge toward settings if keys are missing.
  (async () => {
    try {
      const s = await window.api.getSettings();
      if (!s.credentials.siliconflowKey || !s.credentials.deepseekKey) {
        statusText.textContent =
          "First run: open Settings (gear icon) and add your API keys";
      }
    } catch (error) {
      showError(error);
      statusText.textContent =
        "Settings could not be loaded. Preserve the settings file and follow the recovery guide.";
    }
  })();
} else {
  recordBtn.disabled = true;
  settingsBtn.disabled = true;
  showError(
    "The app bridge failed to load (preload script missing). Restart the app; reinstall if it persists.",
  );
}
