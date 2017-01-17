# Wi-Fi Probe

基于OpenWRT系统进行Wi-Fi探针
  基本思想：利用tcpdump捕捉周围的信号帧，利用probe-request帧和null帧收集mac地址
  使用工具：WinSCP\Putty\tcpdump

流程：
  1. 进入Luci，连接网络，为设备新增加一个wlan，设置为monitor模式
  2. 进入Putty，为设备更新数据包，包括python\tcpdump\usb，详见package.sh
  3. 复制main.py至/root，处理tcpdump捕捉到的信号
  4. 更改/etc/rc.local，设置启动自动执行
  5. 重启
