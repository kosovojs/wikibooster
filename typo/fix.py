from wiki import WikipediaAPI
import sys
import re, regex
import os
os.environ.setdefault('PYWIKIBOT_NO_USER_CONFIG', '1')
sys.path.append(".")

class TypoFix:
	def makeReplacements(self, inputText, replacements):
		# https://stackoverflow.com/a/7088257 - lambda
		made_repls = []

		for repl in replacements:
			tmp_text = inputText
			if repl['match_whole_word'] == 1:
				inputText = regex.sub(r"\b{}\b".format(repl['from']), repl['to'], inputText,re.IGNORECASE)
			else:
				inputText = regex.sub(r"{}".format(repl['from']), repl['to'], inputText,re.IGNORECASE)
			if inputText != tmp_text:
				made_repls.append([repl['from'], repl['to']])

		return inputText, made_repls

	def getData(self, wiki, title, db_inst):
		pageText = WikipediaAPI.getPageText(wiki, title)
		replacements = db_inst.get_typo_replacements()

		if not pageText:
			return {'status': 'error', 'message': 'Could not get page text'}
		#
		newWikitext, repls = self.makeReplacements(pageText, replacements)

		return {'status': 'ok', 'title': title, 'origText': pageText, 'changedText': newWikitext, 'replacements': repls}
