#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: test1.py
Time: 2024/11/29 14:32
"""
import uuid
import time
import logging
from locust import HttpUser, task, between, events

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ApiUser(HttpUser):
    # 定义请求间隔，这里使用between来设置请求之间的时间间隔范围
    wait_time = between(1, 2)  # 每次请求之间的间隔时间为 1 到 2 秒之间的随机数

    headers = {
        "Access-Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2ZXJzaW9uIjoxLCJ1c2VyX3R5cGUiOjQsImxhc3RfZXhwIjoxNzI2Njk1MDA2LCJleHAiOjE3NTgyNTk4MDYsInVzZXJfaWQiOiJkaWdpdGFsIiwidXNlcl9uYW1lIjoiXHU2NTcwXHU1YjU3XHU0ZWJhIiwic291cmNlIjowfQ.9OmhXG4-7kMRTN8s2_lXfWNCGiuS5VoOggXNjwNAlTI"
    }

    @task
    def test_non_streaming_api(self):
        question = "11月27号的新闻联播说了什么"
        now_id = str(uuid.uuid4()) + "-tiantest"
        body = {
            "chat_id": now_id,
            "group_id": now_id,
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        # 发起请求
        with self.client.post("/dwcorpculture/digital/voice", json=body, headers=self.headers) as response:
            # 记录响应时间
            response_time = response.elapsed.total_seconds()
            logging.info(
                f"UUID: {now_id}, Question: {question}, Response Time: {response_time:.2f}s, Status Code: {response.status_code}")

            if response.status_code != 200:
                logging.error(f"Request failed, status code: {response.status_code}")

            return response_time


# 压测结果统计回调函数
@events.request.add_listener
def log_request_stats(request_type, name, response_time, response, exception, **kwargs):
    if response is not None:
        logging.info(f"Request: {name}, Response Time: {response_time}ms, Status Code: {response.status_code}")
    else:
        logging.error(f"Request failed, Exception: {exception}")


# 运行压力测试
if __name__ == "__main__":
    # 启动 Locust 测试
    import os

    os.system("locust -f test1.py")
