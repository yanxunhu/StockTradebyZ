#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for creating executable using Nuitka
Z哥战法 GUI版本打包脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    """使用Nuitka构建可执行文件"""
    
    # 检查Nuitka是否安装
    try:
        import nuitka
        print(f"✓ Nuitka已安装，版本: {nuitka.__version__}")
    except ImportError:
        print("❌ Nuitka未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "nuitka"], check=True)
        print("✓ Nuitka安装完成")
    
    # 项目根目录
    project_root = Path(__file__).parent
    main_script = project_root / "gui_main.py"
    
    if not main_script.exists():
        print(f"❌ 主脚本文件不存在: {main_script}")
        return False
    
    # 构建命令
    build_cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",  # 独立模式，包含所有依赖
        "--onefile",     # 单文件模式
        "--windows-disable-console",  # Windows下隐藏控制台窗口
        "--enable-plugin=tk-inter",   # 启用tkinter插件
        "--include-data-dir=.",       # 包含当前目录的数据文件
        "--output-filename=ZStockTrader.exe",  # 输出文件名
        "--output-dir=dist",          # 输出目录
        "--remove-output",            # 清理之前的构建
        "--assume-yes-for-downloads", # 自动下载依赖
        "--show-progress",            # 显示进度
        "--show-memory",              # 显示内存使用
        str(main_script)
    ]
    
    # 添加Windows特定选项
    if sys.platform == "win32":
        build_cmd.extend([
            "--windows-icon-from-ico=icon.ico" if Path("icon.ico").exists() else "",
            "--product-name=Z哥战法股票策略选择器",
            "--file-description=专业的A股量化选股工具",
            "--product-version=1.0.0",
            "--file-version=1.0.0.0",
            "--copyright=Copyright (c) 2024"
        ])
        # 移除空字符串
        build_cmd = [cmd for cmd in build_cmd if cmd]
    
    print("🚀 开始构建可执行文件...")
    print(f"构建命令: {' '.join(build_cmd)}")
    
    try:
        # 创建输出目录
        os.makedirs("dist", exist_ok=True)
        
        # 执行构建
        result = subprocess.run(build_cmd, cwd=project_root, check=True)
        
        if result.returncode == 0:
            exe_path = project_root / "dist" / "ZStockTrader.exe"
            if exe_path.exists():
                print(f"✅ 构建成功！可执行文件位置: {exe_path}")
                print(f"文件大小: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
                return True
            else:
                print("❌ 构建完成但未找到可执行文件")
                return False
        else:
            print(f"❌ 构建失败，返回码: {result.returncode}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建过程中出错: {e}")
        return False
    except Exception as e:
        print(f"❌ 构建失败: {e}")
        return False

def install_dependencies():
    """安装构建依赖"""
    print("📦 检查并安装依赖...")
    
    dependencies = [
        "nuitka",
        "ordered-set",  # Nuitka依赖
        "zstandard",    # 压缩支持
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✓ {dep} 已安装")
        except ImportError:
            print(f"📥 正在安装 {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"✓ {dep} 安装完成")

def create_icon():
    """创建应用图标（SVG格式）"""
    icon_svg = '''
<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4CAF50;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2E7D32;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- 背景圆形 -->
  <circle cx="32" cy="32" r="30" fill="url(#grad1)" stroke="#1B5E20" stroke-width="2"/>
  
  <!-- 股票图表线条 -->
  <polyline points="8,45 16,35 24,40 32,25 40,30 48,20 56,25" 
            fill="none" stroke="white" stroke-width="3" stroke-linecap="round"/>
  
  <!-- 数据点 -->
  <circle cx="16" cy="35" r="2" fill="white"/>
  <circle cx="24" cy="40" r="2" fill="white"/>
  <circle cx="32" cy="25" r="2" fill="white"/>
  <circle cx="40" cy="30" r="2" fill="white"/>
  <circle cx="48" cy="20" r="2" fill="white"/>
  
  <!-- Z字母 -->
  <text x="32" y="52" font-family="Arial, sans-serif" font-size="16" font-weight="bold" 
        text-anchor="middle" fill="white">Z</text>
</svg>
'''
    
    with open("icon.svg", "w", encoding="utf-8") as f:
        f.write(icon_svg)
    print("✓ 应用图标已创建 (icon.svg)")

def main():
    """主函数"""
    print("🔨 Z哥战法 GUI应用构建工具")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return
    
    print(f"✓ Python版本: {sys.version}")
    print(f"✓ 平台: {sys.platform}")
    
    # 创建图标
    create_icon()
    
    # 安装依赖
    install_dependencies()
    
    # 构建可执行文件
    success = build_executable()
    
    if success:
        print("\n🎉 构建完成！")
        print("\n📋 使用说明:")
        print("1. 可执行文件位于 dist/ZStockTrader.exe")
        print("2. 首次运行前请确保configs.json文件在同一目录")
        print("3. 程序会自动创建data目录存储股票数据")
        print("4. 选股结果会保存在select_results.log文件中")
    else:
        print("\n❌ 构建失败，请检查错误信息")
        print("\n🔧 故障排除:")
        print("1. 确保所有依赖已正确安装")
        print("2. 检查Python环境是否完整")
        print("3. 尝试手动安装nuitka: pip install nuitka")
        print("4. 查看详细错误信息并搜索解决方案")

if __name__ == "__main__":
    main()