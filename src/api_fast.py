# -*- coding: utf-8 -*-
"""
This module provides a FastAPI-based HTTP server for geocoding and reverse geocoding operations.

__author__ = "gisman@gmail.com"

Usage:

Endpoints:
    - GET /: Returns a welcome HTML page with links to API documentation, source code, and an online demo.
    - GET /geocode: Geocodes a single address or multiple addresses provided as a newline-separated string.
    - GET /reverse_geocode: Reverse geocodes a given x and y coordinate.
    - POST /batch_geocode: Geocodes multiple addresses provided in a JSON payload.

Classes:
    - Batch_Geocode_Item: Pydantic model for batch geocoding input.
    - ApiHandler: Handles geocoding and reverse geocoding operations using RocksDB.

Attributes:
    APP_NAME (str): Name of the application.
    VERSION (float): Version of the application.
    DEFAULT_PORT (int): Default port for the server.
    LINES_LIMIT (int): Maximum number of lines for batch geocoding.
    X_AXIS (str): Key for x-axis coordinate in the response.
    Y_AXIS (str): Key for y-axis coordinate in the response.

Functions:
    - read_root: Returns a static HTML page with links to API documentation, source code, and an online demo.
    - geocode: Geocodes a single address or multiple addresses.
    - reverse_geocode: Reverse geocodes a given x and y coordinate.
    - batch_geocode: Geocodes multiple addresses provided in a JSON payload.

Main Execution:
    - Configures logging.
    - Runs the FastAPI server using Uvicorn.

Geocode API HTTP Server 
Usage:
    ./api_fast.py [<port>]
"""

import time
import logging
import os
import rocksdb3
from pyproj import Transformer, CRS

from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import uvicorn

from geocoder.Geocoder import Geocoder
from geocoder.ReverseGeocoder import ReverseGeocoder
from geocoder.db.rocksdb import RocksDbGeocode
import sys

APP_NAME = "Geocode API Server"
VERSION = 0.2
DEFAULT_PORT = 4002
LINES_LIMIT = 3000

X_AXIS = "x_axis"
Y_AXIS = "y_axis"

app = FastAPI()
router = APIRouter()


@app.get("/")
async def read_root():
    """
    Asynchronous function to handle the root endpoint of the Geocode API Server.
    Returns:
        HTMLResponse: A static HTML response containing a welcome message,
        a link to the API documentation, a link to the source code on GitHub,
        and a link to an online demo.
    """

    return HTMLResponse(
        content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Geocode API Server</title>
    </head>
    <body>
        <h1>Welcome to the Geocode API Server</h1>
        <p>For API documentation, visit <a href="/docs">/docs</a></p>
        <p>Source Code: <a href="https://github.com/gisman/geocoder-kr">Github</a></p>
        <p>Online Demo: <a href="https://geocode.gimi9.com/">geocode.gimi9.com</a></p>
    </body>
    </html>
    """
    )


@router.get("/geocode")
async def geocode(q: str):
    """
    Geocodes a given query string.

    Args:
        q (str): A string containing addresses separated by newline characters.

    Returns:
        JSONResponse: A JSON response containing the geocoded addresses.
    """
    addrs = q.split("\n")
    summary = ApiHandler().geocode(addrs)
    return JSONResponse(content=summary)


@router.get("/reverse_geocode")
async def reverse_geocode(x: float, y: float):
    """
    Asynchronously performs reverse geocoding for the given coordinates.

    Args:
        x (float): The longitude of the location to reverse geocode.
        y (float): The latitude of the location to reverse geocode.

    Returns:
        JSONResponse: A JSON response containing the reverse geocoding result.
    """
    val = ApiHandler().reverse_geocode(x, y)
    return JSONResponse(content=val)


class Batch_Geocode_Item(BaseModel):
    """
    Batch_Geocode_Item is a Pydantic model representing a batch geocode request item.

    Attributes:
        q (list[str]): A list of query strings to be geocoded.
    """

    q: list[str]


@router.post("/batch_geocode")
async def batch_geocode(data: Batch_Geocode_Item):
    """
    Geocode multiple addresses asynchronously.

    Args:
        data (Batch_Geocode_Item): An object containing a list of addresses to be geocoded.

    Raises:
        HTTPException: If the input data is invalid (i.e., the list of addresses is empty).

    Returns:
        JSONResponse: A JSON response containing the geocoding summary for the provided addresses.
    """
    # multi addresses geocode
    addrs = data.q
    if not addrs:
        raise HTTPException(status_code=400, detail="Invalid input")
    summary = ApiHandler().geocode(addrs)
    return JSONResponse(content=summary)


# app에 router를 추가
app.include_router(router)


class ApiHandler:
    """
    ApiHandler class provides methods for geocoding and reverse geocoding using RocksDB.

    Attributes:
        geocoder (Geocoder): An instance of Geocoder initialized with RocksDbGeocode.
        reverse_geocoder (ReverseGeocoder): An instance of ReverseGeocoder initialized with RocksDB.
        tf (Transformer): A Transformer object for converting coordinates between EPSG:5179 and EPSG:4326.

    Methods:
        read_key(key):
            Reads a value from the geocoder database using the provided key.

        reverse_geocode(x: float, y: float):
            Performs reverse geocoding for the given coordinates (x, y).

        geocode(addrs):
            Performs geocoding for a list of addresses and returns a summary of the results.
    """

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
        """
        Perform reverse geocoding to find the address corresponding to the given coordinates.

        Args:
            x (float): The longitude of the location to reverse geocode.
            y (float): The latitude of the location to reverse geocode.

        Returns:
            dict: The address information corresponding to the given coordinates.

        Logs:
            Execution time for the reverse geocoding process.
        """
        start_time = time.time()  # 시작 시간 측정

        val = self.reverse_geocoder.search(x, y)

        elapsed_time = time.time() - start_time  # 소요 시간 계산

        # 소요 시간을 로그에 기록
        logging.debug(
            f"Execution time for reverse_geocode({x}, {y}): {elapsed_time:.6f} seconds"
        )

        return val

    def geocode(self, addrs):
        """
        Geocode a list of addresses.

        Args:
            addrs (list): A list of addresses to geocode.

        Returns:
            dict: A summary dictionary containing:
                - total_time (float): The total time taken to geocode the addresses.
                - total_count (int): The total number of addresses processed.
                - success_count (int): The number of successfully geocoded addresses.
                - fail_count (int): The number of addresses that failed to geocode.
                - results (list): A list of dictionaries containing the geocoding results for each address.
                    Each dictionary includes:
                    - inputaddr (str): The input address.
                    - success (bool): Whether the geocoding was successful.
                    - x (float, optional): The x-coordinate of the geocoded address.
                    - y (float, optional): The y-coordinate of the geocoded address.
                    - X_AXIS (float, optional): The transformed x-coordinate.
                    - Y_AXIS (float, optional): The transformed y-coordinate.
        """
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


if __name__ == "__main__":
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

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = DEFAULT_PORT

    uvicorn.run(app, host="0.0.0.0", port=port)

    logging.info(f"Stopping {APP_NAME}...\n")
