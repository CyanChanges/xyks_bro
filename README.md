# 小猿<神>
<找Hook接>口算<法和逆向反编译混淆>, 小子

[中文README](./README_cn.md)

## How
Inspired by
[Hawcett/XiaoYuanKouSuan_Frida_hook](https://github.com/Hawcett/XiaoYuanKouSuan_Frida_hook/).  
Thanks for hook point, some logic and anti-debug target.

There is a method that do encryption to data.  
Which the score and time costs are pass to this method
before it goes to the server.  

We hook the method, 
and modify the cost time right before it goes to the method
and get encrypted.

## Usage
### Requirements
- A Rooted Android
- A Linux Computer with Python(>=3.11, with Poetry)
- In Same Network
- An Android Terminal emulator (with Root-access) (else, ADB(`adb root` or have `su`) & Data Cable)

### Configure Frida Server on your Android

Download `frida-server` from 
https://github.com/frida/frida/releases.

In my case, it is
```frida-server-16.5.6-android-arm64.xz```

> [!NOTE]  
> If you're using a Android with different architecture, 
> you may need replace `arm64` with your architecture.


Download and decompress the `frida-server`.  

<details>

<summary>Example decompress command</summary>

<code>
xz --decompress frida-server-16.5.6-android-arm64.xz
</code>

</details>

Move the file to your Android.  
Open a Terminal (with Termux, or MT File Manager, etc.),
Run:
```shell
chmod +x /data/adb/frida-server
/data/adb/frida-server -l 0.0.0.0:1145
```
May use your `frida-server` path instead of `/data/adb/frida-server`,
Change `0.0.0.0:1145` with your host and port.

### Clone the repository

```shell
git clone CyanChanges/xyks_bro
```

### Install the dependencies
```shell
cd xyks_bro
poetry install
```

### Run the script

```shell
poetry run python -m xyks_bro <your-phone-ip>:1145
```
Replace `<your-phone-ip>` with yours,
Replace `1145` with your port set before.
