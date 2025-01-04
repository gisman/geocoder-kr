## 여러 개의 주소 지오코딩

여러 주소를 한 번에 지오코딩하는 방법은 간단합니다. 각 주소를 배열에 넣고 POST로 요청하세요.

### curl 예

```bash
curl -X 'POST' \
  'https://geocode-kr.gimi9.com/batch_geocode' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "q": [
    "서울특별시 송파구 송파대로8길 10",
    "서울특별시 송파구 양재대로72길 20",
    "서울특별시 구로구 고척로21나길 85-6",
    "서울특별시 노원구 월계로53길 21",
    "서울특별시 서초구 바우뫼로 91"
  ]
}'
```

### python 예

```python
import requests

url = 'https://geocode-kr.gimi9.com/batch_geocode'
headers = {
  'accept': 'application/json',
}
data = {
  "q": [
    "서울특별시 송파구 송파대로8길 10",
    "서울특별시 송파구 양재대로72길 20",
    "서울특별시 구로구 고척로21나길 85-6",
    "서울특별시 노원구 월계로53길 21",
    "서울특별시 서초구 바우뫼로 91"
  ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### javascript 예

```javascript
const axios = require('axios');

const url = 'https://geocode-kr.gimi9.com/batch_geocode';
const headers = {
  'accept': 'application/json',
};
const data = {
  q: [
    "서울특별시 송파구 송파대로8길 10",
    "서울특별시 송파구 양재대로72길 20",
    "서울특별시 구로구 고척로21나길 85-6",
    "서울특별시 노원구 월계로53길 21",
    "서울특별시 서초구 바우뫼로 91"
  ]
};

axios.post(url, data, { headers })
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### Response

```json
{
  "total_time": 0.008105278015136719,
  "total_count": 5,
  "success_count": 5,
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
    },
생략...
  ]
}
```
