import json
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from time import sleep

import requests
from tqdm import tqdm


def mkdir(path):
    if os.path.exists(path) is not True:
        os.makedirs(path)


def download_pic(url, path):
    resp = requests.get(url)
    with open(path, 'wb') as code:
        code.write(resp.content)


def download_emoji(emoji, save_path):
    emoji_name = emoji['text']
    emoji_name = emoji_name[1:-1]
    path = os.path.join(save_path, f'{emoji_name}.png')
    download_pic(emoji['url'], path)


def download_package(package, path):
    package_name = package['text']
    save_path = os.path.join(path, package_name)
    mkdir(save_path)
    all_emote = set(map(lambda e: e['text'][1:-1], package['emote']))
    downloaded_emote = set(map(lambda e: e[:-4], os.listdir(save_path)))
    download_emote_name = all_emote - downloaded_emote
    if len(download_emote_name) == 0:
        return
    going_to_download_emote = filter(lambda e: e['text'][1:-1] in download_emote_name, package['emote'])
    with ThreadPoolExecutor() as executor:
        executor.map(partial(download_emoji, save_path=save_path), going_to_download_emote)
    sleep(3)


if __name__ == '__main__':
    with open('emoji.json', 'r', encoding='utf-8') as fp:
        emojis = json.load(fp)
    emoji_packages = emojis['data']['all_packages']
    package_path = 'bilibili_emoji'
    bar = tqdm(emoji_packages)
    for p in bar:
        if p['text'] == '颜文字':
            continue
        bar.set_description(p['text'])
        download_package(p, package_path)
