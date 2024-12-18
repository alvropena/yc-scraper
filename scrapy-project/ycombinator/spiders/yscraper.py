import json
import scrapy


def make_start_urls_list():
    """Returns a list with the start urls."""
    with open('ycombinator/start_urls.txt', 'r') as f:
        return eval(f.read())


class YCombinator(scrapy.Spider):
    """Crawls ycombinator.com/companies and extracts data about each company."""
    name = 'YCombinatorScraper'
    start_urls = make_start_urls_list()

    def parse(self, response):
        rc = response.css
        st = response.css('[data-page]::attr(data-page)').get()
        if st is not None:
            jo = json.loads(st)['props']
            jc = jo['company']
            yield {
                'company_id': jc['id'],
                'company_name': jc['name'],
                'short_description': jc['one_liner'],
                'long_description': jc['long_description'],
                'batch': jc['batch_name'],
                'status': jc['ycdc_status'],
                'tags': jc['tags'],
                'location': jc['location'],
                'country': jc['country'],
                'year_founded': jc['year_founded'],
                'num_founders': len(jc['founders']),
                'founders': [
                    {
                        'name': f['full_name'],
                        'title': f['title'],
                        'linkedin_url': f.get('linkedin_url'),
                        'twitter_url': f.get('twitter_url'),
                        'github_url': f.get('github_url'),
                    }
                    for f in jc['founders']
                ],
                'team_size': jc['team_size'],
                'website': jc['website'],
                'cb_url': jc['cb_url'],
                'linkedin_url': jc['linkedin_url'],
            }
