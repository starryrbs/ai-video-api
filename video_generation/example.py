"""
视频生成系统使用示例
"""

import time
import os
from dotenv import load_dotenv
from video_generation.factory import VideoGeneratorFactory
from video_generation.base import (
    VideoProvider, TaskStatus,
    TextToVideoRequest, ImageToVideoRequest, SubjectReferenceRequest
)
from video_generation.size_adapter import TongyiModel


def process_task(generator, task_id):
    """通用任务处理函数"""
    print(f"任务ID: {task_id}")
    print("查询任务状态...")

    while True:
        status = generator.get_task_status(task_id)
        print(f"任务进度: {status.progress * 100:.1f}%")
        print(f"状态: {status.status.value}")

        if status.status == TaskStatus.COMPLETED:
            print(f"✅ 视频生成完成!")
            print(f"视频URL: {status.video_url}")
            print(f"缩略图URL: {status.thumbnail_url}")
            return status
        elif status.status == TaskStatus.FAILED:
            print(f"❌ 视频生成失败: {status.error_message}")
            return status
        else:
            print("⏳ 任务处理中，等待5秒后重试...")
            time.sleep(5)


def text_to_video_example(generator):
    """文本生成视频示例"""
    print("\n=== 文本生成视频示例 ===")
    text_request = TextToVideoRequest(
        prompt="一只可爱的猫咪在花园里玩耍，阳光明媚，画面温馨",
        negative_prompt="模糊，低质量",
        width=1024,
        height=576,
        duration=4,
        fps=8,
        style="写实风格"
    )

    print("创建文本生成视频任务...")
    task_response = generator.text_to_video(text_request)
    return process_task(generator, task_response.task_id)


def image_to_video_example(generator):
    """图片生成视频示例"""
    print("\n=== 图片生成视频示例 ===")
    image_request = ImageToVideoRequest(
        image_url="https://p3-search.byteimg.com/img/labis/c4f8e97f684dc590efe1507ca54935a9~480x480.JPEG",
        prompt="让图片中的场景动起来，添加轻微的风吹效果",
        width=1024,
        height=576,
        duration=4,
        motion_strength=0.8
    )

    print("创建图片生成视频任务...")
    task_response = generator.image_to_video(image_request)
    return process_task(generator, task_response.task_id)


def subject_reference_example(generator):
    """参考视频生成示例"""
    print("\n=== 参考视频生成示例 ===")
    reference_request = SubjectReferenceRequest(
        reference_url="https://p3-search.byteimg.com/img/labis/53b3c2c04762fff914f3867ee2f6f7c4~480x480.JPEG",
        prompt="保持相同的动作风格，但改变背景为森林场景",
        width=1024,
        height=576,
        duration=4,
        reference_strength=0.9
    )

    print("创建参考视频生成任务...")
    task_response = generator.subject_reference(reference_request)
    return process_task(generator, task_response.task_id)


def batch_processing_example(generator):
    """批量处理示例"""
    print("\n=== 批量处理示例 ===")
    task_ids = []

    # 创建多个任务
    for i in range(3):
        request = TextToVideoRequest(
            prompt=f"第{i + 1}个视频：美丽的风景",
            width=512,
            height=512,
            duration=3
        )
        response = generator.text_to_video(request)
        task_ids.append(response.task_id)
        print(f"创建任务 {i + 1}: {response.task_id}")

    # 批量查询状态
    print("\n查询所有任务状态:")
    for task_id in task_ids:
        status = generator.get_task_status(task_id)
        print(f"任务 {task_id}: {status.status.value} ({status.progress * 100:.1f}%)")


def main():
    """示例用法"""
    # 加载环境变量
    load_dotenv()

    # 配置API密钥
    config = {
        VideoProvider.TONGYI: {
            "api_key": os.getenv("TONGYI_API_KEY"),
            "api_secret": os.getenv("TONGYI_API_SECRET"),
            "model": TongyiModel.T2V_TURBO
        },
        VideoProvider.VIDU: {
            "api_key": os.getenv("VIDU_API_KEY"),
            "api_secret": os.getenv("VIDU_API_SECRET")
        }
    }

    # 创建生成器
    tongyi_generator = VideoGeneratorFactory.create_generator(
        VideoProvider.TONGYI,
        config[VideoProvider.TONGYI]["api_key"],
        config[VideoProvider.TONGYI]["api_secret"]
    )

    vidu_generator = VideoGeneratorFactory.create_generator(
        VideoProvider.VIDU,
        config[VideoProvider.VIDU]["api_key"],
        config[VideoProvider.VIDU]["api_secret"]
    )

    default_generator = tongyi_generator

    # 运行示例
    text_to_video_example(default_generator)
    image_to_video_example(default_generator)
    subject_reference_example(default_generator)
    batch_processing_example(default_generator)


def check_provider_support():
    """检查支持的供应商"""
    print("支持的视频生成供应商:")
    for provider in VideoGeneratorFactory.get_supported_providers():
        print(f"- {provider.value}")


if __name__ == "__main__":
    print("🎬 视频生成系统示例")
    print("=" * 50)

    check_provider_support()
    print("\n")

    # 注意：这里只是示例代码，实际运行需要有效的API密钥
    main()

    print("📝 使用说明:")
    print("1. 配置各供应商的API密钥")
    print("2. 创建对应的视频生成器实例")
    print("3. 构建请求参数")
    print("4. 调用相应的生成方法")
