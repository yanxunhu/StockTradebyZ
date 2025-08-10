#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI响应性测试脚本
用于测试GUI控件是否可点击和响应
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# 设置环境变量以支持中文字符
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == "win32":
    os.environ['PYTHONUTF8'] = '1'

def test_gui_responsiveness():
    """测试GUI响应性"""
    root = tk.Tk()
    root.title("GUI响应性测试")
    root.geometry("500x400")
    
    # 配置样式
    style = ttk.Style()
    style.configure('Test.TButton', font=('Microsoft YaHei', 10))
    style.configure('Success.TButton', font=('Microsoft YaHei', 10))
    
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill='both', expand=True)
    
    # 测试标签
    title_label = ttk.Label(frame, text="GUI控件响应性测试", 
                           font=('Microsoft YaHei', 14, 'bold'))
    title_label.pack(pady=10)
    
    # 计数器变量
    click_count = tk.IntVar(value=0)
    
    def button_clicked(button_name):
        """按钮点击处理函数"""
        current_count = click_count.get() + 1
        click_count.set(current_count)
        count_label.config(text=f"总点击次数: {current_count}")
        messagebox.showinfo("按钮点击", f"{button_name} 被点击了！\n这是第 {current_count} 次点击。")
        print(f"[DEBUG] {button_name} clicked - Count: {current_count}")
    
    def test_entry_change(*args):
        """输入框变化处理"""
        print(f"[DEBUG] Entry changed: {entry_var.get()}")
    
    def test_checkbox_change():
        """复选框变化处理"""
        state = "选中" if checkbox_var.get() else "未选中"
        print(f"[DEBUG] Checkbox changed: {state}")
        status_label.config(text=f"复选框状态: {state}")
    
    # 创建各种控件进行测试
    
    # 按钮测试
    button_frame = ttk.LabelFrame(frame, text="按钮测试", padding=10)
    button_frame.pack(fill='x', pady=5)
    
    ttk.Button(button_frame, text="普通按钮", 
              command=lambda: button_clicked("普通按钮"),
              style='Test.TButton').pack(side='left', padx=5)
    
    ttk.Button(button_frame, text="成功按钮", 
              command=lambda: button_clicked("成功按钮"),
              style='Success.TButton').pack(side='left', padx=5)
    
    ttk.Button(button_frame, text="退出测试", 
              command=root.destroy).pack(side='left', padx=5)
    
    # 输入框测试
    entry_frame = ttk.LabelFrame(frame, text="输入框测试", padding=10)
    entry_frame.pack(fill='x', pady=5)
    
    ttk.Label(entry_frame, text="输入文本:").pack(side='left')
    entry_var = tk.StringVar()
    entry_var.trace('w', test_entry_change)
    entry = ttk.Entry(entry_frame, textvariable=entry_var, width=30)
    entry.pack(side='left', padx=5)
    
    # 复选框测试
    checkbox_frame = ttk.LabelFrame(frame, text="复选框测试", padding=10)
    checkbox_frame.pack(fill='x', pady=5)
    
    checkbox_var = tk.BooleanVar()
    checkbox = ttk.Checkbutton(checkbox_frame, text="测试复选框", 
                              variable=checkbox_var,
                              command=test_checkbox_change)
    checkbox.pack(side='left')
    
    # 状态显示
    status_frame = ttk.LabelFrame(frame, text="状态显示", padding=10)
    status_frame.pack(fill='x', pady=5)
    
    count_label = ttk.Label(status_frame, text="总点击次数: 0")
    count_label.pack()
    
    status_label = ttk.Label(status_frame, text="复选框状态: 未选中")
    status_label.pack()
    
    # 下拉框测试
    combo_frame = ttk.LabelFrame(frame, text="下拉框测试", padding=10)
    combo_frame.pack(fill='x', pady=5)
    
    ttk.Label(combo_frame, text="选择选项:").pack(side='left')
    combo_var = tk.StringVar(value="选项1")
    combo = ttk.Combobox(combo_frame, textvariable=combo_var, 
                        values=["选项1", "选项2", "选项3", "选项4"],
                        state="readonly")
    combo.pack(side='left', padx=5)
    
    def combo_changed(event):
        print(f"[DEBUG] Combobox changed: {combo_var.get()}")
    
    combo.bind('<<ComboboxSelected>>', combo_changed)
    
    # 测试说明
    info_frame = ttk.LabelFrame(frame, text="测试说明", padding=10)
    info_frame.pack(fill='x', pady=5)
    
    info_text = """请测试以下功能:
1. 点击各种按钮 - 应该显示消息框
2. 在输入框中输入文字 - 控制台应显示调试信息
3. 点击复选框 - 状态应该更新
4. 选择下拉框选项 - 控制台应显示调试信息

如果任何控件无响应，说明存在问题。"""
    
    info_label = ttk.Label(info_frame, text=info_text, justify='left')
    info_label.pack()
    
    print("✅ GUI响应性测试窗口已启动")
    print("请测试各种控件的响应性...")
    print("控制台将显示调试信息")
    
    # 绑定键盘事件测试
    def key_pressed(event):
        print(f"[DEBUG] Key pressed: {event.keysym}")
    
    root.bind('<Key>', key_pressed)
    
    # 启动主循环
    root.mainloop()
    print("GUI测试结束")

if __name__ == "__main__":
    test_gui_responsiveness()