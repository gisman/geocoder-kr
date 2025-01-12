[온라인 데모!](https://geocode-kr.gimi9.com/) | [서비스 데모!](https://geocode.gimi9.com/) | [리버스 지오코딩에 대해 아시나요?](https://gimi9.com/blog/reverse-geocoding/)

geocoder-kr은 한국 주소를 위한 Python 기반 지오코딩 솔루션입니다.
이 솔루션을 사용하면 한국의 주소를 지리적 좌표(위도와 경도)로 변환할 수 있습니다.

# 특징

* 한국 주소 체계에 최적화
* 다양한 주소 형식 지원 (도로명 주소, 지번 주소)
* 지오코딩 및 리버스 지오코딩
* 빠르고 정확한 지오코딩 결과
* 쉬운 설치
* 간편한 API 사용
* 매우 적은 리소스 사용
* 초고속 처리 속도
* 셀프 호스팅 가능

![지오코딩](https://github.com/user-attachments/assets/24df3aed-37d4-4c02-8569-42ee471551b9)

# 설치

```bash
pip install geocoder-kr
```

## 데이터 다운로드 (필수)

geocoder-kr이 동작하려면 데이터 파일이 필요합니다.

1. [code 데이터 다운로드](https://geocode.gimi9.com/static/download/code.tar.gz)

2. [Geocoding 데이터 다운로드](https://geocode.gimi9.com/static/download/rocks.tar.gz)

3. [Reverse Geocoding 데이터 다운로드](https://geocode.gimi9.com/static/download/rocks-reverse-geocoder.tar.gz)

4. 다운로드한 파일을 프로젝트 디렉토리에 다음과 같이 복사하세요.

(참고: 아래의 디렉토리 구조는 [tree-view](https://github.com/gisman/tree-view) 유틸리티를 사용하여 제작되었습니다.)
```bash
 📂 db                                       [12GB]
    ├── 📂 code                              [64MB 3개의 파일]
    │   ├── 📄 PNU.csv [3MB]
    │   ├── 📄 TN_SPRD_RDNM.txt [62MB]
    │   └── 📄 h1_h2_code_match.csv [15KB]
    ├── 📂 rocks                             [3GB 336개의 파일]
    │   ├── 📄 000441.sst [961B]
    │   ├── 📄 004238.sst [65MB]
    │   ├── 📄 004239.sst [65MB]
    │   └── 📄 004240.sst [65MB]
    └── 📂 rocks-reverse-geocoder            [9GB 348개의 파일]
        ├── 📄 005253.sst [65MB]
        ├── 📄 005254.sst [65MB]
        ├── 📄 005256.sst [65MB]
        └── 📄 005257.sst [65MB]
```

# 사용법 (라이브러리)

```python
from geocoder_kr import geocoder, reverse_geocoder

gc = geocoder.Geocoder()
print(gc.search("서울특별시 송파구 장지동 839-5번지"))

rev_gc = reverse_geocoder.ReverseGeocoder()
print(rev_gc.search(127.11609829941841, 37.546857074590875))
```

# 사용법 (API 서버)

## 실행

```bash
uvicorn --host=0.0.0.0 api_fast:app
```

웹 브라우저로 http://localhost:8000/ 에 접속하면 API 서비스의 기본 페이지가 표시됩니다.


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

## 리버스 지오코딩

좌표(위도와 경도)에 해당하는 주소를 찾습니다.

![image](https://github.com/user-attachments/assets/9da15c87-0cfa-43c1-a353-8712d1efbea7)


### Request

> https://geocode-kr.gimi9.com/reverse_geocode/?x=127.12771948485866&y=37.47699735340699

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

## /docs

RESTful API를 설계, 문서화, 테스트하기 위한 [Swagger](https://swagger.io/) 기반의 도구를 제공합니다.

[온라인 문서](https://geocode-kr.gimi9.com/docs#/)

![image](https://github.com/user-attachments/assets/034b7c7f-6a3b-4c15-a454-7da784ef94df)


## 주의사항

이 솔루션은 한국 주소에 특화되어 있으므로 해외 주소에는 사용할 수 없습니다.

정확한 결과를 위해 가능한 한 상세한 주소를 입력하세요.

## 자주 묻는 질문

### geocode-kr.gimi9.com의 API 서버를 사용할 수 있나요?

그렇습니다. 하지만 계약을 해야 합니다. gisman@gmail.com으로 문의해 주세요.

### 데이터 업데이트는 얼마나 자주 하나요?

매일 합니다. 그리고 geocode.gimi9.com에 적용합니다.

다운로드 파일은 비정기적으로 배포합니다.

### 어떤 데이터를 사용하나요?

지오코딩은 [주소정보 누리집](https://www.juso.go.kr/)의 여러 공공데이터를 사용합니다.

리버스 지오코딩은 [브이월드](https://gimi9.com/organization/vworld/)의 연속지적도와 건물도형 공공데이터를 사용합니다.

### 처리 속도는 얼마나 빠른가요?

지오코딩 속도는 초당 3천 건 이상이며, 리버스 지오코딩도 비슷한 속도를 보입니다.

기본적으로 비동기 처리를 사용하며, Uvicorn 서버의 워커 수를 조정하여 동시에 처리할 수 있는 요청 수를 늘릴 수 있습니다.

### 서버의 권장 사양은?

CPU와 메모리는 AWS EC2 t2.micro (1 vCPU, 1GiB 메모리) 수준이면 충분합니다.

저장 장치는 SSD를 권장합니다.

운영 환경에서는 4GB 이상의 RAM을 권장합니다.

## 기여

기여를 환영합니다! GitHub 저장소를 포크하고 풀 리퀘스트를 보내주세요. 버그 리포트, 기능 제안, 문서 개선 등 모든 종류의 기여를 환영합니다.

지오코딩이 안 되는 주소가 있으면 알려주세요.

## 지원 및 문의

문제가 발생하거나 질문이 있으시면 GitHub 이슈를 통해 문의해 주세요.

빠르게 답을 얻으려면 [카톡 오픈채팅](https://open.kakao.com/o/gNplQr7f)으로 문의해주세요. 

## 크레딧

* [Meta의 RocksDB](https://github.com/facebook/rocksdb)를 이용하여 간단한 구조와 빠른 성능을 얻을 수 있었습니다.

## 상업적 이용

상업적 이용은 엄격히 금지됩니다. 상업적으로 사용하려면 gisman@gmail.com 으로 문의해 주세요.

다음과 같은 경우 자유롭게 사용할 수 있습니다. 

* 개인적 사용: 개인이 비영리 목적으로 소프트웨어를 사용하는 경우
* 교육 목적: 학교, 대학 등 교육 기관에서 학습 및 연구 목적으로 사용하는 경우
* 비영리 단체: 자선 단체나 NGO 등이 그들의 미션을 수행하기 위해 사용하는 경우
* 오픈소스 프로젝트: 다른 비상업적 오픈소스 프로젝트에서 해당 솔루션을 활용하는 경우
* 정부 기관: 공공 서비스 제공을 위해 정부 기관에서 사용하는 경우
* 학술 연구: 대학이나 연구소에서 순수 학술 목적으로 사용하는 경우

자세한 내용은 [LICENSE](LICENSE) 파일을 참조하시기 바랍니다.

