# 小猿<神>
<找Hook接>口算<法和逆向反编译混淆>, 小子

## 原理
感谢
[Hawcett/XiaoYuanKouSuan_Frida_hook](https://github.com/Hawcett/XiaoYuanKouSuan_Frida_hook/).  
Hook 点, 通讯逻辑, 反反调试目标

小猿口算有一个用于加密数据的方法,
在数据传给服务端前会将数据通过此函数进行加密. 
包括您的答题时间(`costTime`)等数据.

我们帮您 Hook 了这个方法, 
以在数据被加密前, 
修改您的答题时间等数据.

## 用法
### 建议要求
- Root 过的 Android 设备
- 电脑 Python(>=3.11, with Poetry)
- Android 和 电脑 处在同一个网络之下 (电脑需要能主动连接至 Android)
- Android 终端模拟器 (有 Root 权限) (或者 ADB 和数据线)

### Configure Frida Server on your Android

在 https://github.com/frida/frida/releases.
下载 `frida-server`

本示例中使用的是
```frida-server-16.5.6-android-arm64.xz```

> [!NOTE]  
> 如果您在使用其他架构的 Android 设备, 
> 您可能需要替换 `arm64` 为设备的架构.


下载并解压 `frida-server`.  

<details>

<summary>不会解压 xz? 示例解压命令</summary>

<code>
xz --decompress frida-server-16.5.6-android-arm64.xz
</code>

</details>

将解压后的文件传输至您的 Android 设备.  
打开终端模拟器 (Termux, 或者MT管理器等),
执行以下内容:


```shell
chmod +x /data/adb/frida-server
/data/adb/frida-server -l 0.0.0.0:1145
```

修改 `/data/adb/frida-server` 到您的 `frida-server` 可执行文件的位置.
修改 `0.0.0.0:1145` 到您喜欢的监听地址.

### 克隆此仓库

```shell
git clone CyanChanges/xyks_bro
```

### 使用 Poetry 配置环境和安装依赖
```shell
cd xyks_bro
poetry install
```

### 运行我们的脚本

```shell
poetry run python -m xyks_bro <设备IP>:1145
```
替换 `<设备IP>` 为您 Android 设备的 IP 地址.
替换端口 `1145` 为您之前在 Android 设备配置的监听端口.

### 开始答题吧
当看到控制台出现类似下面的提示时，
表示 Hook 成功了.

```shell
$ poetry run python -m xyks_bro <设备IP>:1145
...
[YY-MM-DD hh:mm:ss] | SUCCESS  | __main__:sc_handler:108 | Hook success, ready to go
```

您可以开始答题, 
无论您的答题时间是多少,
我们都会将时间修改为脚本中预设的 `TIME_MS` (=100) 毫秒.
以帮助您的答题时间更加稳定.

