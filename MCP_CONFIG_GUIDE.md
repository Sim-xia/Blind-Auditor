# 🔧 MCP 配置指南

本文档帮助您在不同的 IDE 和客户端中正确配置 Blind Auditor MCP 服务器。

## 📍 重要：确定项目路径

在配置前，您需要知道项目的**绝对路径**。

### 获取项目绝对路径

**macOS / Linux:**
```bash
cd blind-auditor
pwd
```

**Windows (PowerShell):**
```powershell
cd blind-auditor
Get-Location
```

**Windows (CMD):**
```cmd
cd blind-auditor
cd
```

示例输出：
- macOS: `/Users/yourname/projects/blind-auditor`
- Linux: `/home/yourname/projects/blind-auditor`
- Windows: `C:\Users\yourname\projects\blind-auditor`

---

## 🎯 配置示例

### 1. Antigravity

**位置**: 设置 → MCP Servers → Add Server

**配置**:
```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/yourname/projects/blind-auditor", "blind-auditor"]
    }
  }
}
```

**注意**: 将 `--directory` 后的路径替换为您在上一步获取的实际路径。

---

### 2. Cursor

**位置**: `~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`

**配置**:
```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/yourname/projects/blind-auditor", "blind-auditor"]
    }
  }
}
```

---

### 3. Claude Desktop

**位置**: 
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**配置**:
```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/yourname/projects/blind-auditor", "blind-auditor"]
    }
  }
}
```

---

### 4. Windsurf

**位置**: `~/.codeium/windsurf/mcp_config.json`

**配置**:
```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/yourname/projects/blind-auditor", "blind-auditor"]
    }
  }
}
```

---

## 🔍 配置验证

### 方法 1: 使用 MCP Inspector

```bash
# 进入项目目录
cd /path/to/your/blind-auditor

# 运行 Inspector
npx @anthropic-ai/mcp-inspector uv run blind-auditor
```

您应该看到以下工具：
- ✅ `submit_draft`
- ✅ `submit_audit_result`
- ✅ `reset_session`
- ✅ `update_rules`

### 方法 2: 直接运行服务器

```bash
cd /path/to/your/blind-auditor
uv run blind-auditor
```

如果看到以下输出，说明配置正确：
```
DEBUG: Starting main_debug.py
DEBUG: Importing FastMCP
DEBUG: Importing state and rules
DEBUG: Creating FastMCP instance
DEBUG: Initializing session state
DEBUG: Loading rules
DEBUG: Rules loaded successfully from /path/to/rules.json
DEBUG: About to call mcp.run()
```

---

## ⚠️ 常见问题

### 问题 1: "找不到 uv 命令"

**原因**: uv 未安装或未添加到 PATH

**解决方案**:
1. 安装 uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. 重新打开终端或运行 `source ~/.bashrc` / `source ~/.zshrc`
3. 检查 `~/.local/bin` 是否在 PATH 中

### 问题 2: "找不到 rules.json"

**原因**: 项目文件不完整

**解决方案**:
```bash
# 确保 rules.json 存在
ls rules.json

# 如果不存在，创建默认配置
cat > rules.json << 'EOF'
{
  "project_name": "MyProject",
  "strict_mode": true,
  "max_retries": 3,
  "rules": []
}
EOF
```

### 问题 3: Windows 路径问题

**原因**: Windows 路径使用反斜杠 `\`

**解决方案**: 在 JSON 中使用正斜杠 `/` 或双反斜杠 `\\`

**正确示例**:
```json
{
  "cwd": "C:/Users/yourname/projects/blind-auditor"
}
```

或

```json
{
  "cwd": "C:\\Users\\yourname\\projects\\blind-auditor"
}
```

### 问题 4: Python 版本不兼容

**原因**: Python 版本低于 3.10

**解决方案**:
```bash
# 使用 uv 安装指定版本的 Python
uv python install 3.12

# 然后重新同步
uv sync
```

---

## 📝 配置模板

将以下内容保存为 `mcp_config_template.json`，然后替换路径：

```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "uv",
      "args": ["run", "--directory", "REPLACE_WITH_YOUR_ABSOLUTE_PATH", "blind-auditor"]
    }
  }
}
```

**替换步骤**:
1. 复制上述 JSON
2. 将 `REPLACE_WITH_YOUR_ABSOLUTE_PATH` 替换为您的实际路径
3. 粘贴到对应的配置文件中

---

## ✅ 配置完成后

1. **重启 IDE** - 确保配置生效
2. **测试连接** - 向 Agent 发送测试请求
3. **查看日志** - 检查是否有错误信息

**测试请求示例**:
```
请帮我写一个 Python 函数，用于读取文件内容。
```

如果配置正确，Agent 应该：
1. 生成代码
2. 调用 `submit_draft` 提交审计
3. 进行自我审查
4. 返回审计结果

---

需要更多帮助？请查看 [README.md](README.md) 或 [INSTALL.md](INSTALL.md)。
