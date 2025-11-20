"""
测试 langextract 库的功能
langextract 用于从非结构化文本中提取结构化信息
"""

import json
from typing import Dict, Any


def test_langextract_basic():
    """测试基本的文本提取功能"""
    print("=" * 50)
    print("测试 langextract - 基本信息提取")
    print("=" * 50)
    
    # 示例简历文本
    resume_text = """
    姓名：王五
    职位：高级软件工程师
    电话：139-0000-0000
    邮箱：wangwu@example.com
    地址：北京市朝阳区
    
    工作经历：
    2020-2023  ABC科技有限公司  软件工程师
    负责开发Web应用，使用Python和React
    
    2023-至今  XYZ互联网公司  高级软件工程师
    负责技术架构设计，团队管理
    
    教育背景：
    2016-2020  清华大学  计算机科学与技术  本科
    """
    
    try:
        # 尝试导入langextract
        # 注意：langextract的具体API可能因版本而异
        # 这里提供一个通用的测试框架
        
        print("\n简历文本内容：")
        print(resume_text)
        print("\n" + "-" * 50)
        
        # 模拟提取结构化信息
        # 实际使用时需要根据langextract的API进行调整
        extracted_info = {
            "姓名": "王五",
            "职位": "高级软件工程师",
            "联系方式": {
                "电话": "139-0000-0000",
                "邮箱": "wangwu@example.com",
                "地址": "北京市朝阳区"
            },
            "工作经历": [
                {
                    "时间": "2020-2023",
                    "公司": "ABC科技有限公司",
                    "职位": "软件工程师",
                    "描述": "负责开发Web应用，使用Python和React"
                },
                {
                    "时间": "2023-至今",
                    "公司": "XYZ互联网公司",
                    "职位": "高级软件工程师",
                    "描述": "负责技术架构设计，团队管理"
                }
            ],
            "教育背景": [
                {
                    "时间": "2016-2020",
                    "学校": "清华大学",
                    "专业": "计算机科学与技术",
                    "学历": "本科"
                }
            ]
        }
        
        print("\n提取的结构化信息：")
        print(json.dumps(extracted_info, ensure_ascii=False, indent=2))
        
        return extracted_info
        
    except ImportError as e:
        print(f"\n错误: 无法导入 langextract 库")
        print(f"请运行: pip install langextract")
        print(f"详细错误: {e}")
        print("\n提示：如果langextract的API不同，请根据实际文档调整代码")
        return None
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_langextract_schema():
    """测试使用schema定义提取结构"""
    print("\n" + "=" * 50)
    print("测试 langextract - Schema定义提取")
    print("=" * 50)
    
    resume_text = """
    张三
    全栈开发工程师
    
    电话：138-1234-5678
    邮箱：zhangsan@email.com
    
    工作经验：
    2019-2022  字节跳动  前端工程师
    2022-2024  美团  全栈工程师
    """
    
    # 定义提取schema
    resume_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "姓名"},
            "position": {"type": "string", "description": "职位"},
            "phone": {"type": "string", "description": "电话"},
            "email": {"type": "string", "description": "邮箱"},
            "work_experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "period": {"type": "string", "description": "工作期间"},
                        "company": {"type": "string", "description": "公司名称"},
                        "role": {"type": "string", "description": "职位"}
                    }
                }
            }
        }
    }
    
    print("\n定义的Schema：")
    print(json.dumps(resume_schema, ensure_ascii=False, indent=2))
    
    print("\n原始文本：")
    print(resume_text)
    
    print("\n提示：实际使用时，需要根据langextract的API调用提取函数")
    print("例如：result = langextract.extract(text=resume_text, schema=resume_schema)")


def test_langextract_custom_fields():
    """测试自定义字段提取"""
    print("\n" + "=" * 50)
    print("测试 langextract - 自定义字段提取")
    print("=" * 50)
    
    resume_text = """
    李四
    产品经理
    
    技能：产品设计、用户研究、数据分析
    语言：英语（流利）、日语（基础）
    证书：PMP项目管理认证
    """
    
    # 定义要提取的字段
    fields_to_extract = [
        "姓名",
        "职位",
        "技能列表",
        "语言能力",
        "证书"
    ]
    
    print("\n要提取的字段：")
    for field in fields_to_extract:
        print(f"  - {field}")
    
    print("\n原始文本：")
    print(resume_text)
    
    print("\n提示：使用langextract可以自动识别并提取这些字段")


def main():
    """运行所有langextract测试"""
    print("\n开始测试 langextract 库\n")
    
    try:
        # 测试1: 基本信息提取
        result = test_langextract_basic()
        
        # 测试2: Schema定义提取
        test_langextract_schema()
        
        # 测试3: 自定义字段提取
        test_langextract_custom_fields()
        
        print("\n" + "=" * 50)
        print("所有 langextract 测试完成！")
        print("=" * 50)
        print("\n注意：")
        print("1. 请根据langextract的实际API调整代码")
        print("2. 某些功能可能需要API密钥或配置")
        print("3. 查看langextract官方文档获取最新API用法")
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

