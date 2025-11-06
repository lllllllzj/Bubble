#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包压缩脚本 - 移除隔离属性后再压缩
"""

import os
import sys
import subprocess
from datetime import datetime


def remove_quarantine(app_path):
    """移除隔离属性"""
    print(f"🔧 移除隔离属性...")
    try:
        # 移除扩展属性
        subprocess.run(['xattr', '-cr', app_path], check=True)
        print(f"✅ 已移除隔离属性")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  移除隔离属性失败: {e}")
        return False


def compress_app():
    """压缩应用"""
    app_path = "dist/礼物气泡.app"

    if not os.path.exists(app_path):
        print(f"❌ 错误: 找不到 {app_path}")
        print("请先运行: python3 build.py")
        return False

    print(f"\n📦 开始打包 macOS 应用...\n")

    # 1. 移除隔离属性
    remove_quarantine(app_path)

    # 2. 压缩
    version = datetime.now().strftime("%Y%m%d")
    zip_name = f"礼物气泡-macOS-{version}.zip"

    print(f"\n📦 正在压缩...")
    try:
        subprocess.run([
            'ditto', '-c', '-k', '--keepParent',
            app_path, zip_name
        ], check=True)

        size = os.path.getsize(zip_name) / (1024 * 1024)
        print(f"✅ 压缩完成!")
        print(f"📂 文件: {zip_name}")
        print(f"📊 大小: {size:.2f} MB")

        return True
    except Exception as e:
        print(f"❌ 压缩失败: {e}")
        return False


def create_install_guide():
    """创建安装说明"""
    guide = """# 🎁 礼物气泡 - 安装指南

## 📥 安装步骤

1. 下载 `礼物气泡-macOS-*.zip`
2. 解压得到 `礼物气泡.app`
3. 双击运行

## ⚠️ 无法打开的解决方法

如果提示 "无法打开，因为无法验证开发者"：

### 方法 1: 右键打开 (推荐)
1. 按住 **Control** 键，点击 `礼物气泡.app`
2. 选择 **"打开"**
3. 在弹出对话框中点击 **"打开"**

### 方法 2: 使用终端
1. 打开 **终端** (Terminal)
2. 输入以下命令（将路径替换为实际路径）:
    bash xattr -cr /Applications/礼物气泡.app
    3. 再双击运行

    ### 方法 3: 系统设置
    1. 打开 **系统设置** > **隐私与安全性**
    2. 找到被拦截的应用提示
    3. 点击 **"仍要打开"**

    ## 💡 为什么会被拦截？

    这是 macOS 的安全机制，因为应用没有 Apple 开发者签名。
    这是正常的，应用本身是安全的。

    ## 系统要求

    - macOS 10.13 或更高版本
    - 无需安装 Python

    ## ❓ 问题反馈

    如仍无法运行，请联系开发者。
    """

    with open("安装指南.md", 'w', encoding='utf-8') as f:
        f.write(guide)

    print(f"\n📄 已创建: 安装指南.md")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("📦 礼物气泡 - macOS 打包工具")
    print("=" * 60 + "\n")

    if compress_app():
        create_install_guide()
        print("\n" + "=" * 60)
        print("🎉 打包完成!")
        print("=" * 60)
        print("\n📤 上传文件:")
        print("   1. 礼物气泡-macOS-*.zip")
        print("   2. 安装指南.md")
        print("\n💡 用户下载后按照安装指南操作即可\n")
    else:
        sys.exit(1)