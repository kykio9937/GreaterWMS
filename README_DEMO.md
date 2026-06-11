# GreaterWMS 演示版说明

## 当前演示入口

- 前端地址：`http://127.0.0.1:8080/#/`
- 后端地址：`http://127.0.0.1:8008`
- 演示账号：点击首页 `演示进入`

当前源码已经内置演示闭环：

- 首页演示入口
- 在途运单与在途费用
- 客户对账
- 承运商对账
- 演示账号自动补齐运输演示数据

## 一键启动

在项目根目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\start_demo.ps1
```

脚本会：

1. 启动后端 `8008`
2. 启动前端 `8080`
3. 默认自动打开演示页面

如果你只想启动，不自动打开浏览器：

```powershell
powershell -ExecutionPolicy Bypass -File .\start_demo.ps1 -OpenBrowser no
```

## 停止演示服务

```powershell
powershell -ExecutionPolicy Bypass -File .\stop_demo.ps1
```

## 切换前端请求的接口地址

默认前端接口配置文件：

- `templates/public/statics/baseurl.txt`

本地演示默认值：

```txt
http://127.0.0.1:8008
```

如果你要切到公网后端地址，可以执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\set_demo_api.ps1 -ApiBaseUrl "https://your-demo-api.example.com"
```

这个脚本会同时更新：

- `templates/public/statics/baseurl.txt`
- `templates/dist/spa/statics/baseurl.txt`

## 对外演示的两种方式

### 方式一：本机临时演示

适合临时给别人看。

你需要：

1. 本机执行 `start_demo.ps1`
2. 用内网穿透把 `8080` 和 `8008` 暴露出去
3. 把前端里的接口地址切成公网后端地址

常用工具：

- `cpolar`
- `ngrok`
- `frp`

### 方式二：服务器演示版

适合更稳定的展示。

你需要：

1. 租一台服务器
2. 部署后端和前端
3. 把 `baseurl.txt` 改成服务器后端地址
4. 让别人直接打开前端网址

仓库里已经补好一套可直接落地的文件：

- `docker-compose.demo.yml`
- `deploy_demo.sh`
- `nginx.demo.conf.template`

Linux 服务器上的最短路径可以这样做：

```bash
cd /srv/greaterwms
bash ./deploy_demo.sh https://api-demo.yourdomain.com
```

然后：

1. 前端容器跑在 `8080`
2. 后端容器跑在 `8008`
3. 用 `nginx.demo.conf.template` 配成两个域名
4. 前端域名指向 `8080`
5. 后端域名指向 `8008`

推荐域名方式：

- `demo.yourdomain.com` -> 前端
- `api-demo.yourdomain.com` -> 后端

前端接口地址就填：

```txt
https://api-demo.yourdomain.com
```

## 当前建议

如果现在目标是“先能稳定演示给别人看”，建议顺序是：

1. 先用本地演示版确认页面和业务闭环
2. 再做公网地址或服务器部署
3. 最后再补账号权限、真实业务数据、正式环境配置
