#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一打包脚本 - 自动识别系统并打包
支持 macOS 和 Windows
"""

import os
import sys
import shutil
import platform
import subprocess


def clean_build():
    """清理之前的构建文件"""
    print("🧹 清理旧的构建文件...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['script.spec']

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   删除: {dir_name}/")

    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"   删除: {file_name}")

    print("✅ 清理完成\n")


def check_pyinstaller():
    """检查是否安装了 PyInstaller"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller 已安装 (版本: {PyInstaller.__version__})\n")
        return True
    except ImportError:
        print("❌ 未安装 PyInstaller")
        print("正在安装 PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller 安装成功\n")
            return True
        except:
            print("❌ PyInstaller 安装失败")
            return False


def build_macos():
    """在 macOS 上打包"""
    print("🍎 检测到 macOS 系统")
    print("📦 开始打包 Mac 应用...\n")

    cmd = [
        'pyinstaller',
        '--name=礼物气泡',
        '--windowed',  # 不显示控制台
        '--onefile',  # 打包成单个文件
        '--clean',
        '--noconfirm',
        '--osx-bundle-identifier=com.gift.bubble',
        'script.py'
    ]

    try:
        subprocess.check_call(cmd)
        print("\n✅ Mac 应用打包成功!")
        print(f"📂 输出位置: dist/礼物气泡.app")
        print("\n💡 使用说明:")
        print("   1. 在 Finder 中打开 dist 文件夹")
        print("   2. 双击 '礼物气泡.app' 运行")
        print("   3. 如果提示无法验证开发者,运行以下命令:")
        print("      xattr -cr dist/礼物气泡.app")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ 打包失败")
        return False


def build_windows():
    """在 Windows 上打包"""
    print("🪟 检测到 Windows 系统")
    print("📦 开始打包 Windows 应用...\n")

    cmd = [
        'pyinstaller',
        '--name=礼物气泡',
        '--noconsole',  # 不显示控制台
        '--onefile',  # 打包成单个文件
        '--clean',
        '--noconfirm',
        'script.py'
    ]

    try:
        subprocess.check_call(cmd)
        print("\n✅ Windows 应用打包成功!")
        print(f"📂 输出位置: dist\\礼物气泡.exe")
        print("\n💡 使用说明:")
        print("   1. 在文件资源管理器中打开 dist 文件夹")
        print("   2. 双击 '礼物气泡.exe' 运行")
        print("   3. 如果被杀毒软件拦截,请添加到白名单")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ 打包失败")
        return False


def build_linux():
    """在 Linux 上打包"""
    print("🐧 检测到 Linux 系统")
    print("📦 开始打包 Linux 应用...\n")

    cmd = [
        'pyinstaller',
        '--name=礼物气泡',
        '--onefile',
        '--clean',
        '--noconfirm',
        'script.py'
    ]

    try:
        subprocess.check_call(cmd)
        print("\n✅ Linux 应用打包成功!")
        print(f"📂 输出位置: dist/礼物气泡")
        print("\n💡 使用说明:")
        print("   1. 打开终端,进入 dist 文件夹")
        print("   2. 运行: chmod +x 礼物气泡")
        print("   3. 运行: ./礼物气泡")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ 打包失败")
        return False


def get_file_size(filepath):
    """获取文件大小"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def show_build_info():
    """显示打包信息"""
    print("\n" + "=" * 60)
    print("📊 打包信息")
    print("=" * 60)

    system = platform.system()
    if system == "Darwin":
        app_path = "dist/礼物气泡.app"
        if os.path.exists(app_path):
            print(f"应用名称: 礼物气泡.app")
            print(f"系统平台: macOS")
            print(f"输出路径: {os.path.abspath(app_path)}")
    elif system == "Windows":
        exe_path = "dist/礼物气泡.exe"
        if os.path.exists(exe_path):
            size = get_file_size(exe_path)
            print(f"应用名称: 礼物气泡.exe")
            print(f"系统平台: Windows")
            print(f"文件大小: {size}")
            print(f"输出路径: {os.path.abspath(exe_path)}")
    elif system == "Linux":
        app_path = "dist/礼物气泡"
        if os.path.exists(app_path):
            size = get_file_size(app_path)
            print(f"应用名称: 礼物气泡")
            print(f"系统平台: Linux")
            print(f"文件大小: {size}")
            print(f"输出路径: {os.path.abspath(app_path)}")

    print("=" * 60 + "\n")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🎁 礼物气泡 - 打包工具")
    print("=" * 60 + "\n")

    # 检查 script.py 是否存在
    if not os.path.exists('script.py'):
        print("❌ 错误: 找不到 script.py 文件")
        print("请确保在项目根目录下运行此脚本")
        return 1

    # 检查 PyInstaller
    if not check_pyinstaller():
        return 1

    # 清理旧文件
    clean_build()

    # 根据系统选择打包方式
    system = platform.system()
    print(f"🖥️  当前系统: {system} ({platform.machine()})")
    print(f"🐍 Python 版本: {sys.version.split()[0]}\n")

    success = False
    if system == "Darwin":  # macOS
        success = build_macos()
    elif system == "Windows":
        success = build_windows()
    elif system == "Linux":
        success = build_linux()
    else:
        print(f"❌ 不支持的系统: {system}")
        return 1

    if success:
        show_build_info()
        print("🎉 打包完成!\n")
        return 0
    else:
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户取消打包")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)