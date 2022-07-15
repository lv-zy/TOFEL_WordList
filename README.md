# TOFEL_WordList

## 环境配置

建议使用python3.8环境运行

安装依赖： `pip install requests`

## 使用说明

 该脚本用于读取生词本collection中的单词，根据用户需求来生成未翻译和已翻译的单词本以便复习
 
 usage:
 
    python TOFEL_WordList.py [-h] [-n NUMS] [-r] [-s START] [-d END] [collection]
    
      1. collection ,Specify the path of collection
      
      2. -n ,define how many words in each word list.
      
      3. -r ,If selected, words will be chosen randomly from the collection;otherwise by default order
      
      4. -s ,Specify where to choose the words from the collection
      
      5. -d ,Specify the end of the collection to be chosen
      
      6. -h ,get help

随后在Output文件夹中生成单词本


   
