import argparse
import random
import requests
import json
import os
import re


def translate(word):
    '''Translate word using youdao api
        If failed,return None type
    '''
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        text = response.text
        list_trans = text
        result = json.loads(list_trans)
        result = result['translateResult'][0][0]['tgt']
        return result.strip()
    else:
        return None

def parse_augment():
    """
    Read args from the command line.
    usage:
    1. collection ,Specify the path of collection
    2. -n ,define how many words in each word list.
    3. -r ,If selected, words will be chosen randomly from the collection;otherwise by default order
    4. -s ,Specify where to choose the words from the collection
    5. -d ,Specify the end of the collection to be chosen

    """
    parser = argparse.ArgumentParser(
        prog = 'python TOFEL_WordList.py',
        description = 'A tool for reviewing English words'
    )
    parser.add_argument(
        'collection',
        type = str,
        default = './collection.txt',
        nargs = '?',
        help = 'The path of your collection.If not provided, collection.txt will be used.'
    )
    parser.add_argument(
        '-n', 
        default = 20,
        type = int,
        dest = 'nums',
        help = 'The number of words in each word list'
    )
    parser.add_argument(
        '-r',
        default = False,
        action = 'store_true',
        dest = 'random',
        help = 'If selected, words will be chosen randomly from the collection;otherwise by default order'
    )
    parser.add_argument(
        '-s',
        default = 1,
        type = int,
        dest = 'start',
        help = 'Specify where to choose the words from the collection'

    )
    parser.add_argument(
        '-d',
        type = int,
        default = -1,
        dest = 'end',
        help = 'Specify the end of the collection to be chosen'
    )
    return parser.parse_args()

def ReadWordsFromCollection(Collection_path : str, Start : int, End : int, Random : bool):
    '''Read the collection ,then return the list of words if successfully read,None if any error occurs.'''
    try:
        with open(Collection_path,'r') as f:
            words = list(filter(None, f.read().split("\n")))

            # examine the validity of some args
            words_count = len(words)
            if (End == -1): 
                End = words_count # default end
            if (0<Start and Start <= words_count and Start <= End):
                # split the word list
                words = words[Start-1 : End]
                if(Random):
                    random.shuffle(words)
                return words
            else:
                print("Invalid args:maybe the collection you choose is out of range")
                return None
    except:
        print('A error occurs when open collection')
        return None


def GenerateWordList(TargetWordList : list,count : int, MaxNum : int):
    # untranslated
    i = 1
    
    with open('./Output/untranslated_' + str(count) + '.txt','w') as fout:
        for x in TargetWordList:
            content = '第' + str(i) + '词组:' + x +'\n'
            fout.write(content)
            i += 1
            if (i > MaxNum):
                break
    i = 1
    # translated
    with open('./Output/translated_' + str(count) + '.txt','w') as fout:
        for x in TargetWordList:
            trans_result = None
            try:
                trans_result = translate(x)
            except:
                pass
            if(trans_result==None):
                content = '第' + str(i) + '词组:' + x + ":翻译失败" + '\n'
                fout.write(content)
                i += 1
                if (i > MaxNum):
                    break
            else:

                content = '第' + str(i) + '词组:' + x + ":" + trans_result +'\n'
                fout.write(content)
                i += 1
                if (i > MaxNum):
                    break
    pass

def get_seria():
    '''
    Get the latest seria of the data files
    '''
    index = 0
    for filename in os.listdir('./Output/'):
        group = re.findall(r'untranslated_(\w*?).txt',filename)
        if(group):
            temp_index = group[0]
            index = max(index,int(temp_index))
    return index+1





if __name__ == '__main__':
    if (not os.path.exists('./Output/')):
        os.system('mkdir .\\Output\\')

    args = parse_augment()
    
    

    if (args.random):
        for x in range(5):
            words = ReadWordsFromCollection(args.collection,args.start,args.end,args.random)
            GenerateWordList(words, get_seria(), args.nums)
        pass
    else:
        words = ReadWordsFromCollection(args.collection,args.start,args.end,args.random)
        GenerateWordList(words, get_seria(), args.nums)
        pass