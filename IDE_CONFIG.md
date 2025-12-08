# IDE 配置示例

## Antigravity / Cursor

### 方法 1: 项目级配置（推荐）

在项目根目录创建 `.cursorrules` 文件：

```markdown
## 代码生成规则

**CRITICAL INSTRUCTION**:
每当你为用户生成代码时，你必须遵循以下流程：

1. 内部生成代码（不要直接输出）
2. 调用 MCP 工具 `submit_draft`，传入代码和语言
3. **严格遵守**工具返回的指令

示例：
- 如果返回审计指令，立即切换为审计员角色进行代码审查
- 如果返回修复指令，按要求修正代码并重新提交
- 如果返回放行指令，将最终代码展示给用户
```

### 方法 2: MCP 服务器配置

在 MCP 配置文件中添加（路径依 IDE 而定）：

**Cursor**: `~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`

**Antigravity**: 设置 → MCP Servers

```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "python",
      "args": ["-m", "src.main"],
      "cwd": "/path/to/your/blind-auditor"
    }
  }
}
```

## Claude Desktop

编辑配置文件：`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "blind-auditor": {
      "command": "python",
      "args": ["-m", "src.main"],
      "cwd": "/path/to/your/blind-auditor"
    }
  }
}
```

## Windsurf

TBD（待 Windsurf 发布 MCP 支持）

---

## 验证配置

1. 重启 IDE
2. 在终端运行 MCP Inspector：
   ```bash
   npx @anthropic-ai/mcp-inspector python -m src.main
   ```
3. 确认工具列表中有：
   - `submit_draft`
   - `submit_audit_result`
   - `reset_session`

## 测试流程

向 Agent 发送测试请求：

```
请帮我写一个简单的 Python 函数，用于连接数据库。
```

正确流程：
1. Agent 生成代码 → 调用 `submit_draft`
2. MCP 返回审计指令 → Agent 切换角色审查代码
3. Agent 发现问题（如硬编码密码）→ 调用 `submit_audit_result(passed=False)`
4. MCP 返回修复指令 → Agent 修正代码
5. 循环直至通过或达到重试上限
