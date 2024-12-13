<?php
// 定义你自己的 Token
define('TOKEN', 'YuchenHandle123');  // 这里替换为你自己的 Token

// 检查微信服务器发来的请求是否有效
function checkSignature()
{
    // 获取微信请求传递的参数
    $signature = $_GET["signature"];
    $timestamp = $_GET["timestamp"];
    $nonce = $_GET["nonce"];
    $echostr = $_GET["echostr"];

    // 将token、timestamp、nonce三个参数放入数组中
    $tmpArr = array(TOKEN, $timestamp, $nonce);

    // 对数组进行字典序排序
    sort($tmpArr, SORT_STRING);

    // 将排序后的数组元素拼接成一个字符串
    $tmpStr = implode($tmpArr);

    // 对拼接后的字符串进行sha1加密
    $tmpStr = sha1($tmpStr);

    // 比较加密结果与传递过来的signature是否一致
    if ($tmpStr == $signature) {
        // 校验成功，返回echostr参数内容
        echo $echostr;
    } else {
        // 校验失败
        echo "failed";
    }
}

// 调用checkSignature函数
checkSignature();
?>
