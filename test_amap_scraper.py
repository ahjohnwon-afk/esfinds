#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高德地图采集脚本测试文件
Amap Scraper Test File

这个测试文件展示了如何在代码中使用AmapScraper类
This test file demonstrates how to use the AmapScraper class in code
"""

import sys
import os

# 确保可以导入同目录下的amap_scraper模块
# Ensure we can import amap_scraper from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from amap_scraper import AmapScraper
except ImportError as e:
    print(f"错误: 无法导入amap_scraper模块: {e}")
    print(f"Error: Cannot import amap_scraper module: {e}")
    print("请确保amap_scraper.py文件在同一目录下")
    print("Please ensure amap_scraper.py is in the same directory")
    sys.exit(1)

import json


def example_text_search():
    """示例：关键词搜索"""
    print("=" * 50)
    print("示例1: 关键词搜索")
    print("Example 1: Text Search")
    print("=" * 50)
    
    # 创建采集器实例（需要替换为真实的API Key）
    # Create scraper instance (replace with real API key)
    scraper = AmapScraper(api_key='YOUR_API_KEY')
    
    # 搜索北京的餐厅
    # Search restaurants in Beijing
    result = scraper.search_poi(
        keyword='餐厅',
        city='北京',
        page=1,
        page_size=10
    )
    
    if result and 'pois' in result:
        print(f"找到 {result.get('count', 0)} 条结果")
        print(f"Found {result.get('count', 0)} results")
        
        # 显示前3条结果
        for i, poi in enumerate(result['pois'][:3], 1):
            business = scraper.parse_poi(poi)
            print(f"\n{i}. {business['name']}")
            print(f"   地址: {business['address']}")
            print(f"   电话: {business['tel']}")
            print(f"   坐标: {business['location']}")
    else:
        print("搜索失败或无结果")
        print("Search failed or no results")
    
    print()


def example_around_search():
    """示例：周边搜索"""
    print("=" * 50)
    print("示例2: 周边搜索")
    print("Example 2: Around Search")
    print("=" * 50)
    
    scraper = AmapScraper(api_key='YOUR_API_KEY')
    
    # 搜索天安门广场周围1000米的餐厅
    # Search restaurants within 1000m of Tiananmen Square
    result = scraper.search_around(
        location='116.397428,39.90923',  # 天安门广场坐标
        keyword='餐厅',
        radius=1000,
        page=1,
        page_size=10
    )
    
    if result and 'pois' in result:
        print(f"找到 {result.get('count', 0)} 条结果")
        print(f"Found {result.get('count', 0)} results")
        
        for i, poi in enumerate(result['pois'][:3], 1):
            business = scraper.parse_poi(poi)
            print(f"\n{i}. {business['name']}")
            print(f"   距离: {business['distance']}米")
            print(f"   地址: {business['address']}")
    else:
        print("搜索失败或无结果")
        print("Search failed or no results")
    
    print()


def example_batch_collect():
    """示例：批量采集"""
    print("=" * 50)
    print("示例3: 批量采集并保存")
    print("Example 3: Batch Collection and Save")
    print("=" * 50)
    
    scraper = AmapScraper(api_key='YOUR_API_KEY')
    
    # 批量采集上海的咖啡店
    # Batch collect coffee shops in Shanghai
    businesses = scraper.collect_businesses(
        keyword='咖啡',
        city='上海',
        max_results=30,
        delay=0.5
    )
    
    if businesses:
        print(f"\n成功采集 {len(businesses)} 条商家信息")
        print(f"Successfully collected {len(businesses)} businesses")
        
        # 保存到文件
        output_file = 'test_output.json'
        scraper.save_to_json(businesses, output_file)
        
        # 显示统计信息
        print("\n商家类型分布:")
        print("Business type distribution:")
        types_count = {}
        for b in businesses:
            btype = b.get('type', '未分类')
            types_count[btype] = types_count.get(btype, 0) + 1
        
        for btype, count in sorted(types_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {btype}: {count}")
    else:
        print("采集失败或无结果")
        print("Collection failed or no results")
    
    print()


def example_custom_processing():
    """示例：自定义数据处理"""
    print("=" * 50)
    print("示例4: 自定义数据处理")
    print("Example 4: Custom Data Processing")
    print("=" * 50)
    
    scraper = AmapScraper(api_key='YOUR_API_KEY')
    
    # 搜索并过滤有电话的商家
    # Search and filter businesses with phone numbers
    result = scraper.search_poi(
        keyword='书店',
        city='北京',
        page=1,
        page_size=20
    )
    
    if result and 'pois' in result:
        businesses_with_phone = []
        
        for poi in result['pois']:
            business = scraper.parse_poi(poi)
            # 只保留有电话号码的商家
            if business['tel']:
                businesses_with_phone.append(business)
        
        print(f"找到 {len(result['pois'])} 条结果")
        print(f"Found {len(result['pois'])} results")
        print(f"其中有电话的: {len(businesses_with_phone)} 条")
        print(f"With phone numbers: {len(businesses_with_phone)}")
        
        # 显示前3条有电话的结果
        for i, business in enumerate(businesses_with_phone[:3], 1):
            print(f"\n{i}. {business['name']}")
            print(f"   电话: {business['tel']}")
            print(f"   地址: {business['address']}")
    else:
        print("搜索失败或无结果")
        print("Search failed or no results")
    
    print()


def print_usage_note():
    """打印使用说明"""
    print("=" * 70)
    print("使用说明 / Usage Notes")
    print("=" * 70)
    print("""
注意: 此测试文件需要有效的高德地图API Key才能运行。
Note: This test file requires a valid Amap API key to run.

获取API Key的步骤 / Steps to get API key:
1. 访问 https://lbs.amap.com/
   Visit https://lbs.amap.com/
   
2. 注册并登录账号
   Register and login
   
3. 创建应用并添加Key（选择"Web服务"类型）
   Create application and add key (select "Web Service" type)
   
4. 在代码中替换 'YOUR_API_KEY' 为实际的Key
   Replace 'YOUR_API_KEY' with your actual key in the code

运行测试 / Run tests:
    python test_amap_scraper.py
    
或者使用命令行工具 / Or use command line tool:
    python amap_scraper.py --key YOUR_KEY --keyword 餐厅 --city 北京
""")
    print("=" * 70)
    print()


if __name__ == '__main__':
    print_usage_note()
    
    print("\n注意: 以下示例需要有效的API Key才能执行")
    print("Note: The following examples require a valid API key to execute\n")
    
    # 取消注释以下行来运行示例（需要先设置有效的API Key）
    # Uncomment the following lines to run examples (requires valid API key)
    
    # example_text_search()
    # example_around_search()
    # example_batch_collect()
    # example_custom_processing()
    
    print("若要运行示例，请在代码中设置有效的API Key并取消注释相应的函数调用")
    print("To run examples, set a valid API key in the code and uncomment the function calls")
