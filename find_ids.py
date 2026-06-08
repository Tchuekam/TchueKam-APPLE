
import re

def find_exact_object(content, iid):
    pattern = r'\{"id":"' + iid + r'".*?\}'
    # This might match too little if there are nested objects.
    # But in this JSON, 'disclaimer' can have nested tags.
    # Let's use a better way to find the end of the object.
    
    start_pattern = r'\{"id":"' + iid + r'"'
    match = re.search(start_pattern, content)
    if not match:
        return None
    
    start_index = match.start()
    brace_count = 0
    for i in range(start_index, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return content[start_index:i+1]
    return None

with open('store/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for iid in ['8642adb17d50997f1cf4a93a67f07640', 'f6cd09a197c029b1f5905e5f43b603e0']:
    s = find_exact_object(content, iid)
    if s:
        print(f'ID: {iid}')
        print(f'String: {s}')
        print('---')
