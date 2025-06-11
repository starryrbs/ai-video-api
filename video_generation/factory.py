from typing import Dict, Type
from video_generation.base import BaseVideoGenerator, VideoProvider
from video_generation.providers import (
    TongyiVideoGenerator,
    ViduVideoGenerator,
    PixverseVideoGenerator,
    StabilityVideoGenerator,
    SiliconFlowVideoGenerator,
    RunwayVideoGenerator,
    ZhipuVideoGenerator,
    LumaVideoGenerator
)


class VideoGeneratorFactory:
    """视频生成器工厂类"""

    _generators: Dict[VideoProvider, Type[BaseVideoGenerator]] = {
        VideoProvider.TONGYI: TongyiVideoGenerator,
        VideoProvider.VIDU: ViduVideoGenerator,
        VideoProvider.PIXVERSE: PixverseVideoGenerator,
        VideoProvider.STABILITY: StabilityVideoGenerator,
        VideoProvider.SILICONFLOW: SiliconFlowVideoGenerator,
        VideoProvider.RUNWAY: RunwayVideoGenerator,
        VideoProvider.ZHIPU: ZhipuVideoGenerator,
        VideoProvider.LUMA: LumaVideoGenerator,
    }

    @classmethod
    def create_generator(cls,
                         provider: VideoProvider,
                         api_key: str,
                         api_secret: str = None,
                         model: str = None) -> BaseVideoGenerator:
        """
        创建视频生成器实例
        
        Args:
            provider: 供应商类型
            api_key: API密钥
            api_secret: API密钥(可选)
            model: 模型名称(可选)
            
        Returns:
            BaseVideoGenerator: 视频生成器实例
            
        Raises:
            ValueError: 不支持的供应商类型
        """
        generator_class = cls._generators.get(provider)
        if not generator_class:
            raise ValueError(f"不支持的供应商类型: {provider}")

        return generator_class(api_key, api_secret, model)

    @classmethod
    def get_supported_providers(cls) -> list[VideoProvider]:
        """获取支持的供应商列表"""
        return list(cls._generators.keys())

    @classmethod
    def register_generator(cls,
                           provider: VideoProvider,
                           generator_class: Type[BaseVideoGenerator]):
        """
        注册新的生成器类
        
        Args:
            provider: 供应商类型
            generator_class: 生成器类
        """
        cls._generators[provider] = generator_class
