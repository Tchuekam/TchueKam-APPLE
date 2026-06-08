import os
import re

def make_paths_relative(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace href="/..." with href="./..."
    # Replace src="/..." with src="./..."
    # Avoiding replacing things like href="https://" or href="//"
    
    # Pattern for href="/ or src="/ but not href="//
    new_content = re.sub(r'(href|src)="/(?=[^/])', r'\1="./', content)
    
    # Also handle canonical links if any
    new_content = re.sub(r'content="/(?=[^/])', r'content="./', new_content)

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    modified_count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if make_paths_relative(file_path):
                    print(f"Fixed paths in: {file_path}")
                    modified_count += 1
    
    print(f"\nDone! Modified {modified_count} HTML files.")

if __name__ == "__main__":
    main()
