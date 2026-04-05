import time
import re
import requests
from bs4 import BeautifulSoup

time.sleep(1.33333)
print('________  .____               /\\        ________         .__        __   ')
print('\\_____  \\ |    |    ____   ___) / ______ \\_____  \\   _____|__| _____/  |_ ')
print(' /   |   \\|    | _/ __ \\ / ___\\/  ___/  /   |   \\ /  ___/  |/    \\   __')
print('/    |    \\    |__\\  ___// /_/  >___ \\  /    |    \\\\___ \\|  |   |  \\  |  ')
print('\\_______  /_______ \\___  >___  /____  > \\_______  /____  >__|___|  /__| ')
print('        \\/        \\/   \\/_____/     \\/          \\/     \\/        \\/      ')



user_input = input('Enter password: ')

if user_input == 'ostool':
    print("Access granted!")
    vk_id = input('Enter VK ID: ').strip()

    if not vk_id:
        print("VK ID cannot be empty.")
        exit()

    print("\nSearching for information...\n")

    found_data = {
        "VK Profile": None,
        "Telegram": None,
        "Instagram": None,
        "Twitter": None,
        "Other Mentions": []
    }

    def google_search(query):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = f"https://www.google.com/search?q={query}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for result in soup.find_all('div', class_='yuRUbf'):
                link = result.find('a')
                if link and link.has_attr('href'):
                    links.append(link['href'])
            return links[:5]
        except Exception:
            return []

    vk_links = google_search(f"site:vk.com {vk_id}")
    if vk_links:
        found_data["VK Profile"] = vk_links[0]

    social_queries = [
        (f"site:t.me {vk_id}", "Telegram"),
        (f"site:instagram.com {vk_id}", "Instagram"),
        (f"site:x.com {vk_id}", "Twitter")
    ]

    for query, platform in social_queries:
        links = google_search(query)
        if links:
            found_data[platform] = links[0]

    general_links = google_search(vk_id)
    existing_links = [found_data["VK Profile"], found_data["Telegram"], found_data["Instagram"], found_data["Twitter"]]
    for link in general_links:
        if link not in existing_links and link:
            found_data["Other Mentions"].append(link)

    print("=" * 50)
    print("SEARCH RESULTS")
    print("=" * 50)

    for key, value in found_data.items():
        print(f"\n{key}:")
        if value is None or (isinstance(value, list) and len(value) == 0):
            print("No information found.")
        elif isinstance(value, list):
            for i, link in enumerate(value, 1):
                print(f"{i}. {link}")
        else:
            print(value)
else:
    print('Wrong password!')