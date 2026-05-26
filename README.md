# 鸭鸭图本地加密解密工具

这是一个基于鸭鸭图隐写/载荷协议的本地加密解密工具。它提供简洁 Web 页面和 Electron 桌面壳，用户可以把文件加密成鸭鸭 PNG，也可以把鸭鸭 PNG 解密回原始文件。

## 重要声明

本软件为开源软件，仅用于保护隐私的加密解密功能。用户使用本软件必须遵守所在地以及相关适用地区的法律法规。

严禁将本软件用于任何违法违规用途，严禁用于侵犯他人权益、传播违规内容、规避监管、非法交易、恶意隐藏或分发数据等行为。禁止商用使用。

任何用户因下载、部署、修改、分发或使用本软件产生的法律责任、风险、损失和后果，均由使用者自行承担，开发者不承担由违规使用导致的任何责任。

继续使用、部署或分发本项目，即视为你已经阅读、理解并同意以上声明。

## 功能

- 任意文件加密为鸭鸭 PNG
- 鸭鸭 PNG 解密还原为原始文件
- 可选密码保护
- 压缩档位：`2 / 6 / 8`
- 默认输出路径：`D:\safe`
- 支持自定义输出路径
- 页面不展示图片、视频或文件内容预览，只提供下载和本地保存路径
- 可作为源码版本地 Web 应用运行
- 可打包为 Electron 桌面应用，后端 Python 会被打包进程序，用户电脑无需安装 Python

## 技术路线

项目分为三层：

1. 核心协议层：`web_app/duck_core.py`
   - 复用原项目 `duck_payload_exporter.py` 的鸭鸭图生成能力。
   - 解码逻辑兼容原 ComfyUI 节点的 LSB 载荷提取方式。
   - 对任意文件按 `bytes + 扩展名 + 可选密码` 写入鸭鸭图。
   - 解码时兼容原项目视频 `.binpng` 载荷格式。

2. 本地 Web 后端：`web_app/app.py`
   - 使用 FastAPI 提供本地接口。
   - 默认监听 `127.0.0.1`，只服务本机。
   - 提供加密、解密、下载、健康检查和配置接口。

3. 桌面应用：`web_app/electron/main.js`
   - 使用 Electron 打开本地界面。
   - 使用 PyInstaller 将 Python 后端打包成 `duck-backend.exe`。
   - Electron 启动时自动拉起内置后端，并加载本地页面。

## 目录结构

```text
.
├── duck_payload_exporter.py      # 原鸭鸭图载荷导出逻辑
├── duck_encode_node.py           # ComfyUI 编码节点
├── duck_decode_node.py           # ComfyUI 解码节点
├── requirements.txt              # Python 依赖
└── web_app/
    ├── app.py                    # FastAPI 后端
    ├── duck_core.py              # 纯 Python 加密/解密核心
    ├── backend_entry.py          # PyInstaller 后端入口
    ├── static/                   # Web 页面
    ├── electron/main.js          # Electron 主进程
    ├── package.json              # Electron 打包配置
    ├── run_web.bat               # Windows 源码版启动脚本
    ├── run_web.ps1               # PowerShell 源码版启动脚本
    └── tests/                    # 回归测试
```

## 源码版运行

安装依赖：

```bat
python -m pip install -r requirements.txt
```

启动：

```bat
cd web_app
run_web.bat
```

启动后会自动打开：

```text
http://127.0.0.1:7860
```

如果没有自动打开，可以手动复制到浏览器访问。

## Electron 打包

进入 `web_app`：

```bat
cd web_app
npm install
```

打包 Python 后端：

```bat
powershell -ExecutionPolicy Bypass -File .\build_backend.ps1
```

打包 Electron：

```bat
npm run dist
```

产物默认在：

```text
web_app/dist_electron/
```

说明：打包产物和 `node_modules` 不进入 Git 仓库。Windows 安装包体积较大时，建议通过 GitHub Release 分发。

## 测试

```bat
python -m pytest web_app\tests
```

当前覆盖：

- 核心加密/解密往返
- API 加密/解密往返
- 临时上传目录缺失时自动重建

## 注意事项

- 不要用图片编辑软件重新保存鸭鸭图，否则可能破坏隐藏载荷。
- 加密时设置了密码，解密必须输入相同密码。
- 本工具只做本地处理，不主动上传文件到远端服务器。
- 桌面版会在本机启动一个临时本地后端进程，关闭桌面窗口后会自动结束。
