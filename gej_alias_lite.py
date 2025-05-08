import geopandas as gpd
import json
from shapely.geometry import mapping
from geopy.distance import geodesic
from tqdm import tqdm

shp_path = "./emd"  # .shp, .shx, .dbf 세 파일 존재해야 함
gdf = gpd.read_file(f"{shp_path}.shp", encoding='cp949')

if gdf.crs is None:
    gdf = gdf.set_crs(epsg=5179)
gdf = gdf.to_crs(epsg=4326)

gdf['centroid'] = gdf.geometry.centroid
gdf['lat'] = gdf['centroid'].y
gdf['lng'] = gdf['centroid'].x

# Step 1: 기본 레코드 정리 (불필요 필드 제거)
records = []
for _, row in gdf.iterrows():
    records.append({
        "adm_cd": row.get("EMD_CD", ""),
        "sido": row.get("SIDO_NM", ""),
        "sigungu": row.get("SGG_NM", ""),
        "name": row.get("EMD_KOR_NM", row.get("EMD_NM", "")),
        "lat": row["lat"],
        "lng": row["lng"],
        "neighbors": []  # 나중에 채움
    })

# Step 2: neighbors 계산 (반경 2km)
print("📍 Calculating neighbors...")
for record in tqdm(records):
    base = (record["lat"], record["lng"])
    neighbors = []
    for other in records:
        if record["adm_cd"] == other["adm_cd"]:
            continue
        dist = geodesic(base, (other["lat"], other["lng"])).km
        if dist <= 2.0:
            neighbors.append({
                "adm_cd": other["adm_cd"],
                "name": other["name"]
            })
    record["neighbors"] = neighbors

# Step 3: 저장
output_path = "emd_minimal_neighbors.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"✅ 저장 완료: {output_path}")
