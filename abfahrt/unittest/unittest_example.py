import unittest

__unittest = True

def test_func(number1, number2):
	return number1 + number2
	
class Testing(unittest.TestCase):

	def test1(self):
		self.assertEqual(test_func(1,1),2)
		self.assertEqual(test_func(1,2),3)
		self.assertEqual(test_func(1,2),2)
		
	def test2(self):
		self.assertEqual(test_func(1,1),2)
		self.assertEqual(test_func(1,2),3)
		self.assertEqual(test_func(1,2),3)
				
unittest.main()
