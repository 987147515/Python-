#!/usr/bin/env python3
import requests
import json
import os
import time

# 设置脚本的工作目录为当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

def get_access_token(appid, appsecret):
    """获取 access_token，调用微信 API"""
    # 微信获取 access_token 的 API
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
    
    # 发送 GET 请求获取 access_token
    response = requests.get(url)
    
    # 将响应的 JSON 数据转为 Python 字典
    data = response.json()
    
    # 打印响应内容，查看是否包含 access_token 或错误信息
    print("Response data:", data)
    
    # 检查是否包含 access_token
    if 'access_token' in data:
        return data['access_token'], data['expires_in']
    else:
        # 如果没有 access_token，抛出异常并显示错误信息
        errcode = data.get('errcode', 'Unknown error code')
        errmsg = data.get('errmsg', 'No error message')
        raise Exception(f"Error getting access token: {errcode}, {errmsg}")

def save_access_token_to_file(file_path, access_token, expires_in):
    """将 access_token 保存到文件，保存获取时间"""
    token_data = {
        'access_token': access_token,
        'expires_in': expires_in,
        'created_at': int(time.time())  # 保存获取 token 的时间戳
    }
    
    with open(file_path, 'w') as file:
        json.dump(token_data, file)  # 将字典写入文件

def load_access_token_from_file(file_path):
    """从文件中加载 access_token"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return None

def get_valid_access_token(appid, appsecret, token_file_path):
    """获取有效的 access_token，首先检查文件中的 token 是否有效"""
    # 尝试从文件中加载 access_token
    token_data = load_access_token_from_file(token_file_path)
    
    if token_data:
        # 从文件中加载 access_token 和过期时间
        access_token = token_data.get('access_token')
        expires_in = token_data.get('expires_in')
        created_at = token_data.get('created_at', 0)
        
        # 检查 token 是否已经过期
        if access_token and (int(time.time()) - created_at) < expires_in:
            print("Using cached access token from file.")
            return access_token
    
    # 如果文件中没有有效的 access_token，重新获取
    print("Getting new access token.")
    access_token, expires_in = get_access_token(appid, appsecret)
    
    # 将新的 access_token 存储到文件中
    save_access_token_to_file(token_file_path, access_token, expires_in)
    
    return access_token

# 使用你的 AppID 和 AppSecret
appid = 'wxd692257721c56426'
appsecret = '138e75d2317aba96e0c2576008e75e31'
token_file_path = 'access_token.json'  # 存储 access_token 的文件路径

# 获取有效的 access_token
try:
    access_token = get_valid_access_token(appid, appsecret, token_file_path)
    print("Access Token:", access_token)
except Exception as e:
    print(str(e))
