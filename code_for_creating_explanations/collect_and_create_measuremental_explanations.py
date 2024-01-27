'measurements -> concepts -> bert'
#READ BOTH TODOS BELOW BEFORE STARTING
#CURRENTLY
#remove the looking for punct- skimmed the files with punct, there's one with ':4' -> change the numeric elif so that counts any measuremental unit with at least 1 digit, not all digits.


#trying to do the following:
#alongside printing a file of the measurements with < 2 measurements NOT IN numerical_leftovers (there are none)
#there should also be files of the difficult to categorise questions (have 'per', a number of stopword etc)
#rn doesn't work. fix errors, edit main functio nif need to (not sure)
#there is also a file of everything that isn't in the first two files.
#go through that and look for words that are OBVIOUSLY not measurements, stuff like 'usually
#which aren't stopwords. make a list of them and add them to the list of to fix manually
#then go through 10 of dev and test carefully in case mixed somethign.


#TODO NEXT:
#Tthe check function is complete based on the txt file 
#now i need to alter the function that calls it so that all the question
#where something labelled True is printed in the same file
#(if punctuation, #prints in one file, if number prints in anothe rfile - wait no, best#to print them all in the same file, that way they'll be after each other when#edit them manually)
#check that the automatic changes were made correctly
#then go throug hthe file, see if any more changes can make automatically
#if yes do them and check the file with stuff labelled True again, shoudl be 
#smaller now
#otherwise, make a file of manual changes like for numerical
#go through 10 from each of the other two and see if any more mistakes
#that not caught in the manual file (revolutions -> reovlutions per second etc)
#then make the explanations from the measurements . apply them to both clean_data and to numerical
#so have a version with both numerical and measuremental explanations
#make sure to say km*whatever is the same as N
#then conceptual explanations - see the plan i wrote on other vscode file
#for how to do that.
#the km*whatever being = to N still needs to be fixed, but i'll check if 
#there are any other such cases first


#all the ones missed were also in the numerical_leftovers. Once excluded the numerical_leftovers, no questions with 1 or less words foudn after numbers were found.
#left out the numerical leftovers, add those manually.
#the sentences added manually in numerical bit, check them for e.g. numbers that are in the options. also check the ones where the numbers weren't added manually/
#but when add all the explanations, should i remove the sentences that don't have all three explanations?


import json
import os
import nltk
import ast
import string
#nltk.download('punkt')
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stop_words.remove('m') #so that meter sign m is not flagged as a stop word
import dataset_remove_extra_entries as cl #in the order dev, test, train
MASKINPUTPATH = 'datasets'
TOANNOTATEINPUTPATH = 'numerical_data'
TOANNOTATEFILES = ['finalnumerical_dev.json', 'finalnumerical_test.json', 'finalnumerical_train.json']
NUMERICAL_LEFTOVERS_PATH = 'clean_data'
#original datasets
OUTPUTPATH = 'measuremental_to_numerical'
ALLEXPLANATIONS = 'numerical_measuremental'


def load_dataset(path, names_in_order_dev_test_train, format):#
    datasets_dict = {}
    labels = ['dev', 'test', 'train']
    for i, name in enumerate(names_in_order_dev_test_train):
        file_path = os.path.join(path, name)
        f = open(file_path)
        if format == 'json':
            datasets_dict[labels[i]] = json.load(f)
        elif format == 'txt':
            datasets_dict[labels[i]] = f
    return datasets_dict


