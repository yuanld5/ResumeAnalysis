"""
使用 unstructured 和 langextract 解析 PDF 简历 - 支持 Qwen 和 DeepSeek 模型

通过 Ollama 提供商使用 Qwen 或 DeepSeek 模型进行信息提取

前置要求：
1. 安装并运行 Ollama: https://ollama.ai
2. 下载 Qwen 或 DeepSeek 模型：
   - ollama pull qwen2.5:latest
   - ollama pull deepseek-r1:latest
   或
   - ollama pull qwen2.5:7b
   - ollama pull deepseek-r1:7b
"""

import json
import os
from typing import Dict, Any, Optional
from unstructured.partition.auto import partition
import langextract as lx
from langextract.providers.ollama import OllamaLanguageModel


def parse_pdf_with_unstructured(pdf_path: str) -> str:
    """
    使用 unstructured 解析 PDF 文件
    
    Args:
        pdf_path: PDF 文件路径
        
    Returns:
        提取的文本内容
    """
    print("=" * 60)
    print("步骤 1: 使用 unstructured 解析 PDF 文件")
    print("=" * 60)
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")
    
    print(f"正在解析 PDF: {pdf_path}")
    
    try:
        # 使用 unstructured 解析 PDF
        elements = partition(filename=pdf_path)
        
        # 提取所有文本内容
        text_parts = []
        for element in elements:
            if hasattr(element, 'text') and element.text:
                text_parts.append(element.text.strip())
        
        # 合并文本
        full_text = "\n".join(text_parts)
        
        print(f"✓ 成功解析 PDF")
        print(f"  提取了 {len(elements)} 个元素")
        print(f"  文本总长度: {len(full_text)} 字符")
        print(f"\n前 500 个字符预览：")
        print("-" * 60)
        print(full_text[:500] + "..." if len(full_text) > 500 else full_text)
        print("-" * 60)
        
        return full_text
        
    except Exception as e:
        print(f"✗ PDF 解析失败: {e}")
        raise


def extract_with_qwen_or_deepseek(
    text: str, 
    model_name: str = "qwen2.5:latest",
    ollama_url: str = "http://localhost:11434"
) -> Dict[str, Any]:
    """
    使用 Qwen 或 DeepSeek 模型（通过 Ollama）提取简历信息
    
    Args:
        text: 简历文本内容
        model_name: 模型名称，例如 "qwen2.5:latest", "deepseek-r1:latest"
        ollama_url: Ollama 服务地址
        
    Returns:
        提取的结构化信息
    """
    print("\n" + "=" * 60)
    print(f"步骤 2: 使用 {model_name} 模型提取结构化信息")
    print("=" * 60)
    
    # 定义简历信息的 Schema
    resume_schema = {
        "type": "object",
        "properties": {
            "个人信息": {
                "type": "object",
                "properties": {
                    "姓名": {"type": "string", "description": "求职者的姓名"},
                    "性别": {"type": "string", "description": "性别"},
                    "出生日期": {"type": "string", "description": "出生日期或年龄"},
                    "手机号码": {"type": "string", "description": "联系电话或手机号码"},
                    "电子邮箱": {"type": "string", "description": "电子邮箱地址"},
                    "地址": {"type": "string", "description": "居住地址或现居地址"},
                    "求职意向": {"type": "string", "description": "期望职位或求职意向"}
                }
            },
            "工作经历": {
                "type": "array",
                "description": "工作经历列表",
                "items": {
                    "type": "object",
                    "properties": {
                        "公司名称": {"type": "string", "description": "公司或组织名称"},
                        "职位": {"type": "string", "description": "担任的职位"},
                        "工作时间": {"type": "string", "description": "工作起止时间"},
                        "工作描述": {"type": "string", "description": "工作职责和成就"}
                    }
                }
            },
            "教育背景": {
                "type": "array",
                "description": "教育经历列表",
                "items": {
                    "type": "object",
                    "properties": {
                        "学校名称": {"type": "string", "description": "学校或教育机构名称"},
                        "专业": {"type": "string", "description": "所学专业"},
                        "学历": {"type": "string", "description": "学历层次（本科、硕士、博士等）"},
                        "时间": {"type": "string", "description": "就读时间"}
                    }
                }
            },
            "技能": {
                "type": "array",
                "description": "技能列表",
                "items": {"type": "string", "description": "技能名称"}
            },
            "项目经历": {
                "type": "array",
                "description": "项目经历列表",
                "items": {
                    "type": "object",
                    "properties": {
                        "项目名称": {"type": "string", "description": "项目名称"},
                        "项目描述": {"type": "string", "description": "项目描述"},
                        "时间": {"type": "string", "description": "项目时间"}
                    }
                }
            }
        }
    }
    
    print(f"正在使用 {model_name} 模型提取信息...")
    print("这可能需要一些时间，请耐心等待...")
    
    try:
        # 方法1: 直接使用模型ID（如果模型名称匹配ollama模式）
        # langextract会自动识别ollama模型
        result = lx.extract(
            text=text,
            schema=resume_schema,
            model_id=model_name,  # 例如 "qwen2.5:latest" 或 "deepseek-r1:latest"
        )
        
        print("✓ 成功提取结构化信息")
        return result
        
    except Exception as e:
        print(f"使用自动识别方式失败: {e}")
        print("尝试使用 OllamaLanguageModel 直接实例化...")
        
        try:
            # 方法2: 直接使用 OllamaLanguageModel
            model = OllamaLanguageModel(
                model_id=model_name,
                model_url=ollama_url
            )
            
            result = lx.extract(
                text=text,
                schema=resume_schema,
                model=model  # 直接传入模型实例
            )
            
            print("✓ 成功提取结构化信息")
            return result
            
        except Exception as e2:
            print(f"✗ 信息提取失败: {e2}")
            print("\n故障排除提示：")
            print("1. 确保 Ollama 服务正在运行:")
            print("   - 检查: curl http://localhost:11434/api/tags")
            print("   - 或访问: http://localhost:11434")
            print("2. 确保已下载模型:")
            print(f"   - ollama pull {model_name}")
            print("3. 检查模型名称是否正确")
            print("4. 如果使用自定义 Ollama URL，请检查连接")
            
            # 使用备用方法
            return extract_with_fallback(text)


