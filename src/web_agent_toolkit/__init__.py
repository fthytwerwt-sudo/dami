"""大米低 GI 网页获客工具底座。

本包只提供本地合成沙箱和可替换 Adapter；默认模式为 ``draft_only``，
不包含真实客户联系、消息提交、账号登录或业务决策能力。
"""

from .contracts import DraftResult, KnowledgeResult, PageEvidence, PolicyResult, ToolAction

__all__ = [
    "DraftResult",
    "KnowledgeResult",
    "PageEvidence",
    "PolicyResult",
    "ToolAction",
]

__version__ = "0.1.0"
