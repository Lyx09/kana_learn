#! /usr/bin/python3
# -*- coding: utf-8 -*-

from getopt import getopt
import random
import json
import sys
import os
import re

# Get character
try:
    import msvcrt
    getch = msvcrt.getch
except:
    import sys, tty, termios
    def _unix_getch():
        """Get a single character from stdin, Unix version"""

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())          # Raw read
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    getch = _unix_getch


class Color:
    black  = '\u001b[30m'
    red    = '\u001b[31m'
    green  = '\u001b[32m'
    yellow = '\u001b[33m'
    blue   = '\u001b[34m'
    magenta= '\u001b[35m'
    cyan   = '\u001b[36m'
    white  = '\u001b[37m'
    reset  = '\u001b[0m'


# GOJUON

romaji = '''
a   i   u   e   o
ka  ki  ku  ke  ko
sa  shi su  se  so
ta  chi tsu te  to
na  ni  nu  ne  no
ha  hi  fu  he  ho
ma  mi  mu  me  mo
ya  /   yu  /   yo
ra  ri  ru  re  ro
wa  wi  /   we  wo
n
'''

hiragana = '''
あ い う え お
か き く け こ
さ し す せ そ
た ち つ て と
な に ぬ ね の
は ひ ふ へ ほ
ま み む め も
や /  ゆ /  よ
ら り る れ ろ
わ ゐ /  ゑ を
ん /  /  /  /
'''

katakana = '''
ア イ ウ エ オ
カ キ ク ケ コ
サ シ ス セ ソ
タ チ ツ テ ト
ナ ニ ヌ ネ ノ
ハ ヒ フ ヘ ホ
マ ミ ム メ モ
ヤ /  ユ /  ヨ
ラ リ ル レ ロ
ワ ヰ /  ヱ ヲ
ン /  /  /  /
'''

# DIACRITICS

romaji_diacrit = '''
ga  gi  gu  ge  go
za  zi  zu  ze  zo
da  di  du  de  do
ba  bi  bu  be  bo
pa  pi  pu  pe  po
nga ngi ngu nge ngo
'''

hiragana_diacrit = '''
が ぎ ぐ げ ご
ざ じ ず ぜ ぞ
だ ぢ づ で ど
ば び ぶ べ ぼ
ぱ ぴ ぷ ぺ ぽ
か゚ き゚ く゚ け゚ こ゚
'''

katakana_diacrit = '''
ガ ギ グ ゲ ゴ
ザ ジ ズ ゼ ゾ
ダ ヂ ヅ デ ド
バ ビ ブ ベ ボ
パ ピ プ ペ ポ
カ゚ キ゚ ク゚ ケ゚ コ゚
'''

# YOO_ON / DIGRAPHS

romaji_digraph = '''
kya  kyu  kyo
sha  shu  sho
cha  chu  cho
nya  nyu  nyo
hya  hyu  hyo
mya  myu  myo
rya  ryu  ryo
gya  gyu  gyo
ja   ju   jo
bya  byu  byo
pya  pyu  pyo
ngya ngyu ngyo
'''

hiragana_digraph = '''
きゃ きゅ きょ
しゃ しゅ しょ
ちゃ ちゅ ちょ
にゃ にゅ にょ
ひゃ ひゅ ひょ
みゃ みゅ みょ
りゃ りゅ りょ
ぎゃ ぎゅ ぎょ
じゃ じゅ じょ
びゃ びゅ びょ
ぴゃ ぴゅ ぴょ
き゚ゃ き゚ゅ き゚ょ
'''

katakana_digraphs = '''
キャ キュ キョ
シャ シュ ショ
チャ チュ チョ
ニャ ニュ ニョ
ヒャ ヒュ ヒョ
ミャ ミュ ミョ
リャ リュ リョ
ギャ ギュ ギョ
ジャ ジュ ジョ
ヂャ ヂュ ヂョ
ビャ ビュ ビョ
ピャ ピュ ピョ
'''

def table_to_list(table):
    return re.split('\s+', table.strip())

def kana_from_table(romaji, hiragana, katakana):
    kana_list = []
    ziplist = list(zip(table_to_list(romaji), table_to_list(hiragana),
        table_to_list(katakana)))
    for k in ziplist:
        is_old = False
        if k[0] in ['wi', 'we', 'nga', 'ngi', 'ngu', 'nge', 'ngo']:
            is_old = True
        if k[0] != '/':
            kana_list.append(
                    {
                        'romaji' : k[0],
                        'hiragana' : k[1],
                        'katakana' : k[2],
                        'old' : is_old
                        })
    return kana_list

