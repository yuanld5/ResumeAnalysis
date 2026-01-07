# 使用 Qwen 和 DeepSeek 模型进行简历解析

langextract 支持通过 **Ollama** 提供商使用 Qwen 和 DeepSeek 模型进行信息提取。

## 前置要求

### 1. 安装 Ollama

访问 [https://ollama.ai](https://ollama.ai) 下载并安装 Ollama。

### 2. 下载模型

安装 Ollama 后，在终端运行以下命令下载模型：

```bash
# 下载 Qwen 模型（推荐）
ollama pull qwen2.5:latest
# 或指定版本
ollama pull qwen2.5:7b
ollama pull qwen2.5:14b
ollama pull qwen2.5:32b

# 下载 DeepSeek 模型
ollama pull deepseek-r1:latest
# 或指定版本
ollama pull deepseek-r1:7b
ollama pull deepseek-r1:32b
ollama pull deepseek-coder:latest
```

### 3. 验证安装

```bash
# 检查 Ollama 服务
curl http://localhost:11434/api/tags

# 或查看已安装的模型
ollama list
```

## 使用方法

### 基本用法

```bash
# 激活虚拟环境
source venv/bin/activate

# 使用 Qwen 模型解析简历
python example_resume_parser_qwen_deepseek.py resume.pdf qwen2.5:latest

# 使用 DeepSeek 模型解析简历
python example_resume_parser_qwen_deepseek.py resume.pdf deepseek-r1:latest
```

### 在代码中使用

```python
import langextract as lx
from langextract.providers.ollama import OllamaLanguageModel

# 方法1: 直接使用模型ID（langextract会自动识别）
result = lx.extract(
    text=resume_text,
    schema=resume_schema,
    model_id="qwen2.5:latest"  # 或 "deepseek-r1:latest"
)

# 方法2: 直接实例化 OllamaLanguageModel
model = OllamaLanguageModel(
    model_id="qwen2.5:latest",
    model_url="http://localhost:11434"  # 可选，默认值
)

result = lx.extract(
    text=resume_text,
    schema=resume_schema,
    model=model
)
```

## 支持的模型

### Qwen 系列
- `qwen2.5:latest` - 最新版本
- `qwen2.5:7b` - 7B 参数版本
- `qwen2.5:14b` - 14B 参数版本
- `qwen2.5:32b` - 32B 参数版本

### DeepSeek 系列
- `deepseek-r1:latest` - 最新版本（推理优化）
- `deepseek-r1:7b` - 7B 参数版本
- `deepseek-r1:32b` - 32B 参数版本
- `deepseek-coder:latest` - 代码专用版本

## 模型选择建议

1. **Qwen2.5**: 
   - 中文理解能力强
   - 适合处理中文简历
   - 推荐使用 `qwen2.5:7b` 或 `qwen2.5:14b`

2. **DeepSeek-R1**:
   - 推理能力强
   - 适合复杂的信息提取任务
   - 推荐使用 `deepseek-r1:7b` 或更高版本

3. **性能考虑**:
   - 7B 模型：速度快，适合快速处理
   - 14B/32B 模型：准确度高，但速度较慢

## 配置选项

### 自定义 Ollama URL

如果 Ollama 运行在不同的地址或端口：

```python
model = OllamaLanguageModel(
    model_id="qwen2.5:latest",
    model_url="http://your-server:11434"
)
```

### 设置超时时间

```python
result = lx.extract(
    text=resume_text,
    schema=resume_schema,
    model_id="qwen2.5:latest",
    language_model_params={
        "timeout": 300  # 300秒超时
    }
)
```

### 设置温度参数

```python
result = lx.extract(
    text=resume_text,
    schema=resume_schema,
    model_id="qwen2.5:latest",
    language_model_params={
        "temperature": 0.1  # 较低温度，更确定性的输出
    }
)
```

## 优势

1. **本地运行**: 不需要 API 密钥，数据隐私更好
2. **免费使用**: 完全免费，无使用限制
3. **中文支持**: Qwen 和 DeepSeek 对中文支持优秀
4. **离线可用**: 可以在没有网络的环境中使用

## 故障排除

### 问题：Ollama 服务不可用

```bash
# 检查 Ollama 是否运行
curl http://localhost:11434/api/tags

# 如果失败，启动 Ollama
ollama serve
```

### 问题：模型未找到

```bash
# 检查已安装的模型
ollama list

# 如果模型不存在，下载它
ollama pull qwen2.5:latest
```

### 问题：提取速度慢

- 使用较小的模型（如 7B 而不是 32B）
- 减少文本长度
- 检查系统资源（CPU/内存）

### 问题：提取结果不准确

- 尝试使用更大的模型
- 调整 schema 描述，使其更清晰
- 检查原始文本质量

## 性能对比

| 模型 | 参数量 | 速度 | 准确度 | 推荐场景 |
|------|--------|------|--------|----------|
| qwen2.5:7b | 7B | 快 | 高 | 快速处理，中文简历 |
| qwen2.5:14b | 14B | 中 | 很高 | 平衡性能和准确度 |
| deepseek-r1:7b | 7B | 快 | 高 | 复杂信息提取 |
| deepseek-r1:32b | 32B | 慢 | 极高 | 高精度要求 |

## 示例输出

运行示例后，会生成 JSON 文件，包含提取的结构化信息：

```json
{
  "个人信息": {
    "姓名": "张三",
    "手机号码": "138-0000-0000",
    "电子邮箱": "zhangsan@example.com"
  },
  "工作经历": [
    {
      "公司名称": "ABC科技有限公司",
      "职位": "软件工程师",
      "工作时间": "2020-2023",
      "工作描述": "负责后端开发..."
    }
  ],
  "教育背景": [...],
  "技能": ["Python", "Java", "Docker"]
}
```

## 更多信息

- Ollama 官方文档: https://ollama.ai/docs
- Qwen 模型: https://github.com/QwenLM/Qwen
- DeepSeek 模型: https://www.deepseek.com

