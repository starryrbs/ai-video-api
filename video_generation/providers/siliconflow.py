import requests
import json
from datetime import datetime
from typing import Optional
from video_generation.base import (
    BaseVideoGenerator, VideoProvider, TaskStatus,
    TextToVideoRequest, ImageToVideoRequest, SubjectReferenceRequest,
    VideoTaskResponse, VideoTaskStatus
)


class SiliconFlowVideoGenerator(BaseVideoGenerator):
    """SiliconFlow视频生成器
    
    https://docs.siliconflow.com/cn/api-reference/videos/videos_submit#wan-ai-image-to-video
    """

    def __init__(self, api_key: str, api_secret: Optional[str] = None, model: Optional[str] = None):
        super().__init__(api_key, api_secret, model)
        self.base_url = "https://api.ap.siliconflow.com/v1"
        self.model = model or "Wan-AI/Wan2.1-I2V-14B-720P"

    def _get_provider(self) -> VideoProvider:
        return VideoProvider.SILICONFLOW

    def text_to_video(self, request: TextToVideoRequest) -> VideoTaskResponse:
        """文本生成视频"""
        url = f"{self.base_url}/video/submit"

        payload = {
            "model": self.model,
            "prompt": request.prompt,
            "negative_prompt": request.negative_prompt,
            "image_size": request.resolution or "1280x720",
            "seed": request.seed if request.seed else None
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["requestId"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.now(),
            message="Task submitted"
        )

    def image_to_video(self, request: ImageToVideoRequest) -> VideoTaskResponse:
        """图片生成视频"""
        url = f"{self.base_url}/video/submit"

        payload = {
            "model": self.model,
            "prompt": request.prompt,
            "negative_prompt": request.negative_prompt,
            "image_size": request.resolution or "1280x720",
            "image": request.image_url,
            "seed": request.seed if request.seed else None
        }

        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["requestId"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.now(),
            message="Task submitted"
        )

    def subject_reference(self, request: SubjectReferenceRequest) -> VideoTaskResponse:
        """参考主体生成视频 - SiliconFlow 暂不支持"""
        raise NotImplementedError("SiliconFlow 暂不支持参考主体生成视频")

    def get_task_status(self, task_id: str) -> VideoTaskStatus:
        """获取任务状态"""
        url = f"{self.base_url}/video/status"

        payload = {
            "requestId": task_id
        }

        response = self._make_request(url, payload)

        # 状态映射
        status_map = {
            "Pending": TaskStatus.PENDING,
            "Processing": TaskStatus.PROCESSING,
            "Succeed": TaskStatus.COMPLETED,
            "Failed": TaskStatus.FAILED
        }

        current_status = status_map.get(response["status"], TaskStatus.PENDING)

        # 获取视频URL（如果任务成功）
        video_url = None
        if current_status == TaskStatus.COMPLETED and "results" in response:
            videos = response["results"].get("videos", [])
            if videos:
                video_url = videos[0].get("url")

        return VideoTaskStatus(
            task_id=task_id,
            provider=self.provider,
            status=current_status,
            progress=1.0 if current_status == TaskStatus.COMPLETED else 0.0,
            video_url=video_url,
            thumbnail_url=None,  # API 未提供缩略图
            error_message=response.get("reason") if current_status == TaskStatus.FAILED else None,
            create_time=datetime.now(),
            update_time=datetime.now(),
            estimated_time=None
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
