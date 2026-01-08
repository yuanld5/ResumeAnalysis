#!/usr/bin/env python3
"""
PDF内容提取器 - 使用unstructured
运行环境: venv39 (Python 3.10+)
功能: 使用unstructured读取PDF文件，提取结构化元素并保存到middles文件夹
"""

import os
import sys
from pathlib import Path

def extract_pdf_with_unstructured(pdf_path: str, output_dir: str = "middles") -> str:
    """
    使用 unstructured 混合方法提取 PDF 内容并保存到文件
    方法：pdfminer提取 + unstructured文本分区处理
    
    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录
        
    Returns:
        保存的文本文件路径
    """
    print(f"使用 unstructured 混合方法提取 PDF: {pdf_path}")
    
    # 确保输出目录存在
    Path(output_dir).mkdir(exist_ok=True)
    
    # 生成输出文件名
    pdf_name = Path(pdf_path).stem
    output_file = Path(output_dir) / f"{pdf_name}_extracted.txt"
    
    try:
        # 步骤1: 使用pdfminer提取原始文本
        print("  步骤1: 使用pdfminer提取原始文本...")
        from pdfminer.high_level import extract_text
        raw_text = extract_text(pdf_path)
        
        if not raw_text or len(raw_text) < 50:
            raise ValueError("pdfminer提取的内容过少")
        
        print(f"  ✓ pdfminer 提取成功，共 {len(raw_text)} 字符")
        
        # 步骤2: 使用unstructured进行文本分区和结构化
        print("  步骤2: 使用unstructured进行文本分区...")
        from unstructured.partition.text import partition_text
        elements = partition_text(text=raw_text)
        
        # 步骤3: 处理和优化文本结构
        print("  步骤3: 优化文本结构...")
        processed_parts = []
        
        for element in elements:
            element_text = str(element).strip()
            if element_text:
                element_type = type(element).__name__
                
                # 根据元素类型进行不同处理
                if element_type in ['Title', 'Header']:
                    # 标题类元素，前后加空行强调
                    processed_parts.append(f"\n{element_text}\n")
                elif element_type == 'NarrativeText':
                    # 正文文本，保持原样
                    processed_parts.append(element_text)
                elif element_type == 'ListItem':
                    # 列表项，添加适当缩进
                    processed_parts.append(f"• {element_text}")
                else:
                    # 其他类型，保持原样
                    processed_parts.append(element_text)
        
        # 合并处理后的文本
        processed_text = "\n".join(processed_parts)
        
        # 清理多余的空行和格式
        import re
        processed_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', processed_text)
        processed_text = processed_text.strip()
        
        print(f"  ✓ unstructured 处理成功，分区为 {len(elements)} 个元素")
        print(f"  ✓ 最终文本长度: {len(processed_text)} 字符")
        
        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_text)
        
        print(f"✓ 保存到: {output_file}")
        return str(output_file)
        
    except ImportError as e:
        print(f"  ✗ 缺少依赖: {e}")
        raise ValueError(f"unstructured 依赖缺失: {e}")
    except Exception as e:
        print(f"  ✗ unstructured 混合方法失败: {e}")
        raise ValueError(f"unstructured 处理失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("PDF内容提取器 - 使用unstructured")
    print("=" * 60)
    
    # 可以选择不同的PDF文件进行处理
    available_files = [
        "files/【架构部总监_成都 30-40K】Bryan 10年.pdf",
        "files/【架构部总监_成都 30-40K】Mr.xu 10年以上.pdf",
        "files/【架构部总监_成都 30-40K】mark 10年以上.pdf"
    ]
    
    # 默认处理第一个文件，可以通过命令行参数选择
    if len(sys.argv) > 1:
        try:
            file_index = int(sys.argv[1])
            if 0 <= file_index < len(available_files):
                pdf_file = available_files[file_index]
            else:
                print(f"文件索引超出范围 (0-{len(available_files)-1})")
                return
        except ValueError:
            print("请提供有效的文件索引数字")
            return
    else:
        pdf_file = available_files[0]
    
    print(f"可用文件:")
    for i, file in enumerate(available_files):
        marker = " -> " if file == pdf_file else "    "
        print(f"{marker}{i}: {file}")
    print()
    
    if not os.path.exists(pdf_file):
        print(f"✗ PDF文件不存在: {pdf_file}")
        return
    
    try:
        # 使用 unstructured 提取PDF内容
        text_file = extract_pdf_with_unstructured(pdf_file)
        
        print("\n" + "=" * 60)
        print("提取完成！")
        print(f"输入文件: {pdf_file}")
        print(f"输出文件: {text_file}")
        print("=" * 60)
        
        print(f"\n下一步: 使用 langextract_formatter.py 处理 {text_file}")
        
    except Exception as e:
        print(f"\n✗ 处理失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()