#############################  PART 1: CHECKING FOR DIFFICULT TO CATEGORISE QUESTIONS AND THAT AUTOMATIC CATEGORISATION WORKS WELL##########################
#checks if the measurement automatically selected or the question in general falls in one of several categories
def check_possible_measurement(name, question_index, word_index, possible_measurement, question_list):
    false_positives = {'train': [], 'dev': [], 'test': []}
    assert possible_measurement == question_list[word_index]
    per = False
    is_stopword = False
    number = False
    is_punctuation = False
    if question_index not in false_positives[name]:
        if possible_measurement == 'miles':
            if question_list[word_index+1] == 'per':
                if question_list[word_index+2] == 'hour':
                    possible_measurement = 'miles per hour'
                else:
                    print(question_list, possible_measurement, question_index)
                    raise Exception
        elif possible_measurement == 'mega':
            if question_list[word_index+1] in ['N.', 'N']:
                possible_measurement = 'mega N'
            else:
                print('mega', question_list, possible_measurement, question_index)
                raise Exception
        elif possible_measurement == 'revolutions':
            if question_list[word_index+1] == 'per':
                if question_list[word_index+2] == 'second':
                    possible_measurement = 'revolutions per second'
                else:
                    print('revolutions per', question_list, possible_measurement, question_index)
                    raise Exception
        elif possible_measurement == 'km':
            if question_list[word_index+1] == 'per':
                if question_list[word_index+2] == 'hour':
                    possible_measurement = 'km per hour'
                else:
                    print('km per', question_list, possible_measurement, question_index)
                    raise Exception
        elif possible_measurement == 'miles':
            if question_list[word_index+1] == 'per':
                if question_list[word_index+2] == 'hour':
                    possible_measurement = 'miles per hour'
                else:
                    print('miles per', question_list, possible_measurement, question_index)
                    raise Exception
        elif possible_measurement == 'foot':
            if question_list[word_index+1] == 'per':
                if question_list[word_index+2] == 'second':
                    possible_measurement = 'foot per second'
                else:
                    print('foot per', question_list, possible_measurement, question_index)
                    raise Exception
        elif possible_measurement == 'meter':
            if question_list[word_index+1] == 'per':
                if question_list[word_index+2] == 'minute':
                    possible_measurement = 'meter per minute'
                else:
                    print('meter per', question_list, possible_measurement, question_index)
                    raise Exception

        elif possible_measurement == 'degree':
            if question_list[word_index+1] in ['fahrenheit', 'celsius', '\u00e7', 'ç']:
                possible_measurement = f'degree {question_list[word_index+1]}'
            else:
                print('degree', question_list, possible_measurement, question_index)
        elif possible_measurement in stop_words:
            is_stopword = True
        else:
            for c in possible_measurement:
                if c.isnumeric():
                    number = True
        '''elif 'per' in question_list:
            per = True
            print('per', question_list, possible_measurement, question_index)'''
        if possible_measurement[-1] == '.' or possible_measurement[-1] == ',':
            if len(possible_measurement) > 1:
                if possible_measurement == 'g.':
                    possible_measurement = 'g'
                elif possible_measurement == 'm.':
                    possible_measurement = 'm'
                elif possible_measurement == 'N.':
                    possible_measurement = 'N'
                else:
                    print('punct', question_list, possible_measurement, question_index)
    return possible_measurement, per, is_stopword, number, is_punctuation


def measurements_identify_leftovers(dataset, name, difficult_to_numerically_categorise, clean):#dev train or test not all 3 together
    print(f'Processing {name} dataset')
    two_or_more =[]
    one_or_less =[]
    measuremental_leftovers =[]#questions where a measurement is a stopword, punctuation, number, or the word 'per' is in the sentence (and it's not one of the examples fixed in the check function). Also if there is a number at the very end of a sentence as tokenizer by word_tokenize, it's added here too.
    for ei, entry in enumerate(dataset):
        entry_list = [] #the two (or more or less) numbers in the question
        question_string = entry['question_mask']
        option_1_string = entry['Option1']
        option_2_string = entry['Option2']
        question_list = word_tokenize(question_string) #question_string.split(' ')
        option_1_list = word_tokenize(option_1_string)
        option_2_list = word_tokenize(option_2_string)
        difficult_to_measurementally_categorise = []
        new_measurement = False
        for text in [question_list, option_1_list, option_2_list]:
            for qi, word in enumerate(text):
                if text == question_list:
                    if text[qi-2] == '[' and text[qi-1] == 'Num' and word == ']':
                        if qi != len(text)-1:
                            possible_measurement = text[qi+1]
                            new_measurement = True
                        else:
                            difficult_to_measurementally_categorise.append('[Num] at the end of the sentence')
                else:
                    try:
                        num = float(word)
                        if qi != len(text) -1:
                            possible_measurement = text[qi+1]
                            new_measurement = True
                        else:
                            difficult_to_measurementally_categorise.append('[Num] at the end of the sentence')
                    except:
                        pass
                if new_measurement:
                    possible_measurement, per, is_stopword, number, is_punctuation = check_possible_measurement(name, ei, qi+1, possible_measurement, text)
                    entry_list.append(possible_measurement)
                    if per:
                        difficult_to_measurementally_categorise.append('per')
                    elif is_punctuation:
                        difficult_to_measurementally_categorise.append('punct')
                    elif number:
                        difficult_to_measurementally_categorise.append('num')
                    elif is_stopword:
                        difficult_to_measurementally_categorise.append('stopword')
                new_measurement = False
        if ei not in difficult_to_numerically_categorise:
            if difficult_to_measurementally_categorise:
                measuremental_leftovers.append((ei, entry['question'],option_1_string, option_2_string, entry_list, difficult_to_measurementally_categorise))
            elif len(entry_list) > 1:
                two_or_more.append((entry['question'], entry_list))
            else:
                one_or_less.append((entry['question'], entry_list))
    print(f'{len(two_or_more)} automatically classified, {len(measuremental_leftovers)} printed to be manually classified as words found are not measurements, {len(one_or_less)} printed to be manually classified as less than 2 measurements were found. {len(difficult_to_numerically_categorise)} were excluded from the start as they had to be numerically classified manually (so they will be measurementally classified manually as well) Total: {len(measuremental_leftovers) + len(two_or_more) + len(one_or_less) + len(difficult_to_numerically_categorise)}')
    measuremental_checking_path = os.path.join(OUTPUTPATH, f'measuremental_checking{name}.json')
    missing_measuremental_path = os.path.join(OUTPUTPATH, f'one_or_less_measurements{name}.txt')
    measuremental_output_path = os.path.join(OUTPUTPATH, f'measuremental_{name}.json')
    measuremental_leftovers_path = os.path.join(OUTPUTPATH, f'hard_to_categorise_measurements{name}.json')
    with open(measuremental_checking_path, 'w') as check:
        for item in two_or_more:
            print(f'{item[0]}\t{item[1]}', file=check)
    with open(missing_measuremental_path, 'w') as missing:
        for item in one_or_less:
            print(f'{item[0]}\t{item[1]}', file=missing)
    with open(measuremental_output_path, 'w') as out:
        json.dump(clean, out)
    with open(measuremental_leftovers_path, 'w') as leftovers:
        for item in measuremental_leftovers:
            print(f'{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\t{item[4]}\t{item[5]}', file=leftovers)

