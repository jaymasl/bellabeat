from query import get_user_averages

def safe_convert(value):
    if value is None:
        return 'N/A'
    try:
        return round(float(value), 2)
    except (ValueError, TypeError):
        return value

def format_table_data():
    column_names, data_rows = get_user_averages()
    
    formatted_data = []
    for row in data_rows:
        formatted_row = {}
        for i, column_name in enumerate(column_names):
            if i < len(row):
                formatted_row[column_name] = safe_convert(row[i])
            else:
                formatted_row[column_name] = '0'
        formatted_data.append(formatted_row)
    
    return formatted_data