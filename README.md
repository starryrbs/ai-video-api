# AI 视频生成 API

这是一个统一的AI视频生成API接口，支持多个视频生成服务提供商，包括通义千问和Vidu等。该项目提供了一个简单易用的接口，用于生成各种类型的AI视频。

## 支持的供应商

- 通义万相 (Tongyi)
- Vidu
- PixVerse AI
- Stability AI
- SiliconFlow
- Runway
- 智谱AI (Zhipu)
- Luma Labs

## 功能特点

- 支持多种视频生成方式：
  - 文本生成视频 (Text-to-Video)
  - 图片生成视频 (Image-to-Video)
  - 参考视频生成 (Subject Reference)
- 支持多个视频生成服务提供商
- 统一的API接口
- 异步任务处理
- 批量处理支持
- 进度跟踪和状态查询

## 安装

### 通过 pip 安装（推荐）

```bash
pip install ai-video-api
```

### 从源码安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/ai-video-api.git
cd ai-video-api
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

在使用之前，需要配置相应服务提供商的API密钥。创建`.env`文件并添加以下配置：

```bash
# 通义千问配置
TONGYI_API_KEY=your_tongyi_api_key
TONGYI_API_SECRET=your_tongyi_api_secret

# Vidu配置
VIDU_API_KEY=your_vidu_api_key
VIDU_API_SECRET=your_vidu_api_secret
```

## 运行示例

项目提供了完整的示例代码，位于`video_generation/example.py`。运行示例：

```bash
# 确保已激活虚拟环境
python video_generation/example.py
```

示例代码包含以下功能演示：
- 文本生成视频
- 图片生成视频
- 参考视频生成
- 批量处理

默认情况下，示例会运行参考视频生成功能。要运行其他示例，请修改`main()`函数中的注释：

```python
def main():
    # 取消注释要运行的示例
    text_to_video_example(default_generator)
    # image_to_video_example(default_generator)
    # subject_reference_example(default_generator)
    # batch_processing_example(default_generator)
```

## 使用示例

### 文本生成视频

```python
from video_generation.factory import VideoGeneratorFactory
from video_generation.base import TextToVideoRequest, VideoProvider

# 创建生成器实例
generator = VideoGeneratorFactory.create_generator(
    VideoProvider.TONGYI,
    "your_api_key"
)

# 创建请求
request = TextToVideoRequest(
    prompt="一只可爱的猫咪在花园里玩耍，阳光明媚，画面温馨",
    negative_prompt="模糊，低质量",
    width=1024,
    height=576,
    duration=4,
    fps=8,
    style="写实风格"
)

# 生成视频
response = generator.text_to_video(request)
```

### 图片生成视频

```python
from video_generation.base import ImageToVideoRequest

request = ImageToVideoRequest(
    image_url="your_image_url",
    prompt="让图片中的场景动起来",
    width=1024,
    height=576,
    duration=4,
    motion_strength=0.8
)

response = generator.image_to_video(request)
```

## 任务状态查询

```python
status = generator.get_task_status(task_id)
print(f"进度: {status.progress * 100:.1f}%")
print(f"状态: {status.status.value}")
print(f"视频URL: {status.video_url}")
```

## 注意事项

- 请确保您有足够的API调用额度
- 视频生成可能需要一定时间，建议使用异步方式处理
- 生成的视频URL有效期可能有限，请及时下载保存

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
