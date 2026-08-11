import re
import os

def clean_markdown_for_tts(md_text):
    # 1. Replace horizontal rules with a spoken pause indicator
    text = re.sub(r'^\s*---\s*$', '\n\n[Section Break]\n\n', md_text, flags=re.MULTILINE)
    
    # 2. Replace major headings with spoken introduction phrases
    def heading_repl(match):
        level = len(match.group(1))
        title = match.group(2).strip()
        if title.startswith("Part 2:"):
            return f"\n\nNow, let's move on to {title}.\n\n"
        elif title.startswith("Paper 1:") or title.startswith("Paper 2:") or title.startswith("Paper 3:") or title.startswith("Midterm Exam"):
            return f"\n\nLet's review the questions and answers from {title}.\n\n"
        elif level == 1:
            return f"\n\nMain Chapter: {title}.\n\n"
        elif level == 2:
            return f"\n\nSection: {title}.\n\n"
        else:
            return f"\n\nTopic: {title}.\n\n"
            
    text = re.sub(r'^(#{1,6})\s+(.*)$', heading_repl, text, flags=re.MULTILINE)
    
    # 3. Clean up links: [link text](url) -> link text
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text)
    
    # 4. Remove bold/italic markers: **text** -> text, *text* -> text
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    
    # 5. Clean up list item bullets: '* ' or '- ' at the start of lines
    text = re.sub(r'^\s*[\*\-]\s+', '• ', text, flags=re.MULTILINE)
    
    # 6. Clean up numbered lists
    text = re.sub(r'^\s*(\d+)\.\s+', r'Number \1: ', text, flags=re.MULTILINE)
    
    # 7. Clean up other symbols like brackets, code blocks, etc.
    text = text.replace('`', '')
    
    # 8. Clean up multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def main():
    workspace_dir = '/home/s_goto/Documents/Mid/spic'
    md_file = os.path.join(workspace_dir, 'preparation.md')
    audio_file = os.path.join(workspace_dir, 'preparation_audio.txt')
    
    print("Reading markdown file...")
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    print("Converting markdown format to speech-friendly text...")
    audio_text = (
        "Welcome to your Social and Professional Issues in Computing Midterm Exam Audio Guide. "
        "This spoken script has been optimized for text-to-speech readers to help you learn passively.\n\n"
        + clean_markdown_for_tts(md_content)
    )
    
    print("Writing speech text to file...")
    with open(audio_file, 'w', encoding='utf-8') as f:
        f.write(audio_text)
    print("Done! Audio text saved to preparation_audio.txt")

if __name__ == '__main__':
    main()
