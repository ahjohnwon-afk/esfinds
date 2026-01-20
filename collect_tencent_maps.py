#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tencent Maps Merchant Data Collection Script
采集腾讯地图商家信息脚本 - 关键词：沉香
"""

import requests
import json
import time
import logging
from typing import List, Dict, Any
from datetime import datetime
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('collection.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# API Keys - 每个有2000次请求额度
API_KEYS = [
    'XLJBZ-SNVKL-K6RPE-EIJQW-27QDE-QKBSP',
    'Y2WBZ-YPVKJ-EIDFK-DGFMF-2TGJZ-DEFJM',
    '2BNBZ-WU5E4-QDIUI-K2L3P-RBK5S-HWFRL',
    '3BHBZ-HJWCL-F63P5-EBF3P-JCWDE-5TB6P',
    'V4EBZ-TRW6Q-N245W-2JLIO-KVUZH-ZMBVS'
]

# 搜索关键词
KEYWORD = "沉香"

# 中国主要省份和直辖市
PROVINCES = [
    {"name": "北京市", "code": "110000"},
    {"name": "天津市", "code": "120000"},
    {"name": "河北省", "code": "130000"},
    {"name": "山西省", "code": "140000"},
    {"name": "内蒙古自治区", "code": "150000"},
    {"name": "辽宁省", "code": "210000"},
    {"name": "吉林省", "code": "220000"},
    {"name": "黑龙江省", "code": "230000"},
    {"name": "上海市", "code": "310000"},
    {"name": "江苏省", "code": "320000"},
    {"name": "浙江省", "code": "330000"},
    {"name": "安徽省", "code": "340000"},
    {"name": "福建省", "code": "350000"},
    {"name": "江西省", "code": "360000"},
    {"name": "山东省", "code": "370000"},
    {"name": "河南省", "code": "410000"},
    {"name": "湖北省", "code": "420000"},
    {"name": "湖南省", "code": "430000"},
    {"name": "广东省", "code": "440000"},
    {"name": "广西壮族自治区", "code": "450000"},
    {"name": "海南省", "code": "460000"},
    {"name": "重庆市", "code": "500000"},
    {"name": "四川省", "code": "510000"},
    {"name": "贵州省", "code": "520000"},
    {"name": "云南省", "code": "530000"},
    {"name": "西藏自治区", "code": "540000"},
    {"name": "陕西省", "code": "610000"},
    {"name": "甘肃省", "code": "620000"},
    {"name": "青海省", "code": "630000"},
    {"name": "宁夏回族自治区", "code": "640000"},
    {"name": "新疆维吾尔自治区", "code": "650000"},
    {"name": "台湾省", "code": "710000"},
    {"name": "香港特别行政区", "code": "810000"},
    {"name": "澳门特别行政区", "code": "820000"}
]


class TencentMapsCollector:
    """腾讯地图数据采集器"""
    
    def __init__(self):
        self.api_keys = API_KEYS.copy()
        self.current_key_index = 0
        self.key_usage = {key: 0 for key in API_KEYS}
        self.max_requests_per_key = 2000
        self.all_merchants = []
        self.base_url = "https://apis.map.qq.com/ws/place/v1/search"
        
    def get_current_api_key(self) -> str:
        """获取当前可用的API Key"""
        # 检查当前key是否还有配额
        current_key = self.api_keys[self.current_key_index]
        if self.key_usage[current_key] >= self.max_requests_per_key:
            # 切换到下一个key
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            current_key = self.api_keys[self.current_key_index]
            
            # 如果所有key都用完了
            if all(usage >= self.max_requests_per_key for usage in self.key_usage.values()):
                logging.error("所有API Key配额已用完！")
                return None
                
        return current_key
    
    def search_merchants(self, keyword: str, region: str, page_index: int = 1) -> Dict[str, Any]:
        """搜索商家信息"""
        api_key = self.get_current_api_key()
        if not api_key:
            return {"status": 0, "message": "No API key available"}
        
        params = {
            "keyword": keyword,
            "boundary": f"region({region},0)",
            "page_size": 20,  # 每页最多20条
            "page_index": page_index,
            "key": api_key,
            "output": "json"
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            self.key_usage[api_key] += 1
            
            logging.info(f"API请求: 关键词={keyword}, 区域={region}, 页码={page_index}, "
                        f"Key使用次数={self.key_usage[api_key]}/{self.max_requests_per_key}")
            
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"请求失败: HTTP {response.status_code}")
                return {"status": 0, "message": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logging.error(f"请求异常: {str(e)}")
            return {"status": 0, "message": str(e)}
    
    def collect_by_region(self, region_name: str, region_code: str = None) -> List[Dict[str, Any]]:
        """采集指定区域的数据"""
        merchants = []
        page = 1
        
        logging.info(f"开始采集区域: {region_name}")
        
        while True:
            result = self.search_merchants(KEYWORD, region_name, page)
            
            if result.get("status") != 0:
                logging.error(f"采集失败: {result.get('message', 'Unknown error')}")
                break
            
            data = result.get("data", [])
            if not data:
                logging.info(f"区域 {region_name} 第{page}页无更多数据")
                break
            
            for item in data:
                merchant = {
                    "id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "address": item.get("address", ""),
                    "category": item.get("category", ""),
                    "type": item.get("type", ""),
                    "location": {
                        "lat": item.get("location", {}).get("lat", 0),
                        "lng": item.get("location", {}).get("lng", 0)
                    },
                    "tel": item.get("tel", ""),
                    "province": region_name,
                    "province_code": region_code,
                    "collected_at": datetime.now().isoformat()
                }
                merchants.append(merchant)
            
            logging.info(f"区域 {region_name} 第{page}页采集 {len(data)} 条数据")
            
            # 检查是否还有更多页
            count = result.get("count", 0)
            if page * 20 >= count:
                break
            
            page += 1
            time.sleep(0.2)  # 避免请求过快
        
        logging.info(f"区域 {region_name} 共采集 {len(merchants)} 条数据")
        return merchants
    
    def collect_all_provinces(self):
        """采集全国所有省份的数据"""
        logging.info("=" * 60)
        logging.info(f"开始全国采集 - 关键词: {KEYWORD}")
        logging.info(f"共 {len(PROVINCES)} 个省级行政区")
        logging.info(f"可用API Key数量: {len(self.api_keys)}")
        logging.info(f"总配额: {len(self.api_keys) * self.max_requests_per_key} 次请求")
        logging.info("=" * 60)
        
        for idx, province in enumerate(PROVINCES, 1):
            logging.info(f"\n[{idx}/{len(PROVINCES)}] 正在采集: {province['name']}")
            
            merchants = self.collect_by_region(province["name"], province["code"])
            self.all_merchants.extend(merchants)
            
            # 每采集完一个省份，保存一次数据（防止中途失败）
            self.save_data()
            
            time.sleep(0.5)  # 省份之间间隔
        
        logging.info("\n" + "=" * 60)
        logging.info(f"全国采集完成！共采集 {len(self.all_merchants)} 条商家数据")
        logging.info(f"API使用情况: {self.key_usage}")
        logging.info("=" * 60)
    
    def save_data(self):
        """保存采集的数据"""
        output_file = "merchants_data.json"
        
        # 按省份统计
        stats_by_province = {}
        for merchant in self.all_merchants:
            province = merchant.get("province", "未知")
            stats_by_province[province] = stats_by_province.get(province, 0) + 1
        
        data = {
            "keyword": KEYWORD,
            "total_count": len(self.all_merchants),
            "collected_at": datetime.now().isoformat(),
            "api_usage": self.key_usage,
            "stats_by_province": stats_by_province,
            "merchants": self.all_merchants
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logging.info(f"数据已保存到: {output_file}")


def main():
    """主函数"""
    collector = TencentMapsCollector()
    
    try:
        collector.collect_all_provinces()
    except KeyboardInterrupt:
        logging.info("\n用户中断采集")
    except Exception as e:
        logging.error(f"采集过程出错: {str(e)}", exc_info=True)
    finally:
        # 确保数据被保存
        collector.save_data()


if __name__ == "__main__":
    main()
