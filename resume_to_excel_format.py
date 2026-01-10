#!/usr/bin/env python3
"""
使用unstructured和langextract分析简历，输出格式与演示数据-1022.xlsx中的演示数据sheet一致
"""

import os
import json
import pandas as pd
from datetime import datetime
import sys

# 直接导入现有的模块
sys.path.append('.')
try:
    from unstructured_extractor import extract_pdf_with_unstructured
    from enhanced_langextract_formatter import format_resume_for_excel_format
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保unstructured_extractor.py和enhanced_langextract_formatter.py文件存在")

def run_unstructured_extraction(pdf_file):
    """使用unstructured提取PDF内容"""
    print(f"正在使用unstructured提取PDF内容: {pdf_file}")
    
    # 直接调用函数
    try:
        output_file = extract_pdf_with_unstructured(pdf_file)
        if output_file and os.path.exists(output_file):
            print(f"unstructured提取完成，输出文件: {output_file}")
            return output_file
        else:
            print("unstructured提取失败：输出文件不存在")
            return None
        
    except Exception as e:
        print(f"unstructured提取失败: {e}")
        return None

def run_langextract_formatting(text_file):
    """使用增强版langextract格式化简历数据"""
    print(f"正在使用增强版langextract格式化简历数据: {text_file}")
    
    # 直接调用增强版函数，返回Excel格式数据
    try:
        result = format_resume_for_excel_format(text_file)
        if result:
            print(f"增强版langextract格式化完成")
            return result
        else:
            print("增强版langextract格式化失败：结果为空")
            return None
        
    except Exception as e:
        print(f"增强版langextract格式化失败: {e}")
        return None

def convert_to_excel_format(json_file):
    """将langextract的输出转换为Excel演示数据格式"""
    print(f"正在转换为Excel格式: {json_file}")
    
    # 读取JSON数据
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取JSON文件失败: {e}")
        return None
    
    # 创建Excel格式的数据结构
    excel_data = {
        "员工工号": generate_employee_id(data.get("个人信息", {}).get("姓名", "")),
        "姓名": data.get("个人信息", {}).get("姓名", ""),
        "所属组织": infer_department(data),
        "性别": data.get("个人信息", {}).get("性别", ""),
        "出生日期": format_birth_date(data.get("个人信息", {}).get("年龄", "")),
        "身份证": data.get("个人信息", {}).get("身份证", ""),
        "手机号": mask_phone(data.get("个人信息", {}).get("电话", "")),
        "邮箱": data.get("个人信息", {}).get("邮箱", ""),
        "毕业院校": get_latest_school(data.get("教育背景", [])),
        "最高学历": get_highest_education(data.get("教育背景", [])),
        "担任岗位": infer_position(data),
        "职级": infer_job_level(data),
        "参加工作时间": get_work_start_date(data.get("工作经历", [])),
        "入司日期": "",  # 简历中通常没有入司日期
        "工作经验(年)": calculate_work_years(data),
        "绩效等级": "",  # 简历中通常没有绩效信息
        "职业资质": format_certifications(data.get("技能专长", {})),
        "技术能力标签": format_technical_skills(data.get("技能专长", {})),
        "管理能力标签": format_management_skills(data),
        "业务能力标签": format_business_skills(data),
        "潜力标签": format_potential_tags(data),
        "风险标签": format_risk_tags(data)
    }
    
    return excel_data

def generate_employee_id(name):
    """生成员工工号"""
    if not name:
        return ""
    # 使用时间戳生成唯一ID
    timestamp = str(int(datetime.now().timestamp()))[-6:]
    return f"r{timestamp}"

def infer_department(data):
    """根据简历内容推断所属组织"""
    # 根据技能和工作经历推断部门
    skills = data.get("技能专长", {})
    work_exp = data.get("工作经历", [])
    job_intention = data.get("求职信息", {}).get("求职意向", "")
    
    # 合并所有相关文本
    all_text = " ".join([
        job_intention,
        skills.get("编程语言", ""),
        skills.get("框架技术", ""),
        skills.get("数据库技术", ""),
        skills.get("容器技术", ""),
        skills.get("其他技能", "")
    ] + [exp.get("职位", "") + " " + exp.get("工作描述", "") for exp in work_exp]).lower()
    
    tech_keywords = ["java", "python", "go", "架构", "开发", "技术", "系统", "软件", "后端", "前端"]
    marketing_keywords = ["市场", "营销", "推广", "品牌", "客户", "销售"]
    finance_keywords = ["财务", "会计", "金融", "投资", "成本"]
    product_keywords = ["产品", "需求", "用户", "设计", "产品经理"]
    
    if any(keyword in all_text for keyword in tech_keywords):
        return "技术研发部"
    elif any(keyword in all_text for keyword in marketing_keywords):
        return "市场营销部"
    elif any(keyword in all_text for keyword in finance_keywords):
        return "财务部"
    elif any(keyword in all_text for keyword in product_keywords):
        return "产品部"
    else:
        return "技术研发部"  # 默认为技术部门

