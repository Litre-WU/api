# 启动项目

pip install -r requirements.txt

gunicorn -c gunicorn.py main:app

# docker 启动

docker run -d -p 80:5252 --name api-test litrewu/api
