import json
import re
from pathlib import Path

INPUT_JSON = "zh-modified.json"
OUTPUT_JSON = "zh-modified-correct.json"

# 数字 → 枚举名 映射（可按项目实际继续补）
NUMBER_TO_ENUM = {
    "1": "First",
    "2": "Second",
    "3": "Third",
    "4": "Fourth",
    "5": "Fifth",
}

PLACEHOLDER_PATTERN = re.compile(r"\{#LINKORA_PLACE_HOLDER_(\d+)#\}")


def fix_placeholders(text: str) -> str:

    def replacer(match):
        num = match.group(1)
        enum_name = NUMBER_TO_ENUM.get(num)

        if not enum_name:
            # 找不到映射就原样保留，防止误伤
            return match.group(0)

        # 注意：这里要生成 Kotlin 可用的 ${...}
        return f"${{LinkoraPlaceHolder.{enum_name}.value}}"

    return PLACEHOLDER_PATTERN.sub(replacer, text)


def main():
    data = json.loads(Path(INPUT_JSON).read_text(encoding="utf-8"))

    fixed = {}
    for key, value in data.items():
        if isinstance(value, str):
            fixed[key] = fix_placeholders(value)
        else:
            fixed[key] = value

    Path(OUTPUT_JSON).write_text(json.dumps(fixed,
                                            ensure_ascii=False,
                                            indent=2),
                                 encoding="utf-8")

    print("✅ 占位符纠错完成")
    print(f"📄 输入 : {INPUT_JSON}")
    print(f"📄 输出 : {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
