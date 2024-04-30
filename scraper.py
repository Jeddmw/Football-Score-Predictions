import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage to scrape
url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"

# Request the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table containing match data
    table = soup.find('table', class_='stats_table')
    
    # Check if the table was found
    if table:
        # Extract rows from the table
        rows = table.find_all('tr')
        
        # Open a CSV file to write the extracted data
        with open("premier_league_scores.csv", mode="w", newline="") as csv_file:
            # Create a CSV writer object
            writer = csv.writer(csv_file)
            
            # Write the header row
            writer.writerow(["Date", "Home Team", "Score", "Away Team"])
            
            # Loop over each row to extract match information
            for row in rows:
                # Extract the cells in the row
                cells = row.find_all('td')
                
                if len(cells) >= 7:  # Check if there are enough cells to contain the relevant information
                    date = cells[1].get_text(strip=True)
                    score = cells[5].get_text(strip=True)
                    if len(score) == 0:
                        continue
                    home_team = cells[3].get_text(strip=True)
                    home_score = score[0]
                    away_team = cells[7].get_text(strip=True)
                    away_score = score[2]
                    
                    # Write the extracted information as a new row in the CSV file
                    writer.writerow([date, home_team, home_score, away_team, away_score])
else:
    print(f"Failed to retrieve webpage. Status code: {response.status_code}")
