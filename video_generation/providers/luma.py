import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
from video_generation.base import (
    BaseVideoGenerator, VideoProvider, TaskStatus,
    TextToVideoRequest, ImageToVideoRequest, SubjectReferenceRequest,
    VideoTaskResponse, VideoTaskStatus
)


class LumaVideoGenerator(BaseVideoGenerator):
    """Luma视频生成器
    
    文档：https://docs.lumalabs.ai/docs/video-generation
    """

    def __init__(self, api_key: str, api_secret: Optional[str] = None, model: Optional[str] = None):
        super().__init__(api_key, api_secret, model)
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"
        self.model = model or "ray-2"  # 默认使用 ray-2 模型

    def _get_provider(self) -> VideoProvider:
        return VideoProvider.LUMA

    def text_to_video(self, request: TextToVideoRequest) -> VideoTaskResponse:
        """文本生成视频"""
        url = f"{self.base_url}/generations"

        payload = {
            "prompt": request.prompt,
            "model": self.model,
            "resolution": request.resolution or "720p",  # 可选: 540p, 720p, 1080p, 4k
            "duration": f"{request.duration}s" if request.duration else "5s",
            "aspect_ratio": request.aspect_ratio or "16:9",
            "loop": request.loop if hasattr(request, 'loop') else False
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.fromisoformat(response["created_at"]),
            message=response.get("state")
        )

    def image_to_video(self, request: ImageToVideoRequest) -> VideoTaskResponse:
        """图片生成视频"""
        url = f"{self.base_url}/generations"

        payload = {
            "prompt": request.prompt,
            "model": self.model,
            "keyframes": {
                "frame0": {
                    "type": "image",
                    "url": request.image_url
                }
            },
            "aspect_ratio": request.aspect_ratio or "16:9",
            "loop": request.loop if hasattr(request, 'loop') else False
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.fromisoformat(response["created_at"]),
            message=response.get("state")
        )

    def subject_reference(self, request: SubjectReferenceRequest) -> VideoTaskResponse:
        """参考主体生成视频"""
        url = f"{self.base_url}/generations"

        payload = {
            "prompt": request.prompt,
            "model": self.model,
            "keyframes": {
                "frame0": {
                    "type": "image",
                    "url": request.reference_url
                }
            },
            "aspect_ratio": request.aspect_ratio or "16:9",
            "loop": request.loop if hasattr(request, 'loop') else False
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.fromisoformat(response["created_at"]),
            message=response.get("state")
        )

    def get_task_status(self, task_id: str) -> VideoTaskStatus:
        """获取任务状态"""
        url = f"{self.base_url}/generations/{task_id}"

        response = self._make_request(url, {}, method="GET")

        # 状态映射
        status_map = {
            "pending": TaskStatus.PENDING,
            "dreaming": TaskStatus.PROCESSING,
            "completed": TaskStatus.COMPLETED,
            "failed": TaskStatus.FAILED
        }

        return VideoTaskStatus(
            task_id=task_id,
            provider=self.provider,
            status=status_map.get(response["state"], TaskStatus.PENDING),
            progress=1.0 if response["state"] == "completed" else 0.0,
            video_url=response.get("assets", {}).get("video"),
            thumbnail_url=None,  # Luma API 没有提供缩略图
            error_message=response.get("failure_reason"),
            create_time=datetime.fromisoformat(response["created_at"]),
            update_time=datetime.now(),  # API 没有返回更新时间
            estimated_time=None  # API 没有返回预计时间
        )

    def _make_request(self, url: str, payload: Dict[str, Any], method: str = "POST") -> dict:
        """发起HTTP请求"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # 过滤None值
        payload = {k: v for k, v in payload.items() if v is not None}

        if method == "GET":
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()
        return response.json()