#######################################PART 2: CREATING FILES WITH MEASUREMENTAL EXPLANATIONS#############################################################

def measurements_file_creator(dataset, name, clean, measuremental_manual_additions):#dev train or test not all 3 together
    print(f'Processing {name} dataset')
    count = 0
    no_explanation = 0
    for ei, entry in enumerate(dataset):
        if str(ei) not in measuremental_manual_additions:
            question_string = entry['question_mask']
            option_1_string = entry['Option1']
            option_2_string = entry['Option2']
            #print(question_string)
            question_list = word_tokenize(question_string) #question_string.split(' ')
            option_1_list = word_tokenize(option_1_string)
            option_2_list = word_tokenize(option_2_string)
            new_measurement = False
            entry_list = [] #the two (or more or less) numbers in the question
            for text in [question_list, option_1_list, option_2_list]:
                for qi, word in enumerate(text):
                    if text == question_list:
                        if text[qi-2] == '[' and text[qi-1] == 'Num' and word == ']':
                            if qi != len(text)-1:
                                possible_measurement = text[qi+1]
                                new_measurement = True
                    else:
                        try:
                            num = float(word)
                            if qi != len(text) -1:
                                possible_measurement = text[qi+1]
                                new_measurement = True
                        except:
                            pass
                    if new_measurement:
                        possible_measurement, per, is_stopword, number, is_punctuation = check_possible_measurement(name, ei, qi+1, possible_measurement, text)
                        entry_list.append(possible_measurement)
                        new_measurement = False
        else:
            entry_list = measuremental_manual_additions[str(ei)]
        if entry_list != None:
            if len(entry_list) == 2:
                m_1 = entry_list[0]
                m_2 = entry_list[1]
                #deals with one number which was raising an error
                are_the_same = are_2_measurements_the_same(m_1, m_2)
                if are_the_same:
                    new_data = f'{m_1} and {m_2} are the same measurement unit.'
                else:
                    new_data = f'{m_1} and {m_2} are different measurement units.'
                clean[ei]['measuremental_explanation'] = new_data
                count+=1
            #creates explanations comparing 3 or more numbers.
            elif len(entry_list) > 2:
                entry_number_list = []
                for i,  unit1 in enumerate(entry_list[:-1]):
                    for unit2 in entry_list[i+1:]:
                        one_comparison = []
                        start = f'{unit1} and {unit2} are '
                        are_the_same = are_2_measurements_the_same(unit1, unit2)
                        if are_the_same:
                            one_comparison.append('the same measurement unit')
                        else:
                            one_comparison.append('different measurement units')
                        if len(one_comparison) > 1:
                            measurement_phrase = ', '.join(one_comparison[:-1])
                            measurement_phrase = f'{start}{measurement_phrase} and {one_comparison[-1]}'
                        else:
                            measurement_phrase = f'{start}{one_comparison[-1]}'
                        entry_number_list.append(measurement_phrase)
                measurement_sent = ', '.join(entry_number_list[:-1])
                measurement_sent += f' and {entry_number_list[-1]}.'
                clean[ei]['measuremental_explanation'] = measurement_sent
                count+=1
            elif len(entry_list) < 2:
                print(ei, question_string, entry['Option1'], entry['Option2'], entry_list)
        else:
            no_explanation += 1
    measuremental_path = os.path.join(OUTPUTPATH, f'final{ALLEXPLANATIONS}_{name}.json')#os.path.join(OUTPUTPATH, name)
    with open(measuremental_path, 'w') as f2:
        json.dump(clean, f2)
    print(f'{count} measuremental explanations added to and {no_explanation} explanations not added to the {name} dataset of {len(clean)} questions. {len(clean)-count-no_explanation} explanations unaccounted for.')

