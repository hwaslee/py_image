import sys
sys.path.insert(1, '/Users/andrew/Documents/py_basic/util')
import timeutil
import pandas as pd


# 금지어를 memory에 load하고, 해당단어가 금지어인지 확인하는 기능
class DataLoader:
    wordsset = set()
    postpositions = ['은', '는', '이', '가', '께', '의', '에', '에게', '한테', '한테서', '에게서', '에게서부터',
                     '으로', '로', '로서', '으로서', '로써', '으로써', '이라고', '라고', '만큼', '와', '과', '하고', '따라',
                     '을', '를', '에서  부터', '받은', '더러', '보다', '처럼', '같이', '만', '조차', '조차도', '마저', '마저도',
                     '까지', '까지도', '부터', '적']

    def __init__(self):
        self.elapsed = 0
        self.filename = ''

    # 지정된 금지어 파일에서 금지어를 memory로 load
    def load_data(self, filename):
        self.filename = filename
        loadingtime = timeutil.TimeElapsed()

        num_not_necessary = 0
        name_of_sheet = 'Sheet1'
        filename = '/Users/andrew/Documents/RPA_신세계TV쇼핑/SSG닷컴_RM_키워드(금칙어)_해제 완료.xlsx'

        # df = pd.read_excel('/Users/andrew/Downloads/pWords.xlsx', sheetname='Sheet1')
        df = pd.read_excel(filename, sheet_name=name_of_sheet, header=num_not_necessary)

        count = 0
        # col_lists = ['공통', '공통\n(실증필요단어)', '의류', '속옷', '패션잡화', '가구', '침구/침장', '가전', '스포츠/레저', '식품', '주방용품', \
        #              '이미용\n(실증필요단어)', '생활/잡화', '유아동용품', '문화/서비스', '보석/장신구', '건강', '이미용']
        col_lists = df.columns
        # print('col_lists ==>', col_lists)

        # ---- column들의 길이를 가져온다 ----
        # maxColumnLenghts = []
        # for col in range(len(df.columns)):
        #     maxColumnLenghts.append(max(df.iloc[:,col].astype(str).apply(len)))
        # print('Max Column Lengths ', maxColumnLenghts)

        if num_not_necessary is not None:
            max_index = df.__len__() - num_not_necessary
        else:
            max_index = df.__len__()

        for col in col_lists:
            if col != 'RM키워드':
                print(col, 'skipping')
                continue

            # print('-------------', col, '------------------')
            for i in range(0, max_index):
                cell_value = df.at[i, col]
                if str(cell_value).replace(' ', '') == 'nan':
                    continue

                # 값을 보정 (특히 숫자인 경우 필요)
                if cell_value == 1:
                    cell_value = '100%'

                print('{:3>d} {}'.format(count, cell_value))

                DataLoader.wordsset.add(cell_value)
                count = count + 1

                count = self.add_word_with_postposition(cell_value, count)

        # with open(self.filename, 'r', encoding='utf8') as words_f:
        #     # file에서  읽어서 loading하는 부분은 실 환경에 따라 변경됨.
        #     for line in words_f:
        #         # print('[', line, ']')
        #         data = line.replace('\n', '')
        #         if data.__len__() == 0:
        #             continue
        #
        #         data = data.replace('\t', ' ')
        #         wordslist = data.split(' ')
        #         print(wordslist)
        #
        #         for word in wordslist:
        #             DataLoader.wordsset.add(word)

        print("Time to spend for 금지어  로딩", loadingtime.getelapsed())
        print("Words count", len(DataLoader.wordsset))

    # 정확도 향상 보강1: 금칙어 구성시 excel 명사에 조사를 추가하여 memory로 load
    def add_word_with_postposition(self, cell_value, count) -> int:
        cell_value = DataLoader.cleansing_word(cell_value)
        for post in DataLoader.postpositions:
            DataLoader.wordsset.add(cell_value + post)
            count = count + 1
        return count

    # 금지어를 찾는데, 먼저 전달된 단어로 찾고, 없으면 조사를 붙여서 찾는다
    # return: 금지어발견:100, 미발견:0
    def find_word(self, testdata) -> int:
        filtered_data = DataLoader.cleansing_word(testdata)
        result = DataLoader.search_in_dict(filtered_data)
        if result:
            return 100

        # 단어가 발견 안되면 조사를 붙여서 다시 검색
        for post in DataLoader.postpositions:
            result = DataLoader.search_in_dict(filtered_data + post)
            if result:
                return 100

        # grams = [2, 3, 4, 5]
        # for gram in grams:
        #     start = 0
        #     end_pos = len(testdata) + 1
        #     for end in range(gram, end_pos):
        #         substr = testdata[start:end]
        #         start = start + 1
        #         # print(substr)
        #
        #         result = DataLoader.search_in_dict(substr)
        #         if result:
        #             return 50
        return 0

    # text 내 특수문자를 제거한다
    @staticmethod
    def cleansing_word(testdata):
        chars = [',',  '.', '!', '-', '\"', ';', ':']
        for char in chars:
            testdata = testdata.replace(char, '')
        return testdata

    # 해당 단어를 memory에서 검색하여 금지어인지 검토
    # return: 금지어이면 True, 아니면 False
    @staticmethod
    def search_in_dict(word) -> object:
        return word in DataLoader.wordsset


if __name__ == '__main__':
    loader = DataLoader()
    loader.load_data('/Users/andrew/Documents/RPA_신세계TV쇼핑/SSG닷컴_RM_키워드(금칙어)_해제 완료.xlsx')

    print(loader.find_word('여드름치료'))
    print(loader.find_word('인기로'))
    print(loader.find_word('테스트'))
    print(loader.find_word('테스트를'))