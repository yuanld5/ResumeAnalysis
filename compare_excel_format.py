#!/usr/bin/env python3
"""
对比生成的Excel格式与演示数据格式
"""

import pandas as pd

def compare_formats():
    """对比格式"""
    print("=" * 80)
    print("Excel格式对比分析")
    print("=" * 80)
    
    # 读取演示数据
    print("\n1. 演示数据格式 (rules/演示数据-1022.xlsx):")
    demo_df = pd.read_excel("rules/演示数据-1022.xlsx", sheet_name="演示数据", header=1)
    print(f"字段数量: {len(demo_df.columns)}")
    print("字段列表:")
    for i, col in enumerate(demo_df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    print(f"\n演示数据示例 (第1行):")
    if len(demo_df) > 0:
        for col in demo_df.columns:
            value = demo_df.iloc[0][col]
            if pd.notna(value):
                print(f"  {col}: {value}")
    
    # 读取生成的数据
    print("\n" + "="*80)
    print("2. 生成的简历分析结果:")
    result_df = pd.read_excel("outs/【架构部总监_成都 30-40K】Bryan 10年_excel_format.xlsx")
    print(f"字段数量: {len(result_df.columns)}")
    print("字段列表:")
    for i, col in enumerate(result_df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    print(f"\n生成数据示例:")
    if len(result_df) > 0:
        for col in result_df.columns:
            value = result_df.iloc[0][col]
            if pd.notna(value) and str(value).strip():
                print(f"  {col}: {value}")
    
    # 字段匹配分析
    print("\n" + "="*80)
    print("3. 字段匹配分析:")
    demo_cols = set(demo_df.columns)
    result_cols = set(result_df.columns)
    
    matched = demo_cols & result_cols
    missing = demo_cols - result_cols
    extra = result_cols - demo_cols
    
    print(f"匹配字段 ({len(matched)}个): {', '.join(sorted(matched))}")
    if missing:
        print(f"缺失字段 ({len(missing)}个): {', '.join(sorted(missing))}")
    if extra:
        print(f"额外字段 ({len(extra)}个): {', '.join(sorted(extra))}")
    
    print(f"\n字段匹配率: {len(matched)}/{len(demo_cols)} = {len(matched)/len(demo_cols)*100:.1f}%")

if __name__ == "__main__":
    compare_formats()