def extract_with_fallback(text: str) -> Dict[str, Any]:
    """
    备用方法：使用简单的文本匹配提取信息
    当模型不可用时使用
    """
    print("\n使用备用方法提取信息...")
    
    result = {
        "个人信息": {},
        "工作经历": [],
        "教育背景": [],
        "技能": [],
        "项目经历": []
    }
    
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检测个人信息
        if '姓名' in line or '名字' in line:
            parts = line.split('：') if '：' in line else line.split(':')
            if len(parts) > 1:
                result["个人信息"]["姓名"] = parts[-1].strip()
        elif '电话' in line or '手机' in line or '联系方式' in line:
            parts = line.split('：') if '：' in line else line.split(':')
            if len(parts) > 1:
                result["个人信息"]["手机号码"] = parts[-1].strip()
        elif '邮箱' in line or 'email' in line.lower() or '@' in line:
            if '@' in line:
                result["个人信息"]["电子邮箱"] = line.split()[-1] if ' ' in line else line
        elif '地址' in line:
            parts = line.split('：') if '：' in line else line.split(':')
            if len(parts) > 1:
                result["个人信息"]["地址"] = parts[-1].strip()
        
        # 检测工作经历
        if '工作' in line and ('经历' in line or '经验' in line):
            current_section = "工作经历"
        elif current_section == "工作经历" and line:
            if any(keyword in line for keyword in ['公司', '有限公司', '科技', '股份']):
                result["工作经历"].append({
                    "公司名称": line,
                    "职位": "",
                    "工作时间": "",
                    "工作描述": ""
                })
        
        # 检测教育背景
        if '教育' in line or '学历' in line:
            current_section = "教育背景"
        elif current_section == "教育背景" and line:
            if any(keyword in line for keyword in ['大学', '学院', '学校']):
                result["教育背景"].append({
                    "学校名称": line,
                    "专业": "",
                    "学历": "",
                    "时间": ""
                })
    
    return result


def save_results(data: Dict[str, Any], output_path: str = "resume_extracted.json"):
    """
    保存提取的结果到 JSON 文件
    
    Args:
        data: 提取的结构化数据
        output_path: 输出文件路径
    """
    print("\n" + "=" * 60)
    print("步骤 3: 保存提取结果")
    print("=" * 60)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 结果已保存到: {output_path}")
        print(f"\n提取的数据预览：")
        preview = json.dumps(data, ensure_ascii=False, indent=2)
        print(preview[:1000] + "..." if len(preview) > 1000 else preview)
        
    except Exception as e:
        print(f"✗ 保存失败: {e}")


