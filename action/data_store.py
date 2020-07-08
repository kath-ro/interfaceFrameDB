from utils.db_handler import DB
from utils.log import *

class RelyDataStore(object):
    def __init__(self):
        pass

    @classmethod
    def do(cls, store_point, api_name, case_id, request_source = {}, response_source = {}):
        tmp = {"request":{}, "response":{}}
        for key, value in store_point.items():
            if key == "request":
                # 说明取的是请求参数中的，也即是request_source
                for i in value:
                    if i in request_source:
                        val = request_source[i]
                        if api_name not in tmp["request"]:
                            tmp["request"] = {api_name:{case_id:{i:val}}}
                        elif case_id not in tmp["request"][api_name]:
                            tmp["request"][api_name] = {case_id:{i:val}}
                        else:
                            tmp["request"][api_name][case_id][i] = val
                    else:
                        info("字段[%s]在原始数据request_source中不存在!" %i)
            elif key == "response":
                # 说明取的是响应body中的字段值，也即是response_source
                for i in value:
                    if i in response_source:
                        val = response_source[i]
                        if api_name not in tmp["response"]:
                            tmp["response"] = {api_name: {case_id: {i: val}}}
                        elif case_id not in tmp["response"][api_name]:
                            tmp["response"][api_name] = {case_id: {i: val}}
                        else:
                            tmp["response"][api_name][case_id][i] = val
                    else:
                        info("字段[%s]在原始数据response_source中不存在!" % i)
        if tmp["request"] or tmp["response"]:
            db = DB()
            api_id = db.get_api_id(api_name)
            db.update_store_data(api_id, int(case_id), tmp)

if __name__ == "__main__":
    store_point = {"request": ["username", "password"], "response": ["userid"]}  #
    request_source = {"username":"lisi123", "password":"wang1234dsfe","email":"xx@qq.com"}
    response_source = {"userid":12, "code":"00"}
    data = RelyDataStore.do(store_point, "用户注册",2,request_source, response_source)