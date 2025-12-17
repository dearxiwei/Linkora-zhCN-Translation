import json
import os

# 定义文件路径
directory = "/storage/emulated/0/项目/python/LinkoraString/"
en_file = os.path.join(directory, "default_en.json")
zh_file = os.path.join(directory, "zh.json")
output_file = os.path.join(directory, "zh-modified.json")

def main():
    # 检查文件是否存在
    if not os.path.exists(en_file):
        print(f"错误：找不到英文文件 {en_file}")
        return
    if not os.path.exists(zh_file):
        print(f"错误：找不到中文文件 {zh_file}")
        return

    # 读取英文JSON文件
    with open(en_file, 'r', encoding='utf-8') as f:
        en_dict = json.load(f)
    print(f"英文词典初始键数量: {len(en_dict)}")

    # 读取中文JSON文件
    with open(zh_file, 'r', encoding='utf-8') as f:
        zh_dict = json.load(f)
    print(f"中文词典初始键数量: {len(zh_dict)}")

    # 统计变量
    added_items = []
    deleted_items = []
    missing_keys = 0
    extra_keys = 0

    # --- 第一步：检查删除 (zh中有但en中没有的) ---
    # 注意：这里必须先转换为列表，否则在遍历字典时修改字典会报错
    for key in list(zh_dict.keys()):
        if key not in en_dict:
            # 记录被删除的键值
            deleted_items.append((key, zh_dict[key]))
            # 从字典中移除
            del zh_dict[key]
            extra_keys += 1
            print(f"🗑️ 键: {key} 在英文词典中不存在，已从中文词典中删除。原值: {deleted_items[-1]}")

    # --- 第二步：检查添加 (en中有但zh中没有的) ---
    for key in en_dict:
        if key not in zh_dict:
            # 键不存在，添加到中文词典，并记录
            zh_dict[key] = en_dict[key]
            added_items.append((key, en_dict[key]))
            missing_keys += 1
            print(f"➕ 键: {key} 在中文词典中缺失，已添加。值: {en_dict[key]}")

    # --- 统计信息 ---
    print("\n" + "="*40)
    print("--- 最终统计报告 ---")
    print(f"英文词典键总数: {len(en_dict)}")
    print(f"原始中文词典键总数: {len(zh_dict) + extra_keys}")
    print(f"✅ 保留键数量: {len(zh_dict)}")
    
    if extra_keys > 0:
        print(f"🗑️ 删除数量: {extra_keys} (这些键在英文包中已不存在)")
    else:
        print(f"🗑️ 删除数量: {extra_keys}")
        
    if missing_keys > 0:
        print(f"➕ 新增数量: {missing_keys} (来自英文包的新词条)")
    else:
        print(f"➕ 新增数量: {missing_keys}")

    # --- 保存文件 ---
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(zh_dict, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 更新后的中文词典已保存到: {output_file}")

if __name__ == "__main__":
    main()
