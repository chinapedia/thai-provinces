import json
import requests

# 定义文件路径
input_file = 'Provinces.json'
output_file = 'README.md'

# Wikidata API endpoint
wikidata_url = "https://www.wikidata.org/w/api.php"

# 读取 Provinces.json
with open(input_file, 'r', encoding='utf-8-sig') as f:
    provinces = json.load(f)

# 创建 GFM 格式的表格
table = "| PROVINCE_ID | English Name | Thai Name | Chinese Name |\n"
table += "|-------------|--------------|-----------|--------------|\n"

# 遍历每个省份
for province in provinces:
    province_id = province['PROVINCE_ID']
    eng_name = province['PROVINCE_NAME_ENG']
    thai_name = province['PROVINCE_NAME_THA']
    chi_name = ""

    # 尝试通过 Wikidata API 获取中文名称
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": eng_name,
        "limit": 1
    }

    try:
        response = requests.get(wikidata_url, params=params)
        data = response.json()

        if data['search']:
            entity_id = data['search'][0]['id']
            # 获取中文标签
            entity_params = {
                "action": "wbgetentities",
                "format": "json",
                "ids": entity_id,
                "props": "labels",
                "languages": "zh"
            }
            entity_response = requests.get(wikidata_url, params=entity_params)
            entity_data = entity_response.json()

            if 'zh' in entity_data['entities'][entity_id]['labels']:
                chi_name = entity_data['entities'][entity_id]['labels']['zh']['value']
    except Exception as e:
        print(f"Error fetching data for {eng_name}: {e}")

    # 将结果添加到表格中
    table += f"| {province_id} | {eng_name} | {thai_name} | {chi_name} |\n"

# 保存表格到 README.md 文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(table)

print(f"Markdown table saved to {output_file}")
