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

[설치 설명서](install.md)

# 라이브러리 활용

```python
from geocoder_kr import geocoder, reverse_geocoder

gc = geocoder.Geocoder()
print(gc.search("서울특별시 송파구 장지동 839-5번지"))

rev_gc = reverse_geocoder.ReverseGeocoder()
print(rev_gc.search(127.11609829941841, 37.546857074590875))
```

# API 서버

## 서버 실행

```bash
uvicorn --host=0.0.0.0 api_fast:app
```

웹 브라우저로 http://localhost:8000/ 에 접속하면 API 서비스의 기본 페이지가 표시됩니다.

code 샘플:

* [Simple 지오코딩](simple_geocoding.md)
* [여러 개의 주소 지오코딩](multi_address_geocoding.md)
* [리버스 지오코딩](reverse_geocoding.md)

* [온라인 테스트 도구](docs.md)

## 주의사항

이 솔루션은 한국 주소에 특화되어 있으므로 해외 주소에는 사용할 수 없습니다.

정확한 결과를 위해 가능한 한 상세한 주소를 입력하세요.


## 자주 묻는 질문

### geocode-kr.gimi9.com의 API 서버를 사용할 수 있나요?

그렇습니다. 하지만 계약을 해야 합니다. gisman@gmail.com으로 문의해 주세요.

### 데이터 업데이트는 얼마나 자주 하나요?

매일 합니다. 그리고 geocode.gimi9.com에 적용합니다.

다운로드 파일은 보통 월 1회 비정기적으로 배포합니다.

### 어떤 데이터를 사용하나요?

지오코딩은 [주소정보 누리집](https://www.juso.go.kr/)의 여러 공공데이터를 사용합니다.

리버스 지오코딩은 [브이월드](https://gimi9.com/organization/vworld/)의 연속지적도와 건물도형 공공데이터를 사용합니다.

### 처리 속도는 얼마나 빠른가요?

지오코딩 속도는 초당 3천 건 이상이며, 리버스 지오코딩도 비슷한 속도를 보입니다.

비동기 처리를 사용하므로 동시에 여러 요청을 처리할 수 있습니다. Uvicorn 서버의 워커 수를 조정하여 동시에 처리할 수 있는 요청 수를 늘릴 수 있습니다.

### 서버의 권장 사양은?

CPU와 메모리는 AWS EC2 t2.micro (1 vCPU, 1GiB 메모리) 수준이면 충분합니다.

저장 장치는 SSD를 권장합니다.

운영 환경에서는 4GB 이상의 RAM을 권장합니다.

Ubuntu linux 서버를 권장하며 Windows의 wsl2 Ubuntu도 지원합니다.

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

