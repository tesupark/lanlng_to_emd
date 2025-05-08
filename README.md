# 좌표 읍면동으로 변환해주는 프로그램임.
## 개요
현재 졸업작품 프로젝트에서 위치기반을 적용하려고 하는데, 위도 경도 값을 api호출로 받아오고 싶지 않았음.
따라서 emd.dbf, emd.shp, emd.shx 파일을 
json으로 만들어서 위도 경도 값을 부르면 읍면동과 인접 읍면동을 리턴해주는 기능을 구현하고자 함.

## 준비물
1. [지오서비스](https://www.geoservice.co.kr/)
2. pip install geolocation 