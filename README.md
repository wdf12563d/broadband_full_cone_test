# UDP NAT Type Tester

一个用于检测运营商CGN（运营商级NAT）外层NAT类型的工具，通过UDP穿透测试判断是否为 **Full Cone NAT（NAT1）**。

## 功能特点

- 验证 **EIM（端点独立映射）**：内网端口是否固定映射到公网端口
- 验证 **EIF（端点独立过滤）**：陌生外网IP能否主动穿透CGN
- 支持 **持续发包** 维持CGN会话
- 轻量级，仅依赖Python标准库

## 测试原理

1. Windows端绑定本地端口（如55555），持续向VPS发送UDP包
2. VPS端回显 `PONG`，确认链路通畅
3. 第三方（如手机5G）直接向公网IP:映射端口发送UDP包
4. 如果第三方数据包能被Windows监听窗口接收 → **Full Cone NAT（NAT1）**

## 文件说明

| 文件 | 用途 |
|------|------|
| `windows/nat_tester.py` | Windows端主程序（监听 + 持续发包） |
| `windows/listener.py` | Windows端简化版（仅监听） |
| `vps/vps_echo.py` | VPS端UDP回声服务器 |

## 使用方法

### 1. VPS端（云服务器）

```bash
# 上传 vps_echo.py 到VPS
python3 vps_echo.py
