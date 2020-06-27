from selenium import webdriver
import time

# browser = webdriver.Firefox()
# browser.get('http://www.sse.com.cn/disclosure/fund/etflist/detail.shtml?type=005&fundid=510010&etfClass=1')
# time.sleep(3)
# # 等待一下就加载出来了 selenium niub
# print(browser.page_source)
from pcf_sh.items import PcfShItem

item = PcfShItem()
fund_id = 123123
print(item.__dict__)
print(PcfShItem.__dict__.get('fields'))
for field in PcfShItem.__dict__.get('fields').keys():
    try:
        item[field] = eval(field)
    except NameError:
        pass
print(item)