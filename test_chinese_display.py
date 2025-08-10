#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文字符显示测试脚本
用于验证GUI中的中文字符显示是否正常
"""

import tkinter as tk
from tkinter import ttk
import os
import sys

# 设置环境变量以支持中文字符
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == "win32":
    os.environ['PYTHONUTF8'] = '1'

def test_chinese_display():
    """测试中文字符显示"""
    root = tk.Tk()
    root.title("中文字符显示测试")
    root.geometry("600x400")
    
    # 创建测试组件
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill='both', expand=True)
    
    # 配置样式
    style = ttk.Style()
    style.configure('Title.TLabel', font=('Microsoft YaHei', 16, 'bold'))
    style.configure('Test.TLabel', font=('Microsoft YaHei', 10))
    
    # 标题标签
    title_label = ttk.Label(frame, text="Z哥战法 - 股票策略选择器", style='Title.TLabel')
    title_label.pack(pady=10)
    
    # 测试各种中文文本
    test_texts = [
        "数据获取",
        "策略选择", 
        "配置管理",
        "日志查看",
        "开始选股",
        "查看结果",
        "导出结果",
        "市值范围设置",
        "增量更新模式",
        "小散模式"
    ]
    
    for i, text in enumerate(test_texts):
        label = ttk.Label(frame, text=f"{i+1}. {text}", style='Test.TLabel')
        label.pack(anchor='w', pady=2)
    
    # 创建表格测试
    tree_frame = ttk.LabelFrame(frame, text="表格中文显示测试", padding=10)
    tree_frame.pack(fill='x', pady=10)
    
    columns = ('策略', '股票代码', '股票名称', '选中时间')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=5)
    
    # 配置表格字体
    style = ttk.Style()
    style.configure('Treeview', font=('Microsoft YaHei', 9))
    style.configure('Treeview.Heading', font=('Microsoft YaHei', 10, 'bold'))
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    
    # 添加测试数据
    test_data = [
        ('BBI+KDJ策略', '000001', '平安银行', '2024-01-15'),
        ('超级B1策略', '000002', '万科A', '2024-01-15'),
        ('BBI多空策略', '600036', '招商银行', '2024-01-15')
    ]
    
    for data in test_data:
        tree.insert('', 'end', values=data)
    
    tree.pack(fill='x')
    
    # 文本框测试
    text_frame = ttk.LabelFrame(frame, text="文本框中文显示测试", padding=10)
    text_frame.pack(fill='x', pady=10)
    
    text_widget = tk.Text(text_frame, height=4, font=('Microsoft YaHei', 9))
    text_widget.pack(fill='x')
    
    sample_text = """这是一个中文文本显示测试。
包含各种中文字符：策略、选股、配置、日志等。
测试特殊字符：【】（）、，。？！
测试数字和英文混合：A股、K线、RSI指标、MACD等。"""
    
    text_widget.insert('1.0', sample_text)
    
    # 关闭按钮
    close_btn = ttk.Button(frame, text="关闭测试", command=root.destroy)
    close_btn.pack(pady=10)
    
    print("✅ 中文字符显示测试窗口已打开")
    print("请检查以下内容是否正确显示：")
    print("1. 窗口标题中的中文")
    print("2. 各种标签中的中文文本")
    print("3. 表格标题和内容中的中文")
    print("4. 文本框中的中文段落")
    print("如果所有中文都能正确显示，说明字体配置成功！")
    
    root.mainloop()

if __name__ == "__main__":
    test_chinese_display()