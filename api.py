import re
import requests

HEADER_CLEANER = re.compile('<.*?>||&.*;')
TAGS_CLEANER = re.compile('<.*?>')
TAGS = ['<b>', '<strong>', '<i>', '<u>', '<ins>', '<s>', '<strike>', '<del>', '<code>', '<pre>']
TAGS = TAGS + [f"</{tag}" for tag in TAGS]


def tags_cleaner(content: str) -> str:
    all_tags = TAGS_CLEANER.findall(content)
    for tag in all_tags:
        if tag not in TAGS:
            content = content.replace(tag, ' ')
    return content


def get_catalog(board='/g/'):
    # only first page
    res = requests.get(f'https://a.4cdn.org{board}catalog.json').json()[0]['threads']
    threads = {}

    # without pinned thread
    for i in range(1, 6):
        media = f"{res[i].get('filename')}{res[i].get('ext')}"
        header = res[i].get('sub')  # try to fetch title
        content = re.sub(HEADER_CLEANER, '', res[i].get('com', ''))
        header = content if not header else header  # try to fetch content if title is empty
        if header:
            header = re.sub(TAGS_CLEANER, '', header[:50] + '...' if len(header) > 70 else header)
        else:
            header = media  # try to fetch media if title and content is empty
        
        threads[header] = {
            "id": res[i]['no'],
            "media": f"https://i.4cdn.org/g/{res[i]['tim']}.{media.split('.')[1]}",
            "content": tags_cleaner(res[i].get('com', '')),
            "ext": res[i].get('ext'), 
            "link": f"https://boards.4channel.org/g/thread/{res[i]['no']}"
        }
    
    return threads
