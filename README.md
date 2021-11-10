# **KU - DB Forensics - SQLite Dataset**
Junwoo Seo / 2020010674

### Tools & Environment
Windows 10  
Python 3.8 (x64)  
SQLite Expert Personal 5.4 (x64)  
Hex Editor  

## DataBase Schema
To create a database that meets the conditions of the common mission, the schema is set as the messenger DB.  
The DB schema  is as follows.

#### messages table
| FromID | ForwardID | Message | Media | \_time|
| ------ | --------- | ------- | ----- | ----- |
| 1096 | 7077 | blahblah | image.jpg | 2021-11-09:21:00:06 |
| ... | ... | ... | ... | ... | ... |

#### users table (Primary Key : UserID)
| **UserID** | UserName | Phone | ProfileImage | Sex | UpdateTime |
| ------ | --------- | ------- | ----- | ----- | ----- |
| 1096 | Jason | 010-0000-0000 | image.jpg | 1 | 2021-07-15:12:24:35 |
| ... | ... | ... | ... | ... | ... | ... |


## Random Data Generation
Basically, all data were randomly generated.  
User ID : a 4-digit number between 1000 and 10000 was given  
Message : was composed by randomly selecting 3 from the most used 1000 words.  
Media : it is assumed that the user sends a photo file through messenger, and it is randomly selected from the [casia dataset](https://www.kaggle.com/sophatvathana/casia-dataset). Since not all messages contain images, the degree to which messages contain images is specified.  
\_time : the time the message was sent, and was randomly selected from the time from January 1, 2020 to the present.


```python
def data_rand_generate():
    FromID = random.randint(1000,10000)
    ForwardID = random.randint(1000,10000)
    Message = ' '.join(random.sample(top_1000_word_list, 3))
    Media = blob_rand_generate(1) # seed = 1, means that there is a 10% chance to include an image in the message row.
    _time = date_rand_generate() # datetime.fromtimestamp()

    return FromID, ForwardID, Message, Media, _time
```
```python
def date_rand_generate():
    start = datetime(2020, 1, 1, 00, 00, 00)
    delta = datetime.now().year - 2020 + 1
    end = start + timedelta(days=365 * delta)

    return (start+(end-start)*random.random()).timestamp()
```
```python
def blob_rand_generate(seed):
    if random.randint(0,10) < seed:
        file_path = ["C:\\Users\\junus\\CASIA1\\Au\\*.jpg"]
        images = glob.glob(random.choice(file_path))
        rand_img = random.choice(images)
        with open(rand_img, 'rb') as file:
            binData = file.read()
    else:
        binData=''
        
    return binData
```

## NIST CFTT’s SQLite Forensics Tool Test Cases  
### SFT-01: SQLite header parsing - encoding_type: UTF8, journal_mode: WAL 
```python
def db_generate(db_name, journal_mode, encoding, page_size, rows):
    global top_1000_word_list
    
    data = []
    top_1000_word_list = ['a', 'ability', 'able', 'about', 'above', 'accept', 'according', 'account', 'across', 'act', 'action', 'activity', 'actually', 'add', 'address', 'administration', 'admit', 'adult', 'affect', 'after', 'again', 'against', 'age', 'agency', 'agent', 'ago', 'agree', 'agreement', 'ahead', 'air', 'all', 'allow', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'American', 'among', 'amount', 'analysis', 'and', 'animal', 'another', 'answer', 'any', 'anyone', 'anything', 'appear', 'apply', 'approach', 'area', 'argue', 'arm', 'around', 'arrive', 'art', 'article', 'artist', 'as', 'ask', 'assume', 'at', 'attack', 'attention', 'attorney', 'audience', 'author', 'authority', 'available', 'avoid', 'away', 'baby', 'back', 'bad', 'bag', 'ball', 'bank', 'bar', 'base', 'be', 'beat', 'beautiful', 'because', 'become', 'bed', 'before', 'begin', 'behavior', 'behind', 'believe', 'benefit', 'best', 'better', 'between', 'beyond', 'big', 'bill', 'billion', 'bit', 'black', 'blood', 'blue', 'board', 'body', 'book', 'born', 'both', 'box', 'boy', 'break', 'bring', 'brother', 'budget', 'build', 'building', 'business', 'but', 'buy', 'by', 'call', 'camera', 'campaign', 'can', 'cancer', 'candidate', 'capital', 'car', 'card', 'care', 'career', 'carry', 'case', 'catch', 'cause', 'cell', 'center', 'central', 'century', 'certain', 'certainly', 'chair', 'challenge', 'chance', 'change', 'character', 'charge', 'check', 'child', 'choice', 'choose', 'church', 'citizen', 'city', 'civil', 'claim', 'class', 'clear', 'clearly', 'close', 'coach', 'cold', 'collection', 'college', 'color', 'come', 'commercial', 'common', 'community', 'company', 'compare', 'computer', 'concern', 'condition', 'conference', 'Congress', 'consider', 'consumer', 'contain', 'continue', 'control', 'cost', 'could', 'country', 'couple', 'course', 'court', 'cover', 'create', 'crime', 'cultural', 'culture', 'cup', 'current', 'customer', 'cut', 'dark', 'data', 'daughter', 'day', 'dead', 'deal', 'death', 'debate', 'decade', 'decide', 'decision', 'deep', 'defense', 'degree', 'Democrat', 'democratic', 'describe', 'design', 'despite', 'detail', 'determine', 'develop', 'development', 'die', 'difference', 'different', 'difficult', 'dinner', 'direction', 'director', 'discover', 'discuss', 'discussion', 'disease', 'do', 'doctor', 'dog', 'door', 'down', 'draw', 'dream', 'drive', 'drop', 'drug', 'during', 'each', 'early', 'east', 'easy', 'eat', 'economic', 'economy', 'edge', 'education', 'effect', 'effort', 'eight', 'either', 'election', 'else', 'employee', 'end', 'energy', 'enjoy', 'enough', 'enter', 'entire', 'environment', 'environmental', 'especially', 'establish', 'even', 'evening', 'event', 'ever', 'every', 'everybody', 'everyone', 'everything', 'evidence', 'exactly', 'example', 'executive', 'exist', 'expect', 'experience', 'expert', 'explain', 'eye', 'face', 'fact', 'factor', 'fail', 'fall', 'family', 'far', 'fast', 'father', 'fear', 'federal', 'feel', 'feeling', 'few', 'field', 'fight', 'figure', 'fill', 'film', 'final', 'finally', 'financial', 'find', 'fine', 'finger', 'finish', 'fire', 'firm', 'first', 'fish', 'five', 'floor', 'fly', 'focus', 'follow', 'food', 'foot', 'for', 'force', 'foreign', 'forget', 'form', 'former', 'forward', 'four', 'free', 'friend', 'from', 'front', 'full', 'fund', 'future', 'game', 'garden', 'gas', 'general', 'generation', 'get', 'girl', 'give', 'glass', 'go', 'goal', 'good', 'government', 'great', 'green', 'ground', 'group', 'grow', 'growth', 'guess', 'gun', 'guy', 'hair', 'half', 'hand', 'hang', 'happen', 'happy', 'hard', 'have', 'he', 'head', 'health', 'hear', 'heart', 'heat', 'heavy', 'help', 'her', 'here', 'herself', 'high', 'him', 'himself', 'his', 'history', 'hit', 'hold', 'home', 'hope', 'hospital', 'hot', 'hotel', 'hour', 'house', 'how', 'however', 'huge', 'human', 'hundred', 'husband', 'I', 'idea', 'identify', 'if', 'image', 'imagine', 'impact', 'important', 'improve', 'in', 'include', 'including', 'increase', 'indeed', 'indicate', 'individual', 'industry', 'information', 'inside', 'instead', 'institution', 'interest', 'interesting', 'international', 'interview', 'into', 'investment', 'involve', 'issue', 'it', 'item', 'its', 'itself', 'job', 'join', 'just', 'keep', 'key', 'kid', 'kill', 'kind', 'kitchen', 'know', 'knowledge', 'land', 'language', 'large', 'last', 'late', 'later', 'laugh', 'law', 'lawyer', 'lay', 'lead', 'leader', 'learn', 'least', 'leave', 'left', 'leg', 'legal', 'less', 'let', 'letter', 'level', 'lie', 'life', 'light', 'like', 'likely', 'line', 'list', 'listen', 'little', 'live', 'local', 'long', 'look', 'lose', 'loss', 'lot', 'love', 'low', 'machine', 'magazine', 'main', 'maintain', 'major', 'majority', 'make', 'man', 'manage', 'management', 'manager', 'many', 'market', 'marriage', 'material', 'matter', 'may', 'maybe', 'me', 'mean', 'measure', 'media', 'medical', 'meet', 'meeting', 'member', 'memory', 'mention', 'message', 'method', 'middle', 'might', 'military', 'million', 'mind', 'minute', 'miss', 'mission', 'model', 'modern', 'moment', 'money', 'month', 'more', 'morning', 'most', 'mother', 'mouth', 'move', 'movement', 'movie', 'Mr', 'Mrs', 'much', 'music', 'must', 'my', 'myself', 'name', 'nation', 'national', 'natural', 'nature', 'near', 'nearly', 'necessary', 'need', 'network', 'never', 'new', 'news', 'newspaper', 'next', 'nice', 'night', 'no', 'none', 'nor', 'north', 'not', 'note', 'nothing', 'notice', 'now', 'n\'t', 'number', 'occur', 'of', 'off', 'offer', 'office', 'officer', 'official', 'often', 'oh', 'oil', 'ok', 'old', 'on', 'once', 'one', 'only', 'onto', 'open', 'operation', 'opportunity', 'option', 'or', 'order', 'organization', 'other', 'others', 'our', 'out', 'outside', 'over', 'own', 'owner', 'page', 'pain', 'painting', 'paper', 'parent', 'part', 'participant', 'particular', 'particularly', 'partner', 'party', 'pass', 'past', 'patient', 'pattern', 'pay', 'peace', 'people', 'per', 'perform', 'performance', 'perhaps', 'period', 'person', 'personal', 'phone', 'physical', 'pick', 'picture', 'piece', 'place', 'plan', 'plant', 'play', 'player', 'PM', 'point', 'police', 'policy', 'political', 'politics', 'poor', 'popular', 'population', 'position', 'positive', 'possible', 'power', 'practice', 'prepare', 'present', 'president', 'pressure', 'pretty', 'prevent', 'price', 'private', 'probably', 'problem', 'process', 'produce', 'product', 'production', 'professional', 'professor', 'program', 'project', 'property', 'protect', 'prove', 'provide', 'public', 'pull', 'purpose', 'push', 'put', 'quality', 'question', 'quickly', 'quite', 'race', 'radio', 'raise', 'range', 'rate', 'rather', 'reach', 'read', 'ready', 'real', 'reality', 'realize', 'really', 'reason', 'receive', 'recent', 'recently', 'recognize', 'record', 'red', 'reduce', 'reflect', 'region', 'relate', 'relationship', 'religious', 'remain', 'remember', 'remove', 'report', 'represent', 'Republican', 'require', 'research', 'resource', 'respond', 'response', 'responsibility', 'rest', 'result', 'return', 'reveal', 'rich', 'right', 'rise', 'risk', 'road', 'rock', 'role', 'room', 'rule', 'run', 'safe', 'same', 'save', 'say', 'scene', 'school', 'science', 'scientist', 'score', 'sea', 'season', 'seat', 'second', 'section', 'security', 'see', 'seek', 'seem', 'sell', 'send', 'senior', 'sense', 'series', 'serious', 'serve', 'service', 'set', 'seven', 'several', 'sex', 'sexual', 'shake', 'share', 'she', 'shoot', 'short', 'shot', 'should', 'shoulder', 'show', 'side', 'sign', 'significant', 'similar', 'simple', 'simply', 'since', 'sing', 'single', 'sister', 'sit', 'site', 'situation', 'six', 'size', 'skill', 'skin', 'small', 'smile', 'so', 'social', 'society', 'soldier', 'some', 'somebody', 'someone', 'something', 'sometimes', 'son', 'song', 'soon', 'sort', 'sound', 'source', 'south', 'southern', 'space', 'speak', 'special', 'specific', 'speech', 'spend', 'sport', 'spring', 'staff', 'stage', 'stand', 'standard', 'star', 'start', 'state', 'statement', 'station', 'stay', 'step', 'still', 'stock', 'stop', 'store', 'story', 'strategy', 'street', 'strong', 'structure', 'student', 'study', 'stuff', 'style', 'subject', 'success', 'successful', 'such', 'suddenly', 'suffer', 'suggest', 'summer', 'support', 'sure', 'surface', 'system', 'table', 'take', 'talk', 'task', 'tax', 'teach', 'teacher', 'team', 'technology', 'television', 'tell', 'ten', 'tend', 'term', 'test', 'than', 'thank', 'that', 'the', 'their', 'them', 'themselves', 'then', 'theory', 'there', 'these', 'they', 'thing', 'think', 'third', 'this', 'those', 'though', 'thought', 'thousand', 'threat', 'three', 'through', 'throughout', 'throw', 'thus', 'time', 'to', 'today', 'together', 'tonight', 'too', 'top', 'total', 'tough', 'toward', 'town', 'trade', 'traditional', 'training', 'travel', 'treat', 'treatment', 'tree', 'trial', 'trip', 'trouble', 'true', 'truth', 'try', 'turn', 'TV', 'two', 'type', 'under', 'understand', 'unit', 'until', 'up', 'upon', 'us', 'use', 'usually', 'value', 'various', 'very', 'victim', 'view', 'violence', 'visit', 'voice', 'vote', 'wait', 'walk', 'wall', 'want', 'war', 'watch', 'water', 'way', 'we', 'weapon', 'wear', 'week', 'weight', 'well', 'west', 'western', 'what', 'whatever', 'when', 'where', 'whether', 'which', 'while', 'white', 'who', 'whole', 'whom', 'whose', 'why', 'wide', 'wife', 'will', 'win', 'wind', 'window', 'wish', 'with', 'within', 'without', 'woman', 'wonder', 'word', 'work', 'worker', 'world', 'worry', 'would', 'write', 'writer', 'wrong', 'yard', 'yeah', 'year', 'yes', 'yet', 'you', 'young', 'your', 'yourself']    

    for i in range(0,rows):
        data.append(data_rand_generate())
        
    if os.path.exists(db_name):
        os.remove(db_name)

    con = sqlite3.connect(db_name, check_same_thread=False)
    cur = con.cursor()
    cur.execute(f'PRAGMA journal_mode={journal_mode}')
    cur.execute(f'PRAGMA encoding={encoding}')
    cur.execute(f'PRAGMA page_size={page_size}')
    cur.execute("CREATE TABLE messages (FromID INT, ForwardID INT, Message TEXT, Media BLOB, _time REAL)")
    sql = "INSERT INTO messages (FromID, ForwardID, Message, Media, _time) VALUES (?, ?, ?, ?, ?)"
    cur.executemany(sql, data)
    con.commit()
    con.close()
```
```python   
db_generate('SFT-01-UTF8-WAL.sqlite', 'wal', 'UTF8', 4096, 100)
```


In SFT-01-UTF8-WAL.sqlite, roll back journal is set to WAL. Since the commit is normally completed, sqlite-wal file is not created. To create -wal, we need to create an additional query and raise an error. In this case, -wal file will by empty. In order for a query before committing to be saved in -wal, an error must be generated before committing. The attached -wal file was created using this method, and in this case, the db file will be empty because it does not receive any commits.


### SFT-01: SQLite header parsing - encoding_type: UTF16be, journal_mode: persist
```python   
db_generate('SFT-01-UTF16BE-PERSIST.sqlite', 'persist', 'UTF16BE', 1024, 100)
```

### SFT-01: SQLite header parsing - encoding_type: UTF16le, journal_mode: off
```python   
db_generate('SFT-01-UTF16LE-OFF.sqlite', 'OFF', 'UTF16LE', 8192, 100)
```

### SFT-03: SQLite Recoverable Rows - journal_mode: persist
```python   
def data_rand_delete(db_name, delete_row):
    con = sqlite3.connect(db_name, check_same_thread=False)
    cur = con.cursor()    
    total_row = cur.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    delete_list = random.sample(range(1, total_row), delete_row)
    delete_list = [[i] for i in (delete_list)]
    
    sql = "DELETE FROM messages WHERE rowid=?"
    cur.executemany(sql, delete_list)
    con.commit()
    con.close()
```
```python   
def data_rand_modify(db_name, modify_row):
    con = sqlite3.connect(db_name, check_same_thread=False)
    cur = con.cursor()    
    sql = f"UPDATE messages SET Message='!!!!!!!MODIFIED!!!!!!!' WHERE messages.rowid IN (SELECT rowid FROM messages ORDER BY RANDOM() LIMIT {modify_row})"
    cur.execute(sql)
    con.commit()
    con.close()
```
```python   
db_generate('SFT-03-PERSIST.sqlite', 'persist', 'UTF8', 4096, 2000)
data_rand_delete('SFT-03-PERSIST.sqlite', 100)
data_rand_modify('SFT-03-PERSIST.sqlite', 100)
```
data_rand_delete() : Deletes the specified number of rows from all rows.  
data_rand_modify() : Modifies the message field of the specified number of rows in all rows to “!!!!!!!MODIFIED!!!!!!!”.  

### SFT-03: SQLite Recoverable Rows - journal_mode: wal
```python   
db_generate('SFT-03-WAL.sqlite', 'wal', 'UTF8', 4096, 2000)
data_rand_modify('SFT-03-WAL.sqlite', 100)
data_rand_delete('SFT-03-WAL.sqlite', 100)
con = sqlite3.connect('SFT-03-WAL.sqlite', check_same_thread=False)
cur = con.cursor()
cur.execute("SELECT * FROM messages")
sys.exit("Error!!!")
```

According to the manual of [sqlite3](https://docs.python.org/2/library/sqlite3.html#controlling-transactions) modules used for automation scripts, the sqlite3 opens transactions implicitly before a Data Modification Language statement, and commits transactions implicity befor a non-DML, non-query statement. Therefore, a separate begin-end operation is not used. To implement a situation that meets the condition, an error occurred after executing the delete function. At this time, there is no uncommitted query, so -wal file is empty.

### SFT-05 : Schema Reporting
![image](https://user-images.githubusercontent.com/31686076/141146968-202e52b6-45c1-49c1-b8aa-0ab34c496fdd.png)  
As with the data generation above, the data of the SFT-05 item was also randomly generated. 
User ID : a 4-digit number between 1000 and 10000 was given  
UserName : randomly selected word from the most used 1000 words(might look weird in this case).  
Phone : 010-0000-0000 type data is randomly generated.  
ProfileImage : same concept as the media field of the messages table.  
Sex : 0: Male, 1: Female  
UpdateTime : the time when the user profile was updated. 


## Additional Mission
### DB Files for Understanding 'auto_vacuum' PRAGMA
```python   
def db_generate(db_name, vacuum_mode, rows):
    data = []
    sample = ('111111111111111111111111', '111111111111111111111111', '111111111111111111111111', '111111111111111111111111', '111111111111111111111111', '111111111111111111111111')
    
    for i in range(0,rows):
        data.append(sample)
        
    if os.path.exists(db_name):
        os.remove(db_name)

    con = sqlite3.connect(db_name, check_same_thread=False)
    cur = con.cursor()
    cur.execute(f'PRAGMA auto_vacuum={vacuum_mode}')
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("CREATE TABLE test (AA TEXT, BB TEXT, CC TEXT, DD TEXT, EE TEXT, FF TEXT)")
    sql = "INSERT INTO test (AA, BB, CC, DD, EE, FF) VALUES (?, ?, ?, ?, ?, ?)"
    cur.executemany(sql, data)
    con.commit()
    con.close()
```
```python   
def vacuum(db_name):
    con = sqlite3.connect(db_name, check_same_thread=False)
    cur = con.cursor()
    cur.execute("VACUUM")
    con.commit()
    con.close()
```
```python   
def main():
    n = int(input("1. SAMPLE Generate 2. VACUUM NONE 3. VACUUM FULL 4. VACUUM INCR\n Select Case :"))

    if n == 1: # KU-DBF-AM-02-AV-SAMPLE.sqlite
        db_generate('KU-DBF-AM-02-AV-SAMPLE.sqlite', 0, 2000)
        
    elif n == 2: # KU-DBF-AM-02-AV-NONE.sqlite
        db_generate('KU-DBF-AM-02-AV-NONE.sqlite', '0', 2000)
        for i in range(0, 10):
            data_rand_delete('KU-DBF-AM-02-AV-NONE.sqlite', 100)
        
    elif n == 3: # KU-DBF-AM-02-AV-FULL.sqlite
        db_generate('KU-DBF-AM-02-AV-FULL.sqlite', '1', 2000)
        for i in range(0, 10):
            data_rand_delete('KU-DBF-AM-02-AV-FULL.sqlite', 100)
        vacuum('KU-DBF-AM-02-AV-FULL.sqlite')

    elif n == 4: # KU-DBF-AM-02-AV-INCR.sqlite
        db_generate('KU-DBF-AM-02-AV-INCR.sqlite', '2', 2000)
        for i in range(0, 10):
            data_rand_delete('KU-DBF-AM-02-AV-INCR.sqlite', 100)
        vacuum('KU-DBF-AM-02-AV-INCR.sqlite')

if __name__ == '__main__':
    main()
```

Unlike the randomly generated common mission dataset, the dataset was created with fixed values. This is because it is necessary to quantitatively measure the change in the DB file size as the data changes.  


![image](https://user-images.githubusercontent.com/31686076/141149049-b2c699be-fe07-4b89-b785-79b72498a55f.png)

_KU-DBF-AM-02-AV-SAMPLE.sqlite_ is a DB created with fixed values (6 columns and 2000 rows for '111111111111111111111111' in the data).   
_KU-DBF-AM-02-AV-NONE.sqlite_ is the DB in which the vacuum mode is deactivated and 1000 rows are deleted.   
_KU-DBF-AM-02-AV-FULL.sqlite_ is a DB with 1000 rows deleted in Full Vacuum mode.   
_KU-DBF-AM-02-AV-INCR.sqlite_ is a DB with 1000 rows deleted in Incremental Vacuum mode.   
As shown in the figure above, it can be seen that the size of the DB file is reduced when the vacuum mode is activated.
