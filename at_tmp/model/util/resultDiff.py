


import sys
sys.path.append("/opt/ATEST")

import json_tools

class resultDiff:
    def json_cmp(self,result,prev):


        cmp=json_tools.diff(result,prev)
        if len(cmp):
            return False
        else:
            return True
        # return cmp


if __name__=='__main__':
    a={"message": "success", "status": 1}
    b={"message": "success",  "status":1}
    c={}
    print(type(b),type(c))
    print(resultDiff().json_cmp(b,a))

