[온라인 데모!](https://geocode.gimi9.com/) | [리버스 지오코딩에 대해 아시나요?](https://gimi9.com/blog/reverse-geocoding/)

간편하게 설치할 수 있고 리소스 사용이 적으면서도 초고속 성능을 제공하는 셀프 호스팅 가능한 오픈소스 지오코딩 및 리버스 지오코딩 API.

![지오코딩](https://github.com/user-attachments/assets/24df3aed-37d4-4c02-8569-42ee471551b9)

# 지오코딩 API 예시

## Simple 지오코딩

Request
> http://localhost:4001/api?q=서울특별시 송파구 송파대로8길 10

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


## 여러 개의 주소 지오코딩

여러 주소를 한 번에 지오코딩하는 방법은 간단합니다. 각 주소를 줄바꿈 문자로 구분하세요.

### python 예

```python
import requests

url = 'http://localhost:4001/api/'
headers = {
  'Accept': '*/*',
  'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Pragma': 'no-cache',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest'
}
data = {
  'q': '서울특별시 송파구 송파대로8길 10\n서울특별시 송파구 양재대로72길 20\n서울특별시 구로구 고척로21나길 85-6\n서울특별시 노원구 월계로53길 21\n서울특별시 서초구 바우뫼로 91'
}

response = requests.post(url, headers=headers, data=data)
print(response.json())
```

### javascript 예

```javascript
const xhr = new XMLHttpRequest();
const url = 'http://localhost:4001/api/';
const data = 'q=서울특별시 송파구 송파대로8길 10\n서울특별시 송파구 양재대로72길 20\n서울특별시 구로구 고척로21나길 85-6\n서울특별시 노원구 월계로53길 21\n서울특별시 서초구 바우뫼로 91';

xhr.open('POST', url, true);
xhr.setRequestHeader('Accept', '*/*');
xhr.setRequestHeader('Accept-Language', 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7');
xhr.setRequestHeader('Cache-Control', 'no-cache');
xhr.setRequestHeader('Connection', 'keep-alive');
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
xhr.setRequestHeader('Pragma', 'no-cache');
xhr.setRequestHeader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36');
xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

xhr.onreadystatechange = function () {
  if (xhr.readyState === XMLHttpRequest.DONE) {
    if (xhr.status === 200) {
      console.log(JSON.parse(xhr.responseText));
    } else {
      console.error('Error:', xhr.statusText);
    }
  }
};

xhr.send(data);
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
    {
      "x": 967186,
      "y": 1945578,
      "z": "05656",
      "hc": "1171057000",
      "lc": "1171011200",
      "rc": "117104169373",
      "bn": "1171011200100200002015225",
      "h1": "서울",
      "rm": "양재대로72길",
      "bm": [
        "현대백조",
        "현대백조",
        ""
      ],
      "success": true,
      "errmsg": "",
      "h1_cd": "11",
      "h2_cd": "11710",
      "kostat_h1_cd": "11",
      "kostat_h2_cd": "11240",
      "hash": "송파_양재대로72길_20-0",
      "address": "서울특별시 송파구 양재대로72길 20",
      "addressCls": "ROAD_ADDRESS",
      "toksString": "H1\t서울특별시\nH23\t송파구\nROAD\t양재대로72길\n건번\t20",
      "x_axis": 127.12871584694417,
      "y_axis": 37.5088959535705,
      "inputaddr": "서울특별시 송파구 양재대로72길 20"
    },
    {
      "x": 941720,
      "y": 1944837,
      "z": "08250",
      "hc": "1153074000",
      "lc": "1153010700",
      "rc": "115304148138",
      "bn": "1153010700100470001010403",
      "h1": "서울",
      "rm": "고척로21나길",
      "bm": [
        "건영",
        "건영",
        ""
      ],
      "success": true,
      "errmsg": "",
      "h1_cd": "11",
      "h2_cd": "11530",
      "kostat_h1_cd": "11",
      "kostat_h2_cd": "11170",
      "hash": "구로_고척로21나길_85-6",
      "address": "서울특별시 구로구 고척로21나길 85-6",
      "addressCls": "ROAD_ADDRESS",
      "toksString": "H1\t서울특별시\nH23\t구로구\nROAD\t고척로21나길\n건번\t85-6",
      "x_axis": 126.84064530819364,
      "y_axis": 37.5009601916592,
      "inputaddr": "서울특별시 구로구 고척로21나길 85-6"
    },
    {
      "x": 961048,
      "y": 1959236,
      "z": "01867",
      "hc": "1135057000",
      "lc": "1135010200",
      "rc": "113504130335",
      "bn": "1135010200102760031018659",
      "h1": "서울",
      "rm": "월계로53길",
      "bm": [
        "동원베네스트",
        ""
      ],
      "success": true,
      "errmsg": "",
      "h1_cd": "11",
      "h2_cd": "11350",
      "kostat_h1_cd": "11",
      "kostat_h2_cd": "11110",
      "hash": "노원_월계로53길_21-0",
      "address": "서울특별시 노원구 월계로53길 21",
      "addressCls": "ROAD_ADDRESS",
      "toksString": "H1\t서울특별시\nH23\t노원구\nROAD\t월계로53길\n건번\t21",
      "x_axis": 127.0585412803165,
      "y_axis": 37.63176077853112,
      "inputaddr": "서울특별시 노원구 월계로53길 21"
    },
    {
      "x": 958515,
      "y": 1941900,
      "z": "06751",
      "hc": "1165065100",
      "lc": "1165010200",
      "rc": "116503121009",
      "bn": "1165010200101480003005849",
      "h1": "서울",
      "rm": "바우뫼로",
      "bm": [
        "우성",
        "우성",
        ""
      ],
      "success": true,
      "errmsg": "",
      "h1_cd": "11",
      "h2_cd": "11650",
      "kostat_h1_cd": "11",
      "kostat_h2_cd": "11220",
      "hash": "서초_바우뫼로_91-0",
      "address": "서울특별시 서초구 바우뫼로 91",
      "addressCls": "ROAD_ADDRESS",
      "toksString": "H1\t서울특별시\nH23\t서초구\nROAD\t바우뫼로\n건번\t91",
      "x_axis": 127.03081525069099,
      "y_axis": 37.47539563638899,
      "inputaddr": "서울특별시 서초구 바우뫼로 91"
    }
  ]
}
```

## 리버스 지오코딩

좌표(위도와 경도)에 해당하는 주소를 찾습니다.

### Request

> http://localhost:4001/api/reverse_geocode/?x=127.12771948485866&y=37.47699735340699

### Response

```json
{
"PNU": "1171010900108390005",
"yyyymm": "202404",
"address": "서울특별시 송파구 장지동 839-5번지",
"success": true,
"geom": "POLYGON ((127.127924 37.476489, 127.127981 37.476459, 127.127644 37.476489, 127.127639 37.476490, 127.127685 37.476530, 127.127651 37.476725, 127.127651 37.476726, 127.127613 37.476939, 127.127612 37.476946, 127.127607 37.476976, 127.127584 37.477093, 127.127569 37.477158, 127.127557 37.477209, 127.127525 37.477325, 127.127511 37.477371, 127.127510 37.477375, 127.127490 37.477440, 127.127449 37.477554, 127.127438 37.477583, 127.127435 37.477590, 127.127405 37.477667, 127.127356 37.477778, 127.127349 37.477794, 127.127351 37.477794, 127.127351 37.477794, 127.127313 37.477872, 127.127279 37.477941, 127.127186 37.478126, 127.127133 37.478232, 127.127097 37.478309, 127.127081 37.478346, 127.127051 37.478415, 127.127016 37.478499, 127.126984 37.478585, 127.126954 37.478673, 127.126929 37.478752, 127.126923 37.478768, 127.126898 37.478856, 127.126875 37.478944, 127.126852 37.479042, 127.126821 37.479206, 127.126785 37.479442, 127.126692 37.479489, 127.127058 37.479583, 127.127005 37.479503, 127.127033 37.479300, 127.127047 37.479210, 127.127059 37.479147, 127.127071 37.479088, 127.127085 37.479023, 127.127100 37.478961, 127.127117 37.478899, 127.127134 37.478838, 127.127152 37.478777, 127.127173 37.478715, 127.127193 37.478655, 127.127216 37.478594, 127.127239 37.478534, 127.127268 37.478466, 127.127298 37.478398, 127.127331 37.478328, 127.127446 37.478168, 127.127571 37.477916, 127.127598 37.477781, 127.127645 37.477667, 127.127709 37.477494, 127.127839 37.477158, 127.127877 37.476951, 127.127862 37.476840, 127.127914 37.476550, 127.127924 37.476489))",
"errmsg": ""
}
```

## 설치

간단한 설치. DBMS 필요 없음

```sh
git clone https://github.com/your-repo/geocoder-kr.git
cd geocoder-kr
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 데이터 다운로드

[Geocoding 데이터 다운로드](https://geocode.gimi9.com/static/download/rocks.tar.gz)

[Reverse Geocoding 데이터 다운로드](https://geocode.gimi9.com/static/download/rocks-reverse-geocoder.tar.gz)

다운로드한 파일을 설치 디렉토리에 다음과 같이 복사하세요.

```bash
 📂 db                                       [13GB]
    ├── 📂 rocks                             [4GB 276개의 파일] 지오코딩
    │   ├── 📄 000441.sst [961B]
    │   ├── 📄 004154.sst [65MB]
    │   ├── 📄 004155.sst [65MB]
    │   └── 📄 004156.sst [65MB]
    └── 📂 rocks-reverse-geocoder            [9GB 208개의 파일] 리버스 지오코딩
        ├── 📄 005440.sst [65MB]
        ├── 📄 005441.sst [65MB]
        ├── 📄 005443.sst [65MB]
        └── 📄 005444.sst [65MB]
```

## 자주 묻는 질문

### geocode.gimi9.com의 API 서버를 사용할 수 있나요?

그렇습니다. 하지만 계약을 해야 합니다. gisman@gmail.com으로 문의해 주세요.

### 데이터 업데이트는 얼마나 자주 하나요?

매일 합니다. 그리고 geocode.gimi9.com에 적용합니다.

다운로드 파일은 비정기적으로 배포합니다.

### 어떤 데이터를 사용하나요?

지오코딩은 주소정보 누리집의 여러 공공데이터를 사용합니다.

리버스 지오코딩은 브이월드의 연속지적도와 건물도형 공공데이터를 사용합니다.

### 처리 속도는 얼마나 빠른가요?

지오코딩 속도는 초당 3천건 이상입니다. 리버스 지오코딩은 더 빠릅니다.

### 서버의 권장 사양은?

CPU와 메모리 용량은 처리 속도에 큰 영향을 주지 않습니다. AWS의 t2.micro (1 vCPU, 1GiB Memory) 수준이면 충분합니다.

저장장치로 SSD 사용을 권장합니다.

## 기여

기여를 환영합니다!

* 지오코딩이 안 되는 주소가 있으면 알려주세요.

## 크레딧

* [Meta의 RocksDB](https://github.com/facebook/rocksdb)를 이용하여 간단한 구조와 빠른 성능을 얻을 수 있었습니다.

## 상업적 이용

상업적 이용은 엄격히 금지됩니다.

자세한 내용은 [LICENSE](LICENSE) 파일을 참조하시기 바랍니다.

문의사항: gisman@gmail.com
