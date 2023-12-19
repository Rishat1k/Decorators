from pprint import pprint
import csv
import re
from task_2 import logger


with open("phonebook_raw.csv", newline='', encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

@logger('task_3.log')
def correct_phone_book(contacts_list):
  pattern_number = r"(\+7|8)\s*\(?(\d\d\d)\)?(\s*|-)(\d\d\d)\-?(\d\d)\-?(\d\d)"
  substitute_number = r"+7(\2)\4-\5-\6"
  pattern_additional = r"\(?доб.\s(\d+)\)?"
  substitute_additional = r"доб.\1"
  for person in contacts_list:
    result = re.findall(r"\w+", person[0])
    if len(result) > 2:
      person[2] = result[2]
      person[1] = result[1]
      person[0] = result[0]
    elif len(result) == 2:
      person[1] = result[1]
      person[0] = result[0]
    elif len(result) == 1:
      person[0] = result[0]
      result_2 = re.findall(r"\w+", person[1])
      if len(result_2) == 2:
        person[1] = result_2[0]
        person[2] = result_2[1]
    result_phone = re.sub(pattern_number, substitute_number, person[5])
    person[5] = result_phone
    result_additional = re.sub(pattern_additional, substitute_additional, person[5])
    person[5] = result_additional

@logger('task_3.log')
def removing_duplicates(contacts_list):
  lastname_lst = []
  extra_index = []
  for i in range(len(contacts_list)):
    for j in range(i+1, len(contacts_list)):
      if contacts_list[i][0] == contacts_list[j][0]:
        z = 0
        extra_index.append(j)
        for element in contacts_list[i]:
          if element.strip() == '':
            contacts_list[i][z] = contacts_list[j][z]
          z += 1
  extra_index.sort(reverse=True)
  for index in extra_index:
    contacts_list.pop(index)

if __name__ == "__main__":
  correct_phone_book(contacts_list)
  removing_duplicates(contacts_list)
  print(contacts_list)

  with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)