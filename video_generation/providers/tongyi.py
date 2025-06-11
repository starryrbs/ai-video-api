import requests
from datetime import datetime
from typing import Optional
from video_generation.base import (
    BaseVideoGenerator, VideoProvider, TaskStatus,
    TextToVideoRequest, ImageToVideoRequest, SubjectReferenceRequest,
    VideoTaskResponse, VideoTaskStatus
)
from video_generation.size_adapter import VideoSizeAdapter, TongyiModel


class TongyiVideoGenerator(BaseVideoGenerator):
    """通义万相视频生成器"""

    def __init__(self, api_key: str, api_secret: Optional[str] = None, model: Optional[str] = None):
        super().__init__(api_key, api_secret, model)
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation"
        self.model = model or TongyiModel.T2V_TURBO.value

    def _get_provider(self) -> VideoProvider:
        return VideoProvider.TONGYI

    def text_to_video(self, request: TextToVideoRequest) -> VideoTaskResponse:
        """文本生成视频"""
        url = f"{self.base_url}/video-synthesis"

        # 使用尺寸适配器获取合适的尺寸
        width, height = VideoSizeAdapter.adapt_size(
            request.width,
            request.height,
            self.provider,
            self.model
        )

        payload = {
            "model": self.model,
            "input": {
                "prompt": request.prompt
            },
            "parameters": {
                "size": VideoSizeAdapter.get_size_string(width, height)
            }
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"  # 启用异步调用
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return VideoTaskResponse(
            task_id=data["output"]["task_id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.now(),
            message=data.get("message")
        )

    def image_to_video(self, request: ImageToVideoRequest) -> VideoTaskResponse:
        """图片生成视频"""
        url = f"{self.base_url}/video-synthesis"

        # 使用尺寸适配器获取合适的尺寸
        width, height = VideoSizeAdapter.adapt_size(
            request.width,
            request.height,
            self.provider,
            self.model,  # 默认使用turbo模型
        )

        payload = {
            "model": self.model,  # 或使用 wanx2.1-i2v-plus
            "input": {
                "image_url": request.image_url,
                "prompt": request.prompt
            },
            "parameters": {
                "size": VideoSizeAdapter.get_size_string(width, height),
                "motion_strength": request.motion_strength if request.motion_strength else 0.5  # 默认值为0.5
            }
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"  # 启用异步调用
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return VideoTaskResponse(
            task_id=data["output"]["task_id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.now(),
            message=data.get("message")
        )

    def subject_reference(self, request: SubjectReferenceRequest) -> VideoTaskResponse:
        """参考主体生成视频"""
        url = f"{self.base_url}/video-synthesis"

        # 使用尺寸适配器获取合适的尺寸
        width, height = VideoSizeAdapter.adapt_size(
            request.width,
            request.height,
            self.provider,
            self.model
        )

        payload = {
            "model": self.model,
            "input": {
                "function": "image_reference",
                "prompt": request.prompt,
                "ref_images_url": [request.reference_url]
            },
            "parameters": {
                "obj_or_bg": ["obj"],  # 指定参考图为对象
                "size": VideoSizeAdapter.get_size_string(width, height)
            }
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"  # 启用异步调用
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return VideoTaskResponse(
            task_id=data["output"]["task_id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.now(),
            message=data.get("message")
        )

    def get_task_status(self, task_id: str) -> VideoTaskStatus:
        """获取任务状态"""
        url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # 通义万相状态映射
        status_map = {
            "PENDING": TaskStatus.PENDING,
            "RUNNING": TaskStatus.PROCESSING,
            "SUCCEEDED": TaskStatus.COMPLETED,
            "FAILED": TaskStatus.FAILED,
            "CANCELED": TaskStatus.FAILED,
            "UNKNOWN": TaskStatus.FAILED
        }

        output = data.get("output", {})

        return VideoTaskStatus(
            task_id=task_id,
            provider=self.provider,
            status=status_map.get(output.get("task_status"), TaskStatus.PENDING),
            progress=1.0 if output.get("task_status") == "SUCCEEDED" else 0.0,
            video_url=output.get("video_url"),
            thumbnail_url=None,  # API不返回缩略图
            error_message=output.get("message") if output.get("task_status") == "FAILED" else None,
            create_time=datetime.fromisoformat(output.get("submit_time")) if output.get(
                "submit_time") else datetime.now(),
            update_time=datetime.fromisoformat(output.get("end_time")) if output.get("end_time") else datetime.now(),
            estimated_time=None  # API不返回预计时间
        )

    def _make_request(self, url: str, payload: dict) -> dict:
        """发起HTTP请求"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"  # 启用异步调用
        }

        # 过滤None值
        def filter_none(obj):
            if isinstance(obj, dict):
                return {k: filter_none(v) for k, v in obj.items() if v is not None}
            return obj

        payload = filter_none(payload)

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
