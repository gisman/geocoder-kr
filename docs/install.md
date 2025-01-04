# 설치

간단한 설치. DBMS 필요 없음

## using pip

```bash
pip install geocoder-kr
```

## using source code

```bash
git clone https://github.com/gisman/geocoder-kr.git
cd geocoder-kr
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 데이터 다운로드

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

