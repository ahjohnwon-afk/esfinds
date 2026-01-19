# esfinds.com

A website for displaying Amazon deals and promotions.

## Amap Business Scraper / 高德地图商家采集脚本

This repository also includes a Python script for collecting business information from Amap (Gaode Maps).

### Features

- Search businesses by keyword and city
- Collect detailed business information (name, address, phone, coordinates, ratings)
- Export data to JSON format
- Rate limiting and error handling

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python amap_scraper.py --key YOUR_API_KEY --keyword 餐厅 --city 北京 --max 50
```

For detailed documentation, see [AMAP_SCRAPER_README.md](AMAP_SCRAPER_README.md)

## Website

The main website displays Amazon deals and promotions for various products.

### Files

- `index.html` - Main website page
- `products_data_v.json` - Product data
- `promo_codes.json` - Promotional codes
- `amap_scraper.py` - Amap business scraper script
- `AMAP_SCRAPER_README.md` - Detailed scraper documentation
