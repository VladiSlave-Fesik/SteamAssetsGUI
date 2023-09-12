import requests
import os


def check_url_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def find_available_alt_assets(steam_id):
    alt_assets_text = '_alt_assets_'
    existing = []

    urls = [
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/broadcast_left_panel.jpg',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/broadcast_right_panel.jpg',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/capsule_231x87.jpg',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/capsule_616x353.jpg',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/header.jpg',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/hero_capsule.jpg',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/library_600x900.jpg',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/library_hero.jpg',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/logo.png',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/page_bg_raw.jpg',
        'https://cdn.cloudflare.steamstatic.com/steam/apps/{}/capsule_467x181.jpg',
    ]

    urls.sort()

    for url_template in urls:
        url = url_template.format(steam_id)
        if check_url_exists(url):
            existing.append(url)
            alt_assets = find_available_alt_assets_for_url(url, alt_assets_text)
            existing.extend(alt_assets)

    return existing


def find_available_alt_assets_for_url(url, alt_assets_text):
    alt_assets = []
    photo_name = url.split('/')[-1].split('.')[0]
    i = 0

    while True:
        alt_url = url.replace(photo_name, f"{photo_name}{alt_assets_text}{i}")
        if check_url_exists(alt_url):
            alt_assets.append(alt_url)
        else:
            if i >= 2:
                break
        i += 1

    return alt_assets


def download_image(url, save_dir):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.basename(url)
            save_path = os.path.join(save_dir, file_name)

            # Сохранить файл
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f'Фотография успешно скачана и сохранена в {save_path}')
            return save_path
        else:
            print(f'Ошибка при скачивании фотографии. Код статуса: {response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Произошла ошибка при запросе: {e}')
        return None


steam_id = 304930
existing_urls = find_available_alt_assets(steam_id)

print(f'URLs len = {len(existing_urls)}')
for url in existing_urls:
    download_image(url, 'temp')
