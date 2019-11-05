import sys
sys.path.insert(1, '/Users/andrew/Documents/py_basic/util')
import timeutil
import json
import dataloader
import socket
import io
import errno
import time
import analyser


FOUND = 100
NOT_FOUND = 0


# 서버 문제시 클라이언트에서 재 접속은 잘 되나, 클라이언트 문제시 서버에서 재 설정은 오류

def main():
    global loader
    STX = 2

    # 엑셀 파일에 있는 금칙어를 로드,
    loader = dataloader.DataLoader()
    loader.load_data('/Users/andrew/Downloads/pWords.xlsx')

    # 형태소분석기를 로드
    tokenizer = analyser.Analyser()

    # TCP/IP 구성 정보를 로드
    global tcp_config
    global conn
    global interval

    try:
        with open('tcp_config.json', encoding='utf-8') as json_file:
            tcp_config = json.load(json_file)
    except FileNotFoundError:
        print("No File exists...")
        exit('socket configuration exception')

    host = tcp_config['hostname']
    port = tcp_config['port']
    interval = tcp_config['interval']

    error_cnt = 0
    while True:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn.connect((host, port))
        except ConnectionRefusedError:
            conn.close()
            time.sleep(10)
            continue

        while True:
            try:
                content = conn.recv(200)
            except socket.error as e:
                print("error while receiving :: " + str(e), e.errno)
                if e.errno == errno.EPIPE:
                    conn.close()
                    break
                else:
                    raise
                    # exit("terminating")
            except:
                print("error 2 while receiving :: ")
                print(errno)
                break

            line_time = timeutil.TimeElapsed()

            if len(content) == 0:
                error_cnt += 1
                if error_cnt > 3:
                    error_cnt = 0
                    break

            if content[0] != STX:
                print('wrong data from the server..')
                continue

            actual_data = content[2:]
            print('[' + actual_data.decode(encoding='cp949') + ']')

            # 일반로직에 따라수신한 문장의 단어별 일따라 금지어 존재 검색
            pword_list = check_pword(actual_data.decode(encoding='cp949'))
            if len(pword_list) > 1:
                print(pword_list, len(pword_list))

            # 복합명사 처리를 위해 속기기록을 형태소 분석하여 명사만 가져온다
            nouns_list = tokenizer.get_noun_tokens(actual_data.decode(encoding='cp949'))
            for noun in nouns_list:
                print('Noun', noun)

            print("Time spent to analyse line: ", line_time.getelapsed())
            print('------------------------------------')


def check_pword(content):
    # totaltime = timeutil.TimeElapsed()

    words_found_list = []

    text_lists = content.strip().split(' ')
    print(text_lists)
    # 인식된 각 텍스트를 금칙어에 있는지 확인
    count = 1
    for curr_word in text_lists:
        # 1. single 단어를 검색한다
        result = loader.find_word(curr_word)
        if result == FOUND:
            print("금지어 발견 1-->", '[', curr_word, ']')
            words_found_list.append(curr_word)
            count = count + 1
            continue

        # 미발견 시 복합단어 처리 위해, 그러나 다음 단어가 없으면 더 이상 복합 단어 처리는 하지 않음
        if count + 1 >= len(text_lists):
            count = count + 1
            continue

        next_word = text_lists[count+1]
        # 2. single 단어 검색 안되면, 인접 단어와 space 넣어 조합하여 검색
        combined_word = curr_word + ' ' + next_word
        result = loader.find_word(combined_word)
        if result == FOUND:
            print("복합 금지어 발견 2-->", combined_word)
            count = count + 1
            continue

        # 3. single 단어 검색 안되면, 인접 단어와 space 없이 조합하여 검색
        combined_word = curr_word + next_word
        # print(combined_word, len(combined_word))
        result = loader.find_word(combined_word)
        if result == FOUND:
            print("복합 금지어 발견 3-->", combined_word)
            count = count + 1
            continue

        # 4. 오류 사전에서 combined word에 대한 대체명사를 검색하여 있으면 대체명사로 검색
        try:
            replaced_word = tcp_config[combined_word]
            # print('대체어: [', combined_word, '->', replaced_word, ']')
        except KeyError:
            replaced_word = ''

        if replaced_word != '':
            result = loader.search_in_dict(replaced_word)
            if result:
                print("대체어 금지어 발견 4-->", curr_word, replaced_word)
                count = count + 1
                continue

        # 5. combined word 길이가 4음절 이상이면, ngram 분리하여 각각 검색
        grams = [2, 3, 4, 5, 6]
        combined_word = content.replace(' ', '')
        # print('c-words:', combined_word)
        if len(combined_word) > 3:
            for gram in grams:
                start = 0
                end_pos = len(combined_word) + 1
                for end in range(gram, end_pos):
                    substr = combined_word[start:end]
                    start = start + 1
                    # print('NGRAM 단어:', substr)

                    result = loader.search_in_dict(substr)
                    if result:
                        print("부분 금지어 발견 5-->", curr_word, substr)
                        break

        count = count + 1

    # print("Time spent: ", totaltime.getelapsed())
    return words_found_list


if __name__ == "__main__":
    main()

    '''
     offset = 0
     count = 0
     data = ""
     while True:
         with open('test.txt', 'r', encoding='utf-8') as src_f:
             src_f.seek(offset)
             for line in src_f:
                 data = line.replace('\n', '')
                 if data.__len__() == 0:
                     continue
                 # print(offset, '[' + data + ']')

                 data = data.replace('\t', ' ')
                 texts = data.split(' ')
                 for text in texts:
                     wordtime = timeutil.TimeElapsed()
                     result = loader.find_word(text) or loader.find_word(text + '*') or loader.find_word('*' + text + '*')
                     # result = loader.find_word(text)
                     if result == 100:
                         print("금지어!!!", text, end='')
                     elif result == 50:
                         print("금지어 가능!!!", text, end='')
                     else:
                         print('OK', text, end='')
                     print(", time:[", wordtime.getelapsed(), ']')

             offset = src_f.tell()

         count = count + 1
         if count > 10:
             break
         else:
             time.sleep(10)
     '''