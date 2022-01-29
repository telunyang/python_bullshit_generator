import json, random

'''
原始作者
Bill Hsu (徐子修)
https://github.com/StillFantastic/bullshit

改寫作者
Darren Yang (楊德倫)
'''

# 唬爛類別
class Bullshit:
    # 建構子
    def __init__(self):
        # 讀取唬爛資料集
        with open("./data.json", "r", encoding="utf8") as file:
            self.dict_data = json.loads(file.read())
    
    # 判斷目前句子是否結束
    def isEnd(self, str):
        list_end_symbol = ["。", "？", "！", "?", "!"]
        if any( str[len(str)-1] in symbol for symbol in list_end_symbol ):
            return True
        return False

    # 產生唬爛句子
    def generate(self, param_topic, param_min_length):
        # 計算字數是否超過指定字數
        min_length = 0

        # 使用者輸入的可能是字串(例如 "100")，轉成數值
        param_min_length = int(param_min_length)

        '''
        [隨機排序名人語錄]
        範例
        eg: "盧梭a，浪費時間是一樁大罪過。b"
        eg: "莎士比亞a，本來無望的事，大膽嘗試，往往能成功。b"
        '''
        list_famous = self.dict_data['famous']
        random.shuffle(list_famous)

        '''
        [隨機排序唬爛語錄]
        範例
        eg: "x的發生，到底需要如何實現，不x的發生，又會如何產生。"
        eg: "x的出現，必將帶領人類走向更高的巔峰。"
        '''
        list_bullshit = self.dict_data['bullshit']
        random.shuffle(list_bullshit)     

        # 縮排文字
        str_indent = " " * 4

        # 生成文字資料
        str_gen = ''
        
        # 生成過程中，只要超過指定字數，則跳出迴圈
        while min_length < param_min_length:
            # 取得整數亂數，藉以決定建立新段落、產生名人語錄，還是唬爛語錄
            int_rand = random.randint(0, 99)

            # 根據整數亂數來決定生成的方向
            if int_rand < 5 and self.isEnd(str_gen):
                # 建立新段落
                str_gen += "\n\n" + str_indent

            elif int_rand < 27:
                # 倘若可用的名人語錄都被拿光了，則結束生成，跳出迴圈
                if len(list_famous) == 0:
                    break

                # 取得隨機排序後的名人語錄第 1 句
                sentence_famous = list_famous[0]

                # 沒被取得、剩下的語錄，重新初始化
                list_famous = list_famous[1:]

                # 「曾說過、曾講過」之類的詞，用來取代名人語錄當中的 a 字元
                str_before = self.dict_data['before'][ random.randint(0, len(self.dict_data['before']) - 1 ) ]

                # 「這啟發了我、這不禁讓我深思」之類的詞，用來取代名人語錄當中的 b 字元
                str_after = self.dict_data['after'][ random.randint(0, len(self.dict_data['after']) - 1) ]

                # 取代名人語錄當中的 a 和 b 字元
                sentence_famous = sentence_famous.replace("a", str_before)
                sentence_famous = sentence_famous.replace("b", str_after)

                # 合併生成字串
                str_gen += sentence_famous

            else:
                # 倘若可用的唬爛語錄都被拿光了，則結束生成，跳出迴圈
                if len(list_bullshit) == 0:
                    break

                # 取得隨機排序後的唬爛語錄第 1 句
                sentence_bullshit = list_bullshit[0]

                # 沒被取得、剩下的語錄，重新初始化
                list_bullshit = list_bullshit[1:]

                # 取代唬爛語錄當中的 x 字元
                sentence_bullshit = sentence_bullshit.replace("x", param_topic)

                # 合併生成字串
                str_gen += sentence_bullshit

            # 每次生成句子，都要計算生成字數
            min_length = len(str_gen)

        # 縮排後再回傳
        return str_indent + str_gen