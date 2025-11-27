from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
UPLOAD_FOLDER = 'uploads'
AVATAR_FOLDER = os.path.join(UPLOAD_FOLDER, 'avatars')
FEED_FOLDER = os.path.join(UPLOAD_FOLDER, 'feeds')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# 创建上传文件夹
os.makedirs(AVATAR_FOLDER, exist_ok=True)
os.makedirs(FEED_FOLDER, exist_ok=True)

# 获取服务器地址（可以根据实际部署情况修改）
SERVER_HOST = 'localhost'
SERVER_PORT = 5000
BASE_URL = f'http://{SERVER_HOST}:{SERVER_PORT}'

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(original_filename):
    """生成唯一的文件名"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{timestamp}_{unique_id}.{ext}"

@app.route('/api/upload/avatar', methods=['POST'])
def upload_avatar():
    """上传用户头像"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'msg': '没有文件'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'success': False, 'msg': '没有选择文件'}), 400

        if file and allowed_file(file.filename):
            filename = generate_filename(file.filename)
            filepath = os.path.join(AVATAR_FOLDER, filename)
            file.save(filepath)

            # 返回图片URL
            image_url = f"{BASE_URL}/images/avatars/{filename}"

            return jsonify({
                'success': True,
                'url': image_url,
                'msg': '上传成功'
            })
        else:
            return jsonify({'success': False, 'msg': '不支持的文件格式'}), 400

    except Exception as e:
        print(f"上传头像失败: {str(e)}")
        return jsonify({'success': False, 'msg': str(e)}), 500

@app.route('/api/upload/feed', methods=['POST'])
def upload_feed_image():
    """上传动态图片"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'msg': '没有文件'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'success': False, 'msg': '没有选择文件'}), 400

        if file and allowed_file(file.filename):
            filename = generate_filename(file.filename)
            filepath = os.path.join(FEED_FOLDER, filename)
            file.save(filepath)

            # 返回图片URL
            image_url = f"{BASE_URL}/images/feeds/{filename}"

            return jsonify({
                'success': True,
                'url': image_url,
                'msg': '上传成功'
            })
        else:
            return jsonify({'success': False, 'msg': '不支持的文件格式'}), 400

    except Exception as e:
        print(f"上传动态图片失败: {str(e)}")
        return jsonify({'success': False, 'msg': str(e)}), 500

@app.route('/api/upload/feed/batch', methods=['POST'])
def upload_feed_images_batch():
    """批量上传动态图片（最多9张）"""
    try:
        files = request.files.getlist('files')

        if not files or len(files) == 0:
            return jsonify({'success': False, 'msg': '没有文件'}), 400

        if len(files) > 9:
            return jsonify({'success': False, 'msg': '最多只能上传9张图片'}), 400

        uploaded_urls = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = generate_filename(file.filename)
                filepath = os.path.join(FEED_FOLDER, filename)
                file.save(filepath)

                image_url = f"{BASE_URL}/images/feeds/{filename}"
                uploaded_urls.append(image_url)

        if len(uploaded_urls) == 0:
            return jsonify({'success': False, 'msg': '没有有效的图片文件'}), 400

        return jsonify({
            'success': True,
            'urls': uploaded_urls,
            'count': len(uploaded_urls),
            'msg': f'成功上传{len(uploaded_urls)}张图片'
        })

    except Exception as e:
        print(f"批量上传图片失败: {str(e)}")
        return jsonify({'success': False, 'msg': str(e)}), 500

@app.route('/images/avatars/<filename>')
def get_avatar(filename):
    """获取头像图片"""
    try:
        return send_from_directory(AVATAR_FOLDER, filename)
    except Exception as e:
        print(f"获取头像失败: {str(e)}")
        return jsonify({'success': False, 'msg': '图片不存在'}), 404

@app.route('/images/feeds/<filename>')
def get_feed_image(filename):
    """获取动态图片"""
    try:
        return send_from_directory(FEED_FOLDER, filename)
    except Exception as e:
        print(f"获取动态图片失败: {str(e)}")
        return jsonify({'success': False, 'msg': '图片不存在'}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'success': True,
        'status': 'running',
        'msg': '服务器运行正常'
    })

if __name__ == '__main__':
    print(f"图片服务器启动中...")
    print(f"服务器地址: {BASE_URL}")
    print(f"头像上传接口: {BASE_URL}/api/upload/avatar")
    print(f"动态图片上传接口: {BASE_URL}/api/upload/feed")
    print(f"批量上传接口: {BASE_URL}/api/upload/feed/batch")
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=True)
