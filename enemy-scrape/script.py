import csv
import requests
from bs4 import BeautifulSoup
import time

def scrape_competitor_website(url, max_retries=3):
    # Define initial delay between retries
    delay = 2

    # Retry loop
    for attempt in range(max_retries):
        try:
            # Send a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract services information and pricing
                services = []
                for service_elem in soup.find_all('div', class_='service'):
                    service_name = service_elem.find('h2').text.strip()
                    price_elem = service_elem.find('span', class_='price')
                    price = price_elem.text.strip() if price_elem else 'Price not available'
                    services.append({'name': service_name, 'price': price})

                # Extract contact information
                contact_elem = soup.find('div', class_='contact')
                contact_info = contact_elem.text.strip() if contact_elem else 'Contact information not available'

                return services, contact_info

            # If the response status code is not 200, raise an HTTPError
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        # Exponential backoff for retries
        print(f"Retrying in {delay} seconds...")
        time.sleep(delay)
        delay *= 2  # Double the delay for the next attempt

    print(f"Failed to retrieve data from {url} after {max_retries} attempts.")
    return [], ''

def save_to_files(competitor_name, services, contact_info):
    # Save data to text file
    with open(f"{competitor_name}.txt", 'w') as txt_file:
        txt_file.write(f"Competitor: {competitor_name}\n\n")
        txt_file.write("Services offered:\n")
        for service in services:
            txt_file.write(f"- {service['name']}: {service['price']}\n")
        txt_file.write("\nContact Information:\n")
        txt_file.write(contact_info)

    # Save data to CSV file
    with open(f"{competitor_name}.csv", 'w', newline='') as csv_file:
        fieldnames = ['Competitor', 'Service', 'Price', 'Contact Information']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for service in services:
            writer.writerow({'Competitor': competitor_name, 'Service': service['name'], 'Price': service['price'], 'Contact Information': contact_info})

def main():
    # List of competitor websites to scrape
    competitors = [
        {'name': 'Competitor A', 'url': 'https://www.competitorA.com/services'},
        {'name': 'Competitor B', 'url': 'https://www.competitorB.com/services'},
        # Add more competitors as needed
    ]

    # Iterate over competitors and scrape data
    for competitor in competitors:
        print(f"Scraping data from {competitor['name']}...")
        services, contact_info = scrape_competitor_website(competitor['url'])
        if services or contact_info:
            save_to_files(competitor['name'], services, contact_info)
            print(f"Data saved for {competitor['name']}")
        else:
            print(f"No data found for {competitor['name']}")

if __name__ == "__main__":
    main()
