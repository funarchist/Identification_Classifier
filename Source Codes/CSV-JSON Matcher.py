import collections
import json
import csv
import stringdist
import json
from itertools import product
import re
import months

class Matcher:
        
    def map_string(dictonary, input_str):
        min_dist = round(len(input_str) * 0.6)
        min_dist_value = input_str
        for key, value in dictonary.items():
            dist = stringdist.levenshtein(key, input_str)
        if dist < min_dist:
            if dist == 0:
                return value
            min_dist = dist
            min_dist_value = value
        return min_dist_value

    def apply_regex(string, str_type="mixed"):
        if str_type == "digit":
            return ''.join((re.findall("[0-9]+", string)))
        elif str_type == "letter":
            return ''.join(re.findall("[A-Za-z]+", string))
        elif str_type == "mixed":
            return ''.join(re.findall("[0-9A-Za-z]+", string))
        else:
            return string

    def unify_date(date_str):
        letters = apply_regex(date_str.upper(), "letter")
        date_str = apply_regex(date_str, "digit")
        if len(letters) < 2:
        # Possible formats are:
        # 21.05.1993, 21-05-1993, 210593 etc..
            unifed = date_str[-2:] + date_str[2:4] + date_str[:2]
        else:
        # 21MAY/MAY1993, 21MAY/MAY93 etc...
            month = map_string(months, letters)
        unifed = date_str[-2:] + month + date_str[:2]
        return unifed

    def process(file_csv,file_json):
        mapper = {"id_number": "id_number", "name": "name","birth_date": "birth_date"}
        dummy = 0
        k = 0
        pre_confidence = 0

        with open(file_json +'.json') as fake_data_json:
            json_check = json.load(fake_data_json)
            if all(k in json_check for k in ("first_name", "last_name")):
                new_val = json_check['first_name'] + ' ' + json_check['last_name']
                json_check['name'] = new_val
            del json_check['first_name']
            del json_check['last_name']

        with open(file_json+'.json', 'w') as fake_data_json:
            json.dump(json_check, fake_data_json)

        fake_data_json = open(file_json+'.json')
        
        with open(file_csv+'.csv') as fake_data_csv:
            headers = next(fake_data_csv)
            number_of_header = headers.count(',')
            Data = collections.namedtuple('data', headers)
            fake_data_csv = csv.reader(fake_data_csv, delimiter=',')
            for line_csv, line_json in product(fake_data_csv, fake_data_json):
                csv_obj = Data(*line_csv)
                line_json = json.loads(line_json)
            for i, m in mapper.items():
                json_string = line_json[m]
                if m == 'id_number':
                    line_json[m] = re.sub("[^0-9]", "", json_string)
                if i == 'birth_date':
                    standard_csv_date = unify_date(getattr(csv_obj, i))
                    standard_json_date = unify_date(line_json[m])
                    dist = stringdist.levenshtein(standard_csv_date,standard_json_date)
                    value_csv = str(standard_csv_date)
                    value_json = str(standard_json_date)
                else:
                    dist = stringdist.levenshtein(getattr(csv_obj, i), line_json[m])
                    value_csv = str(getattr(csv_obj, i))
                    value_json = str(line_json[m])
                    upper_lev = max(len(value_csv), len(value_json))
                    confidence = (upper_lev - dist)/upper_lev
                if confidence >= 0.75:
                    dummy += 1
                pre_confdence += confidence
            overall_confidence = pre_confidence / number_of_header
            if overall_confidence >= 0.75:
                return {'Customer ID': str(line_csv[0]), 'Confidence': overall_confidence}
            else:
                pre_confidence = 0
                overall_confidence = 0
                dummy = 0
        return {'Customer ID': None, 'Confidence':overall_confidence}