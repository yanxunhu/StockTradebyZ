# Z哥战法 GUI版本使用指南

## 概述

这是Z哥战法的图形用户界面(GUI)版本，提供了友好的可视化操作界面，支持编译为独立的可执行文件(.exe)。

## 功能特性

### 🖥️ 图形界面功能
- **数据获取**: 可视化配置股票数据下载参数
- **策略选股**: 图形化选择和配置交易策略
- **配置管理**: 可视化编辑策略配置文件
- **日志查看**: 实时查看程序运行日志
- **结果展示**: 表格形式展示选股结果

### 📊 支持的策略
- **BBIKDJSelector** (少妇战法)
- **PeakKDJSelector** (填坑战法)
- **BBIShortLongSelector** (补票战法)
- **BreakoutVolumeKDJSelector** (TePu战法)

## 快速开始

### 方式一：直接运行Python脚本

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行GUI程序**
   ```bash
   python gui_main.py
   ```

### 方式二：构建可执行文件

1. **自动构建** (推荐)
   ```bash
   # Windows用户直接双击运行
   build.bat
   
   # 或者命令行运行
   python build_exe.py
   ```

2. **手动构建**
   ```bash
   # 安装Nuitka
   pip install nuitka
   
   # 构建可执行文件
   python -m nuitka --standalone --onefile --windows-disable-console --enable-plugin=tk-inter gui_main.py
   ```

3. **运行可执行文件**
   - 构建完成后，在 `dist` 目录下找到 `ZStockTrader.exe`
   - 双击运行即可

## 界面说明

### 📈 数据获取页面
- **市值范围**: 设置筛选股票的市值范围（亿元）
- **数据源**: 选择数据来源（AkShare/Tushare/Mootdx）
- **日期范围**: 设置获取数据的时间范围
- **选项**: 增量更新、小盘股模式等

### 🎯 策略选股页面
- **策略选择**: 勾选要使用的交易策略
- **开始选股**: 执行选股算法
- **结果查看**: 表格显示选股结果
- **结果导出**: 将结果导出为CSV文件

### ⚙️ 配置管理页面
- **配置编辑**: 直接编辑JSON配置文件
- **加载/保存**: 导入导出配置文件
- **重置默认**: 恢复默认配置

### 📋 日志查看页面
- **实时日志**: 显示程序运行的实时日志
- **日志操作**: 清空、刷新、保存日志

## 配置文件说明

程序使用 `configs.json` 文件存储策略配置，主要结构：

```json
{
  "selectors": [
    {
      "class": "BBIKDJSelector",
      "alias": "少妇战法",
      "activate": true,
      "params": {
        "j_threshold": 10,
        "bbi_min_window": 20,
        "max_window": 60,
        "price_range_pct": 1,
        "bbi_q_threshold": 0.3,
        "j_q_threshold": 0.10
      }
    }
  ]
}
```

## 使用流程

1. **首次使用**
   - 启动程序
   - 切换到"数据获取"页面
   - 配置参数并获取股票数据

2. **策略选股**
   - 切换到"策略选股"页面
   - 选择要使用的策略
   - 点击"开始选股"
   - 查看选股结果

3. **配置调整**
   - 切换到"配置管理"页面
   - 修改策略参数
   - 保存配置

4. **结果分析**
   - 在"策略选股"页面查看结果表格
   - 导出结果进行进一步分析
   - 在"日志查看"页面查看详细日志

## 文件结构

```
StockTradebyZ/
├── gui_main.py          # GUI主程序
├── build_exe.py         # 可执行文件构建脚本
├── build.bat           # Windows构建批处理文件
├── configs.json        # 策略配置文件
├── requirements.txt    # Python依赖包
├── data/              # 股票数据目录（自动创建）
├── dist/              # 可执行文件输出目录
└── select_results.log # 选股结果日志
```

## 系统要求

- **操作系统**: Windows 7/8/10/11
- **Python版本**: 3.7 或更高版本
- **内存**: 建议 4GB 以上
- **磁盘空间**: 建议 2GB 以上（用于存储股票数据）

## 常见问题

### Q: 构建可执行文件失败怎么办？
A: 
1. 确保Python版本 >= 3.7
2. 检查是否正确安装了所有依赖包
3. 尝试手动安装Nuitka: `pip install nuitka`
4. 查看错误信息，通常是缺少某个依赖包

### Q: 程序运行时提示模块导入错误？
A:
1. 确保在正确的目录下运行程序
2. 检查是否安装了requirements.txt中的所有依赖
3. 尝试重新安装依赖: `pip install -r requirements.txt`

### Q: 数据获取失败怎么办？
A:
1. 检查网络连接
2. 尝试更换数据源（AkShare/Tushare/Mootdx）
3. 检查Tushare token配置（如果使用Tushare）

### Q: 选股结果为空？
A:
1. 确保已经获取了股票数据
2. 检查策略参数是否过于严格
3. 尝试调整策略配置参数

## 技术支持

如果遇到问题，请：
1. 查看"日志查看"页面的错误信息
2. 检查 `select_results.log` 和 `fetch.log` 文件
3. 参考原项目的README.md文件
4. 在GitHub项目页面提交Issue

## 更新日志

### v1.0.0 (2024-01-XX)
- ✨ 新增图形用户界面
- 🚀 支持Nuitka编译为可执行文件
- 📊 可视化策略配置和结果展示
- 📋 实时日志查看功能
- 💾 结果导出功能

---

**注意**: 本工具仅供学习和研究使用，不构成投资建议。投资有风险，入市需谨慎。