#takes two measurements e.g. miles per hour, cm, centimetres, and checks if they are the same
def are_2_measurements_the_same(m1, m2):
        are_the_same = [{'cm', 'cms', 'centi-meters', 'centimeters', 'centimeter', 'centimetres'}, {'mins', 'minutes', 'minute', 'min', 'mintues'}, {'celcius', 'celsius', '\u00e7', 'ç'}, {'secs', 'seconds', 'second'}, {'kg*m*s^-2', 'N'}, {'foot'}, {'feet'}]
        m1 = m1.lower().split(' ')
        m2 = m2.lower().split(' ')
        if m1 == m2:
            return True
        for s in are_the_same:
            if set(m1 + m2) <= s:
                return True
        new_m1 = []
        new_m2 = []
        plural = False
        for word in m1:
            if word[-1] == 's':
                word = word[:-1]
                plural = True
                new_m1.append(word)
            else:
                new_m1.append(word)
        for word in m2:
            if word[-1] == 's':
                plural = True
                word = word[:-1]
                new_m2.append(word)
            else:
                new_m2.append(word)
        if not plural:
            return False
        elif new_m1 == new_m2:
            return True
        for s in are_the_same:
            if set(new_m1 + new_m2) <= s:
                return True
        es = False
        es_m1 = []
        es_m2 = []
        for word in m1:
            if word[-2:] == 'es':
                word = word[:-2]
                es = True
                es_m1.append(word)
            else:
                es_m1.append(word)
        for word in m2:
            if word[-2:] == 'es':
                es = True
                word = word[:-2]
                es_m2.append(word)
            else:
                es_m2.append(word)
        if not es:
            return False
        elif es_m1 == es_m2:
            return True
        for s in are_the_same:
            if set(es_m1 + es_m2) <= s:
                return True 
        #print(m1, m2)
        return False



def add_measuremental_manual_explanations():
    manual_additions_path = os.path.join(MASKINPUTPATH, 'measuremental_leftovers.txt')
    with open(manual_additions_path) as manual_measurement_file:
        train_test_or_dev = None
        train = {}
        dev = {}
        test = {}
        for line in manual_measurement_file:
            line = line.rstrip().split('\t')
            if len(line) == 1 and line[0] in ['train', 'dev', 'test']:
                if line[0] == 'train':
                    train_test_or_dev = 'train'
                elif line[0] == 'test':
                    train_test_or_dev = 'test'
                elif line[0] == 'dev':
                    train_test_or_dev = 'dev'
            else:
                index = line[0]
                if train_test_or_dev == 'train':
                    if len(line) > 1:
                        train[index] = line[1:]
                    else:
                        train[index] = None
                elif train_test_or_dev == 'test':
                    if len(line) > 1:
                        test[index] = line[1:]
                    else:
                        test[index] = None
                if train_test_or_dev == 'dev':
                    if len(line) > 1:
                        dev[index] = line[1:]
                    else:
                        dev[index] = None
        measuremental_manual_additions = [dev, test, train]
        #print(measuremental_manual_additions)
        return measuremental_manual_additions



def general_main(new_0_or_annotated_1_data):
    datasets = load_dataset(MASKINPUTPATH, ['QQA_dev.json', 'QQA_test.json', 'QQA_train.json'], 'json')
    if new_0_or_annotated_1_data:
        clean_datasets = load_dataset(TOANNOTATEINPUTPATH, TOANNOTATEFILES, 'json')
        clean_dev = clean_datasets['dev']
        clean_train = clean_datasets['train']
        clean_test = clean_datasets['test']
    else:
        clean_dev = cl.clean_datasets[0]
        clean_test = cl.clean_datasets[1]
        clean_train = cl.clean_datasets[2]
    return datasets, clean_dev, clean_test, clean_train

