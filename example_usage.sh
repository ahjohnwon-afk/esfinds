#!/bin/bash
# 高德地图商家信息采集示例脚本
# Amap Scraper Example Usage Script

# 注意：请将YOUR_API_KEY替换为你的实际高德地图API密钥
# Note: Replace YOUR_API_KEY with your actual Amap API key
API_KEY="YOUR_API_KEY"

# 检查API Key是否已设置
if [ "$API_KEY" = "YOUR_API_KEY" ]; then
    echo "错误: 请先在脚本中设置你的API Key"
    echo "Error: Please set your API key in the script first"
    exit 1
fi

echo "======================================"
echo "高德地图商家信息采集示例"
echo "Amap Business Scraper Examples"
echo "======================================"
echo ""

# 示例1: 搜索北京的餐厅
echo "示例1: 搜索北京的餐厅（前20条）"
echo "Example 1: Search restaurants in Beijing (first 20)"
python3 amap_scraper.py \
    --key "$API_KEY" \
    --keyword "餐厅" \
    --city "北京" \
    --max 20 \
    --output "beijing_restaurants.json"
echo ""

# 示例2: 搜索上海的咖啡店
echo "示例2: 搜索上海的咖啡店"
echo "Example 2: Search coffee shops in Shanghai"
python3 amap_scraper.py \
    --key "$API_KEY" \
    --keyword "咖啡" \
    --city "上海" \
    --max 30 \
    --output "shanghai_coffee.json"
echo ""

# 示例3: 搜索成都的火锅店（指定POI类型）
echo "示例3: 搜索成都的火锅店"
echo "Example 3: Search hot pot restaurants in Chengdu"
python3 amap_scraper.py \
    --key "$API_KEY" \
    --keyword "火锅" \
    --city "成都" \
    --types "050100" \
    --max 50 \
    --output "chengdu_hotpot.json"
echo ""

# 示例4: 搜索深圳的购物中心
echo "示例4: 搜索深圳的购物中心"
echo "Example 4: Search shopping malls in Shenzhen"
python3 amap_scraper.py \
    --key "$API_KEY" \
    --keyword "购物中心" \
    --city "深圳" \
    --types "060100" \
    --max 40 \
    --output "shenzhen_malls.json"
echo ""

echo "======================================"
echo "所有示例执行完成！"
echo "All examples completed!"
echo "======================================"
echo ""
echo "生成的文件："
echo "Generated files:"
ls -lh *restaurants*.json *coffee*.json *hotpot*.json *malls*.json 2>/dev/null || echo "  (请确保API Key正确以生成文件)"
