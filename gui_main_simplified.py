#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版GUI主程序 - 用于调试响应性问题
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import json
import sys
import os
from pathlib import Path
import subprocess
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, List

# 设置环境变量以支持中文字符
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == "win32":
    os.environ['PYTHONUTF8'] = '1'

class SimplifiedStockTradingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Z哥战法 - 股票策略选择器 (简化版)")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # 设置默认字体以支持中文显示
        try:
            self.root.option_add('*Font', 'Microsoft\\ YaHei 9')
            self.root.option_add('*TkDefaultFont', 'Microsoft\\ YaHei 9')
            self.root.option_add('*TkTextFont', 'Microsoft\\ YaHei 9')
            self.root.option_add('*TkFixedFont', 'Microsoft\\ YaHei 9')
        except Exception:
            # 如果字体设置失败，使用系统默认字体
            pass
        
        # 初始化变量
        self.config_data = {"selectors": []}
        self.strategy_vars = {}
        self.strategy_checkboxes = {}
        self.fetch_thread = None
        self.select_thread = None
        
        # 设置样式
        self.setup_styles()
        
        # 创建主界面
        self.create_widgets()
        
        # 简化的配置加载
        self.load_config_safe()
        
        print("✅ 简化版GUI初始化完成")
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        
        # 配置各种样式
        style.configure('Title.TLabel', font=('Microsoft YaHei', 14, 'bold'))
        style.configure('Heading.TLabel', font=('Microsoft YaHei', 12, 'bold'))
        style.configure('Action.TButton', font=('Microsoft YaHei', 10))
        style.configure('Success.TButton', font=('Microsoft YaHei', 10))
        style.configure('Warning.TButton', font=('Microsoft YaHei', 10))
        
    def create_widgets(self):
        """创建主界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="Z哥战法 - 股票策略选择器", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # 创建各个选项卡
        self.create_fetch_tab()
        self.create_select_tab()
        self.create_config_tab()
        self.create_log_tab()
        
    def create_fetch_tab(self):
        """创建数据获取标签页"""
        fetch_frame = ttk.Frame(self.notebook)
        self.notebook.add(fetch_frame, text="数据获取")
        
        # 标题
        ttk.Label(fetch_frame, text="股票数据获取", 
                 style='Heading.TLabel').pack(pady=10)
        
        # 控制按钮
        button_frame = ttk.Frame(fetch_frame)
        button_frame.pack(pady=10)
        
        self.fetch_button = ttk.Button(button_frame, text="开始获取数据", 
                                      command=self.start_fetch_data,
                                      style='Action.TButton')
        self.fetch_button.pack(side='left', padx=5)
        
        self.stop_fetch_button = ttk.Button(button_frame, text="停止获取", 
                                           command=self.stop_fetch_data,
                                           style='Warning.TButton')
        self.stop_fetch_button.pack(side='left', padx=5)
        
        # 进度条
        self.fetch_progress = ttk.Progressbar(fetch_frame, mode='indeterminate')
        self.fetch_progress.pack(fill='x', padx=20, pady=10)
        
        # 状态显示
        self.fetch_status = ttk.Label(fetch_frame, text="等待开始...")
        self.fetch_status.pack(pady=5)
        
    def create_select_tab(self):
        """创建选股标签页"""
        select_frame = ttk.Frame(self.notebook)
        self.notebook.add(select_frame, text="策略选股")
        
        # 标题
        ttk.Label(select_frame, text="策略选股", 
                 style='Heading.TLabel').pack(pady=10)
        
        # 策略选择框架 - 简化版
        self.strategy_frame = ttk.LabelFrame(select_frame, text="策略选择", padding=10)
        self.strategy_frame.pack(fill='x', padx=20, pady=10)
        
        # 控制按钮
        button_frame = ttk.Frame(select_frame)
        button_frame.pack(pady=10)
        
        self.select_button = ttk.Button(button_frame, text="开始选股", 
                                       command=self.start_stock_selection,
                                       style='Action.TButton')
        self.select_button.pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="查看结果", 
                  command=self.view_results,
                  style='Success.TButton').pack(side='left', padx=5)
        
        # 进度条
        self.select_progress = ttk.Progressbar(select_frame, mode='indeterminate')
        self.select_progress.pack(fill='x', padx=20, pady=10)
        
        # 状态显示
        self.select_status = ttk.Label(select_frame, text="等待开始...")
        self.select_status.pack(pady=5)
        
    def create_config_tab(self):
        """创建配置管理标签页"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="配置管理")
        
        # 配置文件操作
        file_frame = ttk.LabelFrame(config_frame, text="配置文件操作", padding=10)
        file_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(file_frame, text="加载配置", command=self.load_config_file).pack(side='left', padx=5)
        ttk.Button(file_frame, text="保存配置", command=self.save_config_file).pack(side='left', padx=5)
        ttk.Button(file_frame, text="重置默认", command=self.reset_config).pack(side='left', padx=5)
        
        # 配置编辑区域
        edit_frame = ttk.LabelFrame(config_frame, text="配置编辑", padding=10)
        edit_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.config_text = scrolledtext.ScrolledText(edit_frame, wrap=tk.WORD, height=20,
                                                     font=('Microsoft YaHei', 10))
        self.config_text.pack(fill='both', expand=True)
        
    def create_log_tab(self):
        """创建日志查看标签页"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="日志查看")
        
        # 日志控制
        control_frame = ttk.Frame(log_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="清空日志", command=self.clear_log).pack(side='left', padx=5)
        ttk.Button(control_frame, text="刷新日志", command=self.refresh_log).pack(side='left', padx=5)
        ttk.Button(control_frame, text="保存日志", command=self.save_log).pack(side='left', padx=5)
        
        # 日志显示区域
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=25, 
                                                 font=('Microsoft YaHei', 9))
        self.log_text.pack(fill='both', expand=True, padx=10, pady=5)
        
    def load_config_safe(self):
        """安全加载配置文件"""
        try:
            config_path = Path("configs.json")
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                print(f"✅ 配置文件加载成功: {len(self.config_data.get('selectors', []))} 个策略")
                self.update_strategy_checkboxes_safe()
                self.update_config_text()
            else:
                self.config_data = {"selectors": []}
                print("⚠️  未找到configs.json文件，使用默认配置")
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            self.config_data = {"selectors": []}
            
    def update_strategy_checkboxes_safe(self):
        """安全更新策略选择复选框"""
        try:
            # 清除现有的复选框
            for widget in self.strategy_checkboxes.values():
                widget.destroy()
            self.strategy_checkboxes.clear()
            self.strategy_vars.clear()
            
            # 添加新的复选框
            if "selectors" in self.config_data:
                for i, selector in enumerate(self.config_data["selectors"]):
                    alias = selector.get("alias", selector.get("class", f"策略{i+1}"))
                    var = tk.BooleanVar(value=selector.get("activate", True))
                    checkbox = ttk.Checkbutton(self.strategy_frame, text=alias, variable=var)
                    checkbox.grid(row=i//3, column=i%3, sticky='w', padx=10, pady=2)
                    
                    self.strategy_vars[selector["class"]] = var
                    self.strategy_checkboxes[selector["class"]] = checkbox
                    
            print(f"✅ 策略复选框更新完成: {len(self.strategy_checkboxes)} 个")
        except Exception as e:
            print(f"❌ 更新策略复选框失败: {e}")
                
    def update_config_text(self):
        """更新配置文本显示"""
        try:
            self.config_text.delete(1.0, tk.END)
            self.config_text.insert(1.0, json.dumps(self.config_data, indent=2, ensure_ascii=False))
            print("✅ 配置文本更新完成")
        except Exception as e:
            print(f"❌ 更新配置文本失败: {e}")
        
    def start_fetch_data(self):
        """开始获取数据"""
        print("🚀 开始获取数据...")
        self.fetch_status.config(text="正在获取数据...")
        self.fetch_progress.start()
        messagebox.showinfo("测试", "数据获取功能正常响应！")
        self.fetch_progress.stop()
        self.fetch_status.config(text="获取完成")
        
    def stop_fetch_data(self):
        """停止获取数据"""
        print("⏹️ 停止获取数据")
        self.fetch_progress.stop()
        self.fetch_status.config(text="已停止")
        
    def start_stock_selection(self):
        """开始选股"""
        print("🎯 开始选股...")
        self.select_status.config(text="正在选股...")
        self.select_progress.start()
        messagebox.showinfo("测试", "选股功能正常响应！")
        self.select_progress.stop()
        self.select_status.config(text="选股完成")
        
    def view_results(self):
        """查看结果"""
        print("📊 查看结果")
        messagebox.showinfo("测试", "查看结果功能正常响应！")
        
    def load_config_file(self):
        """加载配置文件"""
        print("📁 加载配置文件")
        messagebox.showinfo("测试", "加载配置功能正常响应！")
        
    def save_config_file(self):
        """保存配置文件"""
        print("💾 保存配置文件")
        messagebox.showinfo("测试", "保存配置功能正常响应！")
        
    def reset_config(self):
        """重置配置"""
        print("🔄 重置配置")
        messagebox.showinfo("测试", "重置配置功能正常响应！")
        
    def clear_log(self):
        """清空日志"""
        print("🗑️ 清空日志")
        self.log_text.delete(1.0, tk.END)
        
    def refresh_log(self):
        """刷新日志"""
        print("🔄 刷新日志")
        messagebox.showinfo("测试", "刷新日志功能正常响应！")
        
    def save_log(self):
        """保存日志"""
        print("💾 保存日志")
        messagebox.showinfo("测试", "保存日志功能正常响应！")

def main():
    """主函数"""
    root = tk.Tk()
    app = SimplifiedStockTradingGUI(root)
    
    # 设置图标（如果存在）
    try:
        if Path("icon.ico").exists():
            root.iconbitmap("icon.ico")
    except Exception:
        pass
    
    # 设置关闭协议
    def on_closing():
        if messagebox.askokcancel("退出", "确定要退出程序吗？"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    print("🚀 简化版GUI启动完成")
    print("请测试各种按钮的响应性...")
    
    root.mainloop()

if __name__ == "__main__":
    main()