import geopandas as gpd
import json
from shapely.geometry import Point
from shapely.ops import transform
from tqdm import tqdm

shp_path = "./emd_20250311/emd"
gdf = gpd.read_file(f"{shp_path}.shp", encoding="cp949")

# 1. 유효하지 않은 기하학 수정
gdf["geometry"] = gdf["geometry"].apply(lambda geom: geom if geom.is_valid else geom.buffer(0))

# 2. 좌표계 설정 및 변환
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=5179)
gdf = gdf.to_crs(epsg=4326)

# 3. 중심좌표 계산 (투영 좌표계에서 계산 후 변환)
gdf_proj = gdf.to_crs(epsg=5179)
gdf['centroid'] = gdf_proj.geometry.centroid.to_crs(epsg=4326)
gdf['lat'] = gdf['centroid'].y
gdf['lng'] = gdf['centroid'].x

# 4. neighbors 계산: 경계가 맞닿는 읍면동만 필터링
records = []
print("📍 Calculating geometry-based neighbors...")

for idx, row in tqdm(gdf.iterrows(), total=len(gdf)):
    base_geom = row.geometry
    base_adm_cd = row["EMD_CD"]
    base_name = row["EMD_KOR_NM"]

    # touches() 필터링
    touching = gdf[gdf.geometry.touches(base_geom)]

    neighbors = []
    for _, other in touching.iterrows():
        if other["EMD_CD"] != base_adm_cd:
            neighbors.append({
                "adm_cd": other["EMD_CD"],
                "name": other["EMD_KOR_NM"]
            })

    record = {
        "adm_cd": base_adm_cd,
        "name": base_name,
        "lat": row["lat"],
        "lng": row["lng"],
        "neighbors": neighbors if neighbors else None  # 빈 이웃 처리
    }
    records.append(record)

# 5. 저장
output_path = "emd_touch_neighbors.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"✅ JSON 저장 완료: {output_path}")
