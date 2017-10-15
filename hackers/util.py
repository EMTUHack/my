import csv
from .models import CV_TYPES


def pre_gender(row):
    comp = {"Masculino": "M", "Male": "M", "Feminino": "F", "Female": "F"}
    return comp.get(row["Gender"], "O")


def pre_university(row):
    return row['Universidade '] if row['Universidade '] != 'Outra' else row['Qual? ']


def pre_special(row):
    return row['Necessidade especial'] if row['Necessidade especial'] != 'Outra' else row['Qual? .2']


def pre_diet(row):
    return row['Restrição de dieta'] if row['Restrição de dieta'] != 'Outra' else row['Qual? .1']


def pre_cv_type(value):
    return next((code for code, name in CV_TYPES if name == value), None)


def pre_cv(row):
    comp = {"LinkedIn": "linkedin.com/in/", "GitHub": "github.com/", "Website": "Seu site", "Outro": "Outra forma de currículo"}
    return row[comp[row["Currículo (Enviado para patrocinadores)"]]]


def pre_cv2(row):
    comp = {"LinkedIn": "linkedin.com/in/ ", "GitHub": "github.com/ ", "Website": "Seu site ", "Outro": "Outra forma de currículo "}
    return row.get(comp.get(row["Currículo 2 (Opcional)"], ""), "")


def proc_hacker(row):
    data = {
        "first_name": 'row["First Name"]',
        "last_name": 'row["Last Name"]',
        "email": 'row["Email"]',
        "phone": 'row["Cell Phone"]',
        "gender": 'pre_gender(row)',
        "age": 'row["Age"]',
        "university": 'pre_university(row)',
        "diet": 'pre_diet(row)',
        "special_needs": 'pre_special(row)',
        "shirt_size": 'row["Tamanho da camisa "]',
        "cv_type": 'pre_cv_type(row["Currículo (Enviado para patrocinadores)"])',
        "cv": 'pre_cv(row)',
        "cv2_type": 'pre_cv_type(row["Currículo 2 (Opcional)"])',
        "cv2": 'pre_cv2(row)',
        "facebook": 'row["facebook.com/"]'
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
            results.append(proc_hacker(row))
        except KeyError as e:
            errors.append({"row": row, "name": "{} {}".format(row['First Name'], row['Last Name']), "error": repr(e)})

    return results, errors
