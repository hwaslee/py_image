# from konlpy.tag import Hannanum
from konlpy.tag import Kkma


# analyzer = Hannanum()
analyzer = Kkma()

'''
hannanum.analyze    # 구(Phrase) 분석
hannanum.morphs     # 형태소 분석
hannanum.nouns      # 명사 분석
hannanum.pos        # 형태소 분석 태깅
'''

text = '관리하시고 만약 치료하시는 거예요.'
# text = '롯데마트의 흑마늘 양념 치킨이 논란이 되고 있다.'

# 사용예시
# print('Analyze:', analyzer.analyze(text))
'''
[[[('롯데마트', 'ncn'), ('의', 'jcm')], [('롯데마트의', 'ncn')], [('롯데마트', 'nqq'), ('의', 'jcm')], [('롯데마트의', 'nqq')]],
 [[('흑마늘', 'ncn')], [('흑마늘', 'nqq')]], [[('양념', 'ncn')]],
 [[('치킨', 'ncn'), ('이', 'jcc')], [('치킨', 'ncn'), ('이', 'jcs')], [('치킨', 'ncn'), ('이', 'ncn')]],
 [[('논란', 'ncpa'), ('이', 'jcc')], [('논란', 'ncpa'), ('이', 'jcs')], [('논란', 'ncpa'), ('이', 'ncn')]],
 [[('되', 'nbu'), ('고', 'jcj')], [('되', 'nbu'), ('이', 'jp'), ('고', 'ecc')], [('되', 'nbu'), ('이', 'jp'), ('고', 'ecs')],
  [('되', 'nbu'), ('이', 'jp'), ('고', 'ecx')], [('되', 'paa'), ('고', 'ecc')], [('되', 'paa'), ('고', 'ecs')],
  [('되', 'paa'), ('고', 'ecx')], [('되', 'pvg'), ('고', 'ecc')], [('되', 'pvg'), ('고', 'ecs')],
  [('되', 'pvg'), ('고', 'ecx')], [('되', 'px'), ('고', 'ecc')], [('되', 'px'), ('고', 'ecs')], [('되', 'px'), ('고', 'ecx')]],
 [[('있', 'paa'), ('다', 'ef')], [('있', 'px'), ('다', 'ef')]], [[('.', 'sf')], [('.', 'sy')]]]
'''

print('Morphs:', analyzer.morphs(text))
# ['롯데마트', '의', '흑마늘', '양념', '치킨', '이', '논란', '이', '되', '고', '있', '다', '.']

print('POS:', analyzer.pos(text))

print('Nouns:', analyzer.nouns(text))
# ['롯데', '롯데마트', '마트', '흑', '흑마늘', '마늘', '양념', '치킨', '논란']

# print('Nouns:', analyzer.nouns(u'다람쥐 헌 쳇바퀴에 타고파'))
# ['다람쥐', '쳇바퀴', '타고파']

print('Pos:', analyzer.pos(u'웃으면 더 행복합니다!'))
# [('웃', 'P'), ('으면', 'E'), ('더', 'M'), ('행복', 'N'), ('하', 'X'), ('ㅂ니다', 'E'), ('!', 'S')]
