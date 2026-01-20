# 沉香商家数据采集系统

## 📖 项目简介

这是一个基于腾讯地图API的商家数据采集系统，专门用于采集全国范围内与"沉香"相关的商家信息，并通过可视化网页展示数据。

## ✨ 功能特点

### 数据采集
- 🔑 **多API Key轮换**：支持5个腾讯地图API Key，每个2000次请求配额，共10000次
- 🌏 **全国覆盖**：自动采集全国34个省级行政区的数据
- 💾 **断点续传**：每完成一个省份的采集自动保存，防止数据丢失
- 📊 **详细日志**：完整记录采集过程，便于追踪和调试

### 数据展示
- 🗺️ **中国地图可视化**：使用ECharts展示各省份商家分布热力图
- 🔍 **多维度筛选**：按省份筛选、关键词搜索
- 📋 **分页展示**：清晰的表格展示，支持分页浏览
- 📥 **Excel导出**：一键导出筛选后的数据为Excel文件

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 现代浏览器（Chrome、Firefox、Safari等）

### 安装依赖

```bash
pip install requests
```

### 使用方法

#### 1. 数据采集

运行采集脚本：

```bash
python collect_tencent_maps.py
```

采集过程说明：
- 脚本会自动遍历全国34个省级行政区
- 每采集完一个省份会自动保存数据到 `merchants_data.json`
- 采集日志保存在 `collection.log`
- 支持按 `Ctrl+C` 中断，数据会自动保存

#### 2. 查看数据

在浏览器中打开 `merchants.html` 即可查看采集结果。

**注意**：由于浏览器的安全限制，需要通过HTTP服务器打开文件：

```bash
# Python 3
python -m http.server 8000

# 然后在浏览器访问
# http://localhost:8000/merchants.html
```

## 📁 文件说明

```
.
├── collect_tencent_maps.py  # 数据采集脚本
├── merchants.html            # 数据展示网页
├── merchants_data.json       # 采集的数据（生成）
├── collection.log           # 采集日志（生成）
└── README_MERCHANTS.md      # 本说明文档
```

## 🔧 配置说明

### API Keys配置

在 `collect_tencent_maps.py` 中修改：

```python
API_KEYS = [
    'XLJBZ-SNVKL-K6RPE-EIJQW-27QDE-QKBSP',
    'Y2WBZ-YPVKJ-EIDFK-DGFMF-2TGJZ-DEFJM',
    '2BNBZ-WU5E4-QDIUI-K2L3P-RBK5S-HWFRL',
    '3BHBZ-HJWCL-F63P5-EBF3P-JCWDE-5TB6P',
    'V4EBZ-TRW6Q-N245W-2JLIO-KVUZH-ZMBVS'
]
```

### 搜索关键词配置

在 `collect_tencent_maps.py` 中修改：

```python
KEYWORD = "沉香"  # 修改为您需要的关键词
```

## 📊 数据格式

### merchants_data.json 结构

```json
{
  "keyword": "沉香",
  "total_count": 123,
  "collected_at": "2026-01-20T00:00:00",
  "api_usage": {
    "key1": 150,
    "key2": 200
  },
  "stats_by_province": {
    "广东省": 45,
    "福建省": 30
  },
  "merchants": [
    {
      "id": "xxx",
      "title": "商家名称",
      "address": "详细地址",
      "category": "商业分类",
      "type": "类型",
      "location": {
        "lat": 23.1234,
        "lng": 113.5678
      },
      "tel": "电话号码",
      "province": "省份",
      "province_code": "440000",
      "collected_at": "2026-01-20T00:00:00"
    }
  ]
}
```

## 🎨 网页功能

### 统计概览
- 商家总数
- 覆盖省份数
- 最后更新时间

### 地图可视化
- 全国热力图展示
- 鼠标悬停查看详情
- 支持缩放和拖动

### 数据筛选
- 按省份筛选
- 关键词搜索（商家名称、地址、类别）
- 实时过滤

### 数据导出
- 支持导出为Excel格式
- 包含所有筛选后的数据
- 文件名自动包含日期

## ⚠️ 注意事项

1. **API配额限制**
   - 每个API Key限制2000次请求/天
   - 建议在非高峰期运行采集脚本
   - 脚本会自动轮换Key

2. **请求频率**
   - 脚本已设置合理的请求间隔
   - 避免并发请求导致封禁

3. **数据准确性**
   - 数据来源于腾讯地图API
   - 请以实际情况为准

4. **浏览器兼容性**
   - 推荐使用Chrome、Firefox等现代浏览器
   - IE可能不支持某些功能

## 🔄 更新数据

要更新数据，只需重新运行采集脚本：

```bash
python collect_tencent_maps.py
```

然后刷新浏览器页面即可看到最新数据。

## 🐛 常见问题

### 1. 数据加载失败

确保：
- `merchants_data.json` 文件存在
- 使用HTTP服务器打开HTML文件（不是直接双击打开）
- 检查浏览器控制台错误信息

### 2. API请求失败

检查：
- API Key是否有效
- 网络连接是否正常
- 是否超出配额限制

### 3. 地图不显示

可能原因：
- 网络问题导致地图数据加载失败
- 已使用备用方案，功能不受影响

## 📞 技术支持

如有问题，请检查：
1. `collection.log` 采集日志
2. 浏览器控制台错误信息
3. 网络连接状态

## 📄 许可证

本项目仅供学习和研究使用。使用腾讯地图API需遵守其服务条款。

---

**更新时间**: 2026-01-20
**版本**: 1.0.0
