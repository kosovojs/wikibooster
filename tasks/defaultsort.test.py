import sys
sys.path.append(".")
from defaultsort import Defaultsort
import difflib

import unittest

import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot

#https://realpython.com/python-testing/

testcases = [
	{
		'input':"""
fsdfdsfdfd

[[Kategorija:sdsfdsfsf]]
		""",
		'proposed':'Foo, Bar',
		'expected':"""
fsdfdsfdfd


{{DEFAULTSORT:Foo, Bar}}
[[Kategorija:sdsfdsfsf]]
		"""
	},
	{
		'input':"""
fsdfdsfdfd

[[Kategorija:sdsfdsfsf|Foo, Bar]]
		""",
		'proposed':'Foo, Bar',
		'expected':"""
fsdfdsfdfd


{{DEFAULTSORT:Foo, Bar}}
[[Kategorija:sdsfdsfsf]]
		"""
	},
	{
		'input':"""
fsdfdsfdfd

[[Kategorija:sdsfdsfsf|Foo, Bar]]
[[Kategorija:sdsfdsfsdff|Foo, Bafdsfr]]
		""",
		'proposed':'Foo, Bar',
		'expected':"""
fsdfdsfdfd


{{DEFAULTSORT:Foo, Bar}}
[[Kategorija:sdsfdsfsf]]
[[Kategorija:sdsfdsfsdff|Foo, Bafdsfr]]
		"""
	}
]
""" 
for test in testcases:
	orig = test['input']
	prop = test['proposed']
	expected = test['expected']
	_, wikitext = inst.makeChanges(orig, orig, prop)

	if expected != wikitext:
		print('FAIL')
		#output_list = [li for li in difflib.ndiff(expected, wikitext) if li[0] != ' ']
		pywikibot.showDiff(expected, wikitext)
		print('****')
	else:
		print('ok')
# """

inst = Defaultsort()
inst.setData('lvwiki')

class TestSum(unittest.TestCase):
	def test_sum(self):
		for test in testcases:
			orig = test['input']
			prop = test['proposed']
			expected = test['expected']
			_, wikitext = inst.makeChanges(orig, orig, prop)

			self.assertEqual(wikitext, expected, "Should be equal")

if __name__ == '__main__':
	unittest.main()