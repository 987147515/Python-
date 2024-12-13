#!/usr/bin/env python3
import json
from datetime import datetime

# 直接定义日期
DATE_TOGETHER = "2024年03月10日"
LIAO_BIRTHDAY = "2001年7月31日"
WANG_BIRTHDAY = "2000年8月8日"

# 计算日期差
def calculate_days(date_str):
    """计算从给定日期到今天的天数"""
    try:
        date_obj = datetime.strptime(date_str, "%Y年%m月%d日")
        today = datetime.today()

        # 如果生日已经过去，计算明年的生日
        next_birthday = date_obj.replace(year=today.year)

        # 如果今年的生日已经过去，则计算明年
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)

        delta = next_birthday - today
        return delta.days
    except ValueError:
        print("日期格式错误，请确保格式为：YYYY年MM月DD日")
        raise

# 计算两个日期之间的天数
def calculate_days_between(date_str1, date_str2):
    """计算两个日期之间的天数"""
    try:
        date_obj1 = datetime.strptime(date_str1, "%Y年%m月%d日")
        date_obj2 = datetime.strptime(date_str2, "%Y年%m月%d日")
        delta = date_obj2 - date_obj1
        return abs(delta.days)  # 返回绝对值，确保天数差为正
    except ValueError:
        print("日期格式错误，请确保格式为：YYYY年MM月DD日")
        raise

if __name__ == "__main__":
    # 计算生日倒计时
    days_to_liao_birthday = calculate_days(LIAO_BIRTHDAY)
    days_to_wang_birthday = calculate_days(WANG_BIRTHDAY)

    # 计算2024年03月10日到今天的天数
    date_together = calculate_days_between(datetime.today().strftime("%Y年%m月%d日"), DATE_TOGETHER)

    # 打包成 data
    data = {
        "date_together": date_together,
        "days_to_liao_birthday": days_to_liao_birthday,
        "days_to_wang_birthday": days_to_wang_birthday
    }

    # 输出为 JSON 格式
    print(json.dumps(data, ensure_ascii=False))
