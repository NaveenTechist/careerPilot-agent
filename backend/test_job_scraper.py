from services.job_scraper_service import JobScraperService

scraper = JobScraperService()

text = scraper.scrape("https://careers.honeywell.com/en/sites/Honeywell/job/151724")

print(text[:5000])
