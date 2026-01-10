#!/usr/bin/env python3
"""
分析Excel文件的脚本 - 更好地处理数据格式
"""

import pandas as pd
import sys
import os

def analyze_excel_file(file_path):
    """分析Excel文件并显示格式化的内容"""
    try:
        print(f"正在分析文件: {file_path}")
        print("=" * 80)
        
        # 读取Excel文件
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"发现 {len(sheet_names)} 个工作表:")
        for i, sheet_name in enumerate(sheet_names):
            print(f"  {i+1}. {sheet_name}")
        print()
        
        # 分析每个重要的工作表
        important_sheets = ['演示数据', '人才标签', '演示问题', 'Sheet8']
        
        for sheet_name in important_sheets:
            if sheet_name in sheet_names:
                print(f"\n{'='*60}")
                print(f"工作表: {sheet_name}")
                print(f"{'='*60}")
                
                try:
                    # 尝试不同的读取方式
                    if sheet_name == '演示数据':
                        analyze_demo_data(file_path, sheet_name)
                    elif sheet_name == '人才标签':
                        analyze_talent_tags(file_path, sheet_name)
                    elif sheet_name == '演示问题':
                        analyze_demo_questions(file_path, sheet_name)
                    elif sheet_name == 'Sheet8':
                        analyze_sheet8(file_path, sheet_name)
                        
                except Exception as e:
                    print(f"分析工作表 '{sheet_name}' 时出错: {e}")
        
    except Exception as e:
        print(f"分析Excel文件时出错: {e}")

def analyze_demo_data(file_path, sheet_name):
    """分析演示数据工作表"""
    # 尝试从第1行开始读取（第0行可能是标题）
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    
    print(f"数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    
    # 如果第一行看起来像是真正的列名
    if '员工工号' in str(df.iloc[0]).replace('nan', ''):
        # 重新读取，使用第1行作为列名
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
        print("\n重新读取后:")
        print(f"数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
    
    # 显示前几行数据
    if not df.empty:
        print("\n前5行数据:")
        for i in range(min(5, len(df))):
            print(f"第{i+1}行:")
            for col in df.columns:
                if pd.notna(df.iloc[i][col]):
                    print(f"  {col}: {df.iloc[i][col]}")
            print()

def analyze_talent_tags(file_path, sheet_name):
    """分析人才标签工作表"""
    # 这个表格可能有复杂的结构，尝试多种方式读取
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    print(f"原始数据形状: {df.shape}")
    
    # 查找可能的标题行
    for i in range(min(5, len(df))):
        row_data = df.iloc[i].dropna().tolist()
        if len(row_data) > 5:  # 如果这一行有足够多的数据
            print(f"\n第{i+1}行可能的标题: {row_data[:10]}...")  # 只显示前10个
    
    # 尝试从第2行开始读取
    if len(df) > 2:
        df_clean = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
        print(f"\n使用第2行作为标题后的数据形状: {df_clean.shape}")
        
        # 显示一些示例数据
        if not df_clean.empty:
            print("\n示例数据 (前3行):")
            for i in range(min(3, len(df_clean))):
                row_data = []
                for col in df_clean.columns:
                    if pd.notna(df_clean.iloc[i][col]):
                        row_data.append(f"{col}: {df_clean.iloc[i][col]}")
                if row_data:
                    print(f"第{i+1}行: {'; '.join(row_data[:5])}...")  # 只显示前5个字段

def analyze_demo_questions(file_path, sheet_name):
    """分析演示问题工作表"""
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    print(f"数据形状: {df.shape}")
    
    # 查找问题和答案
    questions = []
    answers = []
    
    for i in range(len(df)):
        for j in range(len(df.columns)):
            cell_value = df.iloc[i, j]
            if pd.notna(cell_value) and isinstance(cell_value, str):
                if cell_value.startswith('问题'):
                    questions.append((i, j, cell_value))
                elif cell_value.startswith('演示结果'):
                    answers.append((i, j, cell_value))
    
    print(f"\n发现 {len(questions)} 个问题:")
    for i, (row, col, question) in enumerate(questions):
        print(f"{i+1}. {question}")
        # 查找对应的答案
        for ans_row, ans_col, answer in answers:
            if abs(ans_row - row) <= 2:  # 答案通常在问题附近
                print(f"   答案: {answer}")
                break
        print()

def analyze_sheet8(file_path, sheet_name):
    """分析Sheet8工作表"""
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    print(f"数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    
    if not df.empty:
        print("\n完整数据:")
        print(df.to_string())

def main():
    file_path = "rules/演示数据-1022.xlsx"
    analyze_excel_file(file_path)

if __name__ == "__main__":
    main()