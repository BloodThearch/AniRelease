from bs4 import BeautifulSoup
import requests

response = requests.get("https://myanimelist.net/anime/874/Digimon_Tamers")

if response.status_code != 200:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    quit()


soup = BeautifulSoup(response.content, "html.parser")

tableTag = soup.find("table")
imgtag = tableTag.find("img")
print(imgtag.get("data-src"))
# for imgtag in imgtags:
#     print(imgtag.get("data-src") or imgtag.get("src"))







# anime_blocks = soup.find_all("div", class_="video-list-outer-vertical")

# episodes_with_images = []

# for block in anime_blocks:
#     img_tag = block.find("img")
#     if not img_tag:
#         continue

#     image_url = img_tag.get("data-src") or img_tag.get("src")
#     if not image_url or "icon-banned-youtube" in image_url:
#         continue  # Skip placeholder or invalid images

#     # Find all episodes
#     episode_links = block.select(".title a")
#     for ep in episode_links:
#         ep_title = ep.get_text(strip=True)
#         ep_url = ep.get("href")
#         if ep_url:
#             episodes_with_images.append({
#                 "title": ep_title,
#                 "url": ep_url,
#                 "image": image_url
#             })

# for d in episodes_with_images:
#     print(d)