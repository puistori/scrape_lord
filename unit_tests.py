import unittest
import obtain_headers
import obtain_proxy
import constants
import random
import pickle

class Testing_Suite(unittest.TestCase):

    def test_obtain_headers(self):
        #answers = obtain_headers.obtain_headers(random.choice(constants.HEADERS))
        #self.assertTrue(len(answers)>1)
        #self.assertTrue(type(answers)==list)
        #self.assertTrue(type(answers[0])==str)
        pass
    def open_sesame(self):
        pickle_in = open('image_data_redo_0','rb')
        answer = pickle.load(pickle_in)
        print('zu laufen')
        print(answer)
        self.assertTrue(len(answer)==2)


if __name__ == '__main__':
    unittest.main()
