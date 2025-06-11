from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple, Dict


class VideoProvider(Enum):
    TONGYI = "tongyi"
    VIDU = "vidu"
    LUMA = "luma"  # 添加 Luma 供应商
    RUNWAY = "runway"  # 添加 Runway 供应商
    SILICONFLOW = "siliconflow"  # 添加 SiliconFlow 供应商
    # 可以添加更多供应商


class TongyiModel(Enum):
    T2V_TURBO = "wanx2.1-t2v-turbo"  # 支持480P和720P
    T2V_PLUS = "wanx2.1-t2v-plus"  # 仅支持720P
    I2V_TURBO = "wanx2.1-i2v-turbo"  # 支持480P和720P
    I2V_PLUS = "wanx2.1-i2v-plus"  # 仅支持720P
    VACE_PLUS = "wanx2.1-vace-plus"  # 仅支持720P


class ViduModel(Enum):
    """Vidu 支持的模型"""
    VIDUQ1 = "viduq1"  # 最新高性能模型，支持4S-1080P
    VIDU_2_0 = "vidu2.0"  # 2.0版本，支持4S和8S
    VIDU_1_5 = "vidu1.5"  # 1.5版本，支持多种分辨率
    VIDU_1_0 = "vidu1.0"  # 1.0版本，基础版本


class LumaModel(Enum):
    """Luma 支持的模型"""
    RAY_2_FLASH = "ray-flash-2"  # 最新高性能模型
    RAY_2 = "ray-2"  # 2.0版本
    RAY_1_6 = "ray-1-6"  # 1.6版本


class RunwayModel(Enum):
    """Runway 支持的模型"""
    GEN4_TURBO = "gen4_turbo"  # 最新高性能模型
    GEN4_IMAGE = "gen4_image"  # 图像生成模型


class SiliconFlowModel(Enum):
    """SiliconFlow 支持的模型"""
    T2V_14B = "Wan-AI/Wan2.1-T2V-14B"  # 文本生成视频标准模型
    T2V_14B_TURBO = "Wan-AI/Wan2.1-T2V-14B-Turbo"  # 文本生成视频加速模型
    I2V_14B_720P = "Wan-AI/Wan2.1-I2V-14B-720P"  # 图片生成视频标准模型
    I2V_14B_720P_TURBO = "Wan-AI/Wan2.1-I2V-14B-720P-Turbo"  # 图片生成视频加速模型


@dataclass
class VideoSize:
    width: int
    height: int


