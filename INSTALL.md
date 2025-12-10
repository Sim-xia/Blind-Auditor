# 📦 Blind Auditor - 安装指南

## 系统要求

- **Python**: 3.10 或更高版本
- **操作系统**: macOS, Linux, Windows
- **包管理器**: [uv](https://docs.astral.sh/uv/) (推荐) 或 pip

## 快速安装 (使用 uv)

### 1. 安装 uv

如果尚未安装 uv，请先安装：

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**使用 Homebrew (macOS/Linux):**
```bash
brew install uv
```

### 2. 克隆或下载项目

```bash
git clone https://github.com/your-repo/blind-auditor.git
cd blind-auditor
```

### 3. 安装依赖

```bash
uv sync
```

这会自动创建虚拟环境并安装所有依赖。

### 4. 验证安装

```bash
uv run blind-auditor
```

如果看到 MCP 服务器启动的调试信息，说明安装成功！

## Docker 安装（可选）

如果您更喜欢使用 Docker：

```bash
# 构建镜像
docker build -t blind-auditor .

# 运行容器
docker run -it blind-auditor
```

## 故障排查

### 问题：找不到 uv 命令

**解决方案**: 
- 确保 uv 已正确安装
- 重新打开终端或运行 `source ~/.bashrc` / `source ~/.zshrc`
- 检查 `~/.local/bin` 是否在 PATH 中

### 问题：Python 版本不兼容

**解决方案**:
```bash
# 使用 uv 安装指定版本的 Python
uv python install 3.12

# 然后重新同步
uv sync
```

### 问题：依赖安装失败

**解决方案**:
```bash
# 清除缓存并重新安装
uv cache clean
uv sync --refresh
```

## 下一步

安装完成后，请查看 [README.md](README.md) 或 [README_CN.md](README_CN.md) 了解如何配置和使用 Blind Auditor。

## 依赖说明

本项目仅依赖一个核心包：
- `mcp[cli]>=1.22.0` - Model Context Protocol 服务器框架

所有其他依赖都是 MCP 的传递依赖，会自动安装。
