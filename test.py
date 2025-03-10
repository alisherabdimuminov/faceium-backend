import openpyxl
import json

def excel_to_json(excel_file, json_file):
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active

    data = []
    headers = [cell.value for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = {headers[i]: row[i] for i in range(len(headers))}
        data.append(row_data)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"JSON saved to {json_file}")

# Example usage
excel_to_json("data.xlsx", "data.json")
