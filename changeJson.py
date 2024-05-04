import json


# 拆分数据项的函数
def parse_data(data):
    """Split data field into multiple sub-items with proper handling of grouped sub-items in parentheses."""
    items = []
    parts = []
    temp_part = ""
    depth = 0

    for char in data:
        if char == "（":
            depth += 1
        elif char == "）":
            depth -= 1

        if char == "、" and depth == 0:
            parts.append(temp_part)
            temp_part = ""
        else:
            temp_part += char

    if temp_part:
        parts.append(temp_part)  # Append the last part if there is any

    # Now handle each part separately
    for part in parts:
        if "（" in part and "）" in part:
            # Clean and split the main and sub-items
            main_part, sub_part = part.split("（")
            sub_part = sub_part.replace("）", "").strip()
            main_part = main_part.strip()
            # Sub-items could be further split by '、'
            sub_items = sub_part.split("、")
            items.append({"main": main_part, "sub": [s.strip() for s in sub_items]})
        else:
            items.append({"main": part.strip(), "sub": []})
    # print(items)
    return items


file_path = "newbeforeTreeData.json"
with open(file_path, "r", encoding="utf-8") as file:
    original_data = json.load(file)


# Resetting the mind map data structure and IDs
mind_map = [
    {
        "id": "1",
        "text": "SDK隐私政策信息",
        "fill": "#0288D1",
        "fontColor": "#FFFFFF",
        "stroke": "#0288D1",
        "fontWeight": "bold",
    }
]


next_id = 2  # Resetting next_id for node creation

total_counts = {}  # 统计不合法 数据项数量 sdk-name : numbers


# 初始化全部的统计信息

