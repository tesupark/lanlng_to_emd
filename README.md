# 좌표 읍면동으로 변환해주는 프로그램임.
## 개요
현재 졸업작품 프로젝트에서 위치기반을 적용하려고 하는데, 위도 경도 값을 api호출로 받아오고 싶지 않았음.
따라서 emd.dbf, emd.shp, emd.shx 파일을 
json으로 만들어서 위도 경도 값을 부르면 읍면동과 인접 읍면동을 리턴해주는 기능을 구현하고자 함.

## 준비물
1. [지오서비스](https://www.geoservice.co.kr/) 회원가입
2. 회원가입 이후 아카이브 에서 읍면동 데이터 다운로드 받기 
3. 압축 풀어서 (emd.*) 파일이 4개 들어있으면 굿.
4. 각 파일에 shp_path 값 수정하기.
5. pip install geopandas shapely tqdm
6. python gej.py
7. python gej_alias_litee.py