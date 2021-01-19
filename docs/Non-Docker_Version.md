# Non-Docker Version
## About
- 直接使用Django在原生環境下運行本API

## Environment
- Ubuntu (18.04)
- Python (3.6.8)
- Django (2.2.6)
- Django-Rest-Framework (3.10.3)

## Get Started
- 安裝python 3.6
  - `sudo apt-get update`
  - `sudo apt-get install python3.6`
- 安裝pip 3(部署時使用版本9.0.1)
  - `sudo apt-get install python3-pip`
- 可以在建立下面的安裝包之前，建立一個虛擬環境
  - 先安裝虛擬環境
    `sudo apt-get install python3-venv`
  - 建立自己的虛擬環境
    `python3 -m venv myvenv`
  - 啟動自己的虛擬環境
    `source ./myvenv/bin/activate`
  - 查看當前的安裝包狀態
    `pip list`
  - 關閉虛擬環境
    `deactivate`
- `git clone`這個專案
- `pip install` 下面的所有安裝包
  - `pip install tensorflow==1.13.2`
  - `pip install numpy==1.16.2`
  - `pip install scikit-image` (部署時使用版本0.16.1)
  - `pip install Pillow` (部署時使用版本6.2.0)
  - `pip install Django` (部署時使用版本2.2.6)
  - `pip install djangorestframework` (部署時使用版本3.10.3)
  - `pip install uwsgi` (部署時使用版本2.0.18) 
- 進入專案文件夾
  - `cd nfsw-detection`
- 運行server
  - 遷移資料庫1：`sudo python3 manage.py makemigrations`
  - 遷移資料庫2：`sudo python3 manage.py migrate`
  - 運行：`sudo python3 manage.py runserver 0.0.0.0:80`