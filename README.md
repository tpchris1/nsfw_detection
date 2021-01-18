# BaTalk NSFW Detection

## About

> BaTalk 

## 環境
* 請參考 [協作](CONTRIBUTING.md)

## 注意事項
* 發 **[issue](.github/issue_templates/)** 請參照格式
* **[協作](CONTRIBUTING.md)** 請參閱指南
* **[日誌](CHANGELOG.md)** 是用 [standord-changelog](https://www.npmjs.com/package/standard-changelog) 自動產生 請勿手動更改

---

## API Usage

**Detect an image.**

| Method | POST
| --- | ---
| Route | https://api.domain.name/{ver}/nsfw-detect
| Response Model | [下面](#response-model)

**POST Body**

| Key | Required | Description
| --- | --- | ---
| image | required | A binary file, base64 data, or a URL for an image.
| type | optional | The type of the file that's being sent; file, base64 or URL
| name | optional | The name of the file, this is automatically detected if uploading a file with a POST and multipart / form-data

#### Response Model

| Key | Format | Description
| --- | --- | ---
| data | mixed | Is null, boolean, or integer value. If it's a post then this will contain an object with the all generated values, such as an ID.
| success | boolean | Was the request successful
| status | integer | HTTP Status Code

### Local API
* tensorflow-open_nsfw

### Cloud API
* [Cloudinary AWS Addons](https://cloudinary.com/documentation/aws_rekognition_ai_moderation_addon)[pycloudinary](https://github.com/cloudinary/pycloudinary)

> 50 次 / 月

* [Sightengine](https://sightengine.com/docs/getstarted)

> 500 次 / 天, 2000 次 / 月

---

## TODO
- [x] 讓 image 可以支援 file 以外的格式
* 可以傳入 file 和 url
> 還需要可以傳入 base64

- [x] 統一回傳的格式
* 目前 統一回傳 possibility
> 未來

- [ ] 把 /api/nsfw/ 改成如上所述的格式
* 尚未動工

- [ ] 權限控制
* 尚未動工

- [ ] 刪除時連同圖片檔案 / 不儲存圖片 / 外部無法讀取圖片
* 尚未動工

- [ ] 將中間值的圖片做二次檢定
* 尚未動工

## Bottole Neck
1. 我時間不太夠r