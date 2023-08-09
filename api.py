import re
import requests

TAGS_CLEANER = re.compile('<.*?>||&.*;')

def get_catalog(board='/g/'):
    # only first page
    res = requests.get(f'https://a.4cdn.org{board}catalog.json').json()[0]['threads']
    threads = {}

    # without pinned thread
    for i in range(1, 6):
        media = f"{res[i].get('filename')}{res[i].get('ext')}"
        header = res[i].get('sub')  # try to fetch title
        content = re.sub(TAGS_CLEANER, '', res[i].get('com'))
        header = content if not header else header  # try to fetch content if title is empty
        if header:
            header = re.sub(TAGS_CLEANER, '', header[:50] + '...' if len(header) > 70 else header)
        else:
            header = media  # try to fetch media if title and content is empty
        
        threads[header] = {
            "id": res[i]['no'],
            "media": f"https://i.4cdn.org/g/{id}.{media.split('.')[1]}" if media else None,
            "content": content,
            "link": f"https://boards.4channel.org/g/thread/{res[i]['no']}"
        }

    return threads


if __name__ == '__main__':
    print(get_catalog())
