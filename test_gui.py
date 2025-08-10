#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI测试脚本
用于验证GUI应用的基本功能
"""

import sys
import os
import json
from pathlib import Path

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        import tkinter as tk
        print("✓ tkinter 导入成功")
    except ImportError as e:
        print(f"❌ tkinter 导入失败: {e}")
        return False
    
    try:
        from tkinter import ttk, messagebox, filedialog, scrolledtext
        print("✓ tkinter 子模块导入成功")
    except ImportError as e:
        print(f"❌ tkinter 子模块导入失败: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas 导入成功")
    except ImportError as e:
        print(f"❌ pandas 导入失败: {e}")
        return False
    
    try:
        import json
        print("✓ json 导入成功")
    except ImportError as e:
        print(f"❌ json 导入失败: {e}")
        return False
    
    return True

def test_project_files():
    """测试项目文件"""
    print("\n📁 测试项目文件...")
    
    required_files = [
        "gui_main.py",
        "build_exe.py",
        "configs.json",
        "requirements.txt",
        "Selector.py",
        "fetch_kline.py",
        "select_stock.py"
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file} 存在")
        else:
            print(f"❌ {file} 缺失")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_config_file():
    """测试配置文件"""
    print("\n⚙️ 测试配置文件...")
    
    try:
        with open("configs.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if "selectors" in config:
            print(f"✓ 配置文件格式正确，包含 {len(config['selectors'])} 个策略")
            
            for i, selector in enumerate(config['selectors']):
                if "class" in selector and "alias" in selector:
                    print(f"  - {selector['alias']} ({selector['class']})")
                else:
                    print(f"  ❌ 策略 {i+1} 格式不正确")
                    return False
            return True
        else:
            print("❌ 配置文件缺少 'selectors' 字段")
            return False
            
    except FileNotFoundError:
        print("❌ 配置文件 configs.json 不存在")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件 JSON 格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

def test_gui_creation():
    """测试GUI创建"""
    print("\n🖥️ 测试GUI创建...")
    
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # 创建测试窗口
        root = tk.Tk()
        root.title("测试窗口")
        root.geometry("300x200")
        
        # 添加一些基本组件
        ttk.Label(root, text="GUI测试成功！").pack(pady=20)
        ttk.Button(root, text="关闭", command=root.destroy).pack()
        
        print("✓ GUI组件创建成功")
        
        # 立即销毁窗口（不显示）
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ GUI创建失败: {e}")
        return False

def test_nuitka_availability():
    """测试Nuitka可用性"""
    print("\n🔨 测试Nuitka可用性...")
    
    try:
        import nuitka
        # 尝试获取版本，如果失败就检查是否可以导入
        try:
            version = nuitka.__version__
            print(f"✓ Nuitka已安装，版本: {version}")
        except AttributeError:
            # 某些版本的Nuitka可能没有__version__属性
            print("✓ Nuitka已安装")
        return True
    except ImportError:
        print("⚠️ Nuitka未安装，可以运行以下命令安装:")
        print("   pip install nuitka")
        return False

def main():
    """主测试函数"""
    print("🧪 Z哥战法 GUI应用测试")
    print("=" * 40)
    
    tests = [
        ("模块导入", test_imports),
        ("项目文件", test_project_files),
        ("配置文件", test_config_file),
        ("GUI创建", test_gui_creation),
        ("Nuitka可用性", test_nuitka_availability)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} 测试出错: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！GUI应用可以正常运行")
        print("\n📋 下一步操作:")
        print("1. 运行 GUI: python gui_main.py")
        print("2. 构建 EXE: python build_exe.py")
        print("3. 或使用批处理: build.bat")
    else:
        print("⚠️ 部分测试失败，请检查上述错误信息")
        print("\n🔧 建议操作:")
        print("1. 安装缺失的依赖: pip install -r requirements.txt")
        print("2. 检查项目文件完整性")
        print("3. 确保Python版本 >= 3.7")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)