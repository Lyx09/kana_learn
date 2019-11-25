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
a ka sa  ta  na ha ma ya ra wa n 
i ki shi chi ni hi mi /  ri wi /
u ku su  tsu nu hu mu yu ru /  /
e ke se  te  ne he me /  re we /
o ko so  to  no ho mo yo ro wo /
'''

hiragana = '''
あ か さ た な は ま や ら わ ん
い き し ち に ひ み /  り ゐ /
う く す つ ぬ ふ む ゆ る /  /
え け せ て ね へ め /  れ ゑ /
お こ そ と の ほ も よ ろ を /
'''

katakana = '''
ア カ サ タ ナ ハ マ ヤ ラ ワ ン
イ キ シ チ ニ ヒ ミ /  リ ヰ /
ウ ク ス ツ ヌ フ ム ユ ル /  /
エ ケ セ テ ネ ヘ メ /  レ ヱ /
オ コ ソ ト ノ ホ モ ヨ ロ ヲ /
'''

# DIACRITICS

romaji_diacrit = '''
ga za da ba pa nga
gi zi di bi pi ngi
gu zu du bu pu ngu
ge ze de be pe nge
go zo do bo po ngo
'''

hiragana_diacrit = '''
が ざ だ ば ぱ か゚ 
ぎ じ ぢ び ぴ き゚ 
ぐ ず づ ぶ ぷ く゚ 
げ ぜ で べ ぺ け゚ 
ご ぞ ど ぼ ぽ こ゚ 
'''

katakana_diacrit = '''
ガ ザ ダ バ パ カ゚
ギ ジ ヂ ビ ピ キ゚
グ ズ ヅ ブ プ ク゚
ゲ ゼ デ ベ ペ ケ゚
ゴ ゾ ド ボ ポ コ゚
'''

# YOO_ON / DIGRAPHS

romaji_digraph = '''
kya sha cha nya hya mya rya gya ja bya pya ngya
kyu shu chu nyu hyu myu ryu gyu ju byu pyu ngyu
kyo sho cho nyo hyo myo ryo gyo jo byo pyo ngyo
'''

hiragana_digraph = '''
きゃ しゃ ちゃ にゃ ひゃ みゃ りゃ ぎゃ じゃ びゃ ぴゃ き゚ゃ
きゅ しゅ ちゅ にゅ ひゅ みゅ りゅ ぎゅ じゅ びゅ ぴゅ き゚ゅ
きょ しょ ちょ にょ ひょ みょ りょ ぎょ じょ びょ ぴょ き゚ょ
'''

katakana_digraphs =  '''
キャ シャ チャ ニャ ヒャ ミャ リャ ギャ ジャ ヂャ ビャ ピャ
キュ シュ チュ ニュ ヒュ ミュ リュ ギュ ジュ ヂュ ビュ ピュ
キョ ショ チョ ニョ ヒョ ミョ リョ ギョ ジョ ヂョ ビョ ピョ
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