def parse_resume_pdf_with_qwen_or_deepseek(
    pdf_path: str, 
    model_name: str = "qwen2.5:latest",
    ollama_url: str = "http://localhost:11434",
    output_json: Optional[str] = None
) -> Dict[str, Any]:
    """
    完整的简历解析流程 - 使用 Qwen 或 DeepSeek 模型
    
    Args:
        pdf_path: PDF 文件路径
        model_name: 模型名称，例如 "qwen2.5:latest", "deepseek-r1:latest"
        ollama_url: Ollama 服务地址
        output_json: 输出 JSON 文件路径（可选）
        
    Returns:
        提取的结构化信息
    """
    print("\n" + "=" * 60)
    print(f"开始解析简历 PDF (使用 {model_name} 模型)")
    print("=" * 60)
    
    # 步骤 1: 使用 unstructured 解析 PDF
    resume_text = parse_pdf_with_unstructured(pdf_path)
    
    # 步骤 2: 使用 Qwen/DeepSeek 模型提取结构化信息
    extracted_data = extract_with_qwen_or_deepseek(
        resume_text, 
        model_name=model_name,
        ollama_url=ollama_url
    )
    
    # 步骤 3: 保存结果
    if output_json:
        save_results(extracted_data, output_json)
    else:
        # 默认输出文件名
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        model_short = model_name.split(':')[0]  # 例如 "qwen2.5"
        output_json = f"{base_name}_extracted_{model_short}.json"
        save_results(extracted_data, output_json)
    
    print("\n" + "=" * 60)
    print("简历解析完成！")
    print("=" * 60)
    
    return extracted_data


def check_ollama_connection(ollama_url: str = "http://localhost:11434") -> bool:
    """
    检查 Ollama 服务是否可用
    
    Args:
        ollama_url: Ollama 服务地址
        
    Returns:
        是否可用
    """
    try:
        import requests
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✓ Ollama 服务可用")
            print(f"  已安装的模型: {[m.get('name', '') for m in models]}")
            return True
        return False
    except Exception as e:
        print(f"✗ Ollama 服务不可用: {e}")
        print(f"  请确保 Ollama 正在运行: {ollama_url}")
        return False


def main():
    """主函数 - 示例用法"""
    import sys
    
    # 检查 Ollama 连接
    print("检查 Ollama 服务...")
    if not check_ollama_connection():
        print("\n请先安装并启动 Ollama:")
        print("1. 访问 https://ollama.ai 下载安装")
        print("2. 启动 Ollama 服务")
        print("3. 下载模型: ollama pull qwen2.5:latest")
        print("   或: ollama pull deepseek-r1:latest")
        return
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "test_resume.pdf"
        print(f"未指定 PDF 文件，将使用默认路径: {pdf_path}")
        print("用法: python example_resume_parser_qwen_deepseek.py <pdf_file_path> [model_name]")
        print()
    
    # 模型选择
    model_name = "qwen2.5:latest"  # 默认使用 Qwen
    if len(sys.argv) > 2:
        model_name = sys.argv[2]
    
    # 支持的模型示例
    supported_models = [
        "qwen2.5:latest",
        "qwen2.5:7b",
        "qwen2.5:14b",
        "qwen2.5:32b",
        "deepseek-r1:latest",
        "deepseek-r1:7b",
        "deepseek-r1:32b",
        "deepseek-coder:latest",
    ]
    
    print(f"\n使用模型: {model_name}")
    print(f"支持的模型示例: {', '.join(supported_models)}")
    
    if not os.path.exists(pdf_path):
        print(f"\n错误: 文件不存在: {pdf_path}")
        print("\n提示：")
        print("1. 请将 PDF 简历文件放在项目目录中")
        print("2. 或使用命令行参数指定文件路径")
        print("3. 示例: python example_resume_parser_qwen_deepseek.py /path/to/resume.pdf qwen2.5:latest")
        return
    
    try:
        # 解析简历
        result = parse_resume_pdf_with_qwen_or_deepseek(
            pdf_path, 
            model_name=model_name
        )
        
        # 打印结果摘要
        print("\n提取结果摘要：")
        if "个人信息" in result and result["个人信息"]:
            print(f"  姓名: {result['个人信息'].get('姓名', '未提取')}")
            print(f"  联系方式: {result['个人信息'].get('手机号码', '未提取')}")
        print(f"  工作经历: {len(result.get('工作经历', []))} 条")
        print(f"  教育背景: {len(result.get('教育背景', []))} 条")
        print(f"  技能: {len(result.get('技能', []))} 项")
        
    except Exception as e:
        print(f"\n处理过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

