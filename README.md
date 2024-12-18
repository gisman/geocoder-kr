[온라인 데모!](https://geocode.gimi9.com/) | [리버스 지오코딩에 대해 아시나요?](https://gimi9.com/blog/reverse-geocoding/)

Self hosting 가능한 오픈소스 지오코딩, 리버스 지오코딩 API. 

![지오코딩](![image](https://github.com/user-attachments/assets/24df3aed-37d4-4c02-8569-42ee471551b9)


# 지오코딩 API

이 프로젝트는 지오코딩 API를 제공합니다. 이 API는 도로명주소와 지번주소를 처리하며, 공공데이터의 잘 정제된 주소를 99% 이상 처리할 수 있습니다.
지오코딩 API를 사용하여 주어진 주소의 지리적 좌표(위도와 경도)를 가져옵니다.

## 주요 기능

- hash 기반 개발: 파싱 단계에서 hash 생성. DB 쿼리는 hash 키로 단 한 번.
- 건물명 단순화: 건물 별칭 관리 안 함.
- 지적도 추가, 주소 유형 추가 등 별도 프로젝트로 분리해서 관리.
- 성능: 


## 목표

- 공공데이터의 잘 정제된 주소를 처리. 99% 이상 처리.
- 도로명주소, 지번주소 모두 처리.
- 번지 없는 지번 주소 지원 안 함.
- 인근지번 지원 안 함.
- 건물 좌표(아파트 동, 대학교 내 건물 등) 처리.
- output: java 버전의 output 기반으로 국가기초구역, 통계청집계구 포함. 블록 제외.
  - 정부표준 행정구역 코드 포함.

## 설치

```sh
git clone https://github.com/your-repo/geocoder-kr.git
cd geocoder-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## DB 다운로드

다운로드한 파일을 

Geocoding: 

Reverse Geocoding: 

## 상업적 이용

[LICENSE](LICENSE) 파일을 참고하세요.

문의: gisman@gmail.com

