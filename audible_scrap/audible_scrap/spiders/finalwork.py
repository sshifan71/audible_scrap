import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd

class FinalworkSpider(CrawlSpider):
    name = "finalwork"
    allowed_domains = ["worldometers.info"]
    start_urls = ["https://worldometers.info/co2-emissions"]

    rules = (
        Rule(
                  LinkExtractor(restrict_xpaths="//a[contains(text(),'Next')]"), 
                  callback="parse_item", 
                  follow=True),
            )

    def parse_item(self, response):
      rows = response.xpath("//table[@id='popbycountry']/tbody/tr")
      data = []

      for row in rows:
         country = row.xpath(".//tr/td[2]/a/text()").get()
         co2_2022 = row.xpath(".//tr/td[3]/text()").get()
         year1change = row.xpath(".//tr/td[4]/text()").get()
         population_2022 = row.xpath(".//tr/td[5]/text()").get()
         per_capita = row.xpath(".//tr/td[6]/text()").get()
         share_of_world = row.xpath(".//tr/td[7]/text()").get()

         data.append({
            "Country": country,
            "CO2 Emission 2020": co2_2022,
            "Change in 1 Year": year1change,
            "Population 2022": population_2022,
            "Per Capita": per_capita,
            "Share of the world": share_of_world,

        })
         
    def store_data(self,data):
       df = pd.DataFrame(data)
       file_name = "co2_emission.xlsx"

       try:
          existing_df = pd.read_excel(file_name)
          updated_df = pd.concat([existing_df, df])
          updated_df.to_excel(file_name, index=False)
       except FileNotFoundError:
          df.to_excel(file_name, index=False)

