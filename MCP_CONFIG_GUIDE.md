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
      "command": "python",
      "args": ["-m", "src.main"],
      "cwd": "/Users/yourname/projects/blind-auditor"
    }
  }
}
```

**注意**: 将 `cwd` 的值替换为您在上一步获取的实际路径。

---

### 2. Cursor

**位置**: `~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`

**配置**:
```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "python",
      "args": ["-m", "src.main"],
      "cwd": "/Users/yourname/projects/blind-auditor"
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
      "command": "python",
      "args": ["-m", "src.main"],
      "cwd": "/Users/yourname/projects/blind-auditor"
    }
  }
}
```

---

### 4. Windsurf

**位置**: TBD（待 Windsurf 发布 MCP 支持）

---

## 🔍 配置验证

### 方法 1: 使用 MCP Inspector

```bash
# 进入项目目录
cd /path/to/your/blind-auditor

# 激活虚拟环境（如果使用）
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 运行 Inspector
npx @anthropic-ai/mcp-inspector python -m src.main
```

您应该看到以下工具：
- ✅ `submit_draft`
- ✅ `submit_audit_result`
- ✅ `reset_session`
- ✅ `update_rules`

### 方法 2: 直接运行服务器

```bash
cd /path/to/your/blind-auditor
python -m src.main
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

### 问题 1: "找不到模块 src.main"

**原因**: `cwd` 路径配置错误

**解决方案**:
1. 检查 `cwd` 是否指向项目根目录（包含 `src/` 文件夹的目录）
2. 确保路径是绝对路径，不是相对路径
3. 确保路径中没有拼写错误

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

### 问题 4: Python 命令未找到

**原因**: Python 未安装或未添加到 PATH

**解决方案**:
- 尝试使用 `python3` 替代 `python`
- 或使用 Python 的完整路径：
  ```json
  {
    "command": "/usr/bin/python3",
    "args": ["-m", "src.main"]
  }
  ```

---

## 📝 配置模板

将以下内容保存为 `mcp_config_template.json`，然后替换路径：

```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "python",
      "args": ["-m", "src.main"],
      "cwd": "REPLACE_WITH_YOUR_ABSOLUTE_PATH"
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
