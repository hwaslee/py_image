import sys
sys.path.insert(1, '/Users/andrew/Documents/py_basic/util')
import timeutil
import json
import dataloader
import textDetectionUsingGCV


DESC = 0
VERTEX = 1
P1 = 0
P2 = 1
P3 = 2
P4 = 3
X = 0
Y = 1
FOUND = 100
NOT_FOUND = 0

def main():
    # 엑셀 파일에 있는 금칙어를 로드,
    loader = dataloader.DataLoader()
    loader.load_data('/Users/andrew/Documents/RPA_신세계TV쇼핑/SSG닷컴_RM_키워드(금칙어)_해제 완료.xlsx')

    totaltime = timeutil.TimeElapsed()
    print('-----------------------------------------------')

    # GCV 오류 발생한 단어에 대한 dictionary를 로드
    gcv_error_data = {}
    try:
        with open('gcv_error_dic.json', encoding='utf-8') as json_file:
            gcv_error_data = json.load(json_file)
    except FileNotFoundError:
        print("No File exists...")
    print('-----------------------------------------------')

    # 상품 이미지 파일을 GCV를 이용하여 텍스트 인식
    hndlr = textDetectionUsingGCV.OCRHandler()
    text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/1. 10160920 다나한 인삼잎 보윤 수분크림.jpg')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/2. 10160902 참존 마유 골든컴플렉스 2종 세트.png')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/3. 10164315  쁘띠프루티 울트라 모이스처라이징 페이셜 마스크팩.jpg')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/4. 10164318 쁘띠프루티 카밍 앤 브라이트 페이셜 마스크팩.png')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/5. 10164572 참존 인텐시브 골드 앰플.jpg')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/6. 10166107 일동제약 퍼스트랩 프로바이오틱 마스크팩.png')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/6. 10166107 일동제약-1.png')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/6. 10166107 일동제약-2.png')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/6. 10166107 일동제약-3.png')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/7. 10167823 이오 에브리원 솝 코코넛레몬.jpg')
    # text_lists =  hndlr.detect_text('/Volumes/USB3-64/Image/8. 10060298 티레이저 기기 + 크림.jpg')
    print('-----------------------------------------------')

    words_found_list = []

    # 인식된 각 텍스트를 금칙어에 있는지 확인
    count = 1
    for curr_word in text_lists[1:]:
        # 1. single 단어를 검색한다
        result = loader.find_word(curr_word[DESC])
        if result == FOUND:
            print("금지어 발견 -->", curr_word[DESC], curr_word[VERTEX])
            words_found_list.append(curr_word)
            count = count + 1
            continue

        # 미발견 시 복합단어 처리 위해, 그러나 다음 단어가 없으면 더 이상 복합 단어 처리는 하지 않음
        if count + 1 >= len(text_lists):
            count = count + 1
            continue

        next_word = text_lists[count+1]
        # single 단어 검색 안되면, 인접 단어와 조합하여 검색. 그러나, 인접하지 않으면 처리하지 않음
        front_p2_x = curr_word[VERTEX][P2][X]
        front_p2_y = curr_word[VERTEX][P2][Y]
        back_p1_x = next_word[VERTEX][P1][X]
        back_p1_y = next_word[VERTEX][P1][Y]
        if abs(front_p2_x - back_p1_x) > 10 or abs(front_p2_y - back_p1_y) > 10:
            count = count + 1
            continue

        # 2. single 단어 검색 안되면, 인접 단어와 space 넣어 조합하여 검색
        combined_word = curr_word[DESC] + ' ' + next_word[DESC]
        result = loader.find_word(combined_word)
        if result == FOUND:
            print("복합 금지어 발견 1-->", combined_word)
            count = count + 1
            continue

        # 3. single 단어 검색 안되면, 인접 단어와 space 없이 조합하여 검색
        combined_word = curr_word[DESC] + next_word[DESC]
        # print(combined_word, len(combined_word))
        result = loader.find_word(combined_word)
        if result == FOUND:
            print("복합 금지어 발견 2-->", combined_word)
            count = count + 1
            continue

        # 4. 오류 사전에서 combined word에 대한 대체명사를 검색하여 있으면 대체명사로 검색
        try:
            replaced_word = gcv_error_data[combined_word]
            # print('대체어: [', combined_word, '->', replaced_word, ']')
        except KeyError:
            replaced_word = ''

        if replaced_word != '':
            result = loader.search_in_dict(replaced_word)
            if result:
                print("대체어 금지어 발견 3-->", curr_word[DESC], curr_word[VERTEX])
                count = count + 1
                continue

        # 5. combined word 길이가 4음절 이상이면, ngram 분리하여 각각 검색
        grams = [2, 3, 4, 5]
        if len(combined_word) > 3:
            for gram in grams:
                start = 0
                end_pos = len(combined_word) + 1
                for end in range(gram, end_pos):
                    substr = combined_word[start:end]
                    start = start + 1
                    # print('NGRAM 단어:', substr)

                    result = loader.search_in_dict(substr)
                    if result == FOUND:
                        print("부분 금지어 발견 4-->", curr_word[DESC], curr_word[VERTEX])
                        break

        count = count + 1

    print("Time spent  for 금지어 발견: ", totaltime.getelapsed())
    print('-----------------------------------------------')


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