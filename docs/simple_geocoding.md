## Simple 지오코딩

Request
> [https://geocode-kr.gimi9.com/geocode?q=서울특별시 송파구 송파대로8길 10](https://geocode-kr.gimi9.com/geocode?q=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EC%86%A1%ED%8C%8C%EA%B5%AC%20%EC%86%A1%ED%8C%8C%EB%8C%80%EB%A1%9C8%EA%B8%B8%2010)

Response
```json
{
  "total_time": 0.007039785385131836,
  "total_count": 1,
  "success_count": 1,
  "fail_count": 0,
  "results": [
    {
      "x": 967118,
      "y": 1942008,
      "z": "05813",
      "hc": "1171064600",
      "lc": "1171010900",
      "rc": "117104169355",
      "bn": "1171010900102530005000001",
      "h1": "서울",
      "rm": "송파대로8길",
      "bm": [
        "송파파인13",
        "송파파인13",
        ""
      ],
      "success": true,
      "errmsg": "",
      "h1_cd": "11",
      "h2_cd": "11710",
      "kostat_h1_cd": "11",
      "kostat_h2_cd": "11240",
      "hash": "송파_송파대로8길_10-0",
      "address": "서울특별시 송파구 송파대로8길 10",
      "addressCls": "ROAD_ADDRESS",
      "toksString": "H1\t서울특별시\nH23\t송파구\nROAD\t송파대로8길\n건번\t10",
      "x_axis": 127.12810603742214,
      "y_axis": 37.476715383128074,
      "inputaddr": "서울특별시 송파구 송파대로8길 10"
    }
  ]
}
```
