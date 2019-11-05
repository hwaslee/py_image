import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


# 롯데홈쇼핑 금지어
# num_not_necessary = 1
# name_of_sheet = '05.31'
# filename = '/Users/andrew/Downloads/pWords.xlsx'
# 신세계TV쇼핑 금지어
num_not_necessary = 0
name_of_sheet = 'Sheet1'
filename = '/Users/andrew/Documents/RPA_신세계TV쇼핑/SSG닷컴_RM_키워드(금칙어)_해제 완료.xlsx'

# df = pd.read_excel('/Users/andrew/Downloads/pWords.xlsx', sheetname='Sheet1')
df = pd.read_excel(filename, sheet_name=name_of_sheet, header=num_not_necessary)

# ---- 각종 값을 점검한다 ----
# print("df ==>", df)
# print('-------------------------')
# print('df.size ==>', df.size)  # 2106
# print('-------------------------')
# print('df.axes ==>', df.axes)
# print('-------------------------')
# print('df.cummax ==>', df.cummax)
# print('-------------------------')
# print('df.cummin ==>', df.cummin)
# print('-------------------------')
# # print(df.head(2))
# print('ndim:', df.ndim)
# print("df.columns ==>", df.columns)

count = 0
# col_lists = ['공통', '공통\n(실증필요단어)', '의류', '속옷', '패션잡화', '가구', '침구/침장', '가전', '스포츠/레저', '식품', '주방용품', \
#              '이미용\n(실증필요단어)', '생활/잡화', '유아동용품', '문화/서비스', '보석/장신구', '건강', '이미용']
col_lists = df.columns
print('col_lists ==>', col_lists)


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
    print('-------------', col, '------------------')
    for i in range(0, max_index):
        cell_value = df.at[i, col]
        if str(cell_value).replace(' ', '') == 'nan':
            continue

        # 값을 보정 (특히 숫자인 경우 필요)
        if cell_value == 1:
            cell_value = '100%'

        print('{:3>d} {}'.format(count, cell_value))
        count = count + 1
