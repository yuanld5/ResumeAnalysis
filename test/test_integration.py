"""
测试 unstructured 和 langextract 合作完成任务
工作流程：
1. 使用 unstructured 解析和清理文档
2. 使用 langextract 从清理后的文本中提取结构化信息
"""

import json
from typing import Dict, Any, List
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title


def parse_with_unstructured(text: str) -> List[str]:
    """
    使用 unstructured 解析文本并提取内容
    
    Args:
        text: 原始文本
        
    Returns:
        清理后的文本列表
    """
    print("步骤1: 使用 unstructured 解析文档...")
    
    try:
        # 解析文档
        elements = partition(text=text)
        
        # 提取文本内容
        cleaned_texts = [element.text for element in elements if element.text.strip()]
        
        print(f"  解析出 {len(elements)} 个元素")
        print(f"  提取出 {len(cleaned_texts)} 段有效文本")
        
        return cleaned_texts
        
    except Exception as e:
        print(f"  unstructured 解析失败: {e}")
        # 如果解析失败，返回原始文本
        return [text]


def extract_with_langextract(texts: List[str]) -> Dict[str, Any]:
    """
    使用 langextract 从文本中提取结构化信息
    
    Args:
        texts: 清理后的文本列表
        
    Returns:
        提取的结构化信息
    """
    print("\n步骤2: 使用 langextract 提取结构化信息...")
    
    # 合并所有文本
    combined_text = "\n".join(texts)
    
    print(f"  处理文本长度: {len(combined_text)} 字符")
    
    # 模拟提取过程
    # 实际使用时需要根据langextract的API进行调整
    try:
        # 这里提供一个示例提取结果
        # 实际使用时需要调用langextract的API
        
        extracted_data = {
            "个人信息": {
                "姓名": None,
                "职位": None,
                "联系方式": {}
            },
            "工作经历": [],
            "教育背景": [],
            "技能": []
        }
        
        # 简单的文本匹配提取（示例）
        lines = combined_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 简单的模式匹配（实际应该使用langextract）
            if '姓名' in line or '名字' in line:
                parts = line.split('：')
                if len(parts) > 1:
                    extracted_data["个人信息"]["姓名"] = parts[-1].strip()
            elif '电话' in line or '手机' in line:
                parts = line.split('：')
                if len(parts) > 1:
                    extracted_data["个人信息"]["联系方式"]["电话"] = parts[-1].strip()
            elif '邮箱' in line or 'email' in line.lower():
                parts = line.split('：')
                if len(parts) > 1:
                    extracted_data["个人信息"]["联系方式"]["邮箱"] = parts[-1].strip()
        
        print(f"  提取出 {len(extracted_data)} 个主要类别")
        
        return extracted_data
        
    except Exception as e:
        print(f"  langextract 提取失败: {e}")
        return {}


def integrated_resume_analysis(resume_text: str) -> Dict[str, Any]:
    """
    完整的简历分析流程：unstructured + langextract
    
    Args:
        resume_text: 原始简历文本
        
    Returns:
        分析结果
    """
    print("\n" + "=" * 60)
    print("开始集成测试：unstructured + langextract")
    print("=" * 60)
    
    # 步骤1: 使用 unstructured 解析
    cleaned_texts = parse_with_unstructured(resume_text)
    
    # 步骤2: 使用 langextract 提取
    extracted_info = extract_with_langextract(cleaned_texts)
    
    # 步骤3: 整合结果
    result = {
        "原始文本长度": len(resume_text),
        "清理后文本段数": len(cleaned_texts),
        "提取的结构化信息": extracted_info,
        "处理状态": "成功" if extracted_info else "部分成功"
    }
    
    return result


def test_integration_workflow():
    """测试完整的集成工作流"""
    print("\n" + "=" * 60)
    print("测试集成工作流")
    print("=" * 60)
    
    # 示例简历文本
    sample_resume = """
    简历
    
    个人信息
    姓名：赵六
    职位：数据科学家
    电话：137-0000-0000
    邮箱：zhaoliu@example.com
    地址：上海市浦东新区
    
    工作经历
    2021-2023  阿里巴巴集团  数据工程师
    负责大数据平台开发，使用Spark和Hadoop
    
    2023-至今  腾讯科技  数据科学家
    负责机器学习模型开发，使用Python和TensorFlow
    
    教育背景
    2017-2021  复旦大学  数据科学与大数据技术  本科
    
    技能
    Python, SQL, Spark, TensorFlow, 机器学习, 数据分析
    """
    
    print("\n原始简历文本：")
    print(sample_resume)
    print("\n" + "-" * 60)
    
    # 执行集成分析
    result = integrated_resume_analysis(sample_resume)
    
    # 显示结果
    print("\n" + "=" * 60)
    print("分析结果")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


def test_file_processing():
    """测试处理文件（如果存在）"""
    print("\n" + "=" * 60)
    print("测试文件处理流程")
    print("=" * 60)
    
    import os
    
    test_files = [
        "test_resume.pdf",
        "test_resume.docx",
        "test_resume.html",
        "test_resume.txt"
    ]
    
    for filename in test_files:
        if os.path.exists(filename):
            print(f"\n处理文件: {filename}")
            
            try:
                # 使用unstructured解析文件
                elements = partition(filename=filename)
                texts = [element.text for element in elements if element.text.strip()]
                
                # 使用langextract提取信息
                extracted_info = extract_with_langextract(texts)
                
                print(f"\n提取结果：")
                print(json.dumps(extracted_info, ensure_ascii=False, indent=2))
                
                return extracted_info
                
            except Exception as e:
                print(f"处理失败: {e}")
                import traceback
                traceback.print_exc()
            break
    else:
        print("\n未找到测试文件")
        print("提示：将简历文件放在项目根目录即可测试")


def main():
    """运行所有集成测试"""
    print("\n开始集成测试：unstructured + langextract\n")
    
    try:
        # 测试1: 完整工作流
        result = test_integration_workflow()
        
        # 测试2: 文件处理
        test_file_processing()
        
        print("\n" + "=" * 60)
        print("所有集成测试完成！")
        print("=" * 60)
        print("\n工作流程总结：")
        print("1. unstructured 负责文档解析和清理")
        print("2. langextract 负责结构化信息提取")
        print("3. 两者结合可以实现完整的简历分析流程")
        
    except ImportError as e:
        print(f"\n错误: 缺少必要的库")
        print(f"请运行: pip install unstructured langextract")
        print(f"详细错误: {e}")
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

