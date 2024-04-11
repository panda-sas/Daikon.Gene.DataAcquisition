def format_publication(input_data):
    output_data = []

    for item in input_data:
        formatted_item = {
            "item1": item.get("id", ""),
            "item2": item.get("source", ""),
            "item3": "",
            "item4": "",
            "item5": "",
            "item6": "",
        }
        output_data.append(formatted_item)

    return output_data
