import scrapy
import requests
import json
from datetime import datetime


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    start_urls = [
        'https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search?q=Software&countryCode2=US&radius=30&radiusUnit=mi&page=1&pageSize=20&facets=employmentType%7CpostedDate%7CworkFromHomeAvailability%7CworkplaceTypes%7CemployerType%7CeasyApply%7CisRemote%7CwillingToSponsor&filters.workplaceTypes=Remote&filters.employmentType=CONTRACTS&filters.postedDate=ONE&currencyCode=USD&fields=id%7CjobId%7Cguid%7Csummary%7Ctitle%7CpostedDate%7CmodifiedDate%7CjobLocation.displayName%7CdetailsPageUrl%7Csalary%7CclientBrandId%7CcompanyPageUrl%7CcompanyLogoUrl%7CcompanyLogoUrlOptimized%7CpositionId%7CcompanyName%7CemploymentType%7CisHighlighted%7Cscore%7CeasyApply%7CemployerType%7CworkFromHomeAvailability%7CworkplaceTypes%7CisRemote%7Cdebug%7CjobMetadata%7CwillingToSponsor&culture=en&recommendations=true&interactionId=0&fj=true&includeRemote=true'
    ]

    custom_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,en-AU;q=0.7,hi;q=0.6,en-IN;q=0.5,en-CA;q=0.4,en-ZA;q=0.3,en-NZ;q=0.2,te;q=0.1,ja;q=0.1',
        'origin': 'https://www.dice.com',
        'referer': 'https://www.dice.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-api-key': '1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=self.custom_headers,
                callback=self.parse
            )

    def parse(self, response):
        # Parse the JSON response
        try:
            jobs = json.loads(response.text)  # Ensure the response is properly parsed as JSON
            for job in jobs.get('data', []):
                # Convert postedDate to YYYY-MM-DD format
                posted_date = job.get('postedDate')
                if posted_date:
                    try:
                        posted_date = datetime.strptime(posted_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
                    except ValueError:
                        self.logger.warning(f"Invalid date format: {posted_date}")
                        posted_date = None

                location = job.get('jobLocation', {}).get('displayName', "Remote") or "Remote"

                payload = {
                    "title": job.get('title'),
                    "company_name": job.get('companyName'),
                    "location": location,
                    "posted_date": posted_date,
                    "details_url": job.get('detailsPageUrl'),
                    "employment_type": job.get('employmentType'),
                }
                # Post the payload to the API
                response = requests.post('http://127.0.0.1:8000/jobs/add/', json=payload)
                if response.status_code == 201:
                    self.logger.info(f"Job added successfully: {payload['title']}")
                else:
                    self.logger.error(f"Failed to add job: {payload['title']}, Status Code: {response.status_code}")
        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON response")
