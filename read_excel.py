#!/usr/bin/env python3
"""
读取Excel文件的脚本
"""

import pandas as pd
import sys
import os

def read_excel_file(file_path):
    """读取Excel文件并显示内容"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return
        
        print(f"正在读取文件: {file_path}")
        print("=" * 60)
        
        # 读取Excel文件，获取所有sheet名称
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"发现 {len(sheet_names)} 个工作表:")
        for i, sheet_name in enumerate(sheet_names):
            print(f"  {i+1}. {sheet_name}")
        print()
        
        # 读取每个工作表
        for sheet_name in sheet_names:
            print(f"工作表: {sheet_name}")
            print("-" * 40)
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                print(f"数据形状: {df.shape} (行数: {df.shape[0]}, 列数: {df.shape[1]})")
                print(f"列名: {list(df.columns)}")
                print()
                
                # 显示前几行数据
                if not df.empty:
                    print("前5行数据:")
                    print(df.head().to_string())
                    print()
                    
                    # 如果数据不多，显示所有数据
                    if df.shape[0] <= 20:
                        print("完整数据:")
                        print(df.to_string())
                        print()
                else:
                    print("工作表为空")
                    print()
                    
            except Exception as e:
                print(f"读取工作表 '{sheet_name}' 时出错: {e}")
                print()
        
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")

def main():
    file_path = "rules/演示数据-1022.xlsx"
    read_excel_file(file_path)

if __name__ == "__main__":
    main()