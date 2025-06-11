from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


class VideoProvider(Enum):
    """视频生成服务提供商"""
    TONGYI = "tongyi"  # 通义万相
    VIDU = "vidu"  # Vidu
    PIXVERSE = "pixverse"  # PixVerse AI
    STABILITY = "stability"  # Stability AI
    SILICONFLOW = "siliconflow"  # SiliconFlow
    RUNWAY = "runway"  # Runway
    ZHIPU = "zhipu"  # 智谱AI
    LUMA = "luma"  # Luma Labs


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"  # 等待中，任务已创建但尚未开始处理
    PROCESSING = "processing"  # 处理中，任务正在执行
    COMPLETED = "completed"  # 已完成，任务成功完成
    FAILED = "failed"  # 失败，任务执行失败


@dataclass
class TextToVideoRequest:
    prompt: str  # 文本提示词，描述要生成的视频内容，例如: "一只可爱的猫咪在花园里玩耍"
    negative_prompt: Optional[str] = None  # 负面提示词，描述不想要的内容，例如: "模糊，低质量，变形"
    width: int = 1024  # 视频宽度（像素），例如: 1024
    height: int = 576  # 视频高度（像素），例如: 576
    duration: int = 4  # 视频时长（秒），例如: 4
    fps: int = 8  # 视频帧率，例如: 8, 24, 30
    style: Optional[str] = None  # 视频风格，例如: "写实风格", "动漫风格", "油画风格"
    seed: Optional[int] = None  # 随机种子，用于复现结果，例如: 42
    resolution: Optional[str] = None  # 视频分辨率，例如: "720p", "1080p", "4k"
    aspect_ratio: Optional[str] = None  # 视频宽高比，例如: "16:9", "9:16", "1:1"


@dataclass
class ImageToVideoRequest:
    image_url: str  # 输入图片的URL，例如: "https://example.com/image.jpg"
    prompt: Optional[str] = None  # 文本提示词，描述要生成的视频内容，例如: "让图片中的猫咪动起来"
    negative_prompt: Optional[str] = None  # 负面提示词，描述不想要的内容，例如: "模糊，低质量，变形"
    width: int = 1024  # 视频宽度（像素），例如: 1024
    height: int = 576  # 视频高度（像素），例如: 576
    duration: int = 4  # 视频时长（秒），例如: 4
    fps: int = 8  # 视频帧率，例如: 8, 24, 30
    motion_strength: float = 1.0  # 运动强度，范围0.0-1.0，例如: 0.5
    seed: Optional[int] = None  # 随机种子，用于复现结果，例如: 42
    resolution: Optional[str] = None  # 视频分辨率，例如: "720p", "1080p", "4k"
    aspect_ratio: Optional[str] = None  # 视频宽高比，例如: "16:9", "9:16", "1:1"


@dataclass
class SubjectReferenceRequest:
    reference_url: str  # 参考图片的URL，例如: "https://example.com/reference.jpg"
    prompt: str  # 文本提示词，描述要生成的视频内容，例如: "让参考图片中的角色跳舞"
    negative_prompt: Optional[str] = None  # 负面提示词，描述不想要的内容，例如: "模糊，低质量，变形"
    width: int = 1024  # 视频宽度（像素），例如: 1024
    height: int = 576  # 视频高度（像素），例如: 576
    duration: int = 4  # 视频时长（秒），例如: 4
    fps: int = 8  # 视频帧率，例如: 8, 24, 30
    reference_strength: float = 1.0  # 参考强度，范围0.0-1.0，例如: 0.8
    seed: Optional[int] = None  # 随机种子，用于复现结果，例如: 42
    resolution: Optional[str] = None  # 视频分辨率，例如: "720p", "1080p", "4k"
    aspect_ratio: Optional[str] = None  # 视频宽高比，例如: "16:9", "9:16", "1:1"


@dataclass
class VideoTaskResponse:
    """视频生成任务响应"""
    task_id: str  # 任务ID，例如: "task_123456"
    provider: VideoProvider  # 服务提供商，例如: VideoProvider.TONGYI
    status: TaskStatus  # 任务状态，例如: TaskStatus.PENDING
    create_time: datetime  # 任务创建时间，例如: datetime.now()
    message: Optional[str] = None  # 任务消息，例如: "任务已提交"


@dataclass
class VideoTaskStatus:
    """视频生成任务状态"""
    task_id: str  # 任务ID，例如: "task_123456"
    provider: VideoProvider  # 服务提供商，例如: VideoProvider.TONGYI
    status: TaskStatus  # 任务状态，例如: TaskStatus.PROCESSING
    progress: float  # 任务进度，范围0.0-1.0，例如: 0.5
    create_time: datetime  # 任务创建时间，例如: datetime.now()
    update_time: datetime  # 任务更新时间，例如: datetime.now()
    video_url: Optional[str] = None  # 视频URL，例如: "https://example.com/video.mp4"
    thumbnail_url: Optional[str] = None  # 缩略图URL，例如: "https://example.com/thumbnail.jpg"
    error_message: Optional[str] = None  # 错误信息，例如: "生成失败：内存不足"
    estimated_time: Optional[int] = None  # 预计剩余时间(秒)，例如: 60


class BaseVideoGenerator(ABC):
    def __init__(self, api_key: str, api_secret: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.model = model
        self.provider = self._get_provider()

    @abstractmethod
    def _get_provider(self) -> VideoProvider:
        """返回当前生成器的供应商类型"""
        pass

    @abstractmethod
    def text_to_video(self, request: TextToVideoRequest) -> VideoTaskResponse:
        """
        文本生成视频
        
        Args:
            request: 文本生成视频的请求参数
            
        Returns:
            VideoTaskResponse: 任务创建响应
        """
        pass

    @abstractmethod
    def image_to_video(self, request: ImageToVideoRequest) -> VideoTaskResponse:
        """
        图片生成视频
        
        Args:
            request: 图片生成视频的请求参数
            
        Returns:
            VideoTaskResponse: 任务创建响应
        """
        pass

    @abstractmethod
    def subject_reference(self, request: SubjectReferenceRequest) -> VideoTaskResponse:
        """
        参考主体生成视频
        
        Args:
            request: 参考主体生成视频的请求参数
            
        Returns:
            VideoTaskResponse: 任务创建响应
        """
        pass

    @abstractmethod
    def get_task_status(self, task_id: str) -> VideoTaskStatus:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            VideoTaskStatus: 任务状态信息
        """
        pass
