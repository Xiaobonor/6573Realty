# RentalProperty 模型說明

### 模型: RentalProperty

- **uuid**: 房屋唯一標識符（主鍵，必須，自動隨機生成）
- **name**: 房屋名稱（必須）
- **description**: 房屋簡介（必須）
- **detailed_description**: 房屋詳細說明（必須）
- **landlord**: 房屋出租者（連結到 User 的 google_id，必須）
- **furniture**: 房屋擁有傢俱（必須，列表，例如有 Refrigerator, Air Conditioner）
- **amenities**: 社區擁有配備（必須，列表，例如有 Elevator, Carriage, Water dispenser）
- **address**: 房屋位置（地址，必須）
- **floor_info**: 房屋樓層/總樓高（必須，例如 "3/5"）
- **rent_price**: 房屋租金（必須）
- **negotiation**: 房屋議價（必須，包含是否允許、議價範圍（最低多少，最高多少））
- **property_type**: 房屋類別（必須，選擇: [整曾住家, 獨立套房, 雅房]）
- **layout**: 房屋格局（必須，選擇: [1房、2房、3房、4房]）
- **allowances**: 允許內容（必須，包含是否允許寵物及額外費用、是否有車位及額外費用）
- **features**: 允許內容（必須，列表，例如是否可開伙、是否可養寵物、是否有陽台）
- **building_type**: 房屋型態（必須，選項: [公寓、電梯大樓、透天、別墅]）
- **area**: 坪數（必須）
- **rent_includes**: 租金包含什麼（必須，包含電、水、網路、管理費等）
- **decoration_style**: 裝潢風格（必須）
- **tenant_preferences**: 租客篩選（必須，列表多選，例如限男租、限女租、禁八大等）
- **community**: 所屬社區（必須，或輸入 None）
- **min_lease_months**: 最短租約月數（必須）
- **has_balcony**: 是否有陽台（必須）
- **bathroom_info**: 衛浴（非必須）
- **building_age**: 屋齡（非必須）
- **tags**: 特色標籤（必須，列表）
- **created_at**: 物件發布時間（必須，自動設置為當前時間）
- **images**: 物件照片（必須，列表，包括網址和圖片標題）
- **view_count**: 物件總瀏覽數（必須，預設為 0）
- **last_updated_at**: 最後更新時間（必須，自動設置為當前時間）
- **last_pushed_at**: 最後推送時間（非必須）
- **rooms**: 房間詳細信息（必須，列表，包括房間類型、評分和標籤）

### 子模型

##### Room
- **room_category**: 房間類型（必須，選項: [bedroom, bathroom, living_room, kitchen, dining_room, study, guest_room, laundry_room, garage, balcony, garden, hallway, exterior]）
- **room_score**: 房間評分（必須，範圍 0 到 100）
- **tags**: 房間標籤（必須，嵌入文檔）

###### RoomTags
- **floor**: 地板相關標籤（必須，列表）
- **walls**: 牆壁相關標籤（必須，列表）
- **view**: 景觀相關標籤（必須，列表）
- **furniture**: 傢俱相關標籤（必須，列表）
- **features**: 特徵標籤（必須，列表）
- **appliances**: 家電相關標籤（必須，列表）
- **lighting**: 照明相關標籤（必須，列表）
- **decor**: 裝飾風格標籤（必須，列表）
- **color_scheme**: 配色相關標籤（必須，列表）
- **size**: 房間大小相關標籤（必須，列表）
- **other**: 其他標籤（必須，列表）

##### Negotiation
- **allow**: 是否允許議價（必須）
- **min_price**: 最低議價範圍（必須）
- **max_price**: 最高議價範圍（必須）

##### Allowance
- **allow**: 是否允許（必須）
- **additional_fee**: 額外費用（必須）

##### RentIncludes
- **electric**: 電費相關（必須，包含是否為台電、每度價格）
- **internet**: 網路相關（必須，包含是否包含在租金內、上傳/下載速度、額外費用）
- **water**: 水費相關（必須，包含是否包含在租金內、額外費用）
- **management_fee**: 管理費相關（必須，包含是否包含在租金內、額外費用）

###### Electric
- **tai_power**: 是否為台電（必須）
- **price_per_unit**: 每度價格（必須）

###### Internet
- **included**: 是否包含在租金內（必須）
- **upload_speed**: 上傳速度（必須）
- **download_speed**: 下載速度（必須）
- **additional_fee**: 額外費用（必須）

###### Water
- **included**: 是否包含在租金內（必須）
- **additional_fee**: 額外費用（必須）

###### ManagementFee
- **included**: 是否包含在租金內（必須）
- **additional_fee**: 額外費用（必須）

##### Image
- **url**: 圖片網址（必須）
- **title**: 圖片標題（必須）
