#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高德地图商家信息采集脚本
Amap (Gaode Maps) Business Information Scraper

This script collects business information from Amap (Gaode Maps) including:
- Business name
- Address
- Phone number
- Coordinates (latitude, longitude)
- Rating and reviews
- Business type/category
"""

import requests
import json
import time
import sys
from typing import List, Dict, Optional
import argparse


class AmapScraper:
    """高德地图商家信息采集器"""
    
    def __init__(self, api_key: str):
        """
        初始化采集器
        
        Args:
            api_key: 高德地图API密钥
        """
        self.api_key = api_key
        self.base_url = "https://restapi.amap.com/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_poi(self, 
                   keyword: str, 
                   city: str = "", 
                   types: str = "",
                   page: int = 1,
                   page_size: int = 20) -> Dict:
        """
        搜索POI（地点）信息
        
        Args:
            keyword: 搜索关键词（商家名称或类型）
            city: 城市名称或城市编码
            types: POI类型，如"餐饮服务|购物服务"
            page: 页码，从1开始
            page_size: 每页结果数量，最大25
            
        Returns:
            包含搜索结果的字典
        """
        url = f"{self.base_url}/place/text"
        
        params = {
            'key': self.api_key,
            'keywords': keyword,
            'offset': min(page_size, 25),
            'page': page,
            'extensions': 'all'  # 返回详细信息
        }
        
        if city:
            params['city'] = city
        if types:
            params['types'] = types
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '1':
                return data
            else:
                print(f"API错误: {data.get('info', '未知错误')}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return {}
    
    def search_around(self,
                     location: str,
                     keyword: str = "",
                     types: str = "",
                     radius: int = 1000,
                     page: int = 1,
                     page_size: int = 20) -> Dict:
        """
        周边搜索
        
        Args:
            location: 中心点坐标 "经度,纬度"
            keyword: 搜索关键词
            types: POI类型
            radius: 搜索半径，单位米，最大50000
            page: 页码
            page_size: 每页结果数量
            
        Returns:
            包含搜索结果的字典
        """
        url = f"{self.base_url}/place/around"
        
        params = {
            'key': self.api_key,
            'location': location,
            'radius': min(radius, 50000),
            'offset': min(page_size, 25),
            'page': page,
            'extensions': 'all'
        }
        
        if keyword:
            params['keywords'] = keyword
        if types:
            params['types'] = types
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '1':
                return data
            else:
                print(f"API错误: {data.get('info', '未知错误')}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return {}
    
    def parse_poi(self, poi: Dict) -> Dict:
        """
        解析POI数据
        
        Args:
            poi: 原始POI数据
            
        Returns:
            解析后的商家信息
        """
        location = poi.get('location', '').split(',')
        
        business_info = {
            'id': poi.get('id', ''),
            'name': poi.get('name', ''),
            'type': poi.get('type', ''),
            'typecode': poi.get('typecode', ''),
            'address': poi.get('address', ''),
            'location': {
                'longitude': location[0] if len(location) > 0 else '',
                'latitude': location[1] if len(location) > 1 else ''
            },
            'tel': poi.get('tel', ''),
            'distance': poi.get('distance', ''),
            'pcode': poi.get('pcode', ''),
            'pname': poi.get('pname', ''),
            'citycode': poi.get('citycode', ''),
            'cityname': poi.get('cityname', ''),
            'adcode': poi.get('adcode', ''),
            'adname': poi.get('adname', ''),
            'business_area': poi.get('business_area', ''),
            'rating': poi.get('biz_ext', {}).get('rating', ''),
            'cost': poi.get('biz_ext', {}).get('cost', ''),
            'photos': []
        }
        
        # 提取照片信息
        photos = poi.get('photos', [])
        if photos:
            for photo in photos:
                business_info['photos'].append({
                    'title': photo.get('title', ''),
                    'url': photo.get('url', '')
                })
        
        return business_info
    
    def collect_businesses(self,
                          keyword: str,
                          city: str = "",
                          types: str = "",
                          max_results: int = 100,
                          delay: float = 0.5) -> List[Dict]:
        """
        批量采集商家信息
        
        Args:
            keyword: 搜索关键词
            city: 城市名称
            types: POI类型
            max_results: 最大结果数量
            delay: 请求间隔（秒），避免请求过快
            
        Returns:
            商家信息列表
        """
        all_businesses = []
        page = 1
        page_size = 25
        
        print(f"开始采集: 关键词='{keyword}', 城市='{city}'")
        
        while len(all_businesses) < max_results:
            print(f"正在获取第 {page} 页...")
            
            result = self.search_poi(
                keyword=keyword,
                city=city,
                types=types,
                page=page,
                page_size=page_size
            )
            
            if not result or 'pois' not in result:
                print("没有更多结果")
                break
            
            pois = result.get('pois', [])
            if not pois:
                print("当前页无结果")
                break
            
            for poi in pois:
                if len(all_businesses) >= max_results:
                    break
                business = self.parse_poi(poi)
                all_businesses.append(business)
            
            # 检查是否还有更多结果
            count = int(result.get('count', 0))
            if len(all_businesses) >= count:
                print(f"已获取所有结果: {count} 条")
                break
            
            page += 1
            time.sleep(delay)  # 延迟，避免请求过快
        
        print(f"采集完成，共获取 {len(all_businesses)} 条商家信息")
        return all_businesses
    
    def save_to_json(self, data: List[Dict], filename: str):
        """
        保存数据到JSON文件
        
        Args:
            data: 要保存的数据
            filename: 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到: {filename}")
        except Exception as e:
            print(f"保存文件失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='高德地图商家信息采集脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 搜索北京的餐厅
  python amap_scraper.py --key YOUR_API_KEY --keyword 餐厅 --city 北京 --max 50

  # 搜索上海的咖啡店
  python amap_scraper.py --key YOUR_API_KEY --keyword 咖啡 --city 上海 --output coffee.json

  # 搜索特定类型的POI（餐饮服务）
  python amap_scraper.py --key YOUR_API_KEY --keyword 火锅 --city 成都 --types 050100
        """
    )
    
    parser.add_argument(
        '--key',
        required=True,
        help='高德地图API密钥（必需）'
    )
    parser.add_argument(
        '--keyword',
        required=True,
        help='搜索关键词（必需）'
    )
    parser.add_argument(
        '--city',
        default='',
        help='城市名称或城市编码（可选）'
    )
    parser.add_argument(
        '--types',
        default='',
        help='POI类型代码（可选）'
    )
    parser.add_argument(
        '--max',
        type=int,
        default=100,
        help='最大结果数量（默认100）'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        help='请求间隔秒数（默认0.5）'
    )
    parser.add_argument(
        '--output',
        default='amap_businesses.json',
        help='输出文件名（默认amap_businesses.json）'
    )
    
    args = parser.parse_args()
    
    # 创建采集器
    scraper = AmapScraper(api_key=args.key)
    
    # 采集数据
    businesses = scraper.collect_businesses(
        keyword=args.keyword,
        city=args.city,
        types=args.types,
        max_results=args.max,
        delay=args.delay
    )
    
    if businesses:
        # 保存结果
        scraper.save_to_json(businesses, args.output)
        
        # 显示统计信息
        print("\n=== 采集统计 ===")
        print(f"总计: {len(businesses)} 条")
        if businesses:
            types_count = {}
            for b in businesses:
                btype = b.get('type', '未分类')
                types_count[btype] = types_count.get(btype, 0) + 1
            print("\n类型分布:")
            for btype, count in sorted(types_count.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {btype}: {count}")
    else:
        print("未获取到任何数据")
        sys.exit(1)


if __name__ == '__main__':
    main()
