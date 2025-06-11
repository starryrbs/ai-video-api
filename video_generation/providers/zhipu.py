import requests
from datetime import datetime
from typing import Optional
from video_generation.base import (
    BaseVideoGenerator, VideoProvider, TaskStatus,
    TextToVideoRequest, ImageToVideoRequest, SubjectReferenceRequest,
    VideoTaskResponse, VideoTaskStatus
)


class ZhipuVideoGenerator(BaseVideoGenerator):
    """智谱AI视频生成器"""

    def __init__(self, api_key: str, api_secret: Optional[str] = None, model: Optional[str] = None):
        super().__init__(api_key, api_secret, model)
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"
        self.model = model or "cogvideox"  # 默认使用 cogvideox 模型

    def _get_provider(self) -> VideoProvider:
        return VideoProvider.ZHIPU

    def text_to_video(self, request: TextToVideoRequest) -> VideoTaskResponse:
        """文本生成视频"""
        url = f"{self.base_url}/video/generations"

        payload = {
            "model": self.model,
            "prompt": request.prompt,
            "quality": request.quality or "speed",  # speed 或 quality
            "with_audio": request.with_audio or False,
            "size": request.resolution or "1920x1080",  # 支持多种分辨率
            "fps": request.fps or 30,  # 30 或 60
            "request_id": request.request_id,  # 可选，用户端唯一标识
            "user_id": request.user_id  # 可选，终端用户唯一ID
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["id"],  # 使用id作为task_id
            provider=self.provider,
            status=self._map_status(response["task_status"]),
            create_time=datetime.now(),  # API没有返回创建时间
            message=response["task_status"]
        )

    def image_to_video(self, request: ImageToVideoRequest) -> VideoTaskResponse:
        """图片生成视频"""
        url = f"{self.base_url}/video/generations"

        payload = {
            "model": self.model,
            "image_url": request.image_url,
            "prompt": request.prompt,  # 可选，与image_url二选一或同时传入
            "quality": request.quality or "speed",
            "with_audio": request.with_audio or False,
            "size": request.resolution or "1920x1080",
            "fps": request.fps or 30,
            "request_id": request.request_id,
            "user_id": request.user_id
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["id"],  # 使用id作为task_id
            provider=self.provider,
            status=self._map_status(response["task_status"]),
            create_time=datetime.now(),
            message=response["task_status"]
        )

    def subject_reference(self, request: SubjectReferenceRequest) -> VideoTaskResponse:
        """参考主体生成视频"""
        url = f"{self.base_url}/video/generations"

        payload = {
            "model": self.model,
            "image_url": request.reference_url,  # 使用reference_url作为image_url
            "prompt": request.prompt,
            "quality": request.quality or "speed",
            "with_audio": request.with_audio or False,
            "size": request.resolution or "1920x1080",
            "fps": request.fps or 30,
            "request_id": request.request_id,
            "user_id": request.user_id
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["id"],  # 使用id作为task_id
            provider=self.provider,
            status=self._map_status(response["task_status"]),
            create_time=datetime.now(),
            message=response["task_status"]
        )

    def get_task_status(self, task_id: str) -> VideoTaskStatus:
        """获取任务状态"""
        url = f"{self.base_url}/async-result/{task_id}"

        response = self._make_request(url, method="GET")

        # 获取视频结果
        video_result = response.get("video_result", [{}])[0] if response.get("video_result") else {}

        return VideoTaskStatus(
            task_id=task_id,
            provider=self.provider,
            status=self._map_status(response["task_status"]),
            progress=1.0 if response["task_status"] == "SUCCESS" else 0.0,
            video_url=video_result.get("url"),
            thumbnail_url=video_result.get("cover_image_url"),
            error_message=None if response["task_status"] != "FAIL" else "任务失败",
            create_time=datetime.now(),  # API没有返回创建时间
            update_time=datetime.now(),  # API没有返回更新时间
            estimated_time=None  # API没有返回预计时间
        )

    def _map_status(self, status: str) -> TaskStatus:
        """映射智谱AI的状态到通用状态"""
        status_map = {
            "PROCESSING": TaskStatus.PROCESSING,
            "SUCCESS": TaskStatus.COMPLETED,
            "FAIL": TaskStatus.FAILED
        }
        return status_map.get(status, TaskStatus.PENDING)

    def _make_request(self, url: str, payload: dict = None, method: str = "POST") -> dict:
        """发起HTTP请求"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        if payload:
            # 过滤None值
            payload = {k: v for k, v in payload.items() if v is not None}

        if method == "GET":
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()
        return response.json()
