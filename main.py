
from scrapy.cmdline import execute
import sys,os

print(os.path.dirname(os.path.abspath(__file__)))
#设置当前的路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#调用execute命令 来执行scrapy
execute(["scrapy","crawl","jobbole"])