def clearscreen():
    os.system('clear')

def parseopt():
    # Default parameters
    list_opt = {
                'diacritics' :  False,
                'digraphs' :    False,
                'old' :         False,
                'random' :      False,
                'src' :         'hiragana',
                'dest' :        'romaji'
            }
    options = getopt(sys.argv[1:],'oragehs:d:' ,['diacritics', 'digraphs',
        'old', 'random', 'extended', 'help', 'src=', 'dst='])[0]
    for opt in options:
        if opt[0] == '-h' or opt[0] == '--help':
            print(f'Usage {sys.argv[0]} [OPTIONS]... [SAVE_FILE]')
            print('A small program to learn japanese kanas')
            print('Mandatory arguments to long options are mandatory for short options too.')
            print('-o, --old            Include old/unused kana')
            print('-h, --help            Display this text')
            print('-e, --extended       Include extended kana combinations (vi, fa, ...)')
            print('-r, --random         Review kana in a random order')
            print('-a, --diacritics     Include diacritics (dakuten and handakuten)')
            print('-g, --digraphs       Include digraphs (yōon) (sha, kyu, ryo, ...)')
            print('-s, --src=ALPHABET   Source alphabet, what will be shown')
            print('-d, --dest=ALPHABET  Destination alphabet, what you have to find')
            print('                     ALPHABET is one of \'hiragana\', \'katakana\' or \'romaji\'')
            exit(1)
        elif opt[0] == '-o' or opt[0] == '--old':
            list_opt['old'] = True
        elif opt[0] == '-r' or opt[0] == '--random':
            list_opt['random'] = True
        elif opt[0] == '-a' or opt[0] == '--diacritics':
            list_opt['diacritics'] = True
        elif opt[0] == '-g' or opt[0] == '--digraphs':
            list_opt['digraphs'] = True
        elif opt[0] == '-s' or opt[0] == '--src':
            if opt[1] not in ['romaji', 'hiragana', 'katakana']:
                print('Invalid source {opt[1]}')
                exit(1)
            list_opt['src'] = opt[1]
        elif opt[0] == '-d' or opt[0] == '--dest':
            if opt[1] not in ['romaji', 'hiragana', 'katakana']:
                print(f'Invalid source {opt[1]}')
                exit(1)
            list_opt['dest'] = opt[1]
        else:
            print(f'Unknown option {opt[0]}')
            exit(1)

    return list_opt

def build_list(list_opt = None):
    kana_list = kana_from_table(romaji, hiragana, katakana)

    if list_opt['diacritics']:
        kana_list.append(kana_from_table(romaji_diacrit, hiragana_diacrit,
            katakana_diacrit))

    if list_opt['digraphs']:
        kana_list.append(kana_from_table(romaji_digraph, hiragana_digraph,
            katakana_digraph))

    if list_opt['random']:
        random.shuffle(kana_list)
    return kana_list

def fix_user_data(user):
    for r in table_to_list(romaji):
        if r not in user:
            user[r] = 0
    return user

def parse_user(filename='userdata.kana'):
    open(filename, 'a').close()
    user_file = open(filename, 'r')
    user_data = user_file.read()
    user_file.close()

    try:
        user = json.loads(user_data)
    except ValueError as e:
        user = dict()
    return fix_user_data(user)

def save_user(user, filename='userdata.kana'):
    user_data = open(filename, 'w')
    user_data.write(json.dumps(user))
    user_data.close()


def main():

    # Check parameter: kana only, dakuten, handakuten, variations...
    opts = parseopt()

    # load previous data
    user = parse_user('userdata.kana')

    # Build the training list
    review_list = build_list(opts)

    for k in review_list:
        clearscreen()

        print(f'What is the {opts["dest"]} for {k[opts["src"]]} ?'
        f'({Color.green}Q{Color.reset}/'
        f'{Color.yellow}W{Color.reset}/'
        f'{Color.red}E{Color.reset} or Z to exit)')

        c = getch()
        while c not in 'qQwWeEzZ':
            c = getch()

        if c == 'z' or c == 'Z' :
            clearscreen()
            break
        elif c == 'q' or c == 'Q':
            user[k['romaji']] += 1
        elif c == 'w' or c == 'W':
            user[k['romaji']] += 1
        elif c == 'e' or c == 'E':
            user[k['romaji']] += 1
        else:
            print('How did you get here ?')

        print(f'It was {k[opts["dest"]]}')
        c = getch()

    save_user(user)


main()
