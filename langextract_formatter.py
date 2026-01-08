#!/usr/bin/env python3
"""
简历格式化器 - 使用langextract
运行环境: venv (Python 3.13)
功能: 使用langextract对middles文件夹下的文本文件进行AI解析，生成结构化JSON
"""

import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import langextract as lx
from langextract.providers.openai import OpenAILanguageModel
from langextract.data import ExampleData, Extraction

# 加载环境变量
load_dotenv()

def format_resume_with_langextract(text_file: str) -> dict:
    """
    使用 langextract 格式化简历内容
    
    Args:
        text_file: 文本文件路径
        
    Returns:
        格式化后的简历数据
    """
    print(f"使用 langextract 格式化简历: {text_file}")
    
    # 读取文本内容
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"文本长度: {len(text)} 字符")
    print(f"前500字符预览: {text[:500]}...")
    
    # 完整的简历信息提取schema
    schema = {
        "个人信息": {
            "姓名": "string",
            "性别": "string", 
            "年龄": "string",
            "电话": "string",
            "邮箱": "string",
            "微信": "string",
            "籍贯": "string",
            "政治面貌": "string",
            "婚姻状况": "string"
        },
        "求职信息": {
            "工作时长": "string",
            "求职意向": "string",
            "期望薪资": "string",
            "期望城市": "string"
        },
        "工作经历": [
            {
                "公司名称": "string",
                "职位": "string", 
                "工作时间": "string",
                "工作描述": "string",
                "主要成果": "string"
            }
        ],
        "教育背景": [
            {
                "学校名称": "string",
                "专业": "string",
                "学历": "string",
                "就读时间": "string"
            }
        ],
        "项目经历": [
            {
                "项目名称": "string",
                "项目时间": "string", 
                "技术栈": "string",
                "项目描述": "string",
                "个人职责": "string"
            }
        ],
        "技能专长": {
            "编程语言": "string",
            "框架技术": "string", 
            "数据库技术": "string",
            "容器技术": "string",
            "其他技能": "string"
        },
        "自我评价": "string"
    }
    
    # 创建精确的示例数据，严格区分工作经历和项目经历
    example_text = """
    张三
    
    男|30岁|籍贯：北京|党员
    
    联系方式
    电话:13800138000
    微信号:13800138000
    邮箱:zhangsan@example.com
    
    求职信息
    工作时长：8年
    求职意向：Java开发
    期望薪资：20-25K
    期望城市：北京
    
    工作经历
    阿里巴巴 Java高级工程师 2020.01-2023.12
    负责电商平台后端开发，参与系统架构设计
    主要成果：完成订单系统重构，性能提升30%
    
    腾讯 Java工程师 2017.06-2019.12
    负责微信支付相关功能开发
    主要成果：完成支付流程优化，交易成功率提升至99.9%
    
    教育背景
    清华大学 计算机科学与技术 本科 2013.09-2017.06
    
    项目经历
    电商平台重构 技术负责人 2021.03-2022.06
    技术栈：Java+Spring+MySQL+Redis
    重构老旧电商系统，提升系统性能和稳定性
    负责架构设计、技术选型、团队协调
    
    个人优势
    精通Java、Spring框架
    熟悉MySQL、Redis等数据库
    """
    
    # 创建精确的 Extraction 对象 - 只包含必要的示例
    extractions = [
        # 个人信息
        Extraction(extraction_class="个人信息_姓名", extraction_text="张三"),
        Extraction(extraction_class="个人信息_性别", extraction_text="男"),
        Extraction(extraction_class="个人信息_年龄", extraction_text="30岁"),
        Extraction(extraction_class="个人信息_电话", extraction_text="13800138000"),
        Extraction(extraction_class="个人信息_邮箱", extraction_text="zhangsan@example.com"),
        Extraction(extraction_class="个人信息_微信", extraction_text="13800138000"),
        Extraction(extraction_class="个人信息_籍贯", extraction_text="北京"),
        Extraction(extraction_class="个人信息_政治面貌", extraction_text="党员"),
        
        # 求职信息
        Extraction(extraction_class="求职信息_工作时长", extraction_text="8年"),
        Extraction(extraction_class="求职信息_求职意向", extraction_text="Java开发"),
        Extraction(extraction_class="求职信息_期望薪资", extraction_text="20-25K"),
        Extraction(extraction_class="求职信息_期望城市", extraction_text="北京"),
        
        # 工作经历 - 严格按照工作经历部分提取
        Extraction(extraction_class="工作经历_公司名称", extraction_text="阿里巴巴"),
        Extraction(extraction_class="工作经历_职位", extraction_text="Java高级工程师"),
        Extraction(extraction_class="工作经历_工作时间", extraction_text="2020.01-2023.12"),
        Extraction(extraction_class="工作经历_工作描述", extraction_text="负责电商平台后端开发，参与系统架构设计"),
        Extraction(extraction_class="工作经历_主要成果", extraction_text="完成订单系统重构，性能提升30%"),
        
        Extraction(extraction_class="工作经历_公司名称", extraction_text="腾讯"),
        Extraction(extraction_class="工作经历_职位", extraction_text="Java工程师"),
        Extraction(extraction_class="工作经历_工作时间", extraction_text="2017.06-2019.12"),
        Extraction(extraction_class="工作经历_工作描述", extraction_text="负责微信支付相关功能开发"),
        Extraction(extraction_class="工作经历_主要成果", extraction_text="完成支付流程优化，交易成功率提升至99.9%"),
        
        # 教育背景
        Extraction(extraction_class="教育背景_学校名称", extraction_text="清华大学"),
        Extraction(extraction_class="教育背景_专业", extraction_text="计算机科学与技术"),
        Extraction(extraction_class="教育背景_学历", extraction_text="本科"),
        Extraction(extraction_class="教育背景_就读时间", extraction_text="2013.09-2017.06"),
        
        # 项目经历 - 严格按照项目经历部分提取
        Extraction(extraction_class="项目经历_项目名称", extraction_text="电商平台重构"),
        Extraction(extraction_class="项目经历_项目时间", extraction_text="2021.03-2022.06"),
        Extraction(extraction_class="项目经历_技术栈", extraction_text="Java+Spring+MySQL+Redis"),
        Extraction(extraction_class="项目经历_项目描述", extraction_text="重构老旧电商系统，提升系统性能和稳定性"),
        Extraction(extraction_class="项目经历_个人职责", extraction_text="负责架构设计、技术选型、团队协调"),
        
        # 技能专长
        Extraction(extraction_class="技能专长_编程语言", extraction_text="精通Java"),
        Extraction(extraction_class="技能专长_框架技术", extraction_text="熟悉Spring框架"),
        Extraction(extraction_class="技能专长_数据库技术", extraction_text="熟悉MySQL、Redis等数据库"),
        Extraction(extraction_class="技能专长_容器技术", extraction_text=""),
        Extraction(extraction_class="技能专长_其他技能", extraction_text=""),
        
        # 自我评价
        Extraction(extraction_class="自我评价", extraction_text="具备良好的团队协作能力和技术学习能力")
    ]
    
    examples = [ExampleData(text=example_text, extractions=extractions)]
    
    # 尝试使用 Qwen API
    qwen_api_key = os.getenv('QWEN_API_KEY')
    if qwen_api_key:
        try:
            print("使用 Qwen API 进行格式化...")
            
            model = OpenAILanguageModel(
                model_id="qwen-plus",
                api_key=qwen_api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            result = lx.extract(
                text,
                schema,
                examples=examples,
                model=model
            )
            
            print("✓ Qwen API 格式化成功")
            return convert_langextract_result(result)
            
        except Exception as e:
            print(f"✗ Qwen API 失败: {e}")
    
    # 尝试使用 DeepSeek API
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
    if deepseek_api_key:
        try:
            print("使用 DeepSeek API 进行格式化...")
            
            model = OpenAILanguageModel(
                model_id="deepseek-chat",
                api_key=deepseek_api_key,
                base_url="https://api.deepseek.com/v1"
            )
            
            result = lx.extract(
                text,
                schema,
                examples=examples,
                model=model
            )
            
            print("✓ DeepSeek API 格式化成功")
            return convert_langextract_result(result)
            
        except Exception as e:
            print(f"✗ DeepSeek API 失败: {e}")
            raise
    
    raise ValueError("没有可用的 API key")

def convert_langextract_result(result) -> dict:
    """
    将 langextract 的结果转换为结构化数据
    
    Args:
        result: langextract 的 AnnotatedDocument 结果
        
    Returns:
        转换后的简历数据
    """
    # 初始化完整的结果结构
    resume_data = {
        "个人信息": {
            "姓名": "",
            "性别": "",
            "年龄": "",
            "电话": "",
            "邮箱": "",
            "微信": "",
            "籍贯": "",
            "政治面貌": "",
            "婚姻状况": ""
        },
        "求职信息": {
            "工作时长": "",
            "求职意向": "",
            "期望薪资": "",
            "期望城市": ""
        },
        "工作经历": [],
        "教育背景": [],
        "项目经历": [],
        "技能专长": {
            "编程语言": "",
            "框架技术": "",
            "数据库技术": "",
            "容器技术": "",
            "其他技能": ""
        },
        "自我评价": "",
        "原始文本": result.text if hasattr(result, 'text') else ""
    }
    
    # 临时存储用于构建列表项 - 使用更智能的分组策略
    work_groups = []  # 存储工作经历组
    edu_groups = []   # 存储教育背景组
    proj_groups = []  # 存储项目经历组
    
    # 从提取结果中获取信息
    if hasattr(result, 'extractions'):
        for extraction in result.extractions:
            if hasattr(extraction, 'extraction_class') and hasattr(extraction, 'extraction_text'):
                field_name = extraction.extraction_class
                field_value = extraction.extraction_text
                
                # 只保存非空值
                if field_value and field_value.strip():
                    field_value = field_value.strip()
                    
                    # 个人信息字段
                    if field_name.startswith("个人信息_"):
                        key = field_name.replace("个人信息_", "")
                        if key in resume_data["个人信息"]:
                            resume_data["个人信息"][key] = field_value
                    
                    # 求职信息字段
                    elif field_name.startswith("求职信息_"):
                        key = field_name.replace("求职信息_", "")
                        if key in resume_data["求职信息"]:
                            resume_data["求职信息"][key] = field_value
                    
                    # 工作经历字段 - 使用智能分组
                    elif field_name.startswith("工作经历_"):
                        key = field_name.replace("工作经历_", "")
                        
                        # 如果是公司名称，开始新的工作经历组
                        if key == "公司名称":
                            work_groups.append({
                                "公司名称": field_value,
                                "职位": "",
                                "工作时间": "",
                                "工作描述": "",
                                "主要成果": ""
                            })
                        # 否则添加到最后一个工作经历组
                        elif work_groups and key in work_groups[-1]:
                            work_groups[-1][key] = field_value
                    
                    # 教育背景字段 - 使用智能分组
                    elif field_name.startswith("教育背景_"):
                        key = field_name.replace("教育背景_", "")
                        
                        if key == "学校名称":
                            edu_groups.append({
                                "学校名称": field_value,
                                "专业": "",
                                "学历": "",
                                "就读时间": ""
                            })
                        elif edu_groups and key in edu_groups[-1]:
                            edu_groups[-1][key] = field_value
                    
                    # 项目经历字段 - 使用智能分组
                    elif field_name.startswith("项目经历_"):
                        key = field_name.replace("项目经历_", "")
                        
                        if key == "项目名称":
                            proj_groups.append({
                                "项目名称": field_value,
                                "项目时间": "",
                                "技术栈": "",
                                "项目描述": "",
                                "个人职责": ""
                            })
                        elif proj_groups and key in proj_groups[-1]:
                            proj_groups[-1][key] = field_value
                    
                    # 技能专长字段
                    elif field_name.startswith("技能专长_"):
                        key = field_name.replace("技能专长_", "")
                        if key in resume_data["技能专长"]:
                            resume_data["技能专长"][key] = field_value
                    
                    # 自我评价
                    elif field_name == "自我评价":
                        resume_data["自我评价"] = field_value
    
    # 将分组结果添加到最终数据中，只保留有效的条目
    resume_data["工作经历"] = [exp for exp in work_groups if exp.get("公司名称")]
    resume_data["教育背景"] = [edu for edu in edu_groups if edu.get("学校名称")]
    resume_data["项目经历"] = [proj for proj in proj_groups if proj.get("项目名称")]
    
    return resume_data

def save_result(data: dict, output_file: str):
    """
    保存结果到 JSON 文件
    
    Args:
        data: 简历数据
        output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 结果已保存到: {output_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("简历格式化器 - 使用langextract")
    print("=" * 60)
    
    # 查找middles文件夹下的文本文件
    middles_dir = Path("middles")
    if not middles_dir.exists():
        print("✗ middles文件夹不存在，请先运行 unstructured_extractor.py")
        return
    
    text_files = list(middles_dir.glob("*_extracted.txt"))
    if not text_files:
        print("✗ middles文件夹下没有找到 *_extracted.txt 文件")
        print("请先运行 unstructured_extractor.py 生成中间文件")
        return
    
    # 选择要处理的文件
    if len(sys.argv) > 1:
        try:
            file_index = int(sys.argv[1])
            if 0 <= file_index < len(text_files):
                text_file = text_files[file_index]
            else:
                print(f"文件索引超出范围 (0-{len(text_files)-1})")
                return
        except ValueError:
            print("请提供有效的文件索引数字")
            return
    else:
        text_file = text_files[0]
    
    print(f"可用文件:")
    for i, file in enumerate(text_files):
        marker = " -> " if file == text_file else "    "
        print(f"{marker}{i}: {file}")
    print()
    
    try:
        # 使用 langextract 格式化简历
        resume_data = format_resume_with_langextract(str(text_file))
        
        # 保存结果
        output_file = f"outs/{text_file.stem.replace('_extracted', '_formatted')}.json"
        
        # 确保输出目录存在
        Path("outs").mkdir(exist_ok=True)
        
        save_result(resume_data, output_file)
        
        print("\n" + "=" * 60)
        print("格式化完成！")
        print(f"输入文件: {text_file}")
        print(f"输出文件: {output_file}")
        print("=" * 60)
        
        # 显示提取的关键信息
        print("\n提取的关键信息:")
        print(f"姓名: {resume_data['个人信息']['姓名']}")
        print(f"求职意向: {resume_data['求职信息']['求职意向']}")
        print(f"期望薪资: {resume_data['求职信息']['期望薪资']}")
        print(f"工作经历数量: {len(resume_data['工作经历'])}")
        print(f"项目经历数量: {len(resume_data['项目经历'])}")
        
    except Exception as e:
        print(f"\n✗ 处理失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()