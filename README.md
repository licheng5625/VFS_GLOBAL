# ❌❌❌❌❌❌❌❌❌❌❌❌使用人数太多导致，加强了防护，已经不可用了❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌

检查是在某个cookie里。目前没有时间去研究。

# VFS_GLOBAL 德国签证
这个帮你查看德国签证的可用时间。
你可以部署到github action自动运行，并且给你发送email。

https://lift-apicn.vfsglobal.com/master/center/deu/chn/zh-CN
可以查看相应的签证中心的代码，比如成都是`GRCG`。

```
vfs_email = os.environ.get('VFS_USER_EAMIL')
vfs_password = os.environ.get('VFS_PASSWORD')
# I just implemented gmail
gmail_sender = "your@gmail.com"
email_receiver = ["a@email.com", "b@email.com"]
#Get your gmail app password from here https://myaccount.google.com/apppasswords
gmail_password = os.environ.get('GMAIL_PWD')

#for the query, the center code you can fine here
startDate = quote("11/05/2023")
endDate = quote("07/11/2023")

#https://lift-apicn.vfsglobal.com/master/center/deu/chn/zh-CN
center = "GRCG"
```


在github action自动运行可能会遇到防火墙。你需要[openVPN](https://github.com/marketplace/actions/openvpn-connect)。
免费的代理你可以在https://www.vpngate.net/cn/ 找到。
```buildoutcfg
name: Python application

on:
  workflow_dispatch:

  schedule:
    - cron: '*/30 * * * *'

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest

    permissions:
      # Give the default GITHUB_TOKEN write permission to commit and push the
      # added or changed files to the repository.
      contents: write

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install secure-smtplib  requests pytz
    - name: Install OpenVPN
      run: |
        sudo apt update
        sudo apt install -y openvpn openvpn-systemd-resolved
    - name: Connect to VPN
      uses: "kota65535/github-openvpn-connect-action@v2"
      with:
        config_file: ./.github/workflows/client.ovpn
        #username: ${{ secrets.OVPN_USERNAME }}
        #password: ${{ secrets.OVPN_PASSWORD }}

    - id: date
      name: Get new time
      run: |
        python app.py
      env:
        VFS_PASSWORD: ${{ secrets.VFS_PASSWORD }}
        GMAIL_PWD: ${{ secrets.GMAIL }}
        VFS_USER_EAMIL: ${{ secrets.VFS_USER_EAMIL }}
```
