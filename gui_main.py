#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Trading Strategy GUI Application
Z哥战法 GUI版本
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

# 导入原有模块
try:
    from fetch_kline import main as fetch_main, get_constituents
    from select_stock import main as select_main
    import Selector
except ImportError as e:
    messagebox.showerror("导入错误", f"无法导入必要模块: {e}")
    sys.exit(1)


class StockTradingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Z哥战法 - 股票策略选择器")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # 设置样式
        self.setup_styles()
        
        # 创建主界面
        self.create_widgets()
        
        # 加载配置
        self.load_config()
        
        # 设置日志
        self.setup_logging()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置样式
        style.configure('Title.TLabel', font=('Microsoft YaHei', 16, 'bold'), foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Microsoft YaHei', 12, 'bold'), foreground='#34495e')
        style.configure('Custom.TButton', font=('Microsoft YaHei', 10))
        style.configure('Success.TButton', background='#27ae60', foreground='white')
        style.configure('Warning.TButton', background='#f39c12', foreground='white')
        style.configure('Danger.TButton', background='#e74c3c', foreground='white')
        
    def create_widgets(self):
        """创建主界面组件"""
        # 主标题
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(title_frame, text="Z哥战法 - 股票策略选择器", style='Title.TLabel').pack()
        ttk.Label(title_frame, text="专业的A股量化选股工具", font=('Microsoft YaHei', 10)).pack()
        
        # 创建笔记本控件（标签页）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 数据获取标签页
        self.create_fetch_tab()
        
        # 策略选股标签页
        self.create_select_tab()
        
        # 配置管理标签页
        self.create_config_tab()
        
        # 日志查看标签页
        self.create_log_tab()
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken')
        status_bar.pack(side='bottom', fill='x')
        
    def create_fetch_tab(self):
        """创建数据获取标签页"""
        fetch_frame = ttk.Frame(self.notebook)
        self.notebook.add(fetch_frame, text="数据获取")
        
        # 参数设置区域
        params_frame = ttk.LabelFrame(fetch_frame, text="参数设置", padding=10)
        params_frame.pack(fill='x', padx=10, pady=5)
        
        # 市值范围
        ttk.Label(params_frame, text="市值范围 (亿元):", style='Heading.TLabel').grid(row=0, column=0, sticky='w', pady=2)
        
        cap_frame = ttk.Frame(params_frame)
        cap_frame.grid(row=0, column=1, sticky='w', padx=10)
        
        ttk.Label(cap_frame, text="最小:").pack(side='left')
        self.min_cap_var = tk.StringVar(value="50")
        ttk.Entry(cap_frame, textvariable=self.min_cap_var, width=10).pack(side='left', padx=2)
        
        ttk.Label(cap_frame, text="最大:").pack(side='left', padx=(10,0))
        self.max_cap_var = tk.StringVar(value="1000")
        ttk.Entry(cap_frame, textvariable=self.max_cap_var, width=10).pack(side='left', padx=2)
        
        # 数据源选择
        ttk.Label(params_frame, text="数据源:", style='Heading.TLabel').grid(row=1, column=0, sticky='w', pady=2)
        self.datasource_var = tk.StringVar(value="akshare")
        datasource_combo = ttk.Combobox(params_frame, textvariable=self.datasource_var, 
                                       values=["akshare", "tushare", "mootdx"], state="readonly", width=15)
        datasource_combo.grid(row=1, column=1, sticky='w', padx=10)
        
        # 日期范围
        ttk.Label(params_frame, text="开始日期:", style='Heading.TLabel').grid(row=2, column=0, sticky='w', pady=2)
        self.start_date_var = tk.StringVar(value=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"))
        ttk.Entry(params_frame, textvariable=self.start_date_var, width=15).grid(row=2, column=1, sticky='w', padx=10)
        
        ttk.Label(params_frame, text="结束日期:", style='Heading.TLabel').grid(row=3, column=0, sticky='w', pady=2)
        self.end_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(params_frame, textvariable=self.end_date_var, width=15).grid(row=3, column=1, sticky='w', padx=10)
        
        # 其他选项
        options_frame = ttk.Frame(params_frame)
        options_frame.grid(row=4, column=0, columnspan=2, sticky='w', pady=10)
        
        self.incremental_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="增量更新", variable=self.incremental_var).pack(side='left')
        
        self.small_player_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="小盘股模式", variable=self.small_player_var).pack(side='left', padx=10)
        
        # 控制按钮
        button_frame = ttk.Frame(fetch_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="开始获取数据", command=self.start_fetch_data, 
                  style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="停止获取", command=self.stop_fetch_data, 
                  style='Danger.TButton').pack(side='left', padx=5)
        
        # 进度显示
        progress_frame = ttk.LabelFrame(fetch_frame, text="进度", padding=10)
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        self.fetch_progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.fetch_progress.pack(fill='x', pady=2)
        
        self.fetch_status_var = tk.StringVar(value="等待开始...")
        ttk.Label(progress_frame, textvariable=self.fetch_status_var).pack()
        
    def create_select_tab(self):
        """创建策略选股标签页"""
        select_frame = ttk.Frame(self.notebook)
        self.notebook.add(select_frame, text="策略选股")
        
        # 策略选择区域
        strategy_frame = ttk.LabelFrame(select_frame, text="策略选择", padding=10)
        strategy_frame.pack(fill='x', padx=10, pady=5)
        
        # 策略列表
        self.strategy_vars = {}
        self.strategy_checkboxes = {}
        
        # 控制按钮
        button_frame = ttk.Frame(select_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="开始选股", command=self.start_stock_selection, 
                  style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="查看结果", command=self.view_results, 
                  style='Custom.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="导出结果", command=self.export_results, 
                  style='Custom.TButton').pack(side='left', padx=5)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(select_frame, text="选股结果", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 创建表格显示结果
        columns = ('策略', '股票代码', '股票名称', '选中时间')
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=150)
        
        # 滚动条
        scrollbar_y = ttk.Scrollbar(result_frame, orient='vertical', command=self.result_tree.yview)
        scrollbar_x = ttk.Scrollbar(result_frame, orient='horizontal', command=self.result_tree.xview)
        self.result_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.result_tree.pack(side='left', fill='both', expand=True)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        
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
        
        self.config_text = scrolledtext.ScrolledText(edit_frame, wrap=tk.WORD, height=20)
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
                                                 font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True, padx=10, pady=5)
        
    def setup_logging(self):
        """设置日志处理"""
        class GUILogHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
                
            def emit(self, record):
                msg = self.format(record)
                def append():
                    self.text_widget.insert(tk.END, msg + '\n')
                    self.text_widget.see(tk.END)
                self.text_widget.after(0, append)
        
        # 添加GUI日志处理器
        gui_handler = GUILogHandler(self.log_text)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        
        # 获取根日志记录器并添加处理器
        root_logger = logging.getLogger()
        root_logger.addHandler(gui_handler)
        root_logger.setLevel(logging.INFO)
        
    def load_config(self):
        """加载配置文件"""
        try:
            config_path = Path("configs.json")
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                self.update_strategy_checkboxes()
                self.update_config_text()
            else:
                self.config_data = {"selectors": []}
                messagebox.showwarning("配置文件", "未找到configs.json文件，将使用默认配置")
        except Exception as e:
            messagebox.showerror("错误", f"加载配置文件失败: {e}")
            self.config_data = {"selectors": []}
            
    def update_strategy_checkboxes(self):
        """更新策略选择复选框"""
        # 清除现有的复选框
        for widget in self.strategy_checkboxes.values():
            widget.destroy()
        self.strategy_checkboxes.clear()
        self.strategy_vars.clear()
        
        # 获取策略框架
        strategy_frame = None
        for child in self.notebook.winfo_children():
            if isinstance(child, ttk.Frame):
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, ttk.LabelFrame) and "策略选择" in str(grandchild['text']):
                        strategy_frame = grandchild
                        break
                if strategy_frame:
                    break
        
        if not strategy_frame:
            return
            
        # 添加新的复选框
        if "selectors" in self.config_data:
            for i, selector in enumerate(self.config_data["selectors"]):
                alias = selector.get("alias", selector.get("class", f"策略{i+1}"))
                var = tk.BooleanVar(value=selector.get("activate", True))
                checkbox = ttk.Checkbutton(strategy_frame, text=alias, variable=var)
                checkbox.grid(row=i//3, column=i%3, sticky='w', padx=10, pady=2)
                
                self.strategy_vars[selector["class"]] = var
                self.strategy_checkboxes[selector["class"]] = checkbox
                
    def update_config_text(self):
        """更新配置文本显示"""
        self.config_text.delete(1.0, tk.END)
        self.config_text.insert(1.0, json.dumps(self.config_data, indent=2, ensure_ascii=False))
        
    def start_fetch_data(self):
        """开始获取数据"""
        def fetch_worker():
            try:
                self.fetch_progress.start()
                self.fetch_status_var.set("正在获取数据...")
                self.status_var.set("数据获取中...")
                
                # 构建参数
                args = [
                    "--min-cap", self.min_cap_var.get(),
                    "--max-cap", self.max_cap_var.get(),
                    "--datasource", self.datasource_var.get(),
                    "--start", self.start_date_var.get(),
                    "--end", self.end_date_var.get()
                ]
                
                if self.incremental_var.get():
                    args.append("--incremental")
                if self.small_player_var.get():
                    args.append("--small-player")
                
                # 模拟调用fetch_kline.py
                sys.argv = ["fetch_kline.py"] + args
                fetch_main()
                
                self.fetch_status_var.set("数据获取完成")
                self.status_var.set("就绪")
                messagebox.showinfo("完成", "数据获取完成！")
                
            except Exception as e:
                self.fetch_status_var.set(f"获取失败: {e}")
                self.status_var.set("就绪")
                messagebox.showerror("错误", f"数据获取失败: {e}")
            finally:
                self.fetch_progress.stop()
                
        # 在新线程中运行
        thread = threading.Thread(target=fetch_worker, daemon=True)
        thread.start()
        
    def stop_fetch_data(self):
        """停止获取数据"""
        # 这里可以添加停止逻辑
        self.fetch_progress.stop()
        self.fetch_status_var.set("已停止")
        self.status_var.set("就绪")
        
    def start_stock_selection(self):
        """开始股票选择"""
        def select_worker():
            try:
                self.status_var.set("选股中...")
                
                # 更新配置文件中的activate状态
                if "selectors" in self.config_data:
                    for selector in self.config_data["selectors"]:
                        class_name = selector["class"]
                        if class_name in self.strategy_vars:
                            selector["activate"] = self.strategy_vars[class_name].get()
                
                # 保存更新的配置
                with open("configs.json", 'w', encoding='utf-8') as f:
                    json.dump(self.config_data, f, indent=2, ensure_ascii=False)
                
                # 运行选股
                select_main()
                
                # 加载结果
                self.load_selection_results()
                
                self.status_var.set("就绪")
                messagebox.showinfo("完成", "选股完成！")
                
            except Exception as e:
                self.status_var.set("就绪")
                messagebox.showerror("错误", f"选股失败: {e}")
                
        thread = threading.Thread(target=select_worker, daemon=True)
        thread.start()
        
    def load_selection_results(self):
        """加载选股结果"""
        try:
            # 清空现有结果
            for item in self.result_tree.get_children():
                self.result_tree.delete(item)
            
            # 读取日志文件获取结果
            log_file = Path("select_results.log")
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # 解析日志获取选股结果
                current_strategy = ""
                for line in lines:
                    line = line.strip()
                    if "选股结果" in line and "策略" in line:
                        # 提取策略名称
                        if "[" in line and "]" in line:
                            current_strategy = line.split("[")[1].split("]")[0]
                    elif line and not line.startswith("[INFO]") and not line.startswith("[WARNING]"):
                        # 假设这是股票代码
                        if current_strategy and len(line) == 6 and line.isdigit():
                            self.result_tree.insert('', 'end', values=(
                                current_strategy, line, f"股票{line}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ))
                            
        except Exception as e:
            logging.error(f"加载选股结果失败: {e}")
            
    def view_results(self):
        """查看详细结果"""
        try:
            log_file = Path("select_results.log")
            if log_file.exists():
                os.startfile(str(log_file))
            else:
                messagebox.showwarning("提示", "未找到结果文件")
        except Exception as e:
            messagebox.showerror("错误", f"打开结果文件失败: {e}")
            
    def export_results(self):
        """导出结果"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                # 导出表格数据到CSV
                import csv
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['策略', '股票代码', '股票名称', '选中时间'])
                    for item in self.result_tree.get_children():
                        values = self.result_tree.item(item)['values']
                        writer.writerow(values)
                messagebox.showinfo("完成", f"结果已导出到: {filename}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")
            
    def load_config_file(self):
        """加载配置文件"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                self.update_strategy_checkboxes()
                self.update_config_text()
                messagebox.showinfo("完成", "配置文件加载成功")
            except Exception as e:
                messagebox.showerror("错误", f"加载配置文件失败: {e}")
                
    def save_config_file(self):
        """保存配置文件"""
        try:
            # 从文本框获取配置
            config_text = self.config_text.get(1.0, tk.END).strip()
            self.config_data = json.loads(config_text)
            
            # 保存到文件
            with open("configs.json", 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            
            self.update_strategy_checkboxes()
            messagebox.showinfo("完成", "配置文件保存成功")
        except json.JSONDecodeError as e:
            messagebox.showerror("错误", f"JSON格式错误: {e}")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置文件失败: {e}")
            
    def reset_config(self):
        """重置为默认配置"""
        if messagebox.askyesno("确认", "确定要重置为默认配置吗？"):
            self.load_config()
            
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        
    def refresh_log(self):
        """刷新日志"""
        # 这里可以重新加载日志文件
        pass
        
    def save_log(self):
        """保存日志"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("完成", f"日志已保存到: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存日志失败: {e}")


def main():
    """主函数"""
    root = tk.Tk()
    app = StockTradingGUI(root)
    
    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # 设置窗口关闭事件
    def on_closing():
        if messagebox.askokcancel("退出", "确定要退出程序吗？"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 启动主循环
    root.mainloop()


if __name__ == "__main__":
    main()