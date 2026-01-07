# 简历解析示例

这个示例展示了如何使用 `unstructured` 和 `langextract` 来解析 PDF 格式的简历并提取结构化信息。

## 功能特点

1. **PDF 解析**: 使用 `unstructured` 库解析 PDF 文件，提取文本内容
2. **信息提取**: 使用 `langextract` 从文本中提取结构化的简历信息
3. **结构化输出**: 将提取的信息保存为 JSON 格式

## 使用方法

### 基本用法

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行示例（需要提供 PDF 文件路径）
python example_resume_parser.py /path/to/resume.pdf
```

### 示例输出

脚本会：
1. 解析 PDF 文件，提取文本
2. 使用 AI 模型提取结构化信息
3. 保存结果到 JSON 文件

输出文件格式：`<原文件名>_extracted.json`

## 提取的信息字段

- **个人信息**: 姓名、性别、出生日期、联系方式、地址、求职意向
- **工作经历**: 公司名称、职位、工作时间、工作描述
- **教育背景**: 学校名称、专业、学历、时间
- **技能**: 技能列表
- **项目经历**: 项目名称、描述、时间

## 配置说明

### API 密钥配置（可选）

如果使用 Google AI API，需要设置环境变量：

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

或者在代码中直接指定：

```python
result = lx.extract(
    text=text,
    schema=resume_schema,
    api_key="your-api-key-here"
)
```

### 模型选择

可以指定不同的模型：

```python
result = lx.extract(
    text=text,
    schema=resume_schema,
    model="gemini-2.0-flash-exp"  # 或其他支持的模型
)
```

## 注意事项

1. **PDF 质量**: 确保 PDF 文件是文本格式（非扫描图片），否则解析效果可能不佳
2. **API 限制**: 使用 langextract 可能需要 API 密钥，注意使用限制和费用
3. **备用方法**: 如果 API 不可用，脚本会自动使用简单的文本匹配方法作为备用

## 故障排除

### 问题：PDF 解析失败

- 检查文件路径是否正确
- 确保 PDF 文件不是加密的
- 尝试使用其他 PDF 文件

### 问题：信息提取失败

- 检查网络连接
- 确认 API 密钥是否正确配置
- 查看错误信息，可能需要调整 schema 定义

### 问题：提取结果不准确

- 调整 schema 中的字段描述，使其更清晰
- 尝试使用不同的模型
- 检查原始文本质量

## 示例代码结构

```python
# 1. 解析 PDF
resume_text = parse_pdf_with_unstructured("resume.pdf")

# 2. 提取信息
extracted_data = extract_resume_info_with_langextract(resume_text)

# 3. 保存结果
save_results(extracted_data, "output.json")
```

## 扩展功能

可以根据需要修改 `resume_schema` 来提取更多或不同的字段。

