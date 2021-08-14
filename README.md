# 项目运行

`pip install -r requirements.txt -i https://pypi.doubanio.com/simple/`

`gunicorn -c gunicorn.py main:app`

# docker 启动服务

`docker pull litrewu/api`

`docker run -d -p 80:5252 --name api-test litrewu/api`
