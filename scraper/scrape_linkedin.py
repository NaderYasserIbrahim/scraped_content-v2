# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import pandas as pd
#
#
# def scrape_linkedin_jobs(search_term="developer", location="Cairo, Cairo, Egypt"):
#     # Set up Chrome options for headless scraping
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#
#     # Setup the WebDriver (optional: pass your chromedriver path)
#     service = Service()  # Adjust path to chromedriver if needed
#     driver = webdriver.Chrome(service=service, options=options)
#
#     url = f"https://www.linkedin.com/jobs/search/?keywords={search_term}&location={location}"
#     print(f"Scraping: {url}")
#     driver.get(url)
#
#     # Wait until the job list is loaded (wait for the first job card)
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "ul.jobs-search__results-list li")))
#     except Exception as e:
#         print(f"Error waiting for page to load: {e}")
#         driver.quit()
#         return
#
#     # Scroll to load dynamic job listings
#     for _ in range(5):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)
#
#     # Find all job cards
#     jobs = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
#     print(f"Found {len(jobs)} job cards")
#
#     results = []
#     for job in jobs:
#         try:
#             # Extract job details
#             title = job.find_element(By.CSS_SELECTOR, "h3.base-search-card__title").text.strip()
#             company = job.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle").text.strip()
#             location = job.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text.strip()
#             job_url = job.find_element(By.CSS_SELECTOR, "a.base-card__full-link").get_attribute("href")
#             posted = job.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
#             logo_elem = job.find_elements(By.CSS_SELECTOR, "img.artdeco-entity-image")
#             logo_url = logo_elem[0].get_attribute("src") if logo_elem else None
#
#             results.append({
#                 "Job Title": title,
#                 "Company Name": company,
#                 "Company Logo": logo_url,
#                 "Location": location,
#                 "Source URL": job_url,
#                 "Posted Date": posted,
#             })
#
#         except Exception as e:
#             print(f"Error processing a job listing: {e}")
#             continue
#
#     driver.quit()
#
#     # If data is found, save to CSV
#     if results:
#         df = pd.DataFrame(results)
#         df.to_csv("linkedin_jobs.csv", index=False)
#         print(f"Scraping completed. {len(results)} jobs saved to linkedin_jobs.csv")
#     else:
#         print("No job cards found.")
#
#
# # Run the scraping function
# scrape_linkedin_jobs()