class VideoSizeAdapter:
    """视频尺寸适配器，用于处理不同供应商的视频尺寸要求"""

    # 通义万相支持的尺寸（按分辨率分类）
    TONGYI_720P_SIZES = {
        "1280*720": VideoSize(1280, 720),  # 16:9
        "960*960": VideoSize(960, 960),  # 1:1
        "720*1280": VideoSize(720, 1280),  # 9:16
        "1088*832": VideoSize(1088, 832),  # 4:3
        "832*1088": VideoSize(832, 1088),  # 3:4
    }

    TONGYI_480P_SIZES = {
        "832*480": VideoSize(832, 480),  # 16:9
        "624*624": VideoSize(624, 624),  # 1:1
        "480*832": VideoSize(480, 832),  # 9:16
    }

    # 模型支持的尺寸映射
    TONGYI_MODEL_SIZES: Dict[TongyiModel, Dict[str, VideoSize]] = {
        TongyiModel.T2V_TURBO: {**TONGYI_720P_SIZES, **TONGYI_480P_SIZES},
        TongyiModel.T2V_PLUS: TONGYI_720P_SIZES,
        TongyiModel.I2V_TURBO: {**TONGYI_720P_SIZES, **TONGYI_480P_SIZES},
        TongyiModel.I2V_PLUS: TONGYI_720P_SIZES,
        TongyiModel.VACE_PLUS: TONGYI_720P_SIZES,
    }

    # Vidu支持的尺寸（按分辨率和比例分类）
    VIDU_512_SIZES = {
        "16:9": {
            "512*288": VideoSize(512, 288),  # 16:9 基础分辨率
        },
        "9:16": {
            "288*512": VideoSize(288, 512),  # 9:16 基础分辨率
        },
        "1:1": {
            "512*512": VideoSize(512, 512),  # 1:1 基础分辨率
        }
    }

    VIDU_720P_SIZES = {
        "16:9": {
            "1280*720": VideoSize(1280, 720),  # 16:9 标准720P
        },
        "9:16": {
            "720*1280": VideoSize(720, 1280),  # 9:16 标准720P
        },
        "1:1": {
            "720*720": VideoSize(720, 720),  # 1:1 标准720P
        }
    }

    VIDU_1080P_SIZES = {
        "16:9": {
            "1920*1080": VideoSize(1920, 1080),  # 16:9 标准1080P
        },
        "9:16": {
            "1080*1920": VideoSize(1080, 1920),  # 9:16 标准1080P
        },
        "1:1": {
            "1080*1080": VideoSize(1080, 1080),  # 1:1 标准1080P
        }
    }

    # Vidu 所有支持的尺寸（兼容性考虑）
    VIDU_SIZES = {
        # 基础分辨率 512
        "512*288": VideoSize(512, 288),  # 16:9
        "288*512": VideoSize(288, 512),  # 9:16
        "512*512": VideoSize(512, 512),  # 1:1
        # 720P 分辨率
        "1280*720": VideoSize(1280, 720),  # 16:9
        "720*1280": VideoSize(720, 1280),  # 9:16
        "720*720": VideoSize(720, 720),  # 1:1
        # 1080P 分辨率
        "1920*1080": VideoSize(1920, 1080),  # 16:9
        "1080*1920": VideoSize(1080, 1920),  # 9:16
        "1080*1080": VideoSize(1080, 1080),  # 1:1
    }

    # Vidu 模型支持的分辨率映射
    VIDU_MODEL_RESOLUTIONS: Dict[ViduModel, list] = {
        ViduModel.VIDUQ1: ["720p", "1080p"],  # viduq1 支持720p和1080p
        ViduModel.VIDU_2_0: ["720p", "1080p"],  # vidu2.0 支持720p和1080p
        ViduModel.VIDU_1_5: ["512", "720p", "1080p"],  # vidu1.5 支持所有分辨率
        ViduModel.VIDU_1_0: ["512"],  # vidu1.0 仅支持基础分辨率
    }

    # Vidu 模型支持的时长映射
    VIDU_MODEL_DURATIONS: Dict[ViduModel, list] = {
        ViduModel.VIDUQ1: [4, 5],  # viduq1 支持4秒和5秒
        ViduModel.VIDU_2_0: [4, 8],  # vidu2.0 支持4秒和8秒
        ViduModel.VIDU_1_5: [4, 8],  # vidu1.5 支持4秒和8秒
        ViduModel.VIDU_1_0: [4, 8],  # vidu1.0 支持4秒和8秒
    }

    # Vidu 支持的视频比例
    VIDU_ASPECT_RATIOS = ["16:9", "9:16", "1:1"]

    # Vidu 支持的运动幅度
    VIDU_MOVEMENT_AMPLITUDES = ["auto", "small", "medium", "large"]

    # Vidu 支持的风格（仅文本生成视频）
    VIDU_STYLES = ["general", "anime"]

    # Luma支持的尺寸（按分辨率和比例分类）
    LUMA_540P_SIZES = {
        "16:9": {
            "960*540": VideoSize(960, 540),  # 16:9 540P
        },
        "9:16": {
            "540*960": VideoSize(540, 960),  # 9:16 540P
        },
        "1:1": {
            "540*540": VideoSize(540, 540),  # 1:1 540P
        }
    }

    LUMA_720P_SIZES = {
        "16:9": {
            "1280*720": VideoSize(1280, 720),  # 16:9 720P
        },
        "9:16": {
            "720*1280": VideoSize(720, 1280),  # 9:16 720P
        },
        "1:1": {
            "720*720": VideoSize(720, 720),  # 1:1 720P
        }
    }

    LUMA_1080P_SIZES = {
        "16:9": {
            "1920*1080": VideoSize(1920, 1080),  # 16:9 1080P
        },
        "9:16": {
            "1080*1920": VideoSize(1080, 1920),  # 9:16 1080P
        },
        "1:1": {
            "1080*1080": VideoSize(1080, 1080),  # 1:1 1080P
        }
    }

    LUMA_4K_SIZES = {
        "16:9": {
            "3840*2160": VideoSize(3840, 2160),  # 16:9 4K
        },
        "9:16": {
            "2160*3840": VideoSize(2160, 3840),  # 9:16 4K
        },
        "1:1": {
            "2160*2160": VideoSize(2160, 2160),  # 1:1 4K
        }
    }

    # Luma 所有支持的尺寸（兼容性考虑）
    LUMA_SIZES = {
        # 540P 分辨率
        "960*540": VideoSize(960, 540),  # 16:9
        "540*960": VideoSize(540, 960),  # 9:16
        "540*540": VideoSize(540, 540),  # 1:1
        # 720P 分辨率
        "1280*720": VideoSize(1280, 720),  # 16:9
        "720*1280": VideoSize(720, 1280),  # 9:16
        "720*720": VideoSize(720, 720),  # 1:1
        # 1080P 分辨率
        "1920*1080": VideoSize(1920, 1080),  # 16:9
        "1080*1920": VideoSize(1080, 1920),  # 9:16
        "1080*1080": VideoSize(1080, 1080),  # 1:1
        # 4K 分辨率
        "3840*2160": VideoSize(3840, 2160),  # 16:9
        "2160*3840": VideoSize(2160, 3840),  # 9:16
        "2160*2160": VideoSize(2160, 2160),  # 1:1
    }

    # Luma 模型支持的分辨率映射
    LUMA_MODEL_RESOLUTIONS: Dict[LumaModel, list] = {
        LumaModel.RAY_2_FLASH: ["540p", "720p", "1080p", "4k"],  # ray-flash-2 支持所有分辨率
        LumaModel.RAY_2: ["540p", "720p", "1080p", "4k"],  # ray-2 支持所有分辨率
        LumaModel.RAY_1_6: ["540p", "720p", "1080p"],  # ray-1-6 支持除4K外的所有分辨率
    }

    # Luma 支持的视频比例
    LUMA_ASPECT_RATIOS = ["16:9", "9:16", "1:1"]

    # Luma 支持的视频时长（秒）
    LUMA_DURATIONS = [4, 5, 8, 10, 15]

    # Runway支持的尺寸（按分辨率和比例分类）
    RUNWAY_720P_SIZES = {
        "16:9": {
            "1280*720": VideoSize(1280, 720),  # 16:9 720P
        },
        "9:16": {
            "720*1280": VideoSize(720, 1280),  # 9:16 720P
        },
        "1:1": {
            "720*720": VideoSize(720, 720),  # 1:1 720P
        }
    }

    RUNWAY_1080P_SIZES = {
        "16:9": {
            "1920*1080": VideoSize(1920, 1080),  # 16:9 1080P
        },
        "9:16": {
            "1080*1920": VideoSize(1080, 1920),  # 9:16 1080P
        },
        "1:1": {
            "1080*1080": VideoSize(1080, 1080),  # 1:1 1080P
        }
    }

    # Runway 所有支持的尺寸（兼容性考虑）
    RUNWAY_SIZES = {
        # 720P 分辨率
        "1280*720": VideoSize(1280, 720),  # 16:9
        "720*1280": VideoSize(720, 1280),  # 9:16
        "720*720": VideoSize(720, 720),  # 1:1
        # 1080P 分辨率
        "1920*1080": VideoSize(1920, 1080),  # 16:9
        "1080*1920": VideoSize(1080, 1920),  # 9:16
        "1080*1080": VideoSize(1080, 1080),  # 1:1
    }

    # Runway 模型支持的分辨率映射
    RUNWAY_MODEL_RESOLUTIONS: Dict[RunwayModel, list] = {
        RunwayModel.GEN4_TURBO: ["720p", "1080p"],  # gen4_turbo 支持720p和1080p
        RunwayModel.GEN4_IMAGE: ["720p", "1080p"],  # gen4_image 支持720p和1080p
    }

    # Runway 支持的视频比例
    RUNWAY_ASPECT_RATIOS = ["16:9", "9:16", "1:1"]

    # Runway 支持的视频时长（秒）
    RUNWAY_DURATIONS = [4, 5, 8, 10, 15]

    # SiliconFlow支持的尺寸（按分辨率和比例分类）
    SILICONFLOW_720P_SIZES = {
        "16:9": {
            "1280*720": VideoSize(1280, 720),  # 16:9 720P
        },
        "9:16": {
            "720*1280": VideoSize(720, 1280),  # 9:16 720P
        },
        "1:1": {
            "720*720": VideoSize(720, 720),  # 1:1 720P
        }
    }

    # SiliconFlow 所有支持的尺寸（兼容性考虑）
    SILICONFLOW_SIZES = {
        # 720P 分辨率
        "1280*720": VideoSize(1280, 720),  # 16:9
        "720*1280": VideoSize(720, 1280),  # 9:16
        "720*720": VideoSize(720, 720),  # 1:1
    }

    # SiliconFlow 模型支持的分辨率映射
    SILICONFLOW_MODEL_RESOLUTIONS: Dict[SiliconFlowModel, list] = {
        SiliconFlowModel.T2V_14B: ["720p"],  # 文本生成视频标准模型支持720p
        SiliconFlowModel.T2V_14B_TURBO: ["720p"],  # 文本生成视频加速模型支持720p
        SiliconFlowModel.I2V_14B_720P: ["720p"],  # 图片生成视频标准模型支持720p
        SiliconFlowModel.I2V_14B_720P_TURBO: ["720p"],  # 图片生成视频加速模型支持720p
    }

    # SiliconFlow 支持的视频比例
    SILICONFLOW_ASPECT_RATIOS = ["16:9", "9:16", "1:1"]

    @classmethod
    def get_supported_sizes(cls, provider: VideoProvider, model: Optional[str] = None) -> dict:
        """获取指定供应商和模型支持的尺寸"""
        if provider.value == VideoProvider.TONGYI.value:
            if model:
                try:
                    tongyi_model = TongyiModel(model)
                    return cls.TONGYI_MODEL_SIZES.get(tongyi_model, cls.TONGYI_720P_SIZES)
                except ValueError:
                    return cls.TONGYI_720P_SIZES  # 默认返回720P尺寸
            return cls.TONGYI_720P_SIZES
        elif provider.value == VideoProvider.VIDU.value:
            return cls.VIDU_SIZES
        elif provider.value == VideoProvider.LUMA.value:
            return cls.LUMA_SIZES
        elif provider.value == VideoProvider.RUNWAY.value:
            return cls.RUNWAY_SIZES
        elif provider.value == VideoProvider.SILICONFLOW.value:
            return cls.SILICONFLOW_SIZES
        return {}

    @classmethod
    def get_vidu_supported_resolutions(cls, model: Optional[str] = None) -> list:
        """获取 Vidu 模型支持的分辨率"""
        if model:
            try:
                vidu_model = ViduModel(model)
                return cls.VIDU_MODEL_RESOLUTIONS.get(vidu_model, ["720p"])
            except ValueError:
                return ["720p"]  # 默认返回720p
        return ["512", "720p", "1080p"]  # 返回所有分辨率

    @classmethod
    def get_vidu_supported_durations(cls, model: Optional[str] = None) -> list:
        """获取 Vidu 模型支持的时长"""
        if model:
            try:
                vidu_model = ViduModel(model)
                return cls.VIDU_MODEL_DURATIONS.get(vidu_model, [4])
            except ValueError:
                return [4]  # 默认返回4秒
        return [4, 5, 8]  # 返回所有时长

    @classmethod
    def get_vidu_size_by_resolution_and_ratio(cls, resolution: str, aspect_ratio: str) -> Optional[VideoSize]:
        """根据分辨率和比例获取 Vidu 视频尺寸"""
        if resolution == "512":
            sizes = cls.VIDU_512_SIZES.get(aspect_ratio, {})
        elif resolution == "720p":
            sizes = cls.VIDU_720P_SIZES.get(aspect_ratio, {})
        elif resolution == "1080p":
            sizes = cls.VIDU_1080P_SIZES.get(aspect_ratio, {})
        else:
            return None

        # 返回该分辨率和比例下的第一个尺寸
        if sizes:
            return list(sizes.values())[0]
        return None

    @classmethod
    def get_luma_supported_resolutions(cls, model: Optional[str] = None) -> list:
        """获取 Luma 模型支持的分辨率"""
        if model:
            try:
                luma_model = LumaModel(model)
                return cls.LUMA_MODEL_RESOLUTIONS.get(luma_model, ["720p"])
            except ValueError:
                return ["720p"]  # 默认返回720p
        return ["540p", "720p", "1080p", "4k"]  # 返回所有分辨率

    @classmethod
    def get_luma_size_by_resolution_and_ratio(cls, resolution: str, aspect_ratio: str) -> Optional[VideoSize]:
        """根据分辨率和比例获取 Luma 视频尺寸"""
        if resolution == "540p":
            sizes = cls.LUMA_540P_SIZES.get(aspect_ratio, {})
        elif resolution == "720p":
            sizes = cls.LUMA_720P_SIZES.get(aspect_ratio, {})
        elif resolution == "1080p":
            sizes = cls.LUMA_1080P_SIZES.get(aspect_ratio, {})
        elif resolution == "4k":
            sizes = cls.LUMA_4K_SIZES.get(aspect_ratio, {})
        else:
            return None

        # 返回该分辨率和比例下的第一个尺寸
        if sizes:
            return list(sizes.values())[0]
        return None

    @classmethod
    def get_runway_supported_resolutions(cls, model: Optional[str] = None) -> list:
        """获取 Runway 模型支持的分辨率"""
        if model:
            try:
                runway_model = RunwayModel(model)
                return cls.RUNWAY_MODEL_RESOLUTIONS.get(runway_model, ["720p"])
            except ValueError:
                return ["720p"]  # 默认返回720p
        return ["720p", "1080p"]  # 返回所有分辨率

    @classmethod
    def get_runway_size_by_resolution_and_ratio(cls, resolution: str, aspect_ratio: str) -> Optional[VideoSize]:
        """根据分辨率和比例获取 Runway 视频尺寸"""
        if resolution == "720p":
            sizes = cls.RUNWAY_720P_SIZES.get(aspect_ratio, {})
        elif resolution == "1080p":
            sizes = cls.RUNWAY_1080P_SIZES.get(aspect_ratio, {})
        else:
            return None

        # 返回该分辨率和比例下的第一个尺寸
        if sizes:
            return list(sizes.values())[0]
        return None

    @classmethod
    def get_siliconflow_supported_resolutions(cls, model: Optional[str] = None) -> list:
        """获取 SiliconFlow 模型支持的分辨率"""
        if model:
            try:
                siliconflow_model = SiliconFlowModel(model)
                return cls.SILICONFLOW_MODEL_RESOLUTIONS.get(siliconflow_model, ["720p"])
            except ValueError:
                return ["720p"]  # 默认返回720p
        return ["720p"]  # 返回所有分辨率

    @classmethod
    def get_siliconflow_size_by_resolution_and_ratio(cls, resolution: str, aspect_ratio: str) -> Optional[VideoSize]:
        """根据分辨率和比例获取 SiliconFlow 视频尺寸"""
        if resolution == "720p":
            sizes = cls.SILICONFLOW_720P_SIZES.get(aspect_ratio, {})
        else:
            return None

        # 返回该分辨率和比例下的第一个尺寸
        if sizes:
            return list(sizes.values())[0]
        return None

    @classmethod
    def get_size_string(cls, width: int, height: int) -> str:
        """将宽高转换为尺寸字符串"""
        return f"{width}*{height}"

    @classmethod
    def parse_size_string(cls, size_str: str) -> Optional[VideoSize]:
        """解析尺寸字符串为VideoSize对象"""
        try:
            width, height = map(int, size_str.split("*"))
            return VideoSize(width, height)
        except (ValueError, AttributeError):
            return None

    @classmethod
    def get_closest_size(cls, width: int, height: int, provider: VideoProvider,
                         model: Optional[str] = None) -> VideoSize:
        """获取最接近目标尺寸的供应商支持尺寸"""
        supported_sizes = cls.get_supported_sizes(provider, model)
        if not supported_sizes:
            return VideoSize(width, height)  # 如果没有支持的尺寸，返回原始尺寸

        # 计算宽高比
        target_ratio = width / height

        # 找到最接近的宽高比
        closest_size = None
        min_ratio_diff = float('inf')

        for size in supported_sizes.values():
            ratio = size.width / size.height
            ratio_diff = abs(ratio - target_ratio)

            if ratio_diff < min_ratio_diff:
                min_ratio_diff = ratio_diff
                closest_size = size

        return closest_size

    @classmethod
    def adapt_size(cls, width: int, height: int, provider: VideoProvider, model: Optional[str] = None) -> Tuple[
        int, int]:
        """适配视频尺寸到指定供应商支持的尺寸"""
        closest_size = cls.get_closest_size(width, height, provider, model)
        return closest_size.width, closest_size.height
