# -*- coding: utf-8 -*-
"""
Geocode API HTTP Server 
Usage::
    ./api.py [<port>]
"""

import time

from http.server import (
    BaseHTTPRequestHandler,
    ThreadingHTTPServer,
    SimpleHTTPRequestHandler,
    HTTPServer,
)
import logging
from markupsafe import escape
import os

from geocoder.Geocoder import Geocoder
from geocoder.ReverseGeocoder import ReverseGeocoder

from geocoder.db.rocksdb import RocksDbGeocode

import json

import rocksdb3
from pyproj import Transformer, CRS
from urllib.parse import urlparse, unquote, unquote_plus, parse_qs

APP_NAME = "Geocode API Server"
VERSION = 0.1
DEFAULT_PORT = 4001

LINES_LIMIT = 3000

X_AXIS = "x_axis"
Y_AXIS = "y_axis"


class ApiHandler(SimpleHTTPRequestHandler):

    # rocks db
    geocoder = Geocoder(RocksDbGeocode("db/rocks", create_if_missing=True))

    reverse_geocoder = ReverseGeocoder(
        rocksdb3.open_default(
            "db/rocks-reverse-geocoder",
        )
    )

    tf = Transformer.from_crs(
        CRS.from_string("EPSG:5179"), CRS.from_string("EPSG:4326"), always_xy=True
    )

    def read_key(self, key):
        val = ApiHandler.geocoder.db.get(key)
        return val

    def reverse_geocode(self, x: float, y: float):
        start_time = time.time()  # 시작 시간 측정

        val = self.reverse_geocoder.search(x, y)

        elapsed_time = time.time() - start_time  # 소요 시간 계산

        # 소요 시간을 로그에 기록
        logging.debug(
            f"Execution time for reverse_geocode({x}, {y}): {elapsed_time:.6f} seconds"
        )

        return val

    def geocode(self, addrs):
        summary = {}
        result = []
        count = 0
        success_count = 0
        fail_count = 0
        start_time = time.time()

        for addr in addrs[:LINES_LIMIT]:
            count += 1
            val = ApiHandler.geocoder.search(addr)
            if not val:
                val = {}
                fail_count += 1
            elif val["success"]:
                if val["x"]:
                    x1, y1 = ApiHandler.tf.transform(val["x"], val["y"])
                    val[X_AXIS] = x1
                    val[Y_AXIS] = y1
                    success_count += 1
                else:
                    fail_count += 1

            val["inputaddr"] = addr
            result.append(val)

        summary["total_time"] = time.time() - start_time
        summary["total_count"] = count
        summary["success_count"] = success_count
        fail_count = count - success_count
        summary["fail_count"] = fail_count
        summary["results"] = result

        return summary

    def do_GET(self):
        # favicon.ico
        if self.path == "/favicon.ico":
            return None

        parsed_path = urlparse(self.path)

        # if params has 'key' key
        # search key and return value
        if parsed_path.query.find("key") > -1:
            key = parsed_path.query.split("=")[1]

            val = self.read_key(key)
            self.send_response(200)  # 응답코드
            self.end_headers()  # 헤더와 본문을 구분
            self.wfile.write(val)
            return

        qs = parse_qs(parsed_path.query)
        if "x" in qs and "y" in qs:
            x = float(qs["x"][0])
            y = float(qs["y"][0])
            val = self.reverse_geocode(x, y)

            self.send_response(200)  # 응답코드
            self.end_headers()  # 헤더와 본문을 구분
            self.wfile.write(json.dumps(val).encode("utf-8"))
            return

        # run geocode and return result
        if parsed_path.query.find("q") > -1:
            q = unquote(parsed_path.query.split("=")[1])
            addrs = q.split("\n")
            summary = self.geocode(addrs)

            self.send_response(200)  # 응답코드
            self.end_headers()  # 헤더와 본문을 구분
            self.wfile.write(json.dumps(summary).encode("utf-8"))
            return

    def do_POST(self):
        """
        HTTP POST 요청을 처리합니다.

        이 메소드는 서버가 POST 요청을 받았을 때 호출됩니다. 요청 데이터를 읽고, 요청 경로에 따라 지오코딩을 수행하고, 지오코딩 결과를 JSON 응답으로 보냅니다.

        - q: 지오코딩할 주소의 개행으로 구분된 목록.

        반환값:
        - 지오코딩 결과를 포함하는 JSON 응답.
        """
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        response_code = 200

        # multi addr geocode
        q = unquote_plus(post_data.split("=")[1])
        addrs = q.split("\n")
        summary = self.geocode(addrs)

        self.send_response(response_code)  # 응답코드
        self.end_headers()  # 헤더와 본문을 구분
        self.wfile.write(json.dumps(summary).encode("utf-8"))


def run(server_class=ThreadingHTTPServer, handler_class=ApiHandler, port=DEFAULT_PORT):
    LOG_PATH = f"{os.getcwd()}/log/geocode-api.log"
    print(f"logging to {LOG_PATH}")

    # 로그 설정
    logging.basicConfig(
        filename=LOG_PATH,
        encoding="utf-8",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        force=True,
    )

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting {APP_NAME}...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info(f"Stopping {APP_NAME}...\n")


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        # profiler.run(run(port=int(argv[1])))
        run(port=int(argv[1]))

    else:
        # profiler.run(run())
        run()
