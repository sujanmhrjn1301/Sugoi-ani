import os
import requests
from jinja2 import Environment, FileSystemLoader

# Print the current working directory
print("Current working directory:", os.getcwd())

# Define the API endpoint
api_url = 'https://api.jikan.moe/v4/top/anime?filter=airing'

# Make the API request
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

top_anime = []
unique_anime_set = set()

    # Loop through the top 5 anime in the list, ensuring no duplicates
for i in range(min(16, len(data['data']))):
    index = data['data'][i]

    # Extract relevant information
    rank = index['rank']
    title_english = index['title_english']

    # Skip if the title is already in the set (duplicate)
    if title_english in unique_anime_set:
        continue

    # Add the title to the set to avoid duplicates
    unique_anime_set.add(title_english)

    # Extract other relevant information
    image_url = index['images']['webp']['image_url']
    title_japanese = index['title_japanese']
    synopsis = index['synopsis']
    synonyms =index['title_synonyms']
    status= index['status']
    type = index['type']
    genres = [genre['name'] for genre in index['genres']]
    score= index['score']
    duration = index['duration'][:2]
    trailer = index['trailer']['url']

    # Add the anime data to the list
    top_anime.append({
        'rank': rank,
        'title_english': title_english,
        'title_japanese': title_japanese,
        'synonyms': synonyms,
        'image_url': image_url,
        'synopsis': synopsis,
        'status': status,
        'genres': genres,
        'type': type,
        'score': score,
        'duration': duration,
        'trailer': trailer
    })
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    # Render the template with the data
    html_content = template.render(top_anime=top_anime)

    # Write the HTML content to a file
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f"Anime: {title_english} and Rank: {rank}")
    print('')

print('index.html file updated with the top unique anime.')
