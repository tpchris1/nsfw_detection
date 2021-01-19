# BaTalk NSFW Detection
---
## About
> 本專案為一使用Tensorflow等ML技術進行不當圖片之過濾，並透過Django架設Web Server以RESTFUL方式進行API開發，採三階段目標進行。
> 第一階段 - 使用ML套件進行圖片判斷並透由Django輸出API，並使用Docker compose包裝
> 第二階段 - 加入權限機制，並能管理圖片檔案，API可透過Nginx協調達到多工處理效果
> 第三階段 - 資料庫紀錄以及分析完成自動學習機制，以因應未成功過濾之圖片，並優化效能、提升容錯能力

## 正式環境
- Ubuntu (18.04)
- Docker (18.09.7, build 2d0083d)
- Docker Compose (1.25.0-rc2, build 661ac20e)
  - 以下為Docker以及Docker Compose會自動安裝
  - Python (3.6.8)
  - Django (2.2.6)
  - Django-Rest-Framework (3.10.3)
  - uWSGI (2.0.18)
  - Nginx (1.14.0 (Ubuntu)) 

## GetStarted
### Non-Docker Version
- [Non-Docker Version](docs/Non-Docker_version.md)
### Docker Version 
- [Docker Version](docs/Docker_version.md)
### uWSGI Dockerized Version 
- [uWSGI Dockerized Version](docs/uWSGI_Dockerized_Version.md)
### nginx+uWSGI Dockerized Version 
- [nginx+uWSGI Dockerized Version](docs/nginx+uWSGI_Dockerized_Version.md)

### Shell File Version
- 更改`nsfw_run.sh`權限
  - `chmod 777 nsfw_run.sh`
- 啟動services
  - `./nsfw_run.sh run -i #`#表示要啟動的container數量
- 停止services
  - `./nsfw_run.sh stop` 停止所有的services
- Debug services
  - `./nsfw_run.sh debug -i #`#表示要啟動的container數量
  - `Ctrl + C` to exit services
- 清除所有掛載出來的`api#-container`(#表示container-index)文件夾
  - `./nsfw_run.sh clear -i #`#表示container數量
- 查看命令幫助
  - `./nsfw_run.sh help`
- `run`和`debug`都會把之前的containers全部關掉

### Admin Backstage
- 訪問`http://{{domain}}/container/{{container_index}}/admin/`
  - 每一個container都有自己的admin，通過相對應的container_index來訪問不同的admin backstage
  - 比如`http://{{domain}}/container/1/admin/` 可以訪問第一個container
- 賬戶密碼的設定在`api/create_admin.py`
  - 目前都是`ID`跟`pw`都是`batalk`
- 在admin刪掉entry後，server上對應media裡面的圖片也會刪掉

### 其他使用規範probability
- Threshold: 
  - x < 0.6 : SFW
  - 0.6 <= x < 0.7 : 人工處理
  - x >= 0.7 : NSFW

## API Usage
---

### 判斷圖片合法性

| Method         | POST                                 |
| -------------- | ------------------------------------ |
| Route          | https://{baseuri}/api/nsfw           |
| Request Body   | [連結](#request-body)                |
| Response Model | [連結](#response-model)              |

#### Request Body

| Key  | Required | Type   | Description                                     |
| ---- | -------- | ------ | ----------------------------------------------- |
| file | required | Mixed  | base64,img url,binary file                      |
| type | required | String | 傳輸圖片的格式                                   | 
| name | required | String | 若使用Form Data方法時圖片的欄位名稱，預設為file   |
| user_id | required | String | 用戶ID，預設為null                            |


#### Response Model

| Key     | Format  | Description                |
| ------- | ------- | -------------------------- |
| data    | object  | NSFW物件                   |
| success | boolean | Was the request successful |
| status  | integer | HTTP Status Code           |

## API Example
---
- URL
```
   {
    "file": "https://i.imgur.com/AD3MbBi.jpg",
    "type": "url",
    "name": "Yourname",
    "user_id": "001"
   }
```
- image
```
   {
    "file": "yourimagepath/",
    "type": "image",
    "name": "Yourname",
    "user_id": "001"
   }
```
- Base64
```
   {
    "file": "data:image/jpeg;base64,/9j/4AAQSkZ...",
    "type": "base64",
    "name": "Yourname",
    "user_id": "001"
   }
```