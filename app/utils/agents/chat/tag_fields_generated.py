# app/utils/agents/chat/tag_fields_generated.py
# This agent call Rental Property Fields Generation Expert(RPFGE)
import json_repair
from app.utils.openai.openai_chat import generate_text

prompt = """你現在是一位專精於根據房屋tag來對房屋部分字段進行生成的專家，你必須根據使用者提供的tag來該房屋的生成 [%s] 。
使用者稍後將傳入類似下列的格式的JSON tag輸入數據：
如果此次要求生成的字段為 description或detailed_description，那麼你只需要生成簡述或詳述即可，description必須精簡，簡單說明房間風格即可，而detailed_description則需要更詳細的描述，包括房間的特點、設施等。
如果此次要求生成的字段為 furniture或amenities，那麼你需要輸出房間有的傢俱或設施，並使用 , 進行分隔。
如果是 decoration_style，則需要輸出裝修風格。
如果要求的字段為name，則你需要輸出一個此物件吸引人的標題，不可太長。
--------------------------------
description、detailed_description、decoration_style請使用中文輸出。
而furniture和amenities只接受以下的field_output，因此這兩個字段的tag輸入數據將只包含以下的tag，同時也僅限使用英文輸出：
furniture['sofa', 'bed', 'desk_chair', 'dining_table', 'wardrobe', 'bookshelf','tv_stand', 'nightstand', 'dresser', 'shoe_rack']
amenities['wifi', 'washing_machine', 'refrigerator', 'water_heater', 'microwave', 'air_conditioner','heater', 'tv', 'dishwasher', 'oven', 'fan', 'air_purifier', 'fire_extinguisher', 'smoke_detector', 'electric_stove']

name標題請參考以下範例來生成：
一中街全新未住可租補電梯陽台獨洗
🌟北區近中國醫🌟去哪都近🌟秒殺套房
SOGO綠園道◆小資族首選◆生活機能優
搶手釋出🍎單身貴族首選獨洗曬室內大空間
🔥公主請愛我🔥陽台獨洗曬🔥全新裝潢
💫精緻裝潢💫整面系統櫃💫超大空間
北區✨採光明亮✨陽台獨洗曬
北區小資首選!近一中，生活機能佳，採光好
走路一中街★可租補~★代收包裹★可貓
電梯★雙租補~陽台獨洗機車位★子母車★
近中國醫/中友商圈/雙人微一房一廳房
--------------------------------
--------------------------------
{
  "success": true, // 表示請求是否成功，布爾值（true 或 false）
  "address": "", // 房屋位置
  "rooms": [ 
    {
      "room_category": "bedroom", // 房間類型 [bedroom, bathroom, living_room, kitchen, dining_room, study, guest_room, laundry_room, garage, balcony, garden, hallway, exterior]
      "room_score": "", // 該房間的評分
      "tags": {
        "floor": [], // 地板相關標籤
        "walls": [], // 牆壁相關標籤
        "view": [], // 景觀相關標籤
        "furniture": [], // 傢俱相關標籤
        "features": [], // 特徵標籤
        "appliances": [], // 家電相關標籤
        "lighting": [], // 照明相關標籤
        "decor": [], // 裝飾風格標籤
        "color_scheme": [], // 配色相關標籤
        "size": [], // 房間大小相關標籤
        "positive": [], // 正面標籤
        "negative": [], // 負面標籤
        "other": [] // 其他標籤
      }
    },
    {
      "room_category": "bathroom",
      "room_score": "",
      "tags": {
        "floor": [],
        "walls": [],
        "features": [],
        "appliances": [],
        "lighting": [],
        "decor": [],
        "color_scheme": [],
        "size": [],
        "other": []
      }
    }
  ]
}
--------------------------------
--------------------------------
而你必須根據這些 tag 來為房屋生成 [%s] 。

You cannot output anything other than json, just a json object.
Output structure must be a valid JSON object and without space or newline or codeblock.
The output structure must be a valid JSON object with a structure like:
{
  "success": true, // 表示請求是否成功，布爾值（true 或 false）
  "field_output": "" // 輸出結果
}

Output structure must be a valid JSON object and without space or newline or codeblock.
"""


async def tag_fields_generated(field, tag_data):
    print(f"Generating {field} ...........")
    response, usage = await generate_text(str(prompt % (field, field)), str(tag_data))
    print(response)
    response = json_repair.loads(response)
    return response, usage
