# uWSGI Dockerized Version 
## About
- 通過Docker，並且使用uWSGI作為接口與Django溝通
- 使用80 port mapping to 8000

## Environment
- Ubuntu (18.04)
- Docker (18.09.7, build 2d0083d)
  - 以下為Docker會自動安裝
  - Python (3.6.8)
  - Django (2.2.6)
  - Django-Rest-Framework (3.10.3)
  - uWSGI (2.0.18)

## Get Started
- 建立docker image
  - `sudo docker build . -t docker_nsfw`
- 檢查現在有什麼images
  - `sudo docker images`
- 啟動container
  - `sudo docker run -p 80:8000 -it docker_nsfw`
