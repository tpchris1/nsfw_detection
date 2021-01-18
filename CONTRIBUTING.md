# 協作指南

## Commits
請參照 [Conventiaol Commits](https://www.conventionalcommits.org)

## 環境配置
* Docker 18
* Docker Compose

## 自動配置

---

DB
* PostgreSQL

---

Nginx
* Nginx

---

API
* Python 3.5.2
* Django 1.11
* Django-Rest-Framework

---

## 初次使用

clone 專案並進入
***注意*** 請 clone 到 batalk 資料夾內
```
git clone <repo_url> batalk && cd batalk
```

啟動 server
```
docker-compose up
```

## 已經啟動的環境

遷移資料庫 (migrations)  
*TODO: 自動化*
```
docker-compose exec api python manage.py makemigrations <app>
docker-compose exec api python manage.py migrate
```

重啟 web
```
docker-compose restart api
```

修改 nginx 設定後套用設定
```
docker-compose build --no-cache nginx
docker-compose up
```
