#!/usr/bin/env python3
import requests
import json
import os
import subprocess
from jinja2 import Template
import sys

# 设置脚本工作目录为当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
sys.path.append(current_dir)

class WeChatAPI:
    def __init__(self, token_file_path):
        # 从文件中读取 access_token
        token_data = self.load_access_token_from_file(token_file_path)
        
        # 检查是否成功读取到 access_token
        if not token_data or 'access_token' not in token_data:
            raise Exception("Access token is not available in file.")
        
        self.access_token = token_data['access_token']  # 获取 access_token
        self.template_id = "YOjHbwQxdlfYqbJ1LnS1Y7CnWtdHEX9xyxn1F1aT0KE"  # 模板ID

        # 获取日期和倒计时数据
        self.dataJson = self.get_time_data()  # 调用 get_time_data() 方法获取日期信息
        print("Data from Time.py:", self.dataJson)  # 调试信息，查看从 Time.py 获取的数据

        # 获取天气数据
        self.weather_data = self.get_weather_data()
        print("Weather Data:", self.weather_data)  # 调试信息，查看从 GetWeather.py 获取的数据

    def load_access_token_from_file(self, file_path):
        """从文件中加载 access_token"""
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return None

    def get_time_data(self):
        """调用 Time.py 脚本并获取日期和倒计时数据"""
        try:
            # 使用 subprocess 调用 Time.py 脚本并捕获输出
            result = subprocess.run(['python3', 'Time.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                # 解析 Time.py 脚本输出的 JSON 数据
                output = result.stdout
                # 打印调试信息，查看 Time.py 的输出
                print("Time.py Output:", output)
                # 将输出的 JSON 数据转换为 Python 字典
                data = json.loads(output)  # 假设 Time.py 脚本返回 JSON 格式的数据
                return data
            else:
                print("Error running Time.py:", result.stderr)
                return {}
        except Exception as e:
            print(f"Error calling Time.py: {e}")
            return {}

    def get_weather_data(self):
        """调用 GetWeather.py 脚本并获取天气数据"""
        try:
            # 使用 subprocess 调用 GetWeather.py 脚本并捕获输出
            result = subprocess.run(['python3', 'GetWeather.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # 打印原始输出和错误输出，检查返回的内容
            print("Raw Output from GetWeather.py:", result.stdout)
            print("Error Output from GetWeather.py:", result.stderr)
            
            if result.returncode == 0:
                # 获取 GetWeather.py 输出的原始数据
                output = result.stdout.strip()
                print("Processed Output from GetWeather.py:", output)  # 打印处理后的输出
                
                # 尝试将输出转为 JSON 格式
                try:
                    weather_data = json.loads(output)  # 假设 GetWeather.py 返回 JSON 格式的数据
                    return weather_data
                except json.JSONDecodeError:
                    print("Failed to decode JSON from GetWeather.py output.")
                    return {}
            else:
                print("Error running GetWeather.py:", result.stderr)
                return {}
        except Exception as e:
            print(f"Error calling GetWeather.py: {e}")
            return {}


    def get_openid(self):
        """
        获取所有用户的openid
        微信公众号开发文档中可以查阅获取openid的方法
        """
        open_ids = []  # 用于存储所有的 openid
        next_openid = ''  # 用于分页的 next_openid
        
        while True:
            # 拼接 API 请求 URL，获取用户列表
            url_openid = f'https://api.weixin.qq.com/cgi-bin/user/get?access_token={self.access_token}&next_openid={next_openid}'
            
            # 发送 GET 请求
            response = requests.get(url_openid)
            data = response.json()
            
            # 打印响应数据，用于调试
            print("Fetching openid: Response data:", data)
            
            # 检查是否包含 openid 列表
            if 'data' in data and 'openid' in data['data']:
                open_ids.extend(data['data']['openid'])  # 将当前的 openid 列表添加到 open_ids 中
                
                # 获取下一个分页的 next_openid
                next_openid = data.get('next_openid', '')
                
                # 如果 next_openid 为空，表示已经没有更多用户，退出循环
                if not next_openid:
                    break
            else:
                print("Error fetching openid:", data)
                break
        
        print("All OpenIDs:", open_ids)  # 打印所有的 openid 列表
        return open_ids  # 返回所有用户的 openid 列表

    def sendmsg(self):
        """
        给所有用户发送消息
        """
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={self.access_token}"
        
        # 获取所有的 openid
        open_ids = self.get_openid()
        
        if open_ids:
            for open_id in open_ids:
                # 打印调试信息：检查从 Time.py 和 GetWeather.py 获取的数据
                print("Data to send:", self.dataJson)
                print("Weather Data to send:", self.weather_data)

                # 构建发送的数据体
                body = {
                    "touser": open_id,
                    "template_id": self.template_id,
                    "url": "https://www.baidu.com/",  # 可替换为其他链接
                    "topcolor": "#FF0000",
                    # 对应模板中的数据模板
                    "data": {
                        "time": {
                            "value": self.weather_data.get("date_together", "未知"),  # 填充今天的日期
                            "color": "#FFDEAD"
                        },
                        "weather": {
                            "value": self.weather_data.get("weather", "未知"),  # 填充天气
                            "color": "#4682B4"
                        },
                        "temperature_highest": {
                            "value": f"{self.weather_data.get('temperature_highest', 'N/A')}°C",  # 填充最高温度
                            "color": "#228B22"
                        },
                        "temperature_lowest": {
                            "value": f"{self.weather_data.get('temperature_lowest', 'N/A')}°C",  # 填充最低温度
                            "color": "#FF99CC"
                        },
                        "date_together": {
                            "value": f"{self.dataJson.get('date_together', '未知')}天",  # 填充“在一起的日期”
                            "color": "#483D8B"
                        },
                        "days_to_liao_birthday": {
                            "value": f"{self.dataJson.get('days_to_liao_birthday', 'N/A')}天",  # 填充廖斯敏的生日倒计时
                            "color": "#D8BFD8"
                        },
                        "days_to_wang_birthday": {
                            "value": f"{self.dataJson.get('days_to_wang_birthday', 'N/A')}天",  # 填充王雨辰的生日倒计时
                            "color": "#D8BFD8"
                        }
                    }
                }
                
                # 打印发送的消息体
                print("Sending message body:", json.dumps(body, ensure_ascii=False))
                
                # 将消息体转为 JSON 格式并编码为 bytes 类型
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))  
                # 发送请求
                response = requests.post(url, data=data)
                result = response.json()  # 将返回信息 JSON 解码
                print("Response from WeChat API:", result)  # 打印微信 API 返回的结果
        else:
            print("当前没有用户关注该公众号！")

# 示例：从 access_token.json 中读取 access_token 并获取 openid 列表
token_file_path = 'access_token.json'  # 存储 access_token 的文件路径
wechat_api = WeChatAPI(token_file_path)


# 给所有用户发送消息
wechat_api.sendmsg()

