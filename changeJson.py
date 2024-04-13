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


original_data = [
    {
        "sdk-name": "淘宝",
        "data": "位置信息、应用列表、剪切板信息、设备信息（IMSI、IMEI、MAC地址、BSSID、SSID、IDFA、MEID、AndroidID）、手机存储权限、音频",
        "purpose": [
            "帮助用户使用淘宝账号安全登录医鹿平台",
            "帮助用户浏览H5页面",
            "H5框架的基础能力和服务",
            "提供平台技术服务；",
        ],
        "url": [
            "https://terms.alicdn.com/legal-agreement/terms/suit_bu1_taobao/suit_bu1_taobao201703241622_61002.html?spm=a2145.7268393.0.0.f9aa5d7ccvMkrK"
        ],
        "ori-url": "https://terms.alicdn.com/legal-agreement/terms/suit_bu1_taobao/suit_bu1_taobao201703241622_61002.html?spm=a2145.7268393.0.0.f9aa5d7ccvMkrK",
        "sdk-url": [
            "https://terms.alicdn.com/legal-agreement/terms/suit_bu1_taobao/suit_bu1_taobao201703241622_61002.html?spm=a2145.7268393.0.0.f9aa5d7ccvMkrK"
        ],
        "url-judge": "是隐私政策",
        "sdk-url-judge": "是sdk隐私政策",
    },
    {
        "sdk-name": "优酷（com.youku）",
        "data": "应用列表",
        "purpose": ["为用户提供视频观看功能；"],
        "url": [
            "https://terms.alicdn.com/legal-agreement/terms/suit_bu1_unification/suit_bu1_unification202005141916_91107.html"
        ],
        "ori-url": "https://terms.alicdn.com/legal-agreement/terms/suit_bu1_unification/suit_bu1_unification202005141916_91107.html",
        "sdk-url": [
            "https://terms.alicdn.com/legal-agreement/terms/suit_bu1_unification/suit_bu1_unification202005141916_91107.html"
        ],
        "url-judge": "是隐私政策",
        "sdk-url-judge": "是sdk隐私政策",
    },
]

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
    mind_map.append(
        {
            "id": sdk_id,
            "text": sdk["sdk-name"],
            "parent": "1",
            "fill": "#11B3A5",
            "fontColor": "#FFFFFF",
            "stroke": "#11B3A5",
            "dir": "verticalRight",
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
            "dir": "verticalRight",
            "headerColor": "#00C7B5",
            "strokeType": "line",
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
                "dir": "verticalRight",
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
                        "dir": "verticalRight",
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
    mind_map.append(
        {
            "id": sdk_url_id,
            "type": "customNode",
            "url": sdk["url"][0],
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

    next_id += 1

with open("afterTreeData.json", "w", encoding="utf-8") as file:
    json.dump(mind_map, file, ensure_ascii=False, indent=4)