# Populate the mind map with data from each SDK
for sdk in original_data:

    # 将三个全部拆开
    more_items = parse_data(sdk["more-data"])
    fuzzy_items = parse_data(sdk["fuzzy-data"])
    less_items = parse_data(sdk["less-data"])

    # print("more_items:", more_items)
    # print("fuzzy_items:",fuzzy_items)
    # print("less_items:", less_items)

    """
        处理less_data
    """
    count_less_items = 0
    # 统计数量 后续进行节点关系的绘制
    if less_items != []:
        for less_item in less_items:
            # 括号内子项不为kong
            if less_item["sub"] != []:
                count_less_items += len(less_item["sub"]) + 1
            else:
                count_less_items += 1

    """
        处理fuzzy_items
    """
    count_fuzzy_items = 0
    # 统计数量 后续进行节点关系的绘制
    fuzzy_data_hash = {}
    # 设置哈希  便于后续进行颜色定位
    if fuzzy_items != []:
        for fuzzy_item in fuzzy_items:
            # 括号内子项不为kong
            if fuzzy_item["sub"] != []:
                count_fuzzy_items += len(fuzzy_item["sub"]) + 1
                for sub_fuzzy_item in fuzzy_item["sub"]:
                    fuzzy_data_hash[sub_fuzzy_item] = 1 
            else:
                count_fuzzy_items += 1
                fuzzy_data_hash[fuzzy_item["main"]] = 1

    """
        处理more_items
    """

    count_more_items = 0
    # 统计数量 后续进行节点关系的绘制
    more_data_hash = {}
    # 设置哈希  便于后续进行颜色定位
    if more_items != []:
        for more_item in more_items:
            # 括号内子项不为kong
            if more_item["sub"] != []:
                count_more_items += len(more_item["sub"]) + 1
                for sub_more_item in more_item["sub"]:
                    more_data_hash[sub_more_item] = 1
            else:
                count_more_items += 1
                more_data_hash[more_item["main"]] = 1

    # print("count_more_items:", count_more_items)
    # print("count_less_items:", count_less_items)
    # print("count_fuzzy_items:", count_fuzzy_items)

    """
        记录全部的数量 到哈希表中
    """
    total_counts[sdk["sdk-name"]] = {
        "more": count_more_items,
        "fuzzy": count_fuzzy_items,
        "less": count_less_items,
        "total": count_more_items + count_less_items + count_fuzzy_items,
    }

    # start from id=2
    # add sdk-name entry
    sdk_id = str(next_id)
    # 使用 ID 的奇偶性来决定节点的方向
    direction = "verticalRight" if int(sdk_id) % 2 == 0 else "verticalLeft"

    """
        添加sdk-name项
        作为次级根节点
    """
    mind_map.append(
        {
            "id": sdk_id,
            "text": sdk["sdk-name"],
            "parent": "1",
            "fill": "#005B4F",
            "fontColor": "#FFFFFF",
            "stroke": "#005B4F",
            "fontWeight": "bold",
            "type": "topic",
            "lineHeight": 14,
            "fontSize": 14,
            "textAlign": "center",
            "fontStyle": "normal",
            "textVerticalAlign": "center",
            "strokeWidth": 1,
            "strokeType": "line",
            "dir": direction,
            "headerColor": "#607D8B",
        }
    )

    # add data entry
    """
        添加数据项这个根节点
    """
    sdk_data_id_loc2 = 1
    sdk_data_id = str(next_id) + "." + str(sdk_data_id_loc2)
    mind_map.append(
        {
            "id": sdk_data_id,
            "text": "数据项",
            "parent": sdk_id,
            "fill": "#11B3A3",
            "fontColor": "#FFFFFF",
            "stroke": "#11B3A5",
            "dir": "verticalRight",
            "headerColor": "#607D8B",
            "fontWeight": "bold",
            "type": "topic",
            "lineHeight": 14,
            "fontSize": 14,
            "textAlign": "center",
            "fontStyle": "normal",
            "textVerticalAlign": "center",
            "strokeWidth": 1,
            "strokeType": "line",
            "open": False,
        }
    )

    """
        添加sdk["data"]中的全部内容
        根据括号进行层级关系的拆分
    """
    # add data sub item
    data_items = parse_data(sdk["data"])
    data_sub_start = 1

    for index, item in enumerate(data_items):
        sdk_data_sub_id = (
            sdk_data_id + "." + str(data_sub_start)
        )  
        """
            节点颜色变换机制
        """
        # 进行节点的颜色变换
        fill_color = "#fff"

        if fuzzy_data_hash.get(item["main"])  == 1:
            fill_color = "#F3EADA"  # 模糊的使用填充蓝色

        if more_data_hash.get(item["main"]) == 1:
            fill_color = "#FFA17A"  # 多说的使用填充红色

        mind_map.append(
            {
                "id": sdk_data_sub_id,
                "text": item["main"],
                "parent": sdk_data_id,
                "fill": fill_color,
                "fontColor": "rgba(0,0,0,0.70)",
                "stroke": "#FFA07A",
                "dir": "verticalRight",
                "headerColor": "#00C7B5",
                "strokeType": "line",
                "type": "topic",
                "lineHeight": 14,
                "fontSize": 14,
                "textAlign": "center",
                "fontStyle": "normal",
                "textVerticalAlign": "center",
            }
        )

        if item["sub"]:
            # contains ()
            data_sub_sub_start = 1
            for sub_data in item["sub"]:
                # single data item
                # Append the data node
                mind_map.append(
                    {
                        "id": sdk_data_sub_id + "." + str(data_sub_sub_start),
                        "text": sub_data,
                        "parent": sdk_data_sub_id,
                        "fill": fill_color,
                        "fontColor": "rgba(0,0,0,0.70)",
                        "stroke": "#FFA07A",
                        "dir": "verticalRight",
                        "headerColor": "#00C7B5",
                        "strokeType": "line",
                        "type": "topic",
                        "lineHeight": 14,
                        "fontSize": 14,
                        "textAlign": "center",
                        "fontStyle": "normal",
                        "textVerticalAlign": "center",
                    }
                )
                data_sub_sub_start += 1

        data_sub_start += 1

    """
            添加当前sdK-name中的 less-data
            使用虚线样式
        """

    for index, item in enumerate(less_items):
        sdk_data_sub_id = sdk_data_id + "." + str(data_sub_start)
        mind_map.append(
            {
                "id": sdk_data_sub_id,
                "text": item["main"],
                "parent": sdk_data_id,
                "fill": "#fff",
                "fontColor": "rgba(0,0,0,0.70)",
                "stroke": "#00C7B5",
                "dir": "verticalRight",
                "headerColor": "#00C7B5",
                "strokeType": "dash",
                "type": "topic",
                "lineHeight": 14,
                "fontSize": 14,
                "textAlign": "center",
                "fontStyle": "normal",
                "textVerticalAlign": "center",
                "strokeWidth": "3",
            }
        )

        if item["sub"]:
            # contains ()
            data_sub_sub_start = 1
            for sub_data in item["sub"]:
                # single data item
                # Append the data node
                mind_map.append(
                    {
                        "id": sdk_data_sub_id + "." + str(data_sub_sub_start),
                        "text": sub_data,
                        "parent": sdk_data_sub_id,
                        "fill": "#fff",
                        "fontColor": "rgba(0,0,0,0.70)",
                        "stroke": "#00C7B5",
                        "dir": "verticalRight",
                        "headerColor": "#00C7B5",
                        "strokeType": "dash",
                        "type": "topic",
                        "lineHeight": 14,
                        "fontSize": 14,
                        "textAlign": "center",
                        "fontStyle": "normal",
                        "textVerticalAlign": "center",
                        "strokeWidth": "3",
                    }
                )

                # Append the connection line
                data_sub_sub_start += 1

        data_sub_start += 1

    """
        添加URL链接节点项
    """
    # add url link
    sdk_data_id_loc2 += 1
    sdk_url_id = str(next_id) + "." + str(sdk_data_id_loc2)
    # 检查 URL 列表是否为空
    if sdk["url"]:
        mind_map.append(
            {
                "id": sdk_url_id,
                "type": "customNode",
                "url": sdk["url"][0],  # 安全地访问第一个元素
                "parent": sdk_id,
            }
        )
    else:
        # URL 列表为空时的处理代码，例如可以跳过或添加默认URL
        print("URL列表为空，跳过添加URL节点。")

    next_id += 1

# Sorting by the total number of illegal data entries in descending order
sorted_sdk_counts = dict(
    sorted(total_counts.items(), key=lambda item: item[1]["total"], reverse=True)
)
# Create statistics summary
stats = {"total_sdks": len(sorted_sdk_counts), "details": sorted_sdk_counts}

output_data = {"statistics": stats, "mindMap": mind_map}

"""
    写入转换格式后的json文件
"""
with open("afterTreeData.json", "w", encoding="utf-8") as file:
    json.dump(output_data, file, ensure_ascii=False, indent=4)
