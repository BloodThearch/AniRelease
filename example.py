import requests
from bs4 import BeautifulSoup

def scrape_anime_list():
    url = "https://myanimelist.net/watch/episode"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all the anime entries
    anime_entries = soup.find_all("div", class_="video-list-outer-vertical")
    
    # List to store the anime names with episode numbers
    anime_list = []
    
    for entry in anime_entries:
        aTags = entry.find_all("a")

        # Extract anime name
        title_tag = aTags[3]
        title = title_tag.text.strip() if title_tag else "Unknown Title"
        
        # Extract episode number
        episode_tag = aTags[0]
        episode = episode_tag.text.strip() if episode_tag else "Unknown Episode"
        
        anime_list.append(f"{title} - {episode}")
    
    return anime_list

# Example usage:
anime_list = scrape_anime_list()
for anime in anime_list:
    print(anime)
