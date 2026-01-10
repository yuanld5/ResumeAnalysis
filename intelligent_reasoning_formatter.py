#!/usr/bin/env python3
"""
智能推理简历格式化器
基于演示数据的复杂推理标签系统，实现智能分析和标签生成
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import langextract as lx
from langextract.providers.openai import OpenAILanguageModel
from langextract.data import ExampleData, Extraction

# 加载环境变量
load_dotenv()

class IntelligentReasoningFormatter:
    """智能推理格式化器"""
    
    def __init__(self):
        self.tech_keywords = {
            'architecture': ['架构', '系统设计', '微服务', '分布式', '高并发', '性能优化'],
            'programming': ['Java', 'Python', 'Go', 'C++', 'JavaScript', 'Scala'],
            'database': ['MySQL', 'Redis', 'MongoDB', 'PostgreSQL', 'Oracle'],
            'cloud': ['AWS', 'Azure', 'Docker', 'Kubernetes', 'DevOps'],
            'ai_ml': ['机器学习', '深度学习', 'AI', '算法', '数据挖掘'],
            'frontend': ['React', 'Vue', 'Angular', 'HTML', 'CSS'],
            'backend': ['Spring', 'Django', 'Flask', 'Node.js']
        }
        
        self.management_indicators = {
            'leadership': ['团队', '管理', '领导', '带领', '负责', '主导'],
            'project_mgmt': ['项目', '规划', '协调', '推进', '交付'],
            'strategic': ['战略', '规划', '决策', '方向', '目标'],
            'cross_dept': ['跨部门', '协作', '沟通', '合作']
        }
        
        self.business_indicators = {
            'innovation': ['创新', '优化', '改进', '提升', '突破'],
            'cost_control': ['成本', '预算', '效率', '节约'],
            'user_focus': ['用户', '客户', '体验', '需求'],
            'market': ['市场', '商业', '业务', '产品']
        }

    def format_resume_with_reasoning(self, text_file: str) -> dict:
        """
        使用智能推理格式化简历
        """
        print(f"使用智能推理格式化器: {text_file}")
        
        # 读取文本内容
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        print(f"文本长度: {len(text)} 字符")
        
        # 首先进行基础信息提取
        basic_info = self._extract_basic_info(text)
        
        # 然后进行智能推理分析
        reasoning_analysis = self._perform_reasoning_analysis(text, basic_info)
        
        # 合并结果
        final_result = {**basic_info, **reasoning_analysis}
        
        return final_result

    def _extract_basic_info(self, text: str) -> dict:
        """提取基础信息"""
        
        # 基础信息提取的schema
        schema = {
            "个人信息": {
                "姓名": "string",
                "性别": "string",
                "年龄": "string",
                "电话": "string",
                "邮箱": "string",
                "地址": "string"
            },
            "教育背景": {
                "学校": "string",
                "专业": "string", 
                "学历": "string"
            },
            "工作经历": {
                "当前职位": "string",
                "工作年限": "string",
                "公司经历": "string",
                "主要职责": "string"
            },
            "技能专长": {
                "技术技能": "string",
                "工具框架": "string",
                "项目经验": "string"
            }
        }
        
        # 创建基础提取示例
        example_text = """
        任街平 - 高级Python开发工程师
        
        个人信息：
        性别：男
        年龄：30岁
        电话：19178927892
        邮箱：r414164729@163.com
        
        教育背景：
        某大学 计算机科学 本科
        
        工作经历：
        2018-至今 某科技公司 高级Python开发工程师
        负责后端系统开发，微服务架构设计
        参与多个大型项目的技术选型和架构设计
        
        技能专长：
        编程语言：Python, Go, Java
        数据库：MySQL, Redis, MongoDB
        框架：Django, Flask, Spring Boot
        工具：Docker, Git, Jenkins
        """
        
        extractions = [
            Extraction(extraction_class="个人信息_姓名", extraction_text="任街平"),
            Extraction(extraction_class="个人信息_性别", extraction_text="男"),
            Extraction(extraction_class="个人信息_年龄", extraction_text="30岁"),
            Extraction(extraction_class="个人信息_电话", extraction_text="19178927892"),
            Extraction(extraction_class="个人信息_邮箱", extraction_text="r414164729@163.com"),
            Extraction(extraction_class="教育背景_学校", extraction_text="某大学"),
            Extraction(extraction_class="教育背景_专业", extraction_text="计算机科学"),
            Extraction(extraction_class="教育背景_学历", extraction_text="本科"),
            Extraction(extraction_class="工作经历_当前职位", extraction_text="高级Python开发工程师"),
            Extraction(extraction_class="工作经历_工作年限", extraction_text="6年"),
            Extraction(extraction_class="工作经历_主要职责", extraction_text="后端系统开发，微服务架构设计，技术选型"),
            Extraction(extraction_class="技能专长_技术技能", extraction_text="Python, Go, Java"),
            Extraction(extraction_class="技能专长_工具框架", extraction_text="Django, Flask, Spring Boot, Docker")
        ]
        
        examples = [ExampleData(text=example_text, extractions=extractions)]
        
        system_prompt = """
        你是专业的简历分析师，请准确提取简历中的基础信息：
        1. 个人信息：姓名、性别、年龄、电话、邮箱、地址
        2. 教育背景：学校、专业、学历
        3. 工作经历：当前职位、工作年限、主要职责
        4. 技能专长：技术技能、工具框架、项目经验
        
        请仔细分析简历内容，准确提取每个字段的信息。
        """
        
        # 使用API进行基础提取
        result = self._call_api(text, schema, examples, system_prompt)
        
        # 转换为基础信息字典
        basic_info = {}
        if hasattr(result, 'extractions'):
            for extraction in result.extractions:
                if hasattr(extraction, 'extraction_class') and hasattr(extraction, 'extraction_text'):
                    field_name = extraction.extraction_class
                    field_value = extraction.extraction_text
                    if field_value and field_value.strip():
                        basic_info[field_name] = field_value.strip()
        
        return basic_info

    def _perform_reasoning_analysis(self, text: str, basic_info: dict) -> dict:
        """执行智能推理分析"""
        
        print("开始智能推理分析...")
        
        # 分析技术能力等级
        tech_analysis = self._analyze_technical_capabilities(text, basic_info)
        
        # 分析管理能力
        mgmt_analysis = self._analyze_management_capabilities(text, basic_info)
        
        # 分析业务能力
        business_analysis = self._analyze_business_capabilities(text, basic_info)
        
        # 分析发展潜力
        potential_analysis = self._analyze_potential(text, basic_info)
        
        # 分析风险因素
        risk_analysis = self._analyze_risks(text, basic_info)
        
        # 生成Excel格式数据
        excel_data = self._generate_excel_format(basic_info, tech_analysis, mgmt_analysis, 
                                                business_analysis, potential_analysis, risk_analysis)
        
        return excel_data

    def _analyze_technical_capabilities(self, text: str, basic_info: dict) -> dict:
        """分析技术能力"""
        
        tech_skills = basic_info.get("技能专长_技术技能", "")
        frameworks = basic_info.get("技能专长_工具框架", "")
        position = basic_info.get("工作经历_当前职位", "")
        responsibilities = basic_info.get("工作经历_主要职责", "")
        
        all_tech_text = f"{tech_skills} {frameworks} {position} {responsibilities}".lower()
        
        capabilities = []
        
        # 编程语言能力分析
        if any(lang.lower() in all_tech_text for lang in ['python', 'java', 'go']):
            if '高级' in position or '架构' in position:
                capabilities.append("后端开发-专家级")
            else:
                capabilities.append("后端开发-高级")
        
        # 架构设计能力
        if any(keyword in all_tech_text for keyword in ['架构', '设计', '微服务', '分布式']):
            if '架构师' in position:
                capabilities.append("架构设计-专家级")
            else:
                capabilities.append("架构设计-高级")
        
        # 数据库能力
        if any(db.lower() in all_tech_text for db in ['mysql', 'redis', 'mongodb']):
            capabilities.append("数据库设计-高级")
        
        # 技术创新能力
        if any(keyword in text for keyword in ['优化', '改进', '提升', '创新']):
            capabilities.append("技术创新-高级")
        
        # 系统优化能力
        if any(keyword in text for keyword in ['性能', '优化', '调优', '高并发']):
            capabilities.append("系统优化-高级")
        
        return {
            "技术能力标签": ";".join(capabilities[:3]) if capabilities else "编程开发-中级"
        }

    def _analyze_management_capabilities(self, text: str, basic_info: dict) -> dict:
        """分析管理能力"""
        
        position = basic_info.get("工作经历_当前职位", "")
        responsibilities = basic_info.get("工作经历_主要职责", "")
        
        all_mgmt_text = f"{position} {responsibilities}".lower()
        
        capabilities = []
        
        # 团队管理能力
        if any(keyword in all_mgmt_text for keyword in ['团队', '管理', '带领', '负责']):
            if '总监' in position or '经理' in position:
                capabilities.append("团队管理-高级")
            else:
                capabilities.append("团队协作-高级")
        
        # 项目管理能力
        if any(keyword in all_mgmt_text for keyword in ['项目', '规划', '协调', '推进']):
            if '高级' in position:
                capabilities.append("项目管理-高级")
            else:
                capabilities.append("项目管理-中级")
        
        # 跨部门协作
        if any(keyword in text for keyword in ['协作', '沟通', '合作', '配合']):
            capabilities.append("跨部门协作-高级")
        
        # 决策能力
        if any(keyword in text for keyword in ['决策', '选型', '方案', '技术选择']):
            capabilities.append("决策能力-高级")
        
        return {
            "管理能力标签": ";".join(capabilities[:3]) if capabilities else "团队协作-中级"
        }

    def _analyze_business_capabilities(self, text: str, basic_info: dict) -> dict:
        """分析业务能力"""
        
        position = basic_info.get("工作经历_当前职位", "")
        responsibilities = basic_info.get("工作经历_主要职责", "")
        
        all_business_text = f"{position} {responsibilities} {text}".lower()
        
        capabilities = []
        
        # 技术战略能力
        if '架构师' in position or '总监' in position:
            capabilities.append("技术战略-高级")
        elif '高级' in position:
            capabilities.append("技术规划-中级")
        
        # 需求分析能力
        if any(keyword in all_business_text for keyword in ['需求', '分析', '设计', '方案']):
            capabilities.append("需求分析-高级")
        
        # 成本控制
        if any(keyword in all_business_text for keyword in ['优化', '效率', '性能', '成本']):
            capabilities.append("成本控制-中级")
        
        # 产品理解
        if any(keyword in all_business_text for keyword in ['产品', '用户', '业务', '功能']):
            capabilities.append("产品理解-中级")
        
        return {
            "业务能力标签": ";".join(capabilities[:3]) if capabilities else "技术实现-中级"
        }

    def _analyze_potential(self, text: str, basic_info: dict) -> dict:
        """分析发展潜力"""
        
        position = basic_info.get("工作经历_当前职位", "")
        education = basic_info.get("教育背景_学历", "")
        school = basic_info.get("教育背景_学校", "")
        responsibilities = basic_info.get("工作经历_主要职责", "")
        
        potential_tags = []
        
        # 职业发展潜力
        if '架构师' in position:
            potential_tags.append("CTO候选人")
        elif '高级' in position:
            potential_tags.append("技术专家候选人")
        else:
            potential_tags.append("高级工程师候选人")
        
        # 技术能力潜力
        if any(keyword in text for keyword in ['架构', '设计', '优化', '创新']):
            potential_tags.append("技术领导力强")
        
        # 学习能力
        if education in ['硕士', '博士'] or any(keyword in school for keyword in ['985', '211', '清华', '北大']):
            potential_tags.append("学习能力强")
        else:
            potential_tags.append("实践能力强")
        
        # 创新能力
        if any(keyword in text for keyword in ['创新', '改进', '优化', '突破']):
            potential_tags.append("创新思维活跃")
        
        # 责任心
        if any(keyword in responsibilities for keyword in ['负责', '主导', '承担', '完成']):
            potential_tags.append("责任心强")
        
        return {
            "潜力标签": ";".join(potential_tags[:3])
        }

    def _analyze_risks(self, text: str, basic_info: dict) -> dict:
        """分析风险因素"""
        
        position = basic_info.get("工作经历_当前职位", "")
        work_years = basic_info.get("工作经历_工作年限", "")
        education = basic_info.get("教育背景_学历", "")
        
        risk_tags = []
        
        # 管理经验风险
        if '高级' in position and not any(keyword in text for keyword in ['管理', '团队', '带领']):
            risk_tags.append("管理经验不足")
        
        # 技术深度风险
        tech_skills = basic_info.get("技能专长_技术技能", "")
        if len(tech_skills.split(',')) < 3:
            risk_tags.append("技术广度待提升")
        
        # 创新能力风险
        if not any(keyword in text for keyword in ['创新', '改进', '优化', '新技术']):
            risk_tags.append("创新意识一般")
        
        # 沟通协作风险
        if not any(keyword in text for keyword in ['协作', '沟通', '合作', '团队']):
            risk_tags.append("协作能力待观察")
        
        # 如果没有明显风险
        if not risk_tags:
            risk_tags.append("无明显风险")
        
        return {
            "风险标签": ";".join(risk_tags[:2])
        }

    def _generate_excel_format(self, basic_info: dict, tech_analysis: dict, 
                             mgmt_analysis: dict, business_analysis: dict, 
                             potential_analysis: dict, risk_analysis: dict) -> dict:
        """生成Excel格式数据"""
        
        # 生成员工工号
        timestamp = str(int(datetime.now().timestamp()))[-6:]
        employee_id = f"r{timestamp}"
        
        # 处理出生日期
        age_str = basic_info.get("个人信息_年龄", "")
        birth_date = self._calculate_birth_date(age_str)
        
        # 处理手机号脱敏
        phone = basic_info.get("个人信息_电话", "")
        masked_phone = self._mask_phone(phone)
        
        # 推断工作年限
        work_years = self._extract_work_years(basic_info.get("工作经历_工作年限", ""))
        
        # 推断职级
        job_level = self._infer_job_level(basic_info.get("工作经历_当前职位", ""), work_years)
        
        excel_data = {
            "员工工号": employee_id,
            "姓名": basic_info.get("个人信息_姓名", ""),
            "所属组织": "技术研发部",  # 基于技术职位推断
            "性别": basic_info.get("个人信息_性别", ""),
            "出生日期": birth_date,
            "身份证": "",  # 简历中通常不包含
            "手机号": masked_phone,
            "邮箱": basic_info.get("个人信息_邮箱", ""),
            "毕业院校": basic_info.get("教育背景_学校", ""),
            "最高学历": basic_info.get("教育背景_学历", ""),
            "担任岗位": basic_info.get("工作经历_当前职位", ""),
            "职级": job_level,
            "参加工作时间": self._estimate_work_start_date(work_years),
            "入司日期": "",  # 简历中通常不包含
            "工作经验(年)": work_years,
            "绩效等级": "",  # 简历中通常不包含
            "职业资质": "",  # 从简历中提取的资质认证
            "技术能力标签": tech_analysis.get("技术能力标签", ""),
            "管理能力标签": mgmt_analysis.get("管理能力标签", ""),
            "业务能力标签": business_analysis.get("业务能力标签", ""),
            "潜力标签": potential_analysis.get("潜力标签", ""),
            "风险标签": risk_analysis.get("风险标签", "")
        }
        
        return excel_data

    def _calculate_birth_date(self, age_str: str) -> str:
        """根据年龄计算出生日期"""
        if not age_str:
            return ""
        
        try:
            age_match = re.search(r'(\d+)', age_str)
            if age_match:
                age = int(age_match.group(1))
                birth_year = datetime.now().year - age
                return f"{birth_year}-01-01"
        except:
            pass
        
        return ""

    def _mask_phone(self, phone: str) -> str:
        """手机号脱敏"""
        if not phone or len(phone) < 7:
            return phone
        
        phone_digits = re.sub(r'\D', '', phone)
        
        if len(phone_digits) >= 11:
            return phone_digits[:3] + "****" + phone_digits[-4:]
        
        return phone

    def _extract_work_years(self, work_years_str: str) -> str:
        """提取工作年数"""
        if not work_years_str:
            return "5"  # 默认值
        
        years_match = re.search(r'(\d+)', work_years_str)
        if years_match:
            return years_match.group(1)
        
        return "5"

    def _infer_job_level(self, position: str, years: str) -> str:
        """推断职级"""
        try:
            years_int = int(years) if years.isdigit() else 5
        except:
            years_int = 5
        
        if "总监" in position or "VP" in position:
            return "P8-总监级"
        elif "架构师" in position:
            return "P7-专家级"
        elif "高级" in position:
            return "P6-高级级"
        elif "经理" in position:
            return "M6-经理级"
        else:
            return "P5-中级"

    def _estimate_work_start_date(self, years: str) -> str:
        """估算参加工作时间"""
        try:
            years_int = int(years) if years.isdigit() else 5
            start_year = datetime.now().year - years_int
            return f"{start_year}-07-01"
        except:
            return "2019-07-01"

    def _call_api(self, text: str, schema: dict, examples: list, system_prompt: str):
        """调用API进行提取"""
        
        # 尝试使用 DeepSeek API
        deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        if deepseek_api_key:
            try:
                print("使用 DeepSeek API 进行智能推理...")
                
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
                
                print("✓ DeepSeek API 智能推理成功")
                return result
                
            except Exception as e:
                print(f"✗ DeepSeek API 失败: {e}")
                raise
        
        raise ValueError("没有可用的 DeepSeek API key")


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python intelligent_reasoning_formatter.py <文本文件路径>")
        sys.exit(1)
    
    text_file = sys.argv[1]
    
    if not os.path.exists(text_file):
        print(f"文件不存在: {text_file}")
        sys.exit(1)
    
    try:
        # 创建智能推理格式化器
        formatter = IntelligentReasoningFormatter()
        
        # 执行智能推理格式化
        excel_data = formatter.format_resume_with_reasoning(text_file)
        
        # 保存结果
        base_name = os.path.splitext(os.path.basename(text_file))[0].replace("_extracted", "")
        output_file = f"outs/{base_name}_intelligent_analysis.json"
        
        # 确保输出目录存在
        os.makedirs("outs", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(excel_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 智能推理分析结果已保存到: {output_file}")
        
        # 显示结果预览
        print("\n=== 智能推理分析结果预览 ===")
        for key, value in excel_data.items():
            print(f"{key}: {value}")
        
        # 显示推理过程总结
        print("\n=== 推理分析总结 ===")
        print(f"技术能力分析: {excel_data.get('技术能力标签', '')}")
        print(f"管理能力分析: {excel_data.get('管理能力标签', '')}")
        print(f"业务能力分析: {excel_data.get('业务能力标签', '')}")
        print(f"发展潜力分析: {excel_data.get('潜力标签', '')}")
        print(f"风险因素分析: {excel_data.get('风险标签', '')}")
        
    except Exception as e:
        print(f"\n✗ 智能推理处理失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()