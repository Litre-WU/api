from spider.car.cwz import CWZ
from spider.car.bj import BJ
from spider.car.ha import HA
from spider.car.gd2 import GD2
from spider.car.sc2 import SCN
from spider.car.sd import SD
from spider.car.cq import CQ
from spider.car.js import JS
from spider.car.zj import ZJ
from spider.car.hi import HI
from spider.car.sn import SN
import sys

sys.setrecursionlimit(100000)


def trs(match):
    match_dict = {
        "京": BJ(),
        "豫": HA(),
        "粤": GD2(),
        "苏": JS(),
        "渝": CQ(),
        "鲁": SD(),
        "陕": SN(),
        # "贵": GZ(),
        # "沪": SH(),
        "川": SCN(),
        "浙": ZJ(),
        "琼": HI(),
        "C": CWZ(),
    }
    if match in match_dict:
        return match_dict[match]
    else:
        return match_dict["C"]

