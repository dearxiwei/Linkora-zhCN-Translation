import json
from pathlib import Path

# ========= 配置 =========
INPUT_JSON = "zh-modified.json"
OUTPUT_KT = "locales_plug.kt"
ENUM_NAME = "Key"
INDENT = "    "


def escape_kotlin_string(s: str) -> str:
    """
    安全转义 Kotlin 字符串
    """
    return (s.replace("\\", "\\\\").replace("\"", "\\\"").replace(
        "\r\n", "\n").replace("\n", "\\n"))


def main():
    input_path = Path(INPUT_JSON)
    if not input_path.exists():
        raise FileNotFoundError(f"找不到输入文件: {INPUT_JSON}")

    data = json.loads(input_path.read_text(encoding="utf-8"))

    lines = []
    lines.append(f"enum class {ENUM_NAME}(val defaultValue: String) {{")

    for key, value in data.items():
        if not isinstance(value, str):
            raise ValueError(f"Key `{key}` 的 value 不是字符串")

        value = escape_kotlin_string(value)
        lines.append(f'{INDENT}{key}(defaultValue = "{value}"),')

    lines.append("}")

    Path(OUTPUT_KT).write_text("\n".join(lines), encoding="utf-8")

    print("✅ 生成完成")
    print(f"📄 输入 : {INPUT_JSON}")
    print(f"📄 输出 : {OUTPUT_KT}")
    print("👉 可直接整体复制 enum 内容到项目中使用")


if __name__ == "__main__":
    main()
