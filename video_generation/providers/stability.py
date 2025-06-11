import requests
import json
from datetime import datetime
from typing import Optional
from video_generation.base import (
    BaseVideoGenerator, VideoProvider, TaskStatus,
    TextToVideoRequest, ImageToVideoRequest, SubjectReferenceRequest,
    VideoTaskResponse, VideoTaskStatus
)


class StabilityVideoGenerator(BaseVideoGenerator):
    """Stability.ai 视频生成器"""

    def __init__(self, api_key: str, api_secret: Optional[str] = None, model: Optional[str] = None):
        super().__init__(api_key, api_secret, model)
        self.base_url = "https://api.stability.ai/v2beta"

    def _get_provider(self) -> VideoProvider:
        return VideoProvider.STABILITY

    def text_to_video(self, request: TextToVideoRequest) -> VideoTaskResponse:
        """文本生成视频 - 未实现"""
        raise NotImplementedError("Stability.ai 不支持文本生成视频")

    def image_to_video(self, request: ImageToVideoRequest) -> VideoTaskResponse:
        """图片生成视频"""
        url = f"{self.base_url}/image-to-video"

        # 构建请求参数
        files = {
            'image': ('image.png', requests.get(request.image_url).content)
        }

        data = {
            'seed': str(request.seed) if request.seed else '0',
            'cfg_scale': '1.8',  # 默认值
            'motion_bucket_id': '127'  # 默认值
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(url, files=files, data=data, headers=headers)
        response.raise_for_status()
        data = response.json()

        return VideoTaskResponse(
            task_id=data["id"],
            provider=self.provider,
            status=TaskStatus.PENDING,
            create_time=datetime.now(),
            message="Task created"
        )

    def subject_reference(self, request: SubjectReferenceRequest) -> VideoTaskResponse:
        """参考主体生成视频 - 未实现"""
        raise NotImplementedError("Stability.ai 不支持参考主体生成视频")

    def get_task_status(self, task_id: str) -> VideoTaskStatus:
        """获取任务状态"""
        url = f"{self.base_url}/image-to-video/result/{task_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "video/*"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 202:
            data = response.json()
            return VideoTaskStatus(
                task_id=task_id,
                provider=self.provider,
                status=TaskStatus.PROCESSING,
                progress=0.0,
                video_url=None,
                thumbnail_url=None,
                error_message=None,
                create_time=datetime.now(),
                update_time=datetime.now(),
                estimated_time=None
            )
        elif response.status_code == 200:
            # 视频生成完成，返回视频URL
            return VideoTaskStatus(
                task_id=task_id,
                provider=self.provider,
                status=TaskStatus.COMPLETED,
                progress=1.0,
                video_url=url,  # 直接使用请求URL作为视频URL
                thumbnail_url=None,
                error_message=None,
                create_time=datetime.now(),
                update_time=datetime.now(),
                estimated_time=None
            )
        else:
            # 处理错误情况
            error_data = response.json()
            return VideoTaskStatus(
                task_id=task_id,
                provider=self.provider,
                status=TaskStatus.FAILED,
                progress=0.0,
                video_url=None,
                thumbnail_url=None,
                error_message=error_data.get("errors", ["Unknown error"])[0],
                create_time=datetime.now(),
                update_time=datetime.now(),
                estimated_time=None
            )