def part_1_main():
    print('Running part 1...')
    datasets, clean_dev, clean_test, clean_train = general_main(0)
    difficult_to_numerically_categorise = {'dev': [4, 6, 9, 10, 18, 21, 35, 37, 38, 39, 41, 43, 53, 55, 56, 71, 72, 77, 78], 'test': [7, 12, 51, 54, 87, 98, 107, 157], 'train': [0, 11, 17, 24, 95, 110, 182, 197, 282, 291, 299, 366, 382, 392, 402, 424, 438, 511,518]}
    measurements_identify_leftovers(datasets['train'], 'train', difficult_to_numerically_categorise['train'], clean_train)
    measurements_identify_leftovers(datasets['dev'], 'dev', difficult_to_numerically_categorise['dev'], clean_dev)
    measurements_identify_leftovers(datasets['test'], 'test', difficult_to_numerically_categorise['test'], clean_test)

def part_2_main():
    print('Running part 2...')
    new_or_annotated_data = None
    while new_or_annotated_data != '0' and new_or_annotated_data != '1':
        new_or_annotated_data = input('Do you want to add measuremental explanations to a new dataset that has no explanations yet (0) or to a dataset with som explanations already added (1)?')
    datasets, clean_dev, clean_test, clean_train = general_main(new_or_annotated_data)
    measuremental_manual_additions = add_measuremental_manual_explanations()
    measurements_file_creator(datasets['train'], 'train', clean_train, measuremental_manual_additions[2])
    measurements_file_creator(datasets['dev'], 'dev', clean_dev, measuremental_manual_additions[0])
    measurements_file_creator(datasets['test'], 'test', clean_test, measuremental_manual_additions[1])

part_1_main()
part_2_main()

#made a list of question difficult to numerically categorise.
#excluded those, got the masked sentence, got words after masked numbers. checked if any sentences not in the above mentioned category where less than 2 found after [num] - were none
#printed rest of questions and the 'measurements' foudn. will go through them to see if any good. will edit the json file since it has colour coding (take screenshot) then
#copy to a text file

def run_through_measurements(measurement_list_and_questions, dataset_to_update):
    for line in measurement_list_and_questions:
        line = line.rstrip()
        line = line.split('\t')
        print(line)
        if len(line) != 2:
            print(line)
            raise Exception
        measurement_list = ast.literal_eval(line[1])
        print(measurement_list)
        break
def check():
    measurement_list_and_questions = load_dataset('measuremental_data', ['measuremental_checkingdev.txt', 'measuremental_checkingtest.txt', 'measuremental_checkingtrain.txt'], 'txt')
    train_dataset_with_measurements = run_through_measurements(measurement_list_and_questions['train'], 'hello')

#check()

#wait. the test set shouldn't have explanations right? right? email. or ask meriem.'''

#adding measurements to clean data
'''on3 add_measurements.py
[nltk_data] Downloading package stopwords to
[nltk_data]     C:\Users\Maria\AppData\Roaming\nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
Running part 1...
Processing train dataset
517 automatically classified, 28 printed to be manually classified as words found are not measurements, 0 printed to be manually classified as less than 2 measurements were found. 19 were excluded from the start as they had to be numerically classified manually (so they will be measurementally classified manually as well) Total: 564
Processing dev dataset
58 automatically classified, 4 printed to be manually classified as words found are not measurements, 0 printed to be manually classified as less than 2 measurements were found. 19 were excluded from the start as they had to be numerically classified manually (so they will be measurementally classified manually as well) Total: 81
Processing test dataset
146 automatically classified, 8 printed to be manually classified as words found are not measurements, 0 printed to be manually classified as less than 2 measurements were found. 8 were excluded from the start as they had to be numerically classified manually (so they will be measurementally classified manually as well) Total: 162
Running part 2...
Processing train dataset
553 measuremental explanations added to and 11 explanations not added to the train dataset of 564 questions. 0 explanations unaccounted for.
Processing dev dataset
68 measuremental explanations added to and 13 explanations not added to the dev dataset of 81 questions. 0 explanations unaccounted for.
Processing test dataset
155 measuremental explanations added to and 7 explanations not added to the test dataset of 162 questions. 0 explanations unaccounted for.'''


#adding measurements to data wit hnumerical explanations
'''553 measuremental explanations added to and 11 explanations not added to the train dataset of 564 questions. 0 explanations unaccounted for.
Processing dev dataset
68 measuremental explanations added to and 13 explanations not added to the dev dataset of 81 questions. 0 explanations unaccounted for.
Processing test dataset
155 measuremental explanations added to and 7 explanations not added to the test dataset of 162 questions. 0 explanations unaccounted for.'''