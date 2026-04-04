set -ex

ls -la lab_5_scraper/
rm lab_5_scraper/scraper.py lab_5_scraper/scraper_config.json
ls -la lab_5_scraper/
mv lab_5_scraper/scraper_dynamic.py lab_5_scraper/scraper.py
mv lab_5_scraper/scraper_dynamic_config.json lab_5_scraper/scraper_config.json
ls -la lab_5_scraper/
