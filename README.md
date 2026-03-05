📌 Google Maps Business Lead Scraper

Demo

![Demo](demo.gif)

🚀 Problem

Many agencies and small businesses need structured lead lists from Google Maps.  
Collecting this data manually is time-consuming and inefficient.

💡 Solution

This Python automation script extracts business information directly from Google Maps search results and exports it into a structured CSV file.

The scraper collects:

- Business Name
- Phone Number
- Website
- Address
- Ignore sponsored results
- Custom search (niche + city)
- Export results to CSV

🛠 Tech Stack:

- Python
- Selenium
- Pandas
- WebDriver Manager

⚙️ How It Works:

1. The user inputs a business niche (e.g., **Dentist**)  
2. The user inputs a city (e.g., **Miami**)  
3. The script opens Google Maps and performs the search  
4. Each business listing is automatically opened  
5. Business data is extracted  
6. Results are exported to a CSV file  

📊 Output Example

| Name | Phone | Website | Address |
|-----|-----|-----|-----|
| Miami Dental Clinic | +1 305... | miamidental.com | Miami, FL |

The final file is exported as:
leads.csv

▶️ How to Run

Clone the repository:
git clone https://github.com/your-username/google-maps-lead-scraper.git

Install dependencies:
pip install -r requirements.txt

Run the script:
python main.py

Then input:
Business niche
City
Number of leads to extract

⚠️ Disclaimer
This project is for educational purposes only.
Users are responsible for complying with Google’s terms of service when using automation tools.
