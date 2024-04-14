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
    print(items)
    return items

file_path = "beforeTreeData.json"
with open(file_path, "r", encoding="utf-8") as file:
    original_data = json.load(file)


# Resetting the mind map data structure and IDs
mind_map = [
    {
        "id": "1",
        "text": "sdk展示根节点（可换名）",
        "fill": "#0288D1",
        "fontColor": "#FFFFFF",
        "stroke": "#0288D1",
        "fontWeight": "bold",
    }
]

next_id = 2  # Resetting next_id for node creation

# Populate the mind map with data from each SDK
for sdk in original_data:
    # start from id=2
    # add sdk-name entry
    sdk_id = str(next_id)
    # 使用 ID 的奇偶性来决定节点的方向
    direction = "verticalRight" if int(sdk_id) % 2 == 0 else "verticalLeft"

    mind_map.append(
        {
            "id": sdk_id,
            "text": sdk["sdk-name"],
            "parent": "1",
            "fill": "#11B3A5",
            "fontColor": "#FFFFFF",
            "stroke": "#11B3A5",
            "dir": direction,
            "headerColor": "#607D8B",
            "fontWeight": "bold",
        }
    )
    mind_map.append(
        {
            "from": "1",
            "to": sdk_id,
            "type": "line",
            "connectType": "curved",
            "stroke": "#CCC",
            "strokeWidth": 2,
            "cornersRadius": 0,
        }
    )

    # add data entry
    sdk_data_id_loc2 = 1
    sdk_data_id = str(next_id) + "." + str(sdk_data_id_loc2)
    mind_map.append(
        {
            "id": sdk_data_id,
            "text": "数据项",
            "parent": sdk_id,
            "fill": "#fff",
            "fontColor": "rgba(0,0,0,0.70)",
            "stroke": "#00C7B5",
            "headerColor": "#00C7B5",
            "strokeType": "line",
            "open":False
        }
    )
    mind_map.append(
        {
            "from": sdk_id,
            "to": sdk_data_id,
            "type": "line",
            "connectType": "curved",
            "stroke": "#CCC",
            "strokeWidth": 2,
            "cornersRadius": 0,
        }
    )
    # add data sub item
    data_items = parse_data(sdk["data"])
    data_sub_start = 1
    for index, item in enumerate(data_items):
        sdk_data_sub_id = sdk_data_id+"."+str(data_sub_start)  # Create a unique sub-node ID
        # single data item
        # Append the data node
        mind_map.append(
            {
                "id": sdk_data_sub_id,
                "text": item["main"],
                "parent": sdk_data_id,
                "fill": "#fff",
                "fontColor": "rgba(0,0,0,0.70)",
                "stroke": "#00C7B5",
                "headerColor": "#00C7B5",
                "strokeType": "line",
            }
        )

        # Append the connection line
        mind_map.append({
            "from": sdk_data_id,
            "to": sdk_data_sub_id,
            "type": "line",
            "connectType": "curved",
            "stroke": "#CCC",
            "strokeWidth": 2,
            "cornersRadius": 0,
        })

        if item['sub']:
            # contains ()
            data_sub_sub_start = 1
            for sub_data in item['sub']:
                # single data item
                # Append the data node
                mind_map.append(
                    {
                        "id": sdk_data_sub_id +"."+ str(data_sub_sub_start),
                        "text": sub_data,
                        "parent": sdk_data_sub_id,
                        "fill": "#fff",
                        "fontColor": "rgba(0,0,0,0.70)",
                        "stroke": "#00C7B5",
                        "headerColor": "#00C7B5",
                        "strokeType": "line",
                    }
                )

                # Append the connection line
                mind_map.append(
                    {
                        "from": sdk_data_sub_id,
                        "to": sdk_data_sub_id + "." + str(data_sub_sub_start),
                        "type": "line",
                        "connectType": "curved",
                        "stroke": "#CCC",
                        "strokeWidth": 2,
                        "cornersRadius": 0,
                    }
                )
                data_sub_sub_start+=1
        data_sub_start+=1

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
        mind_map.append(
            {
                "from": sdk_id,
                "to": sdk_url_id,
                "type": "line",
                "connectType": "curved",
                "stroke": "#CCC",
                "strokeWidth": 2,
                "cornersRadius": 0,
            }
        )
    else:
        # URL 列表为空时的处理代码，例如可以跳过或添加默认URL
        print("URL列表为空，跳过添加URL节点。")

    next_id += 1

with open("afterTreeData.json", "w", encoding="utf-8") as file:
    json.dump(mind_map, file, ensure_ascii=False, indent=4)