def format_birth_date(age_str):
    """根据年龄推算出生日期"""
    if not age_str:
        return ""
    
    try:
        # 提取年龄数字
        import re
        age_match = re.search(r'(\d+)', age_str)
        if age_match:
            age = int(age_match.group(1))
            current_year = datetime.now().year
            birth_year = current_year - age
            # 假设生日在年中
            return f"{birth_year}-06-15"
    except:
        pass
    return ""

def mask_phone(phone):
    """手机号脱敏处理"""
    if not phone or len(phone) < 7:
        return phone
    return phone[:3] + "****" + phone[-4:]

def get_latest_school(education_list):
    """获取最新的毕业院校"""
    if not education_list:
        return ""
    
    # 按时间排序，取最新的
    latest_edu = education_list[0] if education_list else {}
    return latest_edu.get("学校", "")

def get_highest_education(education_list):
    """获取最高学历"""
    if not education_list:
        return ""
    
    education_levels = {
        "博士": 5, "硕士": 4, "本科": 3, "学士": 3,
        "专科": 2, "大专": 2, "高中": 1, "中专": 1
    }
    
    highest_level = 0
    highest_edu = ""
    
    for edu in education_list:
        degree = edu.get("学历", "")
        for level_name, level_value in education_levels.items():
            if level_name in degree and level_value > highest_level:
                highest_level = level_value
                highest_edu = level_name
    
    return highest_edu

def infer_position(data):
    """推断担任岗位"""
    work_exp = data.get("工作经历", [])
    job_intention = data.get("求职信息", {}).get("求职意向", "")
    
    if job_intention:
        return job_intention
    
    if work_exp:
        # 取最新的工作经历中的职位
        latest_job = work_exp[0]
        return latest_job.get("职位", "")
    
    return ""

def infer_job_level(data):
    """推断职级"""
    position = infer_position(data)
    work_years = calculate_work_years(data)
    
    # 根据职位和工作年限推断职级
    position_lower = position.lower()
    
    if any(keyword in position_lower for keyword in ["总监", "vp", "架构师", "技术专家"]):
        return "P8-总监级"
    elif any(keyword in position_lower for keyword in ["经理", "主管", "负责人", "leader"]):
        if work_years >= 8:
            return "M7-高级经理"
        else:
            return "M6-经理级"
    elif any(keyword in position_lower for keyword in ["专家", "资深", "高级"]):
        return "P7-专家级"
    elif work_years >= 5:
        return "P6-高级级"
    else:
        return "P5-中级"

def get_work_start_date(work_exp_list):
    """获取参加工作时间"""
    if not work_exp_list:
        return ""
    
    # 找到最早的工作开始时间
    earliest_date = None
    for exp in work_exp_list:
        start_date = exp.get("开始时间", "")
        if start_date:
            try:
                from dateutil import parser
                parsed_date = parser.parse(start_date)
                if earliest_date is None or parsed_date < earliest_date:
                    earliest_date = parsed_date
            except:
                continue
    
    return earliest_date.strftime("%Y-%m-%d") if earliest_date else ""

def calculate_work_years(data):
    """计算工作经验年数"""
    # 优先使用求职信息中的工作时长
    work_duration = data.get("求职信息", {}).get("工作时长", "")
    if work_duration:
        import re
        years_match = re.search(r'(\d+)', work_duration)
        if years_match:
            return int(years_match.group(1))
    
    # 如果没有，则根据工作经历计算
    work_exp_list = data.get("工作经历", [])
    if not work_exp_list:
        return 0
    
    total_months = 0
    for exp in work_exp_list:
        work_time = exp.get("工作时间", "")
        
        if work_time:
            try:
                from dateutil import parser
                # 解析时间范围，如 "2022.07-2024.08"
                if "-" in work_time:
                    start_str, end_str = work_time.split("-", 1)
                    start_str = start_str.strip()
                    end_str = end_str.strip()
                    
                    # 处理"至今"的情况
                    if "至今" in end_str:
                        end_str = datetime.now().strftime("%Y.%m")
                    
                    start = parser.parse(start_str.replace(".", "-"))
                    end = parser.parse(end_str.replace(".", "-"))
                    
                    months = (end.year - start.year) * 12 + (end.month - start.month)
                    total_months += max(0, months)
            except:
                continue
    
    return round(total_months / 12, 1) if total_months > 0 else 0

def format_certifications(skills_dict):
    """格式化职业资质"""
    if not skills_dict:
        return ""
    
    # 从技能专长中提取可能的认证信息
    cert_keywords = ["认证", "证书", "资格", "PMP", "AWS", "TOGAF", "CPA", "CMA"]
    
    all_skills = " ".join([
        skills_dict.get("编程语言", ""),
        skills_dict.get("框架技术", ""),
        skills_dict.get("数据库技术", ""),
        skills_dict.get("容器技术", ""),
        skills_dict.get("其他技能", "")
    ])
    
    certs = []
    for keyword in cert_keywords:
        if keyword in all_skills:
            certs.append(keyword)
    
    return ";".join(certs[:3]) if certs else ""

