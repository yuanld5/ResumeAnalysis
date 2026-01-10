#!/usr/bin/env python3
"""
增强版简历格式化器 - 使用langextract with enhanced prompts
专门针对Excel演示数据格式进行优化
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import langextract as lx
from langextract.providers.openai import OpenAILanguageModel
from langextract.data import ExampleData, Extraction

# 加载环境变量
load_dotenv()

def format_resume_for_excel_format(text_file: str) -> dict:
    """
    使用 langextract 格式化简历内容，专门针对Excel演示数据格式
    
    Args:
        text_file: 文本文件路径
        
    Returns:
        格式化后的简历数据，匹配Excel演示数据格式
    """
    print(f"使用增强版 langextract 格式化简历: {text_file}")
    
    # 读取文本内容
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"文本长度: {len(text)} 字符")
    
    # 针对Excel演示数据格式的精确schema - 修复数组类型问题
    schema = {
        "基本信息": {
            "姓名": "string - 候选人的真实姓名",
            "性别": "string - 男/女",
            "出生日期": "string - YYYY-MM-DD格式的出生日期",
            "身份证号": "string - 18位身份证号码",
            "手机号": "string - 11位手机号码",
            "邮箱": "string - 电子邮箱地址"
        },
        "教育背景": {
            "毕业院校": "string - 最高学历对应的毕业院校",
            "最高学历": "string - 博士/硕士/本科/专科等"
        },
        "工作信息": {
            "当前职位": "string - 最近或当前的工作职位",
            "工作年限": "string - 总工作年数",
            "参加工作时间": "string - YYYY-MM-DD格式的首次工作时间"
        },
        "技能资质": {
            "职业资质": "string - 各种职业证书和资质认证，用分号分隔",
            "技术技能": "string - 具体的技术技能列表，用分号分隔",
            "管理技能": "string - 管理相关的技能，用分号分隔"
        },
        "能力评估": {
            "技术能力等级": "string - 根据技能描述评估：初级/中级/高级/专家级",
            "管理能力等级": "string - 根据管理经验评估：初级/中级/高级/专家级",
            "业务能力描述": "string - 业务相关能力的描述，用分号分隔"
        },
        "发展潜力": {
            "潜力标签": "string - 基于背景和经验的潜力评估，用分号分隔",
            "风险标签": "string - 可能的风险点评估，用分号分隔"
        }
    }
    
    # 创建详细的示例数据，完全匹配Excel格式要求
    example_text = """
    张明华 - 技术总监简历
    
    个人信息：
    性别：男
    出生日期：1985年3月15日
    身份证：110101198503151000
    联系方式：138****1234
    邮箱：zhang.minghua@company.com
    
    教育背景：
    清华大学 计算机科学与技术 硕士 2005-2008
    北京理工大学 软件工程 本科 2001-2005
    
    工作经历：
    2015.09至今 - 某科技公司 技术总监
    负责技术团队管理，系统架构设计，技术决策
    管理团队规模：15人
    主要成就：主导完成3个大型项目，系统性能提升40%
    
    2010.06-2015.08 - 阿里巴巴 高级架构师
    负责电商平台架构设计和优化
    
    2008.07-2010.05 - 腾讯 Java开发工程师
    负责后端系统开发
    
    技能专长：
    - 精通Java、Spring、MySQL、Redis
    - 熟练掌握分布式系统架构
    - 具备丰富的团队管理经验
    
    职业资质：
    - PMP项目管理认证
    - AWS解决方案架构师认证
    - TOGAF企业架构认证
    
    项目经验：
    电商平台重构项目（2020-2021）
    技术栈：Java + Spring Cloud + MySQL + Redis
    项目规模：日活用户500万+
    个人职责：技术负责人，负责整体架构设计
    """
    
    # 创建精确的 Extraction 对象，严格按照Excel格式
    extractions = [
        # 基本信息
        Extraction(extraction_class="基本信息_姓名", extraction_text="张明华"),
        Extraction(extraction_class="基本信息_性别", extraction_text="男"),
        Extraction(extraction_class="基本信息_出生日期", extraction_text="1985-03-15"),
        Extraction(extraction_class="基本信息_身份证号", extraction_text="110101198503151000"),
        Extraction(extraction_class="基本信息_手机号", extraction_text="13812341234"),
        Extraction(extraction_class="基本信息_邮箱", extraction_text="zhang.minghua@company.com"),
        
        # 教育背景
        Extraction(extraction_class="教育背景_毕业院校", extraction_text="清华大学"),
        Extraction(extraction_class="教育背景_最高学历", extraction_text="硕士"),
        
        # 工作信息
        Extraction(extraction_class="工作信息_当前职位", extraction_text="技术总监"),
        Extraction(extraction_class="工作信息_工作年限", extraction_text="16"),
        Extraction(extraction_class="工作信息_参加工作时间", extraction_text="2008-07-01"),
        
        # 技能资质
        Extraction(extraction_class="技能资质_职业资质", extraction_text="PMP;AWS架构师;TOGAF"),
        Extraction(extraction_class="技能资质_技术技能", extraction_text="Java;Spring;MySQL;Redis;分布式系统"),
        Extraction(extraction_class="技能资质_管理技能", extraction_text="团队管理;项目管理;技术决策"),
        
        # 能力评估
        Extraction(extraction_class="能力评估_技术能力等级", extraction_text="专家级"),
        Extraction(extraction_class="能力评估_管理能力等级", extraction_text="高级"),
        Extraction(extraction_class="能力评估_业务能力描述", extraction_text="技术战略规划;系统架构设计;团队建设"),
        
        # 发展潜力
        Extraction(extraction_class="发展潜力_潜力标签", extraction_text="CTO候选人;技术领导力强;创新能力突出"),
        Extraction(extraction_class="发展潜力_风险标签", extraction_text="无明显风险")
    ]
    
    examples = [ExampleData(text=example_text, extractions=extractions)]
    
    # 添加详细的系统提示
    system_prompt = """
    你是一个专业的简历分析专家，需要从简历中精确提取信息并格式化为标准的HR数据格式。

    重要提取规则：
    1. 姓名：提取候选人的真实姓名，通常在简历开头
    2. 性别：明确提取"男"或"女"，如果没有明确说明则留空
    3. 出生日期：转换为YYYY-MM-DD格式，如"1985年3月15日"转为"1985-03-15"
    4. 身份证号：提取完整的18位身份证号码
    5. 手机号：提取11位手机号码
    6. 邮箱：提取完整的电子邮箱地址
    7. 毕业院校：提取最高学历对应的学校名称
    8. 最高学历：从"博士、硕士、本科、专科"中选择最高的
    9. 当前职位：提取最近或当前的工作职位名称
    10. 工作年限：计算总工作年数，返回数字
    11. 参加工作时间：提取首次参加工作的时间，格式YYYY-MM-DD
    12. 职业资质：提取各种证书和认证，用分号分隔
    13. 技术技能：提取具体的技术技能，用分号分隔
    14. 管理技能：提取管理相关技能，用分号分隔
    15. 技术能力等级：根据技能描述评估为"初级/中级/高级/专家级"
    16. 管理能力等级：根据管理经验评估为"初级/中级/高级/专家级"
    17. 业务能力描述：总结业务相关的能力
    18. 潜力标签：基于教育背景、工作经验评估发展潜力
    19. 风险标签：识别可能的风险点，如"无明显风险"

    请严格按照示例格式提取信息，确保数据的准确性和完整性。
    """
    
    # 尝试使用 Qwen API
    qwen_api_key = os.getenv('QWEN_API_KEY')
    if qwen_api_key:
        try:
            print("使用 Qwen API 进行增强格式化...")
            
            model = OpenAILanguageModel(
                model_id="qwen-plus",
                api_key=qwen_api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                system_prompt=system_prompt
            )
            
            result = lx.extract(
                text,
                schema,
                examples=examples,
                model=model
            )
            
            print("✓ Qwen API 增强格式化成功")
            return convert_to_excel_structure(result)
            
        except Exception as e:
            print(f"✗ Qwen API 失败: {e}")
    
    # 尝试使用 DeepSeek API
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
    if deepseek_api_key:
        try:
            print("使用 DeepSeek API 进行增强格式化...")
            
            model = OpenAILanguageModel(
                model_id="deepseek-chat",
                api_key=deepseek_api_key,
                base_url="https://api.deepseek.com/v1",
                system_prompt=system_prompt
            )
            
            result = lx.extract(
                text,
                schema,
                examples=examples,
                model=model
            )
            
            print("✓ DeepSeek API 增强格式化成功")
            return convert_to_excel_structure(result)
            
        except Exception as e:
            print(f"✗ DeepSeek API 失败: {e}")
            raise
    
    raise ValueError("没有可用的 API key")

def convert_to_excel_structure(result) -> dict:
    """
    将 langextract 的结果转换为Excel演示数据结构
    
    Args:
        result: langextract 的 AnnotatedDocument 结果
        
    Returns:
        Excel格式的简历数据
    """
    # 初始化Excel格式的数据结构
    excel_data = {
        "员工工号": "",
        "姓名": "",
        "所属组织": "",
        "性别": "",
        "出生日期": "",
        "身份证": "",
        "手机号": "",
        "邮箱": "",
        "毕业院校": "",
        "最高学历": "",
        "担任岗位": "",
        "职级": "",
        "参加工作时间": "",
        "入司日期": "",
        "工作经验(年)": "",
        "绩效等级": "",
        "职业资质": "",
        "技术能力标签": "",
        "管理能力标签": "",
        "业务能力标签": "",
        "潜力标签": "",
        "风险标签": ""
    }
    
    # 从提取结果中获取信息
    extracted_data = {}
    if hasattr(result, 'extractions'):
        for extraction in result.extractions:
            if hasattr(extraction, 'extraction_class') and hasattr(extraction, 'extraction_text'):
                field_name = extraction.extraction_class
                field_value = extraction.extraction_text
                
                if field_value and field_value.strip():
                    extracted_data[field_name] = field_value.strip()
    
    # 映射到Excel格式
    # 基本信息映射
    excel_data["姓名"] = extracted_data.get("基本信息_姓名", "")
    excel_data["性别"] = extracted_data.get("基本信息_性别", "")
    excel_data["出生日期"] = extracted_data.get("基本信息_出生日期", "")
    excel_data["身份证"] = extracted_data.get("基本信息_身份证号", "")
    excel_data["邮箱"] = extracted_data.get("基本信息_邮箱", "")
    
    # 手机号脱敏处理
    phone = extracted_data.get("基本信息_手机号", "")
    if phone and len(phone) >= 7:
        excel_data["手机号"] = phone[:3] + "****" + phone[-4:]
    else:
        excel_data["手机号"] = phone
    
    # 教育背景映射
    excel_data["毕业院校"] = extracted_data.get("教育背景_毕业院校", "")
    excel_data["最高学历"] = extracted_data.get("教育背景_最高学历", "")
    
    # 工作信息映射
    excel_data["担任岗位"] = extracted_data.get("工作信息_当前职位", "")
    excel_data["参加工作时间"] = extracted_data.get("工作信息_参加工作时间", "")
    excel_data["工作经验(年)"] = extracted_data.get("工作信息_工作年限", "")
    
    # 生成员工工号
    if excel_data["姓名"]:
        timestamp = str(int(datetime.now().timestamp()))[-6:]
        excel_data["员工工号"] = f"r{timestamp}"
    
    # 推断所属组织
    excel_data["所属组织"] = infer_department_from_skills(
        extracted_data.get("技能资质_技术技能", ""),
        extracted_data.get("工作信息_当前职位", "")
    )
    
    # 推断职级
    excel_data["职级"] = infer_job_level_from_position(
        extracted_data.get("工作信息_当前职位", ""),
        extracted_data.get("工作信息_工作年限", "0")
    )
    
    # 技能和资质映射
    excel_data["职业资质"] = extracted_data.get("技能资质_职业资质", "")
    
    # 格式化技能标签
    tech_skills = extracted_data.get("技能资质_技术技能", "")
    tech_level = extracted_data.get("能力评估_技术能力等级", "中级")
    if tech_skills:
        skills_list = tech_skills.split(';')[:3]  # 最多3个技能
        excel_data["技术能力标签"] = ";".join([f"{skill}-{tech_level}" for skill in skills_list])
    
    mgmt_skills = extracted_data.get("技能资质_管理技能", "")
    mgmt_level = extracted_data.get("能力评估_管理能力等级", "中级")
    if mgmt_skills:
        skills_list = mgmt_skills.split(';')[:3]
        excel_data["管理能力标签"] = ";".join([f"{skill}-{mgmt_level}" for skill in skills_list])
    
    excel_data["业务能力标签"] = extracted_data.get("能力评估_业务能力描述", "")
    excel_data["潜力标签"] = extracted_data.get("发展潜力_潜力标签", "")
    excel_data["风险标签"] = extracted_data.get("发展潜力_风险标签", "")
    
    # 默认值设置
    excel_data["入司日期"] = ""  # 简历中通常没有
    excel_data["绩效等级"] = ""  # 简历中通常没有
    
    return excel_data

def infer_department_from_skills(tech_skills: str, position: str) -> str:
    """根据技能和职位推断部门"""
    all_text = (tech_skills + " " + position).lower()
    
    if any(keyword in all_text for keyword in ["java", "python", "架构", "开发", "技术", "系统"]):
        return "技术研发部"
    elif any(keyword in all_text for keyword in ["市场", "营销", "推广", "品牌"]):
        return "市场营销部"
    elif any(keyword in all_text for keyword in ["财务", "会计", "金融"]):
        return "财务部"
    elif any(keyword in all_text for keyword in ["产品", "需求", "用户"]):
        return "产品部"
    else:
        return "综合部门"

def infer_job_level_from_position(position: str, work_years: str) -> str:
    """根据职位和工作年限推断职级"""
    try:
        years = int(work_years) if work_years.isdigit() else 0
    except:
        years = 0
    
    position_lower = position.lower()
    
    if "总监" in position or "vp" in position_lower:
        return "P8-总监级"
    elif "经理" in position or "主管" in position:
        if years >= 8:
            return "M7-高级经理"
        else:
            return "M6-经理级"
    elif "专家" in position or "架构师" in position:
        return "P7-专家级"
    elif years >= 5:
        return "P6-高级级"
    else:
        return "P5-中级"

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python enhanced_langextract_formatter.py <文本文件路径>")
        sys.exit(1)
    
    text_file = sys.argv[1]
    
    if not os.path.exists(text_file):
        print(f"文件不存在: {text_file}")
        sys.exit(1)
    
    try:
        # 使用增强版 langextract 格式化简历
        excel_data = format_resume_for_excel_format(text_file)
        
        # 保存结果
        base_name = os.path.splitext(os.path.basename(text_file))[0].replace("_extracted", "")
        output_file = f"outs/{base_name}_excel_format.json"
        
        # 确保输出目录存在
        os.makedirs("outs", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(excel_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Excel格式数据已保存到: {output_file}")
        
        # 显示结果预览
        print("\n=== Excel格式数据预览 ===")
        for key, value in excel_data.items():
            print(f"{key}: {value}")
        
    except Exception as e:
        print(f"\n✗ 处理失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()