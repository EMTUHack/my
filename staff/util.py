import csv


def proc_staff(row):
    data = {
        "first_name": 'row["First Name"]',
        "last_name": 'row["Last Name"]',
        "email": 'row["Email"]',
    }
    final = {}
    for k, v in data.items():
        try:
            final[k] = eval(v)
        except KeyError as e:
            pass
    return final


def proc(file):
    results = []
    errors = []
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        try:
            results.append(proc_staff(row))
        except KeyError as e:
            errors.append({"row": row, "name": "{} {}".format(row['First Name'], row['Last Name']), "error": repr(e)})

    return results, errors
