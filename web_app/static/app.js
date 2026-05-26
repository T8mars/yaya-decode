const encodeTab = document.querySelector("#encodeTab");
const decodeTab = document.querySelector("#decodeTab");
const encodeForm = document.querySelector("#encodeForm");
const decodeForm = document.querySelector("#decodeForm");
const result = document.querySelector("#result");
const serverStatus = document.querySelector("#serverStatus");
const outputInputs = document.querySelectorAll("[data-output-dir]");

function setMode(mode) {
  const isEncode = mode === "encode";
  encodeTab.classList.toggle("is-active", isEncode);
  decodeTab.classList.toggle("is-active", !isEncode);
  encodeTab.setAttribute("aria-selected", String(isEncode));
  decodeTab.setAttribute("aria-selected", String(!isEncode));
  encodeForm.classList.toggle("is-hidden", !isEncode);
  decodeForm.classList.toggle("is-hidden", isEncode);
  result.innerHTML = "<span>等待操作</span>";
}

function formatBytes(bytes) {
  if (!Number.isFinite(bytes)) return "";
  const units = ["B", "KB", "MB", "GB"];
  let size = bytes;
  let index = 0;
  while (size >= 1024 && index < units.length - 1) {
    size /= 1024;
    index += 1;
  }
  return `${size.toFixed(index === 0 ? 0 : 2)} ${units[index]}`;
}

function setBusy(form, busy) {
  form.querySelectorAll("button, input, select").forEach((el) => {
    el.disabled = busy;
  });
}

function normalizeErrorMessage(payload) {
  const detail = payload && payload.detail ? payload.detail : payload;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === "string") return item;
        const location = Array.isArray(item.loc) ? item.loc.join(".") : "";
        const message = item.msg || JSON.stringify(item);
        return location ? `${location}: ${message}` : message;
      })
      .join("；");
  }
  if (detail && typeof detail === "object") {
    return detail.msg || JSON.stringify(detail);
  }
  return "操作失败";
}

async function submitForm(form, endpoint, label) {
  const formData = new FormData(form);
  setBusy(form, true);
  result.innerHTML = `<span>${label}中...</span>`;
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      body: formData,
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(normalizeErrorMessage(payload));
    }
    result.innerHTML = `
      <div><strong>完成：</strong>${payload.filename}</div>
      <div>大小：${formatBytes(payload.size)}</div>
      <div>路径：${payload.path}</div>
      <a href="${payload.download_url}">下载到本地查看</a>
    `;
  } catch (error) {
    result.innerHTML = `<span class="error">${error.message}</span>`;
  } finally {
    setBusy(form, false);
  }
}

async function loadConfig() {
  try {
    const response = await fetch("/api/config");
    const config = await response.json();
    outputInputs.forEach((input) => {
      input.value = config.default_output_dir || "D:\\safe";
    });
    serverStatus.textContent = "已连接";
  } catch {
    serverStatus.textContent = "未连接";
  }
}

encodeTab.addEventListener("click", () => setMode("encode"));
decodeTab.addEventListener("click", () => setMode("decode"));
encodeForm.addEventListener("submit", (event) => {
  event.preventDefault();
  submitForm(encodeForm, "/api/encode", "加密");
});
decodeForm.addEventListener("submit", (event) => {
  event.preventDefault();
  submitForm(decodeForm, "/api/decode", "解密");
});

loadConfig();
