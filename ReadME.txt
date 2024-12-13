GetAccessToken.py 
功能：获取微信的 access_token，并将其保存到 access_token.json 中。
定时任务：该脚本需要每小时运行一次，确保 access_token 始终有效。


GetWeather.py
功能：抓取并解析上海某天气网站的天气数据，返回当天的天气、最高温度、最低温度等信息。
返回格式：返回一个字典，包含当前日期、天气、最高温度和最低温度。

SendALL.py
功能：通过微信 API 向所有用户发送模板消息，包含天气信息、日期和倒计时。
依赖：依赖 GetAccessToken.py 获取 access_token，依赖 GetWeather.py 获取天气数据，依赖 Time.py 获取日期倒计时数据。

Time.py
功能：计算并返回特定日期（如纪念日）到今天的天数，以及一些倒计时信息（如生日倒计时）。


access_token.json
功能：存储微信的 access_token。由 GetAccessToken.py 脚本更新。

wechat_verify.php
功能：用于微信公众平台验证服务器的有效性。可用于接入微信接口时的服务器验证。

History 调试文件
