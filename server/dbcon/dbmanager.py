import pymongo

class MongoDbManager :
    hostname = None
    client = None
    db = None
    cursor = None
    
    def __init__(self, _hostname, _db , _col_name) :
        self.hostname = _hostname
        self.client =  pymongo.MongoClient(host= self.hostname, port=27017)
        if self.check_connection() :
            self.db = self.client[_db]
            self.cursor = self.db[_col_name]
            print("[DBmanager] init : ["+_db+"]["+_col_name+"]")

            
    def check_connection (self) :
        count = 0 
        while count < 3 : #최대 3회까지 재연결 시도
            try:
                print()
                self.client.server_info()
                return True
            except:
                count+=1
                print("[DBmanager] connect fail retry... {}".format(count))
                #self.client = pymongo.MongoClient(host= self.hostname, port=27017)
        print("[DBmanager] failed connection")
        return False

    def add_data ( self, _data):
        if self.check_connection() :
            print("[DBmanager] add data :",end='')
            print(_data)
            if type(_data) is list:
                reuslt = self.cursor.insert_many(_data)
            else :
                result = self.cursor.insert_one(_data)
            self.client.close()
            return result    
        else :
            print("[DBmanager] failed to add data")
            self.client.close()
            return False
    
    def get_data ( self, _query):
        if self.check_connection() :
            print("[DBmanager] get data by :",end='')
            print(_query)
            result = self.cursor.find(_query)
            self.client.close()
            return result
        else :
            print("[DBmanager] failed to get data")
            self.client.close()
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
                self.client.close()
                return False
            self.cursor.delete_many(_query)
            if self.get_data(_query).count() == 0:
                print("[DBmanager] data deleted")
                self.client.close()
                return True
            else : 
                print("[DBmanager] data delete fail : data still exist")
                self.client.close()
                return False
        else :
            return False
        
    