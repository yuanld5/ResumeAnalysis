#!/bin/bash

# 最终版本简历分析一键脚本
# 使用方法: ./run_final_analysis.sh "files/简历文件.pdf"

set -e  # 遇到错误立即退出

# 检查参数
if [ $# -eq 0 ]; then
    echo "使用方法: ./run_final_analysis.sh \"files/简历文件.pdf\""
    echo "示例: ./run_final_analysis.sh \"files/【架构部总监_成都 30-40K】Bryan 10年.pdf\""
    exit 1
fi

PDF_FILE="$1"

# 检查文件是否存在
if [ ! -f "$PDF_FILE" ]; then
    echo "❌ 错误: 文件不存在 - $PDF_FILE"
    exit 1
fi

echo "🚀 开始处理简历: $PDF_FILE"
echo "=================================================="

# 第1步：PDF提取（使用venv39环境）
echo "📄 第1步: 使用unstructured提取PDF内容..."
source venv39/bin/activate
python unstructured_extractor.py "$PDF_FILE"
deactivate

# 获取生成的文本文件路径
BASE_NAME=$(basename "$PDF_FILE" .pdf)
TEXT_FILE="middles/${BASE_NAME}_extracted.txt"

# 检查文本文件是否生成成功
if [ ! -f "$TEXT_FILE" ]; then
    echo "❌ 错误: PDF提取失败，未生成文本文件"
    exit 1
fi

echo "✅ PDF提取完成: $TEXT_FILE"

# 第2步：智能推理分析（使用venv环境）
echo ""
echo "🧠 第2步: 使用AI进行智能推理分析..."
source venv/bin/activate
python final_comprehensive_formatter.py "$TEXT_FILE"
deactivate

# 获取最终结果文件路径
RESULT_FILE="outs/${BASE_NAME}_final_comprehensive.json"

echo ""
echo "=================================================="
echo "🎉 分析完成！"
echo ""
echo "📁 生成的文件:"
echo "   📄 提取文本: $TEXT_FILE"
echo "   📊 分析结果: $RESULT_FILE"
echo ""
echo "🔍 查看结果:"
echo "   cat \"$RESULT_FILE\""
echo ""
echo "✨ 智能推理标签已生成，包含:"
echo "   🔧 技术能力标签 (基于技能深度推理)"
echo "   👥 管理能力标签 (基于经验推理)"  
echo "   💼 业务能力标签 (基于价值创造推理)"
echo "   🚀 潜力标签 (基于发展方向推理)"
echo "   ⚠️  风险标签 (基于短板识别推理)"