def data_flow_pipeline(input_data):
    processed = [x * 2 for x in input_data if x > 0]
    return sum(processed)
