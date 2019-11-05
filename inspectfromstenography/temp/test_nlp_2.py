import time
from konlpy.tag import Kkma, Twitter, Komoran, Hannanum


# texts = ['관리하시고 치료하시는 거예요.', '롯데마트의 흑마늘 양념 치킨이 만약에 논란이 되고 있다.']
texts = ['가장 좋은', '전 상담원 통화중', '전혀', '단 한번', '더', '덜', '방송에서만', '봉제선이 없는', '실크와 같은']

pos_taggers = [('Komoran', Komoran()), ('kkma', Kkma()), ('twitter', Twitter()), ('Hannanum', Hannanum())]
results = []
for name, tagger in pos_taggers:
    tokens = []
    process_time = time.time()
    for text in texts:
        result = tagger.pos(text)
        print(name, "POS", result)
        tokens.append(result)

        result = tagger.morphs(text)
        print(name, "MORPHS", result)
        tokens.append(result)

        result = tagger.nouns(text)
        print(name, "NOUNS", result)
        tokens.append(result)

    process_time = time.time() - process_time
    print('tagger name = %10s, %.3f secs' % (name, process_time))
    results.append(tokens)
    print('----------------------------------')