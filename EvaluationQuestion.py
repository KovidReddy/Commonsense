import json as js
import csv
# read the file which contains the parsed sentence
with open('C:\\Users\\pylak\\Documents\\Fall_2018\\NLP\\PROJECT\\file4.json', encoding="utf8") as f:
    data = js.load(f)
# loop through each of the elements
tempe_list = []
count = 0
csv_list = []
for element in data['data']:
    if element['type'] != "prop causes action":
        continue
    action = element['knowledge']['causes']['value']
    prop = element['knowledge']['value']
    file_list = element['parser']
    str = ''
    temp_list = []
    parse_list = []
    for elem in file_list:
        str = elem.replace("has", "")
        str = str.replace("\n", "")
        str = str.replace("(", "")
        str = str.replace("(", "")
        str = str.replace(")", "")
        temp_list = str.split(',')
        parse_list.append(temp_list)
    if parse_list == []:
        continue
    del parse_list[-1]
    # for the scenario where there is only recipient
    recipient = ""
    # Default Agent
    agent = 'Tom'
    for elem in parse_list:
        if elem[1] == 'instance_of' and elem[2] == action:
            action = ''.join(el for el in elem[0] if el.isalnum() and not el.isdigit())

    agent2 = ''
    sent = ''
    ques = ''
    obj = ''
    away_flag = False
    rec_flg = False
    agent_flg = False
    part_flg = False
    recgrp_flg = False
    agentgrp_flg = False
    agent_istrait = False
    agent_person = False
    rec_person = False
    obj_flag = False
    for elem in parse_list:
        if elem[0][0:len(action)] == action and elem[1] == 'away_from_location':
            away_flag = True
            away = ''.join(el for el in elem[2] if el.isalnum() and not el.isdigit())
        if elem[0][0:len(action)] == action and elem[1] == 'recipient':
            recipient = elem[2]
            recipient = ''.join(el for el in recipient if el.isalnum() and not el.isdigit())
            rec_flg = True
        if elem[0][0:len(action)] == action and elem[1] == 'agent':
            agent2 = ''.join(el for el in elem[2] if el.isalnum() and not el.isdigit())
            agent_flg = True
        if elem[0][0:len(action)] == action and elem[1] == 'is_participant_in':
            participant = ''.join(el for el in elem[2] if el.isalnum() and not el.isdigit())
            part_flg = True
        if elem[0][0:len(action)] == action and elem[1] == 'object':
            obj = ''.join(el for el in elem[2] if el.isalnum() and not el.isdigit())
            obj_flag = True
        if elem[1] == 'agent':
            agent = ''.join(el for el in elem[2] if el.isalnum() and not el.isdigit())
        if elem[0] == recipient and elem[1] == 'is_subclass_of':
            if elem[2] == 'group':
                recgrp_flg = True
            elif elem[2] == 'person':
                rec_person = True
        if elem[0][0:len(agent)] == agent and elem[1] == 'trait' and elem[2][0:len(prop)] == prop:
            agent_istrait = True
        if elem[0][0:len(recipient)] == recipient and elem[1] == 'trait' and elem[2][0:len(prop)] == prop:
            rec_istrait = True
        if elem[0] == agent and elem[1] == 'is_subclass_of':
            if elem[2] == 'person':
                agent_person = True
                agent = elem[0]
            elif elem[2] == 'group':
                agentgrp_flg = True
            else:
                agent_person = False
                agent = 'Tom'

    space = ' '
    dot = '.'
    prep = 'It was'
    prep_agent = 'He was'
    prepq = 'What was'
    prepq_agent = 'Who was'
    prepgrp = 'They were'
    away_from = 'away from'
    q = '?'
    conj = 'in'
    ans = ''
    opt1 = '1.'
    opt2 = '2.'
    opt3 = '3. I cannot understand the question'
    csv_list_temp = []
    if agent == recipient or agent == agent2:
        agent = 'Mark'

    if away_flag == True:
        sent = agent + space + action + space + away + space + away_from + space + recipient + dot + space + prep + space + prop
        ques = prepq + space + prop + q
        ans = opt1 + space + agent + space + opt2 + space + recipient + space + opt3
    elif agent_flg == True and rec_flg == True:
        if (recgrp_flg == True and rec_istrait == True) or (agentgrp_flg == True and agent_istrait == True):
            sent = agent2 + space + action + space + recipient + dot + space + prepgrp + space + prop
            ques = prepq_agent + space + prop + q
            ans = opt1 + space + agent2 + space + opt2 + space + recipient + space + opt3
        elif (rec_person == True and rec_istrait == True) or (agent_person == True and agent_istrait == True):
            sent = agent2 + space + action + space + recipient + dot + space + prep_agent + space + prop
            ques = prepq_agent + space + prop + q
            ans = opt1 + space + agent2 + space + opt2 + space + recipient + space + opt3
        else:
            sent = agent2 + space + action + space + recipient + dot + space + prep + space + prop
            ques = prepq + space + prop + q
            ans = opt1 + space + agent2 + space + opt2 + space + recipient + space + opt3

    elif agent_flg == True and rec_flg == False:
        if (agent_person == True and agent_istrait == True):
            sent = agent2 + space + action + space + agent + dot + space + prep_agent + space + prop
            ques = prepq_agent + space + prop + q
            ans = opt1 + space + agent2 + space + opt2 + space + agent + space + opt3
        else:
            sent = agent2 + space + action + space + agent + dot + space + prep + space + prop
            ques = prepq + space + prop + q
            ans = opt1 + space + agent + space + opt2 + space + agent2 + space + opt3
    elif part_flg == True and obj_flag == True:
            sent = obj + space + action + space + conj + space + participant + dot + space + prep + space + prop
            ques = prepq + space + prop + q
            ans = opt1 + space + obj + space + opt2 + space + participant + space + opt3
    elif rec_flg == True and agent_flg == False:
        if recgrp_flg == True and rec_istrait == True:
            sent = agent + space + action + space + recipient + dot + space + prepgrp + space + prop
        elif agentgrp_flg == True and agent_istrait == True:
            sent = agent + space + action + space + recipient + dot + space + prepgrp + space + prop
        else:
            sent = agent + space + action + space + recipient + dot + space + prep + space + prop
        ques = prepq + space + prop + q
        ans = opt1 + space + agent + space + opt2 + space + recipient + space + opt3

    if sent != '' and ques != '':
        temp_dict = {'sentence':'','question':'', 'text':''}
        temp_dict['sentence'] = sent
        temp_dict['question'] = ques
        temp_dict['text'] = element['text']
        temp_dict['knowledge'] = element['knowledge']
        tempe_list.append(temp_dict)
        csv_list_temp.append(sent)
        csv_list_temp.append(ques)
        csv_list_temp.append(ans)
        csv_list.append(csv_list_temp)
        csv_list_temp = []

main_dict = {"data":[]}
main_dict['data'] = tempe_list
print(main_dict)
print(len(main_dict['data']))
csv_list.insert(0,['Sentence', 'Question', 'Answers'])
print(csv_list)
# Export JSON File
# with open('C:\\Users\\pylak\\Documents\\Fall_2018\\NLP\\PROJECT\\Output1.json', 'w') as outfile:
#     js.dump(main_dict, outfile)
#
# print('JSON file Created')

with open('C:\\Users\\pylak\\Documents\\Fall_2018\\NLP\\PROJECT\\Output4.csv', 'w', encoding='utf-8', newline="") as file:
    writer = csv.writer(file)
    writer.writerows(csv_list)

print('CSV file created')