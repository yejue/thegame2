"""
本页目的 返回一个字典和一堆屎一样的东西
"""
import random


class InsertData:

    message = '一别三季，庆国庆月又新年'

    def __init__(self):
        self.pri = self.get_pr()[1]

    def get_pr(self):
        """返回pub 和 pri key"""
        # pub = self.get_read('utils/pub.key')
        # pri = self.get_read('utils/privatekey.key')
        pub = self.get_read('pub.key')
        pri = self.get_read('privatekey.key')
        return pub, pri

    def get_read(self, filename):
        """ 返回f.read"""
        with open('{}'.format(filename), 'r') as f:
            print(f.read())
            return f.read()

    def insert(self):
        temp = {}
        keysave = self.pri
        for i in range(len(keysave)):
            temp.update({'{}'.format(i): keysave[i]})
        return temp

    @staticmethod
    def shit_data():
        shit_data = ''.join([chr(random.randint(8996, 11000)) for _ in range(80)])
        return shit_data


if __name__ == '__main__':
    data = InsertData().insert()

