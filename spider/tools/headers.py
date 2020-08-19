import os
from random import choice, randint
from user_agent import generate_user_agent, generate_navigator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def ua():
    random_ip = '.'.join(str(randint(0, 255)) for _ in range(4))
    return {"User-Agent": generate_user_agent(), "X-FORWARDED-FOR": random_ip, "X-REAL-IP": random_ip,
            "CLIENT-IP": random_ip}


async def async_ua():
    ip = '.'.join(str(randint(0, 255)) for _ in range(4))
    return {"User-Agent": generate_user_agent(), "X-FORWARDED-FOR": ip, "X-REAL-IP": ip,
            "CLIENT-IP": ip}


# def ua():
#     # file = os.path.join(BASE_DIR, "useragents.txt")
#     # with open(file, 'r') as f:
#     #     ua_list = f.readlines()
#     # random_ip = str(randint(1, 255)) + '.' + str(randint(1, 255)) + '.' + str(randint(1, 255)) + '.' + str(
#     #         randint(1, 255))
#     header = {
#         # "User-Agent": choice(ua_list).strip(),
#         "User-Agent": generate_user_agent(),
#         # "X-FORWARDED-FOR": random_ip,
#         # "X-REAL-IP": random_ip,
#         # "Accept-Encoding": "gzip, deflate, br",
#     }
#     return header


if __name__ == '__main__':
    rs = ua()
    print(rs)
