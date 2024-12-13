#!/usr/bin/env python3
import requests
import datetime
from bs4 import BeautifulSoup
import json

def get_weather():
    """
    获取天气信息
    """
    url = 'https://www.weather.com.cn/weather/101020100.shtml'  # 昆明天气网站
    sysdate = datetime.date.today()

    try:
        r = requests.get(url, timeout=30)  # 用requests抓取网页
        r.raise_for_status()  # 异常时停止
        r.encoding = r.apparent_encoding  # 编码格式
        html = r.text
        #print("网页请求成功，开始解析HTML内容。")  # 调试输出
    except Exception as e:
        return {"error": f"无法获取天气信息: {e}"}

    final_list = []
    soup = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup库解析网页
    body = soup.body  # 从soup里截取body的一部分
    data = body.find('div', {'id': '7d'})  # 找到 id = 7d 的标签
    
    if not data:
        return {"error": "未找到天气信息，请检查网页结构。"}

    # 调试输出，确认是否能找到数据块
    #print("找到天气数据块。")

    ul = data.find('ul')  # 用find方法找ul标签
    if not ul:
        return {"error": "未找到天气列表，请检查网页结构。"}
    
    # 调试输出，确认是否能找到天气列表
    #print("找到天气列表。")

    lis = ul.find_all('li')  # 找到ul中的li标签，也就是列表，其中存放着日期、天气、风力等信息
    
    for day in lis:
        temp_list = []
        date = day.find('h1').string  # 找到日期
        if str(sysdate.day) in date:  # 判断日期是否为今天
            temp_list.append(date)  # 添加日期
            
            info = day.find_all('p')  # 找到所有的p标签
            temp_list.append(info[0].string if info else "未知天气")  # 天气情况
            
            # 最高温度
            temperature_highest = (
                info[1].find('span').string.replace('℃', ' ') 
                if info[1].find('span') else "未知"
            )
            # 最低温度
            temperature_lowest = (
                info[1].find('i').string.replace('℃', ' ') 
                if info[1].find('i') else "未知"
            )
            
            temp_list.append(temperature_highest)  # 添加最高气温
            temp_list.append(temperature_lowest)  # 添加最低气温
            
            final_list.append(temp_list)  # 添加到最终列表

            # 打包返回数据
            data = {
                "date_together": sysdate.strftime('%Y年%m月%d日'),  # 当前日期
                "weather": final_list[0][1],  # 天气情况
                "temperature_highest": final_list[0][2].strip(),  # 最高气温
                "temperature_lowest": final_list[0][3].strip(),  # 最低气温
            }
            #print("返回的数据：", data)  # 调试输出
            return data

    return {"error": "未找到今天的天气信息。"}

# 调用函数并输出结果
if __name__ == "__main__":
      # 获取天气数据并输出字典
    data = get_weather()  # 调用 get_weather 而非 get_weather_data
    # 直接输出字典
    print(json.dumps(data, ensure_ascii=False))  # 打印返回的数据
