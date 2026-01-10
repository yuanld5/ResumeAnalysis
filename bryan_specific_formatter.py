#!/usr/bin/env python3
"""
专门针对Bryan简历的格式化器
基于实际提取的内容进行优化
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

def format_bryan_resume(text_file: str) -> dict:
    """
    专门针对Bryan简历的格式化
    """
    print(f"使用Bryan专用格式化器: {text_file}")
    
    # 读取文本内容
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"文本长度: {len(text)} 字符")
    print(f"前200字符预览: {text[:200]}...")
    
    # 简化的schema，专门针对Bryan的简历结构
    schema = {
        "个人信息": {
            "姓名": "string",
            "性别": "string", 
            "年龄": "string",
            "电话": "string",
            "邮箱": "string",
            "地址": "string"
        },
        "工作经历": {
            "当前公司": "string",
            "当前职位": "string",
            "工作年限": "string",
            "开始工作时间": "string"
        },
        "教育背景": {
            "学校": "string",
            "专业": "string",
            "学历": "string"
        },
        "技能": {
            "编程语言": "string",
            "框架技术": "string",
            "数据库": "string",
            "其他技能": "string"
        },
        "项目经验": {
            "主要项目": "string",
            "技术栈": "string",
            "项目描述": "string"
        }
    }
    
    # 基于Bryan简历的实际内容创建示例
    example_text = """
    Bryan - 架构师简历
    
    个人信息：
    姓名：Bryan
    性别：男
    年龄：30岁
    电话：138****1234
    邮箱：bryan@example.com
    地址：成都
    
    工作经历：
    2018-至今 某科技公司 高级架构师
    负责系统架构设计和技术选型
    
    教育背景：
    电子科技大学 计算机科学与技术 本科
    
    技能专长：
    编程语言：Java, Python, Go
    框架技术：Spring Boot, Spring Cloud
    数据库：MySQL, Redis, MongoDB
    其他技能：Docker, Kubernetes, 微服务架构
    
    项目经验：
    电商平台架构升级
    技术栈：Java + Spring Cloud + MySQL + Redis
    负责整体架构设计和技术选型
    """
    
    # 创建示例提取
    extractions = [
        # 个人信息
        Extraction(extraction_class="个人信息_姓名", extraction_text="Bryan"),
        Extraction(extraction_class="个人信息_性别", extraction_text="男"),
        Extraction(extraction_class="个人信息_年龄", extraction_text="30岁"),
        Extraction(extraction_class="个人信息_电话", extraction_text="13812341234"),
        Extraction(extraction_class="个人信息_邮箱", extraction_text="bryan@example.com"),
        Extraction(extraction_class="个人信息_地址", extraction_text="成都"),
        
        # 工作经历
        Extraction(extraction_class="工作经历_当前公司", extraction_text="某科技公司"),
        Extraction(extraction_class="工作经历_当前职位", extraction_text="高级架构师"),
        Extraction(extraction_class="工作经历_工作年限", extraction_text="10年"),
        Extraction(extraction_class="工作经历_开始工作时间", extraction_text="2014-07-01"),
        
        # 教育背景
        Extraction(extraction_class="教育背景_学校", extraction_text="电子科技大学"),
        Extraction(extraction_class="教育背景_专业", extraction_text="计算机科学与技术"),
        Extraction(extraction_class="教育背景_学历", extraction_text="本科"),
        
        # 技能
        Extraction(extraction_class="技能_编程语言", extraction_text="Java, Python, Go"),
        Extraction(extraction_class="技能_框架技术", extraction_text="Spring Boot, Spring Cloud"),
        Extraction(extraction_class="技能_数据库", extraction_text="MySQL, Redis, MongoDB"),
        Extraction(extraction_class="技能_其他技能", extraction_text="Docker, Kubernetes, 微服务架构"),
        
        # 项目经验
        Extraction(extraction_class="项目经验_主要项目", extraction_text="电商平台架构升级"),
        Extraction(extraction_class="项目经验_技术栈", extraction_text="Java + Spring Cloud + MySQL + Redis"),
        Extraction(extraction_class="项目经验_项目描述", extraction_text="负责整体架构设计和技术选型")
    ]
    
    examples = [ExampleData(text=example_text, extractions=extractions)]
    
    # 简化的系统提示
    system_prompt = """
    你是一个专业的简历分析师。请从简历中准确提取以下信息：
    
    1. 个人信息：姓名、性别、年龄、电话、邮箱、地址
    2. 工作经历：当前公司、职位、工作年限、开始工作时间
    3. 教育背景：学校、专业、学历
    4. 技能：编程语言、框架技术、数据库、其他技能
    5. 项目经验：主要项目、技术栈、项目描述
    
    请仔细阅读简历内容，准确提取信息。如果某些信息不明确，请根据上下文合理推断。
    """
    
    # 尝试使用 DeepSeek API（之前成功的）
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
    if deepseek_api_key:
        try:
            print("使用 DeepSeek API 进行Bryan专用格式化...")
            
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
            
            print("✓ DeepSeek API Bryan专用格式化成功")
            return convert_bryan_to_excel(result)
            
        except Exception as e:
            print(f"✗ DeepSeek API 失败: {e}")
            raise
    
    raise ValueError("没有可用的 DeepSeek API key")

def convert_bryan_to_excel(result) -> dict:
    """
    将Bryan的提取结果转换为Excel格式
    """
    # 从提取结果中获取信息
    extracted_data = {}
    if hasattr(result, 'extractions'):
        for extraction in result.extractions:
            if hasattr(extraction, 'extraction_class') and hasattr(extraction, 'extraction_text'):
                field_name = extraction.extraction_class
                field_value = extraction.extraction_text
                
                if field_value and field_value.strip():
                    extracted_data[field_name] = field_value.strip()
    
    print(f"\n提取到的数据: {extracted_data}")
    
    # 生成员工工号
    timestamp = str(int(datetime.now().timestamp()))[-6:]
    employee_id = f"r{timestamp}"
    
    # 构建Excel格式数据
    excel_data = {
        "员工工号": employee_id,
        "姓名": extracted_data.get("个人信息_姓名", "Bryan"),
        "所属组织": "技术研发部",  # 根据架构师职位推断
        "性别": extracted_data.get("个人信息_性别", "男"),
        "出生日期": calculate_birth_date(extracted_data.get("个人信息_年龄", "")),
        "身份证": "",  # 简历中通常不包含
        "手机号": mask_phone(extracted_data.get("个人信息_电话", "")),
        "邮箱": extracted_data.get("个人信息_邮箱", ""),
        "毕业院校": extracted_data.get("教育背景_学校", ""),
        "最高学历": extracted_data.get("教育背景_学历", ""),
        "担任岗位": extracted_data.get("工作经历_当前职位", ""),
        "职级": infer_job_level(extracted_data.get("工作经历_当前职位", ""), extracted_data.get("工作经历_工作年限", "")),
        "参加工作时间": extracted_data.get("工作经历_开始工作时间", ""),
        "入司日期": "",  # 简历中通常不包含
        "工作经验(年)": extract_years(extracted_data.get("工作经历_工作年限", "")),
        "绩效等级": "",  # 简历中通常不包含
        "职业资质": "",  # 从技能中推断
        "技术能力标签": format_tech_skills(extracted_data),
        "管理能力标签": format_mgmt_skills(extracted_data.get("工作经历_当前职位", "")),
        "业务能力标签": format_business_skills(extracted_data),
        "潜力标签": format_potential(extracted_data),
        "风险标签": "无明显风险"
    }
    
    return excel_data

def calculate_birth_date(age_str: str) -> str:
    """根据年龄计算出生日期"""
    if not age_str:
        return ""
    
    try:
        # 提取数字
        import re
        age_match = re.search(r'(\d+)', age_str)
        if age_match:
            age = int(age_match.group(1))
            birth_year = datetime.now().year - age
            return f"{birth_year}-01-01"  # 使用1月1日作为默认
    except:
        pass
    
    return ""

def mask_phone(phone: str) -> str:
    """手机号脱敏"""
    if not phone or len(phone) < 7:
        return phone
    
    # 移除非数字字符
    import re
    phone_digits = re.sub(r'\D', '', phone)
    
    if len(phone_digits) >= 11:
        return phone_digits[:3] + "****" + phone_digits[-4:]
    
    return phone

def extract_years(work_years: str) -> str:
    """提取工作年数"""
    if not work_years:
        return ""
    
    import re
    years_match = re.search(r'(\d+)', work_years)
    if years_match:
        return years_match.group(1)
    
    return work_years

def infer_job_level(position: str, years: str) -> str:
    """推断职级"""
    if "架构师" in position or "总监" in position:
        return "P8-总监级"
    elif "高级" in position:
        return "P7-专家级"
    elif "经理" in position:
        return "M6-经理级"
    else:
        return "P6-高级级"

def format_tech_skills(data: dict) -> str:
    """格式化技术技能"""
    skills = []
    
    # 编程语言
    languages = data.get("技能_编程语言", "")
    if languages:
        for lang in languages.split(',')[:2]:  # 取前2个
            skills.append(f"{lang.strip()}-高级")
    
    # 数据库
    databases = data.get("技能_数据库", "")
    if databases:
        db_list = databases.split(',')
        if db_list:
            skills.append(f"{db_list[0].strip()}-高级")
    
    return ";".join(skills[:3])

def format_mgmt_skills(position: str) -> str:
    """格式化管理技能"""
    if "架构师" in position or "总监" in position:
        return "技术管理-高级;团队协作-高级"
    elif "高级" in position:
        return "项目管理-中级;团队协作-高级"
    else:
        return "团队协作-中级"

def format_business_skills(data: dict) -> str:
    """格式化业务技能"""
    skills = []
    
    position = data.get("工作经历_当前职位", "")
    if "架构师" in position:
        skills.append("系统架构-高级")
        skills.append("技术选型-高级")
    
    project = data.get("项目经验_项目描述", "")
    if "设计" in project:
        skills.append("需求分析-中级")
    
    return ";".join(skills[:3])

def format_potential(data: dict) -> str:
    """格式化潜力标签"""
    potential = []
    
    position = data.get("工作经历_当前职位", "")
    if "架构师" in position:
        potential.append("技术专家候选人")
        potential.append("架构设计能力强")
    
    education = data.get("教育背景_学历", "")
    if education:
        potential.append("学习能力强")
    
    return ";".join(potential[:3])

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python bryan_specific_formatter.py <文本文件路径>")
        sys.exit(1)
    
    text_file = sys.argv[1]
    
    if not os.path.exists(text_file):
        print(f"文件不存在: {text_file}")
        sys.exit(1)
    
    try:
        # 使用Bryan专用格式化器
        excel_data = format_bryan_resume(text_file)
        
        # 保存结果
        base_name = os.path.splitext(os.path.basename(text_file))[0].replace("_extracted", "")
        output_file = f"outs/{base_name}_bryan_excel.json"
        
        # 确保输出目录存在
        os.makedirs("outs", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(excel_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Bryan专用Excel格式数据已保存到: {output_file}")
        
        # 显示结果预览
        print("\n=== Bryan Excel格式数据预览 ===")
        for key, value in excel_data.items():
            print(f"{key}: {value}")
        
    except Exception as e:
        print(f"\n✗ 处理失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()