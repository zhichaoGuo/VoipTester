# VoipTester
一个用于测试VOIP话机的工具lib

## 功能需求
1. 与且仅与一个ip进行模拟的sip信令交互，此ip为待测设备的ip【remote_ip】
2. 接收且仅接收待测设备一个sip端口的信令【remote_port】
3. 建立rtp的回环播放
4. 实现rtp种类的识别与应答（默认使用第一种编解码）

## 设计文档
### 流程控制
    dut ---->   VoipTester  ---->   dut
                    
    buf ---->   SipMessage
                    ↓   
                SipCall     ---->   buf


                
    
