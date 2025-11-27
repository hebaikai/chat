"""
测试脚本 - 测试图片上传功能
使用方法：python test_upload.py <图片路径>
"""

import requests
import sys
import os

SERVER_URL = 'http://localhost:5000'

def test_health():
    """测试服务器健康状态"""
    print("测试服务器健康检查...")
    try:
        response = requests.get(f'{SERVER_URL}/api/health')
        if response.status_code == 200:
            print("✓ 服务器运行正常")
            print(f"  响应: {response.json()}")
            return True
        else:
            print(f"✗ 服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 无法连接到服务器: {e}")
        print("  请确保服务器已启动 (python app.py)")
        return False

def test_upload_avatar(image_path):
    """测试头像上传"""
    print(f"\n测试头像上传: {image_path}")

    if not os.path.exists(image_path):
        print(f"✗ 文件不存在: {image_path}")
        return None

    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f'{SERVER_URL}/api/upload/avatar', files=files)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✓ 头像上传成功")
                print(f"  图片URL: {data['url']}")
                return data['url']
            else:
                print(f"✗ 上传失败: {data.get('msg')}")
                return None
        else:
            print(f"✗ 上传失败: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ 上传出错: {e}")
        return None

def test_upload_feed(image_path):
    """测试动态图片上传"""
    print(f"\n测试动态图片上传: {image_path}")

    if not os.path.exists(image_path):
        print(f"✗ 文件不存在: {image_path}")
        return None

    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f'{SERVER_URL}/api/upload/feed', files=files)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✓ 动态图片上传成功")
                print(f"  图片URL: {data['url']}")
                return data['url']
            else:
                print(f"✗ 上传失败: {data.get('msg')}")
                return None
        else:
            print(f"✗ 上传失败: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ 上传出错: {e}")
        return None

def test_get_image(image_url):
    """测试图片访问"""
    print(f"\n测试图片访问: {image_url}")

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            print("✓ 图片访问成功")
            print(f"  内容类型: {response.headers.get('Content-Type')}")
            print(f"  文件大小: {len(response.content)} 字节")
            return True
        else:
            print(f"✗ 图片访问失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 访问出错: {e}")
        return False

def main():
    print("=" * 50)
    print("图片服务器测试脚本")
    print("=" * 50)

    # 测试健康检查
    if not test_health():
        return

    # 检查是否提供了图片路径
    if len(sys.argv) < 2:
        print("\n使用方法: python test_upload.py <图片路径>")
        print("示例: python test_upload.py test.jpg")
        return

    image_path = sys.argv[1]

    # 测试头像上传
    avatar_url = test_upload_avatar(image_path)
    if avatar_url:
        test_get_image(avatar_url)

    # 测试动态图片上传
    feed_url = test_upload_feed(image_path)
    if feed_url:
        test_get_image(feed_url)

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == '__main__':
    main()
