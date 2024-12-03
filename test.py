#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: test.py
Time: 2024/11/29 13:00
"""
import logging
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import uuid
import random

# 配置日志
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


# 请求非流式接口的函数
# def test_non_streaming_api(url, question, stream: bool):
#     headers = {
#         "Access-Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2ZXJzaW9uIjoxLCJ1c2VyX3R5cGUiOjQsImxhc3RfZXhwIjoxNzI2Njk1MDA2LCJleHAiOjE3NTgyNTk4MDYsInVzZXJfaWQiOiJkaWdpdGFsIiwidXNlcl9uYW1lIjoiXHU2NTcwXHU1YjU3XHU0ZWJhIiwic291cmNlIjowfQ.9OmhXG4-7kMRTN8s2_lXfWNCGiuS5VoOggXNjwNAlTI"
#     }
#
#     now_id = str(uuid.uuid4()) + "-tiantest"
#     body = {
#         "chat_id": now_id,
#         "group_id": now_id,
#         "stream": True,
#         "messages": [
#             {
#                 "role": "user",
#                 "content": question
#             }
#         ]
#     }
#
#     try:
#         start_time = time.time()
#         resp = requests.post(url, headers=headers, json=body)
#         end_time = time.time()
#
#         resp.raise_for_status()  # 如果返回状态码不是2xx会抛出异常
#         logging.info(
#             f"UUID: {now_id}, Question: {question}, Response Time: {end_time - start_time:.2f} seconds, Response: {resp.text}")
#         return end_time - start_time  # 返回响应时间
#
#     except requests.RequestException as e:
#         logging.error(f"Request failed for UUID {now_id}, Error: {e}")
#         return None


def test_non_streaming_api_stream(url, question):
    headers = {
        "Access-Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2ZXJzaW9uIjoxLCJ1c2VyX3R5cGUiOjQsImxhc3RfZXhwIjoxNzI2Njk1MDA2LCJleHAiOjE3NTgyNTk4MDYsInVzZXJfaWQiOiJkaWdpdGFsIiwidXNlcl9uYW1lIjoiXHU2NTcwXHU1YjU3XHU0ZWJhIiwic291cmNlIjowfQ.9OmhXG4-7kMRTN8s2_lXfWNCGiuS5VoOggXNjwNAlTI"
    }

    now_id = str(uuid.uuid4()) + "-tzc-tian"
    body = {
        "chat_id": now_id,
        "group_id": now_id,
        "stream": True,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }

    try:
        start_time = time.time()

        # 设置 stream=True 以支持流式响应
        resp = requests.post(url, headers=headers, json=body, stream=True)

        # 逐块读取流式响应
        response_text = ""
        for chunk in resp.iter_content(chunk_size=1024):  # 每次读取 1024 字节
            if chunk:
                response_text += chunk.decode("utf-8")
                # 你可以在这里根据需要做进一步的处理，比如实时打印流数据

        end_time = time.time()

        resp.raise_for_status()  # 如果返回状态码不是2xx会抛出异常
        logging.info(
            f"UUID: {now_id}, Question: {question}, Response Time: {end_time - start_time:.2f} seconds, Response: {response_text}")

        return end_time - start_time  # 返回响应时间

    except requests.RequestException as e:
        logging.error(f"Request failed for UUID {now_id}, Error: {e}")
        return None

# 压测函数
def pressure_test_non_streaming_api(url, questions, concurrency):
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(test_non_streaming_api_stream, url, question) for question in questions]
        start_time = time.time()
        total_requests = 0
        total_failures = 0
        total_response_time = 0

        for future in futures:
            response_time = future.result()  # 阻塞，等待每个请求的完成
            if response_time is not None:
                total_requests += 1
                total_response_time += response_time
            else:
                total_failures += 1

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Pressure Test Completed. Total Time: {total_time:.2f} seconds")
        print(f"Total Requests: {total_requests}, Failed Requests: {total_failures}")
        print(f"Average Response Time: {total_response_time / total_requests if total_requests > 0 else 0:.2f} seconds")
        print(f"Throughput: {total_requests / total_time:.2f} requests per second")


if __name__ == "__main__":
    url = "http://10.141.103.12:8002/dwcorpculture/digital/voice"

    # 一批问题
    questions = [
        "11月27号的新闻联播说了什么",
        "近一个月有哪些证券公司被处罚了",
        "联网检索一下最近一周国际上有什么重要的金融政策",
        "分析一下平安银行的股价",
        "发改委最新提到的稳增长措施是什么",
        "数字经济的发展将如何影响传统行业",
        "国务院 9 月份出台什么政策",
        "11月27号的新闻联播说了什么",
        "近一个月有哪些证券公司被处罚了",
        "联网检索一下最近一周国际上有什么重要的金融政策",
        "分析一下平安银行的股价",
        "发改委最新提到的稳增长措施是什么",
        "数字经济的发展将如何影响传统行业",
        "国务院 9 月份出台什么政策",
        "11月27号的新闻联播说了什么",
        "近一个月有哪些证券公司被处罚了",
        "联网检索一下最近一周国际上有什么重要的金融政策",
        "分析一下平安银行的股价",
        "发改委最新提到的稳增长措施是什么",
        "数字经济的发展将如何影响传统行业",
        "国务院 9 月份出台什么政策"
    ]

    pressure_test_non_streaming_api(url, questions, concurrency=50)


