import requests
import json
from datetime import datetime
from typing import Optional
from video_generation.base import (
    BaseVideoGenerator, VideoProvider, TaskStatus,
    TextToVideoRequest, ImageToVideoRequest, SubjectReferenceRequest,
    VideoTaskResponse, VideoTaskStatus
)


class ViduVideoGenerator(BaseVideoGenerator):
    """Vidu视频生成器"""

    def __init__(self, api_key: str, api_secret: Optional[str] = None, model: Optional[str] = None):
        super().__init__(api_key, api_secret, model)
        self.base_url = "https://api.vidu.cn"  # 更新为正确的 API 端点
        self.model = model or "viduq1"  # 默认使用 viduq1 模型

    def _get_provider(self) -> VideoProvider:
        return VideoProvider.VIDU

    def text_to_video(self, request: TextToVideoRequest) -> VideoTaskResponse:
        """文本生成视频"""
        url = f"{self.base_url}/ent/v2/text2video"

        # 根据 Vidu V2 API 文档构建请求参数
        payload = {
            "model": self.model or "viduq1",  # 默认使用 viduq1 模型
            "style": request.style or "general",  # 可选: general, anime, realistic 等
            "prompt": request.prompt,
            "duration": str(request.duration) if request.duration else "5",  # 字符串格式
            "seed": str(request.seed) if request.seed else "0",  # 字符串格式
            "aspect_ratio": request.aspect_ratio or "16:9",  # 可选: 16:9, 9:16, 1:1
            "resolution": request.resolution or "1080p",  # 可选: 512, 720p, 1080p
            "movement_amplitude": request.movement_amplitude or "auto"  # 可选: auto, small, medium, large
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["task_id"],  # API 返回 task_id
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.fromisoformat(response["created_at"]) if "created_at" in response else datetime.now(),
            message=response.get("state")  # API 返回 state 字段
        )

    def image_to_video(self, request: ImageToVideoRequest) -> VideoTaskResponse:
        """图片生成视频"""
        # 使用 Vidu V2 API 的正确端点和参数格式
        url = f"{self.base_url}/vidu/ent/v2/img2video"

        # 根据 Vidu V2 API 文档构建请求参数
        payload = {
            "model": self.model or "viduq1",  # 默认使用 viduq1 模型
            "images": [request.image_url],  # 图片URL数组格式
            "prompt": request.prompt,
            "duration": str(request.duration) if request.duration else "5",  # 字符串格式
            "seed": str(request.seed) if request.seed else "0",  # 字符串格式
            "resolution": request.resolution or "720p",  # 可选: 512, 720p, 1080p
            "movement_amplitude": request.motion_strength or "auto"  # 可选: auto, small, medium, large
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["task_id"],  # API 返回 task_id
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.fromisoformat(response["created_at"]) if "created_at" in response else datetime.now(),
            message=response.get("state")  # API 返回 state 字段
        )

    def subject_reference(self, request: SubjectReferenceRequest) -> VideoTaskResponse:
        """参考主体生成视频"""
        url = f"{self.base_url}/ent/v2/reference2video"

        # 根据 Vidu V2 API 文档构建请求参数
        payload = {
            "model": self.model or "vidu2.0",  # 默认使用 vidu2.0 模型
            "images": [request.reference_url],  # 参考图片URL数组
            "prompt": request.prompt,
            "duration": str(request.duration) if request.duration else "4",  # 字符串格式
            "seed": str(request.seed) if request.seed else "0",  # 字符串格式
            "aspect_ratio": request.aspect_ratio or "16:9",  # 可选: 16:9, 9:16, 1:1
            "resolution": request.resolution or "720p",  # 可选: 512, 720p, 1080p
            "movement_amplitude": request.movement_amplitude or "auto"  # 可选: auto, small, medium, large
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["task_id"],  # API 返回 task_id
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.fromisoformat(response["created_at"]) if "created_at" in response else datetime.now(),
            message=response.get("state")  # API 返回 state 字段
        )

    def get_task_status(self, task_id: str) -> VideoTaskStatus:
        """获取任务状态"""
        url = f"{self.base_url}/ent/v2/tasks/{task_id}/creations"
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # 状态映射
        status_map = {
            "pending": TaskStatus.PENDING,
            "processing": TaskStatus.PROCESSING,
            "success": TaskStatus.COMPLETED,
            "failed": TaskStatus.FAILED
        }

        # 获取第一个生成结果（如果有的话）
        creation = data.get("creations", [{}])[0] if data.get("creations") else {}

        return VideoTaskStatus(
            task_id=task_id,
            provider=self.provider,
            status=status_map.get(data["state"], TaskStatus.PENDING),
            progress=1.0 if data["state"] == "success" else 0.0,
            video_url=creation.get("url"),
            thumbnail_url=creation.get("cover_url"),
            error_message=data.get("err_code"),
            create_time=datetime.now(),  # API 没有返回创建时间
            update_time=datetime.now(),  # API 没有返回更新时间
            estimated_time=None  # API 没有返回预计时间
        )

    def _make_request(self, url: str, payload: dict) -> dict:
        """发起HTTP请求"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 过滤None值
        payload = {k: v for k, v in payload.items() if v is not None}

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
