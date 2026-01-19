# 高德地图商家信息采集脚本

## 简介

这是一个用于采集高德地图（Amap/Gaode Maps）商家信息的Python脚本。可以根据关键词、城市、POI类型等条件搜索并采集商家的详细信息。

## 功能特性

- ✅ 关键词搜索商家信息
- ✅ 支持城市范围限定
- ✅ 支持POI类型过滤
- ✅ 批量采集，自动翻页
- ✅ 采集信息包括：
  - 商家名称
  - 详细地址
  - 联系电话
  - 经纬度坐标
  - 商家类型
  - 评分和人均消费
  - 商家照片
- ✅ 自动保存为JSON格式
- ✅ 请求速率控制，避免频繁请求
- ✅ 完善的错误处理

## 安装依赖

```bash
pip install requests
```

或者使用requirements文件：

```bash
pip install -r requirements.txt
```

## 获取高德地图API Key

1. 访问高德开放平台：https://lbs.amap.com/
2. 注册账号并登录
3. 进入控制台创建应用
4. 添加Key，选择"Web服务"类型
5. 复制生成的API Key

## 使用方法

### 基本用法

```bash
python amap_scraper.py --key YOUR_API_KEY --keyword 餐厅 --city 北京
```

### 完整参数说明

```
必需参数:
  --key KEY          高德地图API密钥
  --keyword KEYWORD  搜索关键词（如：餐厅、咖啡馆、酒店）

可选参数:
  --city CITY        城市名称或城市编码（如：北京、上海、0755）
  --types TYPES      POI类型代码（如：050100代表餐饮服务）
  --max MAX          最大结果数量（默认100）
  --delay DELAY      请求间隔秒数（默认0.5秒，避免请求过快）
  --output OUTPUT    输出文件名（默认amap_businesses.json）
```

### 使用示例

#### 1. 搜索北京的餐厅（获取50条）

```bash
python amap_scraper.py --key YOUR_API_KEY --keyword 餐厅 --city 北京 --max 50
```

#### 2. 搜索上海的咖啡店并保存到指定文件

```bash
python amap_scraper.py --key YOUR_API_KEY --keyword 咖啡 --city 上海 --output shanghai_coffee.json
```

#### 3. 搜索成都的火锅店（使用POI类型代码）

```bash
python amap_scraper.py --key YOUR_API_KEY --keyword 火锅 --city 成都 --types 050100 --max 200
```

#### 4. 搜索深圳的酒店（使用城市编码）

```bash
python amap_scraper.py --key YOUR_API_KEY --keyword 酒店 --city 0755 --max 100
```

## 常用POI类型代码

| 类型代码 | 类型名称 |
|---------|---------|
| 050000 | 餐饮服务 |
| 050100 | 中餐厅 |
| 050200 | 外国餐厅 |
| 050300 | 快餐厅 |
| 060000 | 购物服务 |
| 060100 | 购物中心 |
| 060200 | 便民商店/便利店 |
| 070000 | 生活服务 |
| 080000 | 体育休闲服务 |
| 080100 | 体育场馆 |
| 080200 | 运动场所 |
| 100000 | 医疗保健服务 |
| 110000 | 住宿服务 |
| 110100 | 宾馆酒店 |
| 120000 | 风景名胜 |
| 130000 | 商务住宅 |
| 140000 | 政府机构及社会团体 |
| 150000 | 科教文化服务 |
| 160000 | 交通设施服务 |
| 170000 | 金融保险服务 |
| 180000 | 公司企业 |
| 190000 | 道路附属设施 |
| 200000 | 地名地址信息 |

完整的POI分类代码请参考：https://lbs.amap.com/api/webservice/guide/api/search

## 输出数据格式

采集的数据将保存为JSON格式，结构如下：

```json
[
  {
    "id": "B000A7BD6C",
    "name": "肯德基(王府井店)",
    "type": "餐饮服务;快餐厅;快餐厅",
    "typecode": "050301",
    "address": "东城区王府井大街200号",
    "location": {
      "longitude": "116.410033",
      "latitude": "39.909187"
    },
    "tel": "010-65253715",
    "distance": "",
    "pcode": "110000",
    "pname": "北京市",
    "citycode": "010",
    "cityname": "北京市",
    "adcode": "110101",
    "adname": "东城区",
    "business_area": "王府井",
    "rating": "4.5",
    "cost": "35",
    "photos": [
      {
        "title": "门面照片",
        "url": "https://..."
      }
    ]
  }
]
```

### 字段说明

- `id`: 商家唯一标识
- `name`: 商家名称
- `type`: 商家类型（中文描述）
- `typecode`: POI类型代码
- `address`: 详细地址
- `location`: 坐标信息
  - `longitude`: 经度
  - `latitude`: 纬度
- `tel`: 联系电话
- `cityname`: 所在城市
- `adname`: 所在区县
- `business_area`: 商圈名称
- `rating`: 评分（如果有）
- `cost`: 人均消费（如果有）
- `photos`: 商家照片列表

## 注意事项

1. **API限额**: 高德地图API有调用次数限制，个人开发者版本通常为每日3000次。请合理控制采集频率。

2. **延迟设置**: 建议设置合理的请求延迟（--delay参数），避免请求过于频繁被限制。

3. **数据准确性**: 采集的数据来自高德地图，数据的准确性和时效性依赖于高德地图的更新。

4. **商业使用**: 如需商业使用，请确保遵守高德地图API的使用协议。

5. **隐私保护**: 请遵守相关法律法规，保护用户隐私，不要滥用采集的数据。

## 常见问题

### Q1: 提示"API错误: INVALID_USER_KEY"

A: 请检查你的API Key是否正确，或者Key是否已经启用了"Web服务"权限。

### Q2: 返回结果很少或为空

A: 可能原因：
- 搜索关键词过于具体，建议使用更通用的关键词
- 城市名称错误或城市没有相关商家
- POI类型代码不匹配

### Q3: 如何提高采集速度？

A: 可以适当降低`--delay`参数，但需要注意：
- 不要设置过小的延迟，可能导致被限流
- 建议最小延迟为0.3秒
- 如果遇到频繁失败，请增加延迟时间

### Q4: 采集的数据不完整

A: 部分商家可能没有提供完整的信息（如电话、评分等），这是正常现象。可以在后续数据处理中过滤或补充。

## 高级用法

### 周边搜索

如果需要使用周边搜索功能（搜索指定坐标周围的商家），可以在代码中调用`search_around`方法：

```python
from amap_scraper import AmapScraper

scraper = AmapScraper(api_key='YOUR_API_KEY')

# 搜索指定坐标（经度,纬度）周围1000米的餐厅
result = scraper.search_around(
    location='116.397428,39.90923',
    keyword='餐厅',
    radius=1000
)
```

### 自定义数据处理

你可以修改`parse_poi`方法来自定义需要采集的字段，或者在`collect_businesses`方法中添加数据过滤逻辑。

## 技术支持

如有问题或建议，欢迎提Issue。

## 许可证

MIT License

## 相关链接

- 高德开放平台: https://lbs.amap.com/
- 高德Web服务API文档: https://lbs.amap.com/api/webservice/summary
- POI分类编码表: https://lbs.amap.com/api/webservice/guide/api/search
