import io_my

key = "1QDt5WQos1zbaKSAnhUcLxc2Q4JbaTfXbz5JneOBEvDo"
gid = [0,291367008]
filename = "data/test"

def test1():
    io_my.download(key,gid=gid,outputfile=filename)


key = "1QDt5WQos1zbaKSAnhUcLxc2Q4JbaTfXbz5JneOBEvDo"
api_key = "70f5008cd958bf16b61ad9d7488c0fdba0bced9c"
 
def test2():
    io_my.get_sheet_ids(key, api_key)


test2()