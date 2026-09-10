def process_user_data(user_id, data):
    total = 0
    if data:
        for item in data:
            total += item.get("value", 0)
    return total
