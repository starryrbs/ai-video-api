import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
from video_generation.base import (
    BaseVideoGenerator, VideoProvider, TaskStatus,
    TextToVideoRequest, ImageToVideoRequest, SubjectReferenceRequest,
    VideoTaskResponse, VideoTaskStatus
)

class RunwayVideoGenerator(BaseVideoGenerator):
    """Runway视频生成器"""
    
    def __init__(self, api_key: str, api_secret: Optional[str] = None, model: Optional[str] = None):
        super().__init__(api_key, api_secret, model)
        self.base_url = "https://api.dev.runwayml.com/v1"
        self.model = model or "gen4_turbo"  # 默认使用 gen4_turbo 模型
    
    def _get_provider(self) -> VideoProvider:
        return VideoProvider.RUNWAY
    
    def text_to_video(self, request: TextToVideoRequest) -> VideoTaskResponse:
        """文本生成视频"""
        url = f"{self.base_url}/text_to_video"
        
        payload = {
            "model": self.model,
            "prompt_text": request.prompt,
            "ratio": request.aspect_ratio or "16:9",
            "duration": request.duration or 5
        }
        
        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.now(),  # API 没有返回创建时间
            message=response.get("status")
        )
    
    def image_to_video(self, request: ImageToVideoRequest) -> VideoTaskResponse:
        """图片生成视频"""
        url = f"{self.base_url}/image_to_video"
        
        payload = {
            "model": self.model,
            "promptImage": request.image_url,
            "promptText": request.prompt,
            "ratio": request.aspect_ratio or "1280:720",
            "duration": request.duration or 5
        }
        
        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.now(),  # API 没有返回创建时间
            message=response.get("status")
        )
    
    def subject_reference(self, request: SubjectReferenceRequest) -> VideoTaskResponse:
        """参考主体生成视频"""
        url = f"{self.base_url}/image_to_video"
        
        payload = {
            "model": self.model,
            "promptImage": request.reference_url,
            "promptText": request.prompt,
            "ratio": request.aspect_ratio or "1280:720",
            "duration": request.duration or 5
        }
        
        response = self._make_request(url, payload)
        return VideoTaskResponse(
            task_id=response["id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.now(),  # API 没有返回创建时间
            message=response.get("status")
        )
    
    def get_task_status(self, task_id: str) -> VideoTaskStatus:
        """获取任务状态"""
        url = f"{self.base_url}/tasks/{task_id}"
        
        response = self._make_request(url, {}, method="GET")
        
        # 状态映射
        status_map = {
            "PENDING": TaskStatus.PENDING,
            "PROCESSING": TaskStatus.PROCESSING,
            "SUCCEEDED": TaskStatus.COMPLETED,
            "FAILED": TaskStatus.FAILED
        }
        
        return VideoTaskStatus(
            task_id=task_id,
            provider=self.provider,
            status=status_map.get(response["status"], TaskStatus.PENDING),
            progress=1.0 if response["status"] == "SUCCEEDED" else 0.0,
            video_url=response.get("output", [None])[0],  # API 返回 output 数组
            thumbnail_url=None,  # API 没有提供缩略图
            error_message=response.get("error"),
            create_time=datetime.now(),  # API 没有返回创建时间
            update_time=datetime.now(),  # API 没有返回更新时间
            estimated_time=None  # API 没有返回预计时间
        )
    
    def _make_request(self, url: str, payload: Dict[str, Any], method: str = "POST") -> dict:
        """发起HTTP请求"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Runway-Version": "2024-11-06"  # 使用最新的 API 版本
        }
        
        # 过滤None值
        payload = {k: v for k, v in payload.items() if v is not None}
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, json=payload, headers=headers)
            
        response.raise_for_status()
        return response.json()