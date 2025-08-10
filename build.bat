@echo off
chcp 65001 >nul
echo ========================================
echo Z哥战法 GUI应用构建脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo.
echo 正在安装依赖包...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo 开始构建可执行文件...
python build_exe.py

echo.
echo 构建完成！按任意键退出...
pause >nul