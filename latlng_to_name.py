
import json
from geopy.distance import geodesic

# JSON 파일에서 데이터 읽기
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# 위도, 경도를 입력받아 가장 가까운 읍면동을 찾는 함수
def find_closest_area(input_lat, input_lng, data):
    closest_area = None
    min_distance = float('inf')

    for area in data:
        area_location = (area['lat'], area['lng'])
        distance = geodesic((input_lat, input_lng), area_location).km

        if distance < min_distance:
            min_distance = distance
            closest_area = area

    return closest_area, min_distance

# 입력을 받습니다.
input_lat = float(input("위도를 입력하세요: "))
input_lng = float(input("경도를 입력하세요: "))

# 파일에서 데이터 로드
filename = 'emd_touch_neighbors.json'
data = load_data(filename)

# 가장 가까운 읍면동과 그 인접 읍면동을 찾습니다.
closest_area, min_distance = find_closest_area(input_lat, input_lng, data)

# 결과 출력
if closest_area:
    print(f"가장 가까운 읍면동: {closest_area['name']} (거리: {min_distance:.2f} km)")
    print("인접 읍면동들:")
    for neighbor in closest_area['neighbors']:
        print(f"- {neighbor['name']}")
