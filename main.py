from scraper import GoogleMapsScraper

niche = input("Enter niche: ")
city = input("Enter city: ")
quantity = int(input("How many businesses to extract? "))

scraper = GoogleMapsScraper(niche, city, quantity)
scraper.run()