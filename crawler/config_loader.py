# -*- coding: utf-8 -*-
"""
框架配置加载器
从 YAML 配置文件加载各文档框架的配置
"""

import logging
import os
from typing import Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


class FrameworkConfigLoader:
    """
    框架配置加载器
    从 YAML 文件加载框架配置，支持热重载
    """

    _instance: Optional["FrameworkConfigLoader"] = None
    _config: Dict = {}
    _config_path: Optional[str] = None

    def __new__(cls, config_path: str = None):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: str = None):
        """
        初始化配置加载器

        Args:
            config_path: 配置文件路径，默认为 crawler/framework_config.yaml
        """
        if not self._config_path or config_path:
            self._config_path = config_path or self._get_default_config_path()
            self.load_config()

    @staticmethod
    def _get_default_config_path() -> str:
        """获取默认配置文件路径"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "framework_config.yaml")

    def load_config(self) -> None:
        """
        加载配置文件

        Raises:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: 配置文件格式错误
        """
        if not os.path.exists(self._config_path):
            raise FileNotFoundError(f"Config file not found: {self._config_path}")

        with open(self._config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

        logger.info(f"[FrameworkConfigLoader] Loaded config from: {self._config_path}")
        logger.debug(f"[FrameworkConfigLoader] Config keys: {self._config.keys()}")

    def reload(self) -> None:
        """重新加载配置文件（支持热重载）"""
        self.load_config()
        logger.info("[FrameworkConfigLoader] Config reloaded")

    def get_framework_config(self, framework: str) -> Dict:
        """
        获取指定框架的配置

        Args:
            framework: 框架名称

        Returns:
            框架配置字典，如果框架不存在则返回 unknown 框架的配置
        """
        frameworks = self._config.get("frameworks", {})
        return frameworks.get(framework, frameworks.get("unknown", {}))

    def get_patterns(self, framework: str) -> Dict:
        """
        获取框架特征模式

        Args:
            framework: 框架名称

        Returns:
            包含 url、html、meta 模式的字典
        """
        config = self.get_framework_config(framework)
        return config.get("patterns", {})

    def get_selectors(self, framework: str) -> Dict:
        """
        获取框架 CSS 选择器配置

        Args:
            framework: 框架名称

        Returns:
            包含 title、content、tags 选择器的字典
        """
        config = self.get_framework_config(framework)
        return config.get("selectors", {})

    def get_strip_tags(self, framework: str) -> List[str]:
        """
        获取框架需要移除的标签列表

        Args:
            framework: 框架名称

        Returns:
            需要移除的标签列表
        """
        config = self.get_framework_config(framework)
        return config.get("strip_tags", [])

    def get_link_extractor_config(self, framework: str) -> Dict:
        """
        获取框架链接提取器配置

        Args:
            framework: 框架名称

        Returns:
            包含 allow、deny 规则的字典
        """
        config = self.get_framework_config(framework)
        return config.get("link_extractor", {})

    def get_supported_frameworks(self) -> List[str]:
        """
        获取支持的框架列表

        Returns:
            框架名称列表
        """
        frameworks = self._config.get("frameworks", {})
        return list(frameworks.keys())


# 全局配置加载器实例
_config_loader: Optional[FrameworkConfigLoader] = None


def get_config_loader(config_path: str = None) -> FrameworkConfigLoader:
    """
    获取全局配置加载器实例（单例）

    Args:
        config_path: 配置文件路径（仅在首次调用时有效）

    Returns:
        FrameworkConfigLoader 实例
    """
    global _config_loader
    if _config_loader is None:
        _config_loader = FrameworkConfigLoader(config_path)
    return _config_loader
