import geopandas as gpd
import json
from shapely.geometry import mapping
from geopy.distance import geodesic
from tqdm import tqdm  # 진행률 표시용

# 1. SHP 파일 읽기
shp_path = "./emd"
gdf = gpd.read_file(f"{shp_path}.shp", encoding='cp949')

# 2. 좌표계 설정 및 변환
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=5179)
gdf = gdf.to_crs(epsg=4326)

# 3. 중심 좌표 계산
gdf['centroid'] = gdf.geometry.centroid
gdf['lat'] = gdf['centroid'].y
gdf['lng'] = gdf['centroid'].x

# 4. 기본 속성 리스트 생성
records = []
for _, row in gdf.iterrows():
    records.append({
        "name": row.get("EMD_KOR_NM", row.get("EMD_NM", "")),
        "adm_cd": row.get("EMD_CD", ""),
        "sido": row.get("SIDO_NM", ""),
        "sigungu": row.get("SGG_NM", ""),
        "lat": row["lat"],
        "lng": row["lng"],
        "geometry": mapping(row.geometry.simplify(0.001)),
    })

# 5. neighbors 계산 (반경 2km 이내)
print("📍 Calculating neighbors...")
for record in tqdm(records):
    base_coord = (record["lat"], record["lng"])
    neighbors = []
    for other in records:
        if record["adm_cd"] == other["adm_cd"]:
            continue
        other_coord = (other["lat"], other["lng"])
        distance_km = geodesic(base_coord, other_coord).km
        if distance_km <= 2.0:
            neighbors.append({
                "adm_cd": other["adm_cd"],
                "name": other["name"]
            })
    record["neighbors"] = neighbors

# 6. 저장
output_path = "eupmyeondong_with_neighbors.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"✅ 저장 완료: {output_path}")
