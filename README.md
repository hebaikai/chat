# 小游戏图片服务器

这是一个用于微信小程序的图片上传和存储服务器，使用 Python Flask 框架开发。

## 功能特性

- ✅ 用户头像上传
- ✅ 动态图片上传（支持批量上传，最多9张）
- ✅ 图片访问接口
- ✅ 跨域支持（CORS）
- ✅ 自动生成唯一文件名

## 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install Flask flask-cors
```

## 启动服务器

### 方式1：直接运行（推荐）

```bash
python app.py
```

### 方式2：使用启动脚本

双击运行 `start_server.bat` 文件

服务器将在 `http://localhost:5000` 启动

## API 接口说明

### 1. 健康检查
- **路径**: `/api/health`
- **方法**: GET
- **说明**: 检查服务器是否正常运行

### 2. 上传头像
- **路径**: `/api/upload/avatar`
- **方法**: POST
- **参数**:
  - `file`: 图片文件（表单形式）
- **返回**:
  ```json
  {
    "success": true,
    "url": "http://localhost:5000/images/avatars/20250127120000_xxx.jpg",
    "msg": "上传成功"
  }
  ```

### 3. 上传单张动态图片
- **路径**: `/api/upload/feed`
- **方法**: POST
- **参数**:
  - `file`: 图片文件（表单形式）
- **返回**:
  ```json
  {
    "success": true,
    "url": "http://localhost:5000/images/feeds/20250127120000_xxx.jpg",
    "msg": "上传成功"
  }
  ```

### 4. 批量上传动态图片
- **路径**: `/api/upload/feed/batch`
- **方法**: POST
- **参数**:
  - `files`: 多个图片文件（表单形式，最多9张）
- **返回**:
  ```json
  {
    "success": true,
    "urls": [
      "http://localhost:5000/images/feeds/20250127120000_xxx.jpg",
      "http://localhost:5000/images/feeds/20250127120001_yyy.jpg"
    ],
    "count": 2,
    "msg": "成功上传2张图片"
  }
  ```

### 5. 获取头像图片
- **路径**: `/images/avatars/{filename}`
- **方法**: GET
- **说明**: 直接访问图片URL

### 6. 获取动态图片
- **路径**: `/images/feeds/{filename}`
- **方法**: GET
- **说明**: 直接访问图片URL

## 支持的图片格式

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

## 文件存储结构

```
小游戏后端/
├── app.py              # 主服务器文件
├── requirements.txt    # Python依赖
├── README.md          # 说明文档
├── start_server.bat   # Windows启动脚本
└── uploads/           # 图片存储目录（自动创建）
    ├── avatars/       # 用户头像
    └── feeds/         # 动态图片
```

## 修改服务器地址

如果需要部署到服务器，请修改 `app.py` 中的以下配置：

```python
SERVER_HOST = 'localhost'  # 改为服务器IP或域名
SERVER_PORT = 5000         # 改为需要的端口
```

## 注意事项

1. 确保已安装 Python 3.7 或更高版本
2. 图片文件会自动保存在 `uploads` 文件夹中
3. 每次上传的图片都会生成唯一的文件名，避免重名
4. 服务器支持跨域请求，可直接从小程序调用
5. 如果部署到云服务器，记得开放对应端口（默认5000）

## 小程序端调用示例

### 上传图片示例（TypeScript）

```typescript
// 上传单张图片
async uploadImage(filePath: string): Promise<string> {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: 'http://localhost:5000/api/upload/feed',
      filePath: filePath,
      name: 'file',
      success: (res) => {
        const data = JSON.parse(res.data)
        if (data.success) {
          resolve(data.url)
        } else {
          reject(data.msg)
        }
      },
      fail: reject
    })
  })
}

// 批量上传图片
async uploadImages(filePaths: string[]): Promise<string[]> {
  const uploadPromises = filePaths.map(path => this.uploadImage(path))
  return Promise.all(uploadPromises)
}
```

## 故障排除

### 问题：模块未找到
解决：运行 `pip install -r requirements.txt`

### 问题：端口已被占用
解决：修改 `app.py` 中的 `SERVER_PORT` 为其他端口

### 问题：小程序无法访问
解决：
1. 检查服务器是否启动
2. 检查IP地址和端口是否正确
3. 小程序开发时需要开启"不校验合法域名"选项
