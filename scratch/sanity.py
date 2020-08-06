class B:
	@classmethod
	def test(cls):
		print(1)

b= B()
b.test()
B.test()

b.test= lambda: print(2)
b.test()
B.test()

B.test= lambda: print(3)
b.test()
B.test()