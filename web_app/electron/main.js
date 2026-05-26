const { app, BrowserWindow, dialog } = require("electron");
const { spawn } = require("child_process");
const http = require("http");
const net = require("net");
const path = require("path");

let backendProcess = null;
let mainWindow = null;

function getFreePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.on("error", reject);
    server.listen(0, "127.0.0.1", () => {
      const address = server.address();
      const port = address.port;
      server.close(() => resolve(port));
    });
  });
}

function backendPath() {
  if (app.isPackaged) {
    return path.join(process.resourcesPath, "backend", "duck-backend.exe");
  }
  return path.join(__dirname, "..", "dist_backend", "duck-backend", "duck-backend.exe");
}

function waitForBackend(port, attempts = 80) {
  const url = `http://127.0.0.1:${port}/api/health`;
  return new Promise((resolve, reject) => {
    let tries = 0;
    const tick = () => {
      tries += 1;
      const req = http.get(url, (res) => {
        res.resume();
        if (res.statusCode === 200) {
          resolve();
        } else if (tries >= attempts) {
          reject(new Error(`Backend health check failed: ${res.statusCode}`));
        } else {
          setTimeout(tick, 250);
        }
      });
      req.on("error", () => {
        if (tries >= attempts) {
          reject(new Error("Backend did not start in time."));
        } else {
          setTimeout(tick, 250);
        }
      });
      req.setTimeout(1000, () => {
        req.destroy();
      });
    };
    tick();
  });
}

async function startBackend() {
  const exe = backendPath();
  const port = await getFreePort();
  backendProcess = spawn(exe, ["--host", "127.0.0.1", "--port", String(port)], {
    cwd: path.dirname(exe),
    windowsHide: true,
    stdio: "ignore",
  });

  backendProcess.on("exit", () => {
    backendProcess = null;
  });

  await waitForBackend(port);
  return port;
}

function stopBackend() {
  if (backendProcess) {
    backendProcess.kill();
    backendProcess = null;
  }
}

async function createWindow() {
  const port = await startBackend();
  mainWindow = new BrowserWindow({
    width: 980,
    height: 720,
    minWidth: 820,
    minHeight: 580,
    title: "Duck Privacy Tool",
    backgroundColor: "#f6f7f8",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  await mainWindow.loadURL(`http://127.0.0.1:${port}`);
}

app.whenReady().then(() => {
  createWindow().catch((error) => {
    dialog.showErrorBox("Duck Privacy Tool 启动失败", error.message);
    app.quit();
  });
});

app.on("window-all-closed", () => {
  stopBackend();
  app.quit();
});

app.on("before-quit", () => {
  stopBackend();
});
