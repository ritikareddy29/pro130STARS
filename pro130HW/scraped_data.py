import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data from the first URL
def scrape_giant_star_data():
    url = "https://en.wikipedia.org/wiki/List_of_nearest_giant_stars"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    giant_star_table = soup.find("table", attrs={"class": "wikitable"})
    if giant_star_table is None:
        raise ValueError("Unable to find the table for giant stars.")
    rows = giant_star_table.find_all('tr')[1:]  # Exclude header row

    stars_data = []
    for row in rows:
        cols = row.find_all('td')
        # Extracting only specific columns: Star_name, Mass, Luminosity, Distance
        star_data = [cols[0].text.strip(), cols[1].text.strip(), cols[4].text.strip(), cols[3].text.strip()]
        stars_data.append(star_data)

    print("Scraped Giant Star Data:")
    for data in stars_data:
        print(data)

    return stars_data

# Function to scrape data from the second URL
def scrape_dwarf_star_data():
    url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", attrs={"class": "wikitable"})
    if table is None:
        raise ValueError("Unable to find the table for dwarf stars.")
    headers = ["Star_name", "Distance", "Mass", "Radius"]
    rows = table.find_all('tr')[1:]

    dwarf_star_data = []
    for row in rows:
        cols = row.find_all('td')
        # Extracting only specific columns: Star_name, Mass, Luminosity, Distance
        star_data = [cols[0].text.strip(), cols[5].text.strip(), cols[8].text.strip(), cols[9].text.strip()]
        dwarf_star_data.append(star_data)

    print("\nScraped Dwarf Star Data:")
    for data in dwarf_star_data:
        print(data)

    return dwarf_star_data

# Scrape data from both URLs
giant_star_data = scrape_giant_star_data()
dwarf_star_data = scrape_dwarf_star_data()

# Convert the bright star data to DataFrame
giant_star_df = pd.DataFrame(giant_star_data, columns=["Star_name", "Distance", "Mass", "Radius"])

# Convert the dwarf star data to DataFrame
dwarf_star_df = pd.DataFrame(dwarf_star_data, columns=["Star_name", "Distance", "Mass", "Radius"])

# Merge both DataFrames
merged_data = pd.concat([giant_star_df, dwarf_star_df], ignore_index=True)

# Save the merged data to CSV
merged_data.to_csv("merged_stars_data.csv", index=False)

print("\nMerged Data:")
print(merged_data)