def format_technical_skills(skills_dict):
    """格式化技术能力标签"""
    if not skills_dict:
        return ""
    
    tech_skills = []
    
    # 编程语言技能
    programming = skills_dict.get("编程语言", "")
    if programming:
        if any(keyword in programming.lower() for keyword in ["精通", "专家", "资深"]):
            tech_skills.append(f"编程语言-专家级")
        else:
            tech_skills.append(f"编程语言-高级")
    
    # 框架技术
    framework = skills_dict.get("框架技术", "")
    if framework:
        tech_skills.append(f"框架技术-高级")
    
    # 数据库技术
    database = skills_dict.get("数据库技术", "")
    if database:
        tech_skills.append(f"数据库技术-高级")
    
    # 容器技术
    container = skills_dict.get("容器技术", "")
    if container:
        tech_skills.append(f"容器技术-高级")
    
    return ";".join(tech_skills[:3])  # 最多显示3个技能

def format_management_skills(data):
    """格式化管理能力标签"""
    work_exp = data.get("工作经历", [])
    position = infer_position(data)
    
    management_skills = []
    
    # 根据职位判断管理能力
    if any(keyword in position for keyword in ["经理", "主管", "总监", "负责人"]):
        management_skills.append("团队管理-高级")
        management_skills.append("项目管理-高级")
    
    # 根据工作内容判断
    for exp in work_exp:
        content = exp.get("工作内容", "").lower()
        if any(keyword in content for keyword in ["管理", "领导", "带领"]):
            if "跨部门协作-高级" not in management_skills:
                management_skills.append("跨部门协作-高级")
            break
    
    return ";".join(management_skills[:3])

def format_business_skills(data):
    """格式化业务能力标签"""
    work_exp = data.get("工作经历", [])
    skills = data.get("技能", [])
    
    business_skills = []
    
    # 根据工作经历和技能判断业务能力
    all_text = " ".join([exp.get("工作内容", "") for exp in work_exp] + skills).lower()
    
    if any(keyword in all_text for keyword in ["需求分析", "业务分析"]):
        business_skills.append("需求分析-高级")
    
    if any(keyword in all_text for keyword in ["客户", "用户"]):
        business_skills.append("客户沟通-高级")
    
    if any(keyword in all_text for keyword in ["创新", "优化", "改进"]):
        business_skills.append("业务优化-高级")
    
    return ";".join(business_skills[:3])

def format_potential_tags(data):
    """格式化潜力标签"""
    work_years = calculate_work_years(data)
    education = get_highest_education(data.get("教育背景", []))
    position = infer_position(data)
    
    potential_tags = []
    
    # 根据工作年限和职位判断潜力
    if work_years >= 8 and any(keyword in position for keyword in ["经理", "主管"]):
        potential_tags.append("管理潜力强")
    
    if education in ["硕士", "博士"]:
        potential_tags.append("学习能力强")
    
    if any(keyword in position for keyword in ["技术", "架构", "开发"]):
        potential_tags.append("技术发展潜力")
    
    return ";".join(potential_tags[:3])

def format_risk_tags(data):
    """格式化风险标签"""
    work_exp = data.get("工作经历", [])
    
    risk_tags = []
    
    # 分析工作稳定性
    if len(work_exp) > 5:
        risk_tags.append("工作稳定性待观察")
    
    # 分析技能匹配度
    skills = data.get("技能", [])
    if len(skills) < 3:
        risk_tags.append("技能广度有限")
    
    # 如果没有明显风险，返回无风险
    if not risk_tags:
        return "无明显风险"
    
    return ";".join(risk_tags[:2])

def save_to_excel(excel_data, output_file):
    """保存为Excel格式"""
    # 创建DataFrame
    df = pd.DataFrame([excel_data])
    
    # 保存为Excel文件
    df.to_excel(output_file, index=False, sheet_name="简历分析结果")
    print(f"Excel文件已保存: {output_file}")

def main():
    if len(sys.argv) != 2:
        print("使用方法: python resume_to_excel_format.py <PDF文件路径>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    if not os.path.exists(pdf_file):
        print(f"文件不存在: {pdf_file}")
        sys.exit(1)
    
    print(f"开始处理简历文件: {pdf_file}")
    
    # 步骤1: 使用unstructured提取内容
    text_file = run_unstructured_extraction(pdf_file)
    if not text_file:
        print("unstructured提取失败")
        sys.exit(1)
    
    # 步骤2: 使用增强版langextract格式化
    excel_data = run_langextract_formatting(text_file)
    if not excel_data:
        print("增强版langextract格式化失败")
        sys.exit(1)
    
    # 步骤3: 保存为Excel文件
    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    output_file = f"outs/{base_name}_excel_format.xlsx"
    save_to_excel(excel_data, output_file)
    
    # 打印结果预览
    print("\n=== 分析结果预览 ===")
    for key, value in excel_data.items():
        print(f"{key}: {value}")
    
    print(f"\n处理完成！输出文件: {output_file}")

if __name__ == "__main__":
    main()