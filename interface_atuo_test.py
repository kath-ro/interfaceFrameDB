from utils.db_handler import DB
from action.get_rely import GetRely
from utils.HttpClient import HttpClient
from action.data_store import RelyDataStore
from action.check_result import CheckResult
from utils.log import *

def main():
    # 连接数据库，获取连接实例对象
    db = DB()
    # 从数据库中获取需要执行的api集合
    api_list = db.get_api_list()
    for id, api in enumerate(api_list, 1):
        api_id = api[0]
        api_name = api[1]
        req_url = api[2]
        req_method = api[3]
        parm_type = api[4]
        # 通过api_id获取它对应的测试用例
        api_case_list = db.get_api_case(api_id)
        for idx, case in enumerate(api_case_list, 1):
            case_id = case[0]
            request_data = eval(case[2]) if case[2] else {}
            rely_data = case[3]
            protocol_code = case[4]
            data_store = eval(case[6]) if case[6] else {}
            check_point = eval(case[7]) if case[7] else {}
            # 接下来进行数据依赖的处理
            if rely_data:
                rely_data = eval(rely_data)
                request_data = GetRely.get(request_data, rely_data)
            else:
                info("接口[%s]的第%s用例不需要依赖数据!" %(api_name, idx))
            # 接下来进行接口请求，并获取响应body
            hc = HttpClient()
            responseObj = hc.request(req_url, req_method, parm_type, request_data)
            code = responseObj.status_code
            info("接口[%s]的第%s用例的实际响应结果为:%s" %(api_name, idx, responseObj.json()))
            if  code == int(protocol_code):
                # 进行数据依赖存储
                RelyDataStore.do(data_store, api_name, case_id, request_data, responseObj.json())
                info("接口[%s]的第%s用例的依赖数据存储成功！" %(api_name, idx))
                # 接下来进行结果校验
                error_info = CheckResult.check(responseObj.json(), check_point)
                if error_info:
                    debug("接口[%s]的第%s用例校验结果失败，错误信息：%s" %(api_name, idx, error_info))
                else:
                    info("接口[%s]的第%s用例运行成功！" %(api_name, idx))
            else:
                info("接口[%s]的第%s用例响应协议code=%s，不是期望值code=%s" %(api_name, idx, code, protocol_code))


if __name__ == "__main__":
    main()