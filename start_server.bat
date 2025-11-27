@echo off
chcp 65001 > nul
echo =====================================
echo     小游戏图片服务器启动脚本
echo =====================================
echo.

echo [1/3] 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)
echo.

echo [2/3] 检查依赖...
pip show Flask > nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo 依赖已就绪
)
echo.

echo [3/3] 启动服务器...
echo.
echo =====================================
echo   服务器地址: http://localhost:5000
echo   按 Ctrl+C 可停止服务器
echo =====================================
echo.

python app.py

pause
