import pymongo

class MongoDbManager :
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['webapp']
    cursor = None

    def __init__(self, col_name) :
        self.cursor = self.db[col_name]
        self.check_connection()
        print("[DBmanager] init : [webapp]["+col_name+"]")
        
    def check_connection (self) :
        count = 0 
        while count < 3 : #최대 3회까지 재연결 시도
            try:
                self.client.admin.command('ismaster')
                print("[DBmanager] connected ")
                return True
            except:
                count+=1
                print("[DBmanager] connect fail retry... {}".format(count))
                self.client = pymongo.MongoClient(host='localhost', port=27017)
        print("[DBmanager] failed connection")
        return False

    def add_data ( self, _data):
        if self.check_connection() :
            print("[DBmanager] add data :",end='')
            print(_data)
            if type(_data) is list:
                return self.cursor.insert_many(_data)
            else :
                return self.cursor.insert_one(_data)
        else :
            print("[DBmanager] failed to add data")
            return False
    
    def get_data ( self, _query):
        if self.check_connection() :
            print("[DBmanager] get data by :",end='')
            print(_query)
            return self.cursor.find(_query)
        else :
            print("[DBmanager] failed to get data")
            return False

    def del_data ( self, _query):
        if self.check_connection():
            print("[DBmanager] delete data by :",end='')
            print(_query)
            target = self.get_data(_query)
            if target.count() != 0 :
                for x in target:
                    print(x)
                print("[DBmanager] above delete target data exist")
            else : 
                print("[DBmanager] data delete fail : no such data")
                return False
            self.cursor.delete_many(_query)
            if self.get_data(_query).count() == 0:
                print("[DBmanager] data deleted")
                return True
            else : 
                print("[DBmanager] data delete fail : data still exist")
                return False
        else :
            return False
        
    