"""
测试 unstructured 库的功能
unstructured 用于解析非结构化文档（如PDF、Word、HTML等）
"""

import os
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title


def test_unstructured_text():
    """测试解析纯文本"""
    print("=" * 50)
    print("测试 unstructured - 纯文本解析")
    print("=" * 50)
    
    # 示例文本
    sample_text = """
    张三
    软件工程师
    
    联系方式：
    电话：138-0000-0000
    邮箱：zhangsan@example.com
    
    工作经历：
    2020-2023  ABC科技有限公司
    负责后端开发，使用Python和Django框架
    
    2023-至今  XYZ互联网公司
    负责系统架构设计，使用微服务架构
    """
    
    # 使用unstructured解析文本
    elements = partition(text=sample_text)
    
    print(f"\n解析出 {len(elements)} 个元素：\n")
    for i, element in enumerate(elements, 1):
        print(f"元素 {i}:")
        print(f"  类型: {type(element).__name__}")
        print(f"  内容: {element.text[:100]}...")
        print()
    
    return elements


def test_unstructured_chunking():
    """测试文档分块功能"""
    print("=" * 50)
    print("测试 unstructured - 文档分块")
    print("=" * 50)
    
    sample_text = """
    简历
    
    个人信息
    姓名：李四
    职位：产品经理
    
    教育背景
    2015-2019  北京大学  计算机科学  本科
    
    工作经历
    2019-2021  腾讯科技  产品助理
    2021-2023  阿里巴巴  产品经理
    """
    
    # 解析文档
    elements = partition(text=sample_text)
    
    # 按标题分块
    chunks = chunk_by_title(elements)
    
    print(f"\n文档被分成 {len(chunks)} 个块：\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"块 {i}:")
        print(f"  内容: {chunk.text[:150]}...")
        print()
    
    return chunks


def test_unstructured_file():
    """测试解析文件（如果存在）"""
    print("=" * 50)
    print("测试 unstructured - 文件解析")
    print("=" * 50)
    
    # 检查是否有测试文件
    test_files = [
        "test_resume.pdf",
        "test_resume.docx",
        "test_resume.html",
        "test_resume.txt"
    ]
    
    for filename in test_files:
        if os.path.exists(filename):
            print(f"\n找到测试文件: {filename}")
            try:
                elements = partition(filename=filename)
                print(f"成功解析，共 {len(elements)} 个元素")
                print(f"前3个元素预览：")
                for i, element in enumerate(elements[:3], 1):
                    print(f"  {i}. {element.text[:80]}...")
            except Exception as e:
                print(f"解析失败: {e}")
            break
    else:
        print("\n未找到测试文件，跳过文件解析测试")
        print("提示：可以将简历文件放在项目根目录进行测试")


def main():
    """运行所有unstructured测试"""
    print("\n开始测试 unstructured 库\n")
    
    try:
        # 测试1: 纯文本解析
        elements = test_unstructured_text()
        
        # 测试2: 文档分块
        chunks = test_unstructured_chunking()
        
        # 测试3: 文件解析
        test_unstructured_file()
        
        print("\n" + "=" * 50)
        print("所有 unstructured 测试完成！")
        print("=" * 50)
        
    except ImportError as e:
        print(f"\n错误: 无法导入 unstructured 库")
        print(f"请运行: pip install unstructured")
        print(f"详细错误: {e}")
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

