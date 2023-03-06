import os
from googletrans import Translator
from google.cloud import translate_v2 as translate
from bs4 import BeautifulSoup
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"aesthetic-cacao-378709-e9aa2b09bf8c.json"

def translate_html_files(source_dir, target_dir):
    client = translate.Client()

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            if filename.endswith('.html'):
                source_file = os.path.join(root, filename)
                target_file = os.path.join(target_dir, source_file[len(source_dir)+1:])

                # read source file contents
                with open(source_file, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')

                # translate text within tags
                for tag in soup.find_all(text=True):
                    if tag.parent.name not in ['style', 'script', '[document]', 'head', 'title']:
                        text = tag.strip()
                        if text:
                            # split text into chunks of max 5000 characters
                            chunk_size = 5000
                            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

                            # translate each chunk separately and combine the results
                            translated_chunks = []
                            for chunk in chunks:
                                translation = client.translate(chunk, source_language='en', target_language='hi')
                                translated_chunks.append(translation['translatedText'])

                            # replace original text with translated text
                            tag.replace_with(''.join(translated_chunks))

                # write target file contents
                if not os.path.exists(os.path.dirname(target_file)):
                    os.makedirs(os.path.dirname(target_file))
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(str(soup))

translate_html_files('./www.classcentral.com/subject','test2/subject')