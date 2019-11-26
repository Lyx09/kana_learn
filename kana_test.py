#! /usr/bin/python3
# -*- coding: utf-8 -*-

import random
import getopt
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

def table_to_list(table):
    return re.split('\W+', table.strip())

def kana_from_table(romaji, hiragana, katakana):
    kana_list = []
    ziplist = list(zip(table_to_list(romaji), table_to_list(hiragana),
        table_to_list(katakana)))
    print(ziplist)
    getch()
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

hiragana_digraph
=
'''
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

katakana_digraphs
=

'''
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

def clearscreen():
    os.system('clear')

def parseopt():
    print()

def build_list(list_opt = None):
    '''

    0: Romaji
    1: Hiragana
    2: Katakana
    3: Dakuten
    4: Handakuten
    5: Diacritics
    6: Digraphs
    7: Old
    8: Shuffle
    '''

    if list_opt == None:
        list_opt = {
                'diacritics' :  False,
                'digraphs' :    False,
                'old' :         True,
                'shuffle' :     True
                }

    kana_list = kana_from_table(romaji, hiragana, katakana)
    
    if list_opt['diacritics']:
        kana_list.append(kana_from_table(romaji_diacrit, hiragana_diacrit, 
            katakana_diacrit))

    if list_opt['digraphs']:
        kana_list.append(kana_from_table(romaji_digraph, hiragana_digraph, 
            katakana_digraph))

    if list_opt['shuffle']:
        random.shuffle(kana_list)
    return kana_list


def main():
    user_data = open('userdata.kana', 'w')
    src = 'romaji'
    dest = 'hiragana'

    # Check parameter: kana only, dakuten, handakuten, variations...
    parseopt()

    # load previous data

    review_list = build_list()

    for k in review_list:
        clearscreen()

        print(f'What is the {dest} for {k[src]} ?'
        f'({Color.green}Q{Color.reset}/'
        f'{Color.yellow}W{Color.reset}/'
        f'{Color.red}E{Color.reset} or Z to exit)')

        c = getch()
        while c not in 'qQwWeEzZ':
            c = getch()

        if c == 'z' or c == 'Z' :
            clearscreen()
            sys.exit(1)
        elif c == 'q' or c == 'Q':
            print('q')
        elif c == 'w' or c == 'W':
            print('w')
        elif c == 'e' or c == 'E':
            print('e')
        else:
            print('How did you get here ?')
        
        print(f'It was {k[dest]}')
        c = getch()


main()
