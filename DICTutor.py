import sys, os
import xml.etree.cElementTree as ET
import re
from gooey import Gooey, GooeyParser
from time import sleep

def Total(count):
    print(f'{"-"*10}\nнайдено : {count}')

os.chdir('/'.join(sys.argv[0].split('/')[:-1]))
# sys.stdout.reconfigure(encoding='utf-8')

docs = '''
. - Один любой символ, кроме новой строки.
? - 0 или 1 вхождение шаблона слева
+ - 1 и более вхождений шаблона слева
* - 0 и более вхождений шаблона слева
[..] - Один из символов в скобках ([^..] — любой символ, кроме тех, что в скобках)
^ и $ - Начало и конец строки соответственно
{n,m} - От n до m вхождений ({,m} — от 0 до m)
a|b - Соответствует a или b
() - Группирует выражение и возвращает найденный текст
'''

about = {
    'type': 'AboutDialog',
    'menuTitle': 'информация',
    'name': 'DICTutor',
    'description': 'поиск примеров слов по регулярным выражениям',
    'version': '0',
    'developer': 'https://github.com/G0-G4'
}

goo = {
    'type': 'Link',
    'menuTitle': 'сделано с помощью Gooey',
    'url': 'https://github.com/chriskiehl/Gooey'
}

XDXF = {
    'type': 'Link',
    'menuTitle': 'о формате XDXF',
    'url': 'https://github.com/soshial/xdxf_makedict'
}

helper = {
    'type': 'MessageDialog',
    'menuTitle': 'помощь по маскам',
    'message': docs
}

@Gooey(language = 'russian', program_name = 'DICTutor',
        menu = [{'name': 'помощь', 'items': [helper]},
        {'name' : 'инф' , 'items' : [about, goo, XDXF]}],
        image_dir = 'images',
        language_dir = 'translation',
        progress_regex = r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
        progress_expr = "current / total * 100",
        force_stop_is_error = False, 
        show_success_modal = False,
        show_stop_warning = False)

def main():
    parser = GooeyParser()
    g = parser.add_argument_group('Параметры', 'Задайте Параметры Поиска')
    g.add_argument(
        'dict',
        help='выберите словарь',
        widget = 'Dropdown',
        choices = list(os.listdir('dicts'))
    )

    g.add_argument(
        'regex',
        help = 'введите маску'
    )

    g.add_argument(
        'number',
        help='введите кол-во слов'
    ) 

    args = parser.parse_args()
    tree = ET.parse(f'dicts/{args.dict}/dict.xdxf')
    root = tree.getroot()

    count = 0
    n = int(args.number)
    with open('WORDS.txt','w', encoding='UTF-8') as fout:
        for article in root.iterfind('ar'):
            for key in article.iterfind('k'):
                if re.search(args.regex, key.text):
                    print(key.text.strip(), file = fout, flush = True) # очищение буфера, для немедленного сохранения в файл
                    print("progress: {}/{}".format(count + 1, n))
                    sleep(0.001)
                    count += 1
                    if count >= n:
                        break
            if count >= n:
                break

if __name__ == "__main__":
    main()