# nginx+uWSGI Dockerized Versions
## About
- 通過Docker compose，建立nginx和api(uWSGI+Django)兩個獨立services
- 使用nginx作為獨立proxy server，與uWSGI通過unix file socket溝通
- uwsgi再通過container內部的port作為接口與Django溝通

## Environment
- Ubuntu (18.04)
- Docker (18.09.7, build 2d0083d)
  - 以下為Docker以及Docker Compose會自動安裝
  - Python (3.6.8)
  - Django (2.2.6)
  - Django-Rest-Framework (3.10.3)
  - uWSGI (2.0.18)
  - Nginx (1.14.0 (Ubuntu)) 

## Get Started
- 建立`nginx`和`api`services
  - `docker-compose build`
- 查看現在有哪些services
  - `docker-compose ps`
- 啟動兩個services
  - `docker-compose up`:會看到up的過程
  - `docker-compose up -d`:直接在背景運行
- 進入兩個已經up的services
  - `docker-compose exec nginx bash` 進入nginx的container
  - `docker-compose exec api bash` 進入api的container