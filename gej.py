import geopandas as gpd
import json
from shapely.geometry import mapping

# 1. SHP 파일 읽기 (EUC-KR 인코딩)
shp_path = "./emd"  # .shp, .shx, .dbf 세 파일 존재해야 함
gdf = gpd.read_file(f"{shp_path}.shp", encoding='cp949')

# 2. 좌표계 설정 및 위경도 변환
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=5179)  # 대부분 SHP는 5179
gdf = gdf.to_crs(epsg=4326)  # 전체를 위경도로 변환

# 3. 중심 좌표 계산
gdf['centroid'] = gdf.geometry.centroid
gdf['lat'] = gdf['centroid'].y
gdf['lng'] = gdf['centroid'].x

# 4. JSON 리스트 생성
result = []
for _, row in gdf.iterrows():
    result.append({
        "name": row.get("EMD_KOR_NM", row.get("EMD_NM", "")),
        "adm_cd": row.get("EMD_CD", ""),
        "sido": row.get("SIDO_NM", ""),
        "sigungu": row.get("SGG_NM", ""),
        "lat": row["lat"],
        "lng": row["lng"],
        "geometry": mapping(row.geometry.simplify(0.001))  # GeoJSON 좌표
    })

# 5. 저장
output_path = "eupmyeondong_mapped1.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"✅ 저장 완료: {output_path}")
