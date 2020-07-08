import re
from utils.log import *

class CheckResult(object):
    def __init__(self):
        pass

    @classmethod
    def check(self, responseObj, checkPoint):
        errorKey = {}
        for key, value in checkPoint.items():
            sourceData = responseObj[key] if key in responseObj else ""
            if isinstance(value, str):
                # 说明是等值校验
                if key in responseObj:
                    if not sourceData == value:
                        errorKey[key] = sourceData
                else:
                    errorKey[key] = "not exists"
            elif isinstance(value, dict):
                info("sourceData", sourceData)
                #说明是需要通过正则校验或校验数据类型
                if "type" in value:
                    #说明是数据类型校验
                    typeS = value["type"]
                    if typeS == "N":
                        # 说明是整形
                        if not isinstance(sourceData, int):
                            errorKey[key] = sourceData
                    elif typeS == "S":
                       #说明是字符串类型
                        if not isinstance(sourceData, str):
                            errorKey[key] = sourceData
                    elif typeS == "xxx":
                        pass
                elif "value" in value:
                    # 说明是正则表达式校验
                    regStr = value["value"]
                    rg = re.match(regStr, "%s" %sourceData)
                    if not rg:
                        errorKey[key] = sourceData
        return  errorKey

if __name__ == "__main__":
    r = {"code": "01", "userid": 12, "id": "12"}
    c = {"code": "00", "userid": {"type": "N"}, "id": {"value": "\d+"}}
    print(CheckResult.check(r, c))