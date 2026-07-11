# 语言、命名与中文注释（language, naming and Chinese annotations）

状态：`active`
适用习惯：H20

自然语言默认中文在前、英文原词在后。机器字段、函数名、变量名、CLI 参数、环境变量、固定文件名和原始报错保留英文，但必须有中文用途说明。

新建或大改代码时，模块 docstring、核心判断、输入输出、异常和边界使用中文注释；不得把用户无法理解的纯英文脚本当作交付。Prompt 和回报字段使用 `Goal｜目标`、`Context｜上下文` 等双语表达。

新建用户可读业务文件和目录默认 `中文名_english_name`。固定工具链文件、Python 模块和 JSON Schema 是例外；必须在索引记录 `toolchain_exception: true` 及中文用途。已有文件不因形式而改名。
