# 📦 Blind Auditor - 安装指南

## 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: macOS, Linux, Windows
- **包管理器**: pip (Python 自带)

## 快速安装

### 1. 克隆或下载项目

```bash
git clone https://github.com/your-repo/blind-auditor.git
cd blind-auditor
```

### 2. 创建虚拟环境（推荐）

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证安装

```bash
python -m src.main --help
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

### 问题：找不到 Python 命令

**解决方案**: 
- 确保已安装 Python 3.8+
- 尝试使用 `python3` 替代 `python`

### 问题：pip 安装失败

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

### 问题：权限错误

**解决方案**:
```bash
# 使用 --user 标志
pip install --user -r requirements.txt
```

## 下一步

安装完成后，请查看 [README.md](README.md) 或 [README_CN.md](README_CN.md) 了解如何配置和使用 Blind Auditor。

## 依赖说明

本项目仅依赖一个核心包：
- `mcp[cli]>=1.22.0` - Model Context Protocol 服务器框架

所有其他依赖都是 MCP 的传递依赖，会自动安装。
