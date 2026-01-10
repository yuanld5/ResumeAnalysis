#!/usr/bin/env python3
"""
最终版本简历分析一键脚本
完整的PDF到智能推理分析流程
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None, env_vars=None):
    """执行命令并返回结果"""
    try:
        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)
        
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            env=env,
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ 命令执行失败: {command}")
            print(f"错误输出: {result.stderr}")
            return False
        
        print(result.stdout)
        return True
        
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python run_final_analysis.py \"files/简历文件.pdf\"")
        print("示例: python run_final_analysis.py \"files/【架构部总监_成都 30-40K】Bryan 10年.pdf\"")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(pdf_file):
        print(f"❌ 错误: 文件不存在 - {pdf_file}")
        sys.exit(1)
    
    print(f"🚀 开始处理简历: {pdf_file}")
    print("=" * 50)
    
    # 第1步：PDF提取（使用venv39环境）
    print("📄 第1步: 使用unstructured提取PDF内容...")
    
    # 构建venv39的Python路径
    venv39_python = "venv39/bin/python"
    if not os.path.exists(venv39_python):
        print(f"❌ 错误: venv39环境不存在 - {venv39_python}")
        sys.exit(1)
    
    # 执行PDF提取
    extract_command = f"{venv39_python} unstructured_extractor.py \"{pdf_file}\""
    if not run_command(extract_command):
        print("❌ PDF提取失败")
        sys.exit(1)
    
    # 检查生成的文本文件
    base_name = Path(pdf_file).stem
    text_file = f"middles/{base_name}_extracted.txt"
    
    if not os.path.exists(text_file):
        print(f"❌ 错误: PDF提取失败，未生成文本文件 - {text_file}")
        sys.exit(1)
    
    print(f"✅ PDF提取完成: {text_file}")
    
    # 第2步：智能推理分析（使用venv环境）
    print("")
    print("🧠 第2步: 使用AI进行智能推理分析...")
    
    # 构建venv的Python路径
    venv_python = "venv/bin/python"
    if not os.path.exists(venv_python):
        print(f"❌ 错误: venv环境不存在 - {venv_python}")
        sys.exit(1)
    
    # 执行智能推理分析
    analysis_command = f"{venv_python} final_comprehensive_formatter.py \"{text_file}\""
    if not run_command(analysis_command):
        print("❌ 智能推理分析失败")
        sys.exit(1)
    
    # 检查最终结果文件
    result_file = f"outs/{base_name}_final_comprehensive.json"
    
    if not os.path.exists(result_file):
        print(f"❌ 错误: 分析结果文件未生成 - {result_file}")
        sys.exit(1)
    
    print("")
    print("=" * 50)
    print("🎉 分析完成！")
    print("")
    print("📁 生成的文件:")
    print(f"   📄 提取文本: {text_file}")
    print(f"   📊 分析结果: {result_file}")
    print("")
    print("🔍 查看结果:")
    print(f"   cat \"{result_file}\"")
    print("")
    print("✨ 智能推理标签已生成，包含:")
    print("   🔧 技术能力标签 (基于技能深度推理)")
    print("   👥 管理能力标签 (基于经验推理)")
    print("   💼 业务能力标签 (基于价值创造推理)")
    print("   🚀 潜力标签 (基于发展方向推理)")
    print("   ⚠️  风险标签 (基于短板识别推理)")
    
    # 显示结果预览
    try:
        import json
        with open(result_file, 'r', encoding='utf-8') as f:
            result_data = json.load(f)
        
        print("")
        print("📊 分析结果预览:")
        print(f"   姓名: {result_data.get('姓名', '')}")
        print(f"   职位: {result_data.get('担任岗位', '')}")
        print(f"   🔧 技术能力: {result_data.get('技术能力标签', '')}")
        print(f"   👥 管理能力: {result_data.get('管理能力标签', '')}")
        print(f"   💼 业务能力: {result_data.get('业务能力标签', '')}")
        print(f"   🚀 发展潜力: {result_data.get('潜力标签', '')}")
        print(f"   ⚠️  风险评估: {result_data.get('风险标签', '')}")
        
    except Exception as e:
        print(f"⚠️  无法预览结果: {e}")

if __name__ == "__main__":
    main()