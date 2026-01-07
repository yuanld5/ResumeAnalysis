# 使用 Qwen API 进行简历解析

本示例展示如何使用 Qwen API（通过 OpenAI 兼容接口）进行简历解析。

## 环境变量配置

### 方法1: 使用 .env 文件（推荐）

在项目根目录创建或编辑 `.env` 文件：

```bash
QWEN_API_KEY=sk-9c76a51a6ea24cd6b65db4cc037dba31
```

代码会自动加载 `.env` 文件中的环境变量。

### 方法2: 直接在 shell 中设置

```bash
# macOS/Linux
export QWEN_API_KEY="sk-9c76a51a6ea24cd6b65db4cc037dba31"

# Windows PowerShell
$env:QWEN_API_KEY="sk-9c76a51a6ea24cd6b65db4cc037dba31"
```

### 方法3: 在代码中直接设置

```python
import os
os.environ["QWEN_API_KEY"] = "sk-9c76a51a6ea24cd6b65db4cc037dba31"
```

## 使用方法

### 基本用法

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行解析（会自动从环境变量读取 API key）
python example_resume_parser_qwen_api.py resume.pdf

# 指定模型
python example_resume_parser_qwen_api.py resume.pdf qwen-max
```

### 支持的 Qwen 模型

- `qwen-plus` - 通用模型（推荐，默认）
- `qwen-max` - 最强模型，准确度最高
- `qwen-turbo` - 快速模型，速度优先
- `qwen-max-longcontext` - 长文本模型，适合超长简历

### 在代码中使用

```python
from example_resume_parser_qwen_api import parse_resume_pdf_with_qwen_api

# 使用默认模型 (qwen-plus)
result = parse_resume_pdf_with_qwen_api("resume.pdf")

# 指定模型
result = parse_resume_pdf_with_qwen_api(
    "resume.pdf",
    model_name="qwen-max"
)

# 直接传入 API key（如果环境变量未设置）
result = parse_resume_pdf_with_qwen_api(
    "resume.pdf",
    model_name="qwen-plus",
    api_key="sk-9c76a51a6ea24cd6b65db4cc037dba31"
)
```

## API 配置

Qwen API 使用 OpenAI 兼容接口：

- **Base URL**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **API Key**: 从环境变量 `QWEN_API_KEY` 读取
- **模型命名**: 使用 Qwen 官方模型名称

## 输出结果

解析完成后会生成 JSON 文件，包含以下信息：

- **个人信息**: 姓名、联系方式、地址等
- **工作经历**: 公司、职位、时间、描述
- **教育背景**: 学校、专业、学历、时间
- **技能**: 技能列表
- **项目经历**: 项目名称、描述、时间

## 故障排除

### 问题：API 密钥未找到

```
错误: 未找到 Qwen API 密钥
```

**解决方案**:
1. 检查 `.env` 文件是否存在且包含 `QWEN_API_KEY`
2. 或在 shell 中设置环境变量
3. 或在代码中直接传入 `api_key` 参数

### 问题：API 调用失败

```
错误: 信息提取失败
```

**可能原因**:
1. API 密钥无效或过期
2. 网络连接问题
3. API 配额不足
4. 模型名称不正确

**解决方案**:
1. 验证 API 密钥是否正确
2. 检查网络连接
3. 查看 API 使用配额
4. 确认模型名称是否在支持列表中

### 问题：模型不支持

如果遇到模型不支持的错误，请确认：
- 模型名称拼写正确
- 您的账户有权限使用该模型
- 模型在 Qwen API 中可用

## 性能建议

1. **快速处理**: 使用 `qwen-turbo`
2. **高准确度**: 使用 `qwen-max`
3. **长文本**: 使用 `qwen-max-longcontext`
4. **平衡**: 使用 `qwen-plus`（默认）

## 安全提示

⚠️ **重要**: 
- 不要将 API 密钥提交到 Git 仓库
- `.env` 文件已在 `.gitignore` 中，不会被提交
- 如果需要在团队中共享，使用环境变量管理工具

## 更多信息

- Qwen API 文档: https://help.aliyun.com/zh/model-studio/
- DashScope 控制台: https://dashscope.console.aliyun.com/

