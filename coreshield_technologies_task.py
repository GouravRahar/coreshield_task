

locations_json = [
    {"id": "loc_01", "latitude": 37.7749, "longitude": -122.4194},
    {"id": "loc_04", "latitude": 27.8749, "longitude": 122.4194},
    {"id": "loc_05", "latitude": 57.2749, "longitude": -112.4344},
    {"id": "loc_06", "latitude": 14.0522, "longitude": -119.2531},
    {"id": "loc_07", "latitude": 64.0522, "longitude": -108.2330},
    {"id": "loc_02", "latitude": 34.0522, "longitude": -118.2437},
    {"id": "loc_08", "latitude": 24.0522, "longitude": -168.2197},
    {"id": "loc_03", "latitude": 40.7128, "longitude": -74.0060},
    {"id": "loc_89", "latitude": 23.7128, "longitude": -43.0060}
]

metadata_json = [
    {"id": "loc_01", "type": "restaurant", "rating": 4.5, "reviews": 120},
    {"id": "loc_04", "type": "restaurant", "rating": 4.1, "reviews": 500},
    {"id": "loc_05", "type": "restaurant", "rating": 3.7, "reviews": 110},
    {"id": "loc_02", "type": "hotel", "rating": 4.2, "reviews": 200},
    {"id": "loc_06", "type": "hotel", "rating": 4.0, "reviews": 700},
    {"id": "loc_07", "type": "hotel", "rating": 2.0, "reviews": 900},
    {"id": "loc_03", "type": "cafe", "rating": 4.7, "reviews": 150},
    {"id": "loc_08", "type": "cafe", "rating": 4.5, "reviews": None}
]

#1. This is 1st Point, Here we are merging the data based on the id of both jsons
merged_data = []
for loc in locations_json:
    for meta in metadata_json:
        if loc["id"] == meta["id"]:
            merged_data.append({
                "id": loc["id"],
                "latitude": loc["latitude"],
                "longitude": loc["longitude"],
                "type": meta["type"],
                "rating": meta["rating"],
                "reviews": meta["reviews"]
            })
            break







#2. This is the 2nd point, Here we are counting the total no of lat and long of every type
type_counts = {}
for entry in merged_data:
    entry_type = entry["type"]
    if "latitude" in entry and "longitude" in entry and entry_type:
        type_counts[entry_type] = type_counts.get(entry_type, 0) + 1

print("Valid points per type:", type_counts)








#3. This is the 3rd point, Here we are counting the avg per type in one loop only, in every iteration we are 
type_ratings = {}  # {type: {"avg": float, "count": int}}
for entry in merged_data:
    entry_type = entry["type"]
    rating = entry["rating"]
    #making sure the rating is correct only
    if isinstance(rating, (int, float)):
        if entry_type not in type_ratings:
            type_ratings[entry_type] = {"avg": rating, "count": 1}
        else:
            #counting avg on the go for the current type
            current = type_ratings[entry_type]
            new_count = current["count"] + 1
            current["avg"] = (current["avg"] * (new_count - 1) + rating) / new_count
            current["count"] = new_count

average_ratings = {t: round(r["avg"],2) for t, r in type_ratings.items()}
print("Average rating per type:", average_ratings)








#4. This is the 4th point, Here we are getting the max no of review for particular loc_id
max_reviews_location = {}
for data in merged_data:
    if isinstance(data.get('reviews'),int) and max_reviews_location.get('reviews',0)<=data.get('reviews'):
        max_reviews_location = data
if max_reviews_location:
    print("Location with highest reviews:", max_reviews_location["id"], "with", max_reviews_location["reviews"], "reviews")










#5. This is the 5th point, Here we are getting the incomplete data, we are assuming that incomplete data means
# it is present in 1 of json but not both
incomplete_data = []

loc_ids = {loc["id"] for loc in locations_json}
meta_ids = {meta["id"] for meta in metadata_json}
missing_in_metadata = loc_ids - meta_ids
if missing_in_metadata:
    incomplete_data.extend([{"id": id, "issue": "Missing metadata"} for id in missing_in_metadata])
missing_in_locations = meta_ids - loc_ids
if missing_in_locations:
    incomplete_data.extend([{"id": id, "issue": "Missing location data"} for id in missing_in_locations])
for entry in merged_data:
    issues = []
    if not (-90 <= entry["latitude"] <= 90):
        issues.append("Invalid latitude")
    if not (-180 <= entry["longitude"] <= 180):
        issues.append("Invalid longitude")
    if "rating" not in entry or not isinstance(entry["rating"], (int, float)):
        issues.append("Missing or invalid rating")
    if "reviews" not in entry or not isinstance(entry["reviews"], int):
        issues.append("Missing or invalid reviews")
    if issues:
        incomplete_data.append({"id": entry["id"], "issues": issues})

if incomplete_data:
    print("Locations with incomplete data:", incomplete_data)
else:
    print("No incomplete data found.")