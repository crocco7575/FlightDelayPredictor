def fix_month_case(date_str):
    parts = date_str.split('-')  # ['19', 'JUN', '2025']
    if len(parts) == 3:
        parts[1] = parts[1].capitalize()  # Make 'JUN' → 'Jun'
    return '-'.join(parts)

# Example
#print(fix_month_case("19-JUN-2025"))  # Output: "19-Jun-2025"