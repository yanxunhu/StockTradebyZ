#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI问题调试脚本
用于检查GUI可能存在的问题
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os
import sys

# 设置环境变量以支持中文字符
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == "win32":
    os.environ['PYTHONUTF8'] = '1'

def debug_gui_main():
    """调试主GUI可能的问题"""
    
    # 检查是否有其他GUI实例在运行
    print("=== GUI调试信息 ===")
    print(f"Python版本: {sys.version}")
    print(f"Tkinter版本: {tk.TkVersion}")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 检查必要的模块
    try:
        import pandas
        print(f"✅ pandas版本: {pandas.__version__}")
    except ImportError:
        print("❌ pandas未安装")
    
    try:
        import json
        print("✅ json模块可用")
    except ImportError:
        print("❌ json模块不可用")
    
    # 检查配置文件
    config_files = ['configs.json', 'config.json']
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ 找到配置文件: {config_file}")
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                print(f"   配置文件大小: {len(str(config_data))} 字符")
            except Exception as e:
                print(f"   ❌ 配置文件读取错误: {e}")
        else:
            print(f"⚠️  配置文件不存在: {config_file}")
    
    # 创建简化的GUI来测试基本功能
    root = tk.Tk()
    root.title("GUI调试测试")
    root.geometry("600x500")
    
    # 测试字体设置
    try:
        root.option_add('*Font', 'Microsoft\\ YaHei 9')
        print("✅ 字体设置成功")
    except Exception as e:
        print(f"❌ 字体设置失败: {e}")
    
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill='both', expand=True)
    
    # 状态变量
    status_var = tk.StringVar(value="等待测试...")
    click_count = tk.IntVar(value=0)
    
    # 状态显示
    status_label = ttk.Label(frame, textvariable=status_var, 
                            font=('Microsoft YaHei', 12))
    status_label.pack(pady=10)
    
    count_label = ttk.Label(frame, text="点击次数: 0", 
                           font=('Microsoft YaHei', 10))
    count_label.pack(pady=5)
    
    def simple_click():
        """简单点击测试"""
        current = click_count.get() + 1
        click_count.set(current)
        count_label.config(text=f"点击次数: {current}")
        status_var.set(f"按钮响应正常 - 第{current}次点击")
        print(f"[DEBUG] 按钮点击 #{current}")
    
    def blocking_operation():
        """模拟阻塞操作"""
        status_var.set("执行阻塞操作中...")
        root.update()  # 强制更新界面
        time.sleep(3)  # 模拟耗时操作
        status_var.set("阻塞操作完成")
        print("[DEBUG] 阻塞操作完成")
    
    def threaded_operation():
        """在线程中执行操作"""
        def worker():
            status_var.set("线程操作中...")
            time.sleep(3)
            status_var.set("线程操作完成")
            print("[DEBUG] 线程操作完成")
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def test_messagebox():
        """测试消息框"""
        result = messagebox.askyesno("测试", "消息框是否正常显示？")
        status_var.set(f"消息框测试: {'正常' if result else '取消'}")
        print(f"[DEBUG] 消息框测试结果: {result}")
    
    # 创建测试按钮
    button_frame = ttk.LabelFrame(frame, text="功能测试", padding=10)
    button_frame.pack(fill='x', pady=10)
    
    ttk.Button(button_frame, text="简单点击测试", 
              command=simple_click).pack(side='left', padx=5)
    
    ttk.Button(button_frame, text="阻塞操作测试", 
              command=blocking_operation).pack(side='left', padx=5)
    
    ttk.Button(button_frame, text="线程操作测试", 
              command=threaded_operation).pack(side='left', padx=5)
    
    ttk.Button(button_frame, text="消息框测试", 
              command=test_messagebox).pack(side='left', padx=5)
    
    # 输入测试
    input_frame = ttk.LabelFrame(frame, text="输入测试", padding=10)
    input_frame.pack(fill='x', pady=10)
    
    entry_var = tk.StringVar()
    def on_entry_change(*args):
        status_var.set(f"输入内容: {entry_var.get()}")
        print(f"[DEBUG] 输入变化: {entry_var.get()}")
    
    entry_var.trace('w', on_entry_change)
    
    ttk.Label(input_frame, text="输入测试:").pack(side='left')
    entry = ttk.Entry(input_frame, textvariable=entry_var, width=30)
    entry.pack(side='left', padx=5)
    
    # 选择测试
    select_frame = ttk.LabelFrame(frame, text="选择测试", padding=10)
    select_frame.pack(fill='x', pady=10)
    
    # 复选框
    check_var = tk.BooleanVar()
    def on_check_change():
        state = "选中" if check_var.get() else "未选中"
        status_var.set(f"复选框: {state}")
        print(f"[DEBUG] 复选框变化: {state}")
    
    check = ttk.Checkbutton(select_frame, text="复选框测试", 
                           variable=check_var, command=on_check_change)
    check.pack(side='left', padx=10)
    
    # 下拉框
    combo_var = tk.StringVar(value="选项1")
    combo = ttk.Combobox(select_frame, textvariable=combo_var,
                        values=["选项1", "选项2", "选项3"],
                        state="readonly")
    combo.pack(side='left', padx=10)
    
    def on_combo_change(event):
        status_var.set(f"下拉框: {combo_var.get()}")
        print(f"[DEBUG] 下拉框变化: {combo_var.get()}")
    
    combo.bind('<<ComboboxSelected>>', on_combo_change)
    
    # 日志区域
    log_frame = ttk.LabelFrame(frame, text="调试日志", padding=10)
    log_frame.pack(fill='both', expand=True, pady=10)
    
    log_text = tk.Text(log_frame, height=8, font=('Consolas', 9))
    log_text.pack(fill='both', expand=True)
    
    # 重定向print到日志区域
    class LogRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget
        
        def write(self, message):
            if message.strip():  # 忽略空行
                self.text_widget.insert(tk.END, message)
                self.text_widget.see(tk.END)
                self.text_widget.update()
        
        def flush(self):
            pass
    
    # 设置日志重定向
    log_redirector = LogRedirector(log_text)
    
    def toggle_log_redirect():
        if hasattr(toggle_log_redirect, 'original_stdout'):
            sys.stdout = toggle_log_redirect.original_stdout
            del toggle_log_redirect.original_stdout
            status_var.set("日志重定向已关闭")
        else:
            toggle_log_redirect.original_stdout = sys.stdout
            sys.stdout = log_redirector
            status_var.set("日志重定向已开启")
    
    ttk.Button(log_frame, text="切换日志重定向", 
              command=toggle_log_redirect).pack(pady=5)
    
    # 退出按钮
    ttk.Button(frame, text="退出测试", 
              command=root.destroy).pack(pady=10)
    
    print("\n=== GUI调试测试启动 ===")
    print("请测试各种控件的响应性")
    print("如果发现问题，请查看控制台输出")
    
    # 检查主线程
    print(f"当前线程: {threading.current_thread().name}")
    print(f"活动线程数: {threading.active_count()}")
    
    root.mainloop()
    
    # 恢复stdout
    if hasattr(toggle_log_redirect, 'original_stdout'):
        sys.stdout = toggle_log_redirect.original_stdout
    
    print("GUI调试测试结束")

if __name__ == "__main__":
    debug_gui_main()