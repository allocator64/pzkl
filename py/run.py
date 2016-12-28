#!/usr/bin/env python3

import templates
import mystem
import sys
from importlib.machinery import SourceFileLoader

def get_argument(flag):

	if flag in sys.argv:
		idx = sys.argv.index(flag)
		if len(sys.argv) > idx + 1:
			return sys.argv[idx + 1]

	return None

if any(map(lambda x: x in sys.argv,["-h","--help"])) or len(sys.argv) < 2:
	print("Usage: {0} file_with_text.txt [-t module_with_templates] [-m path_to_mystem] [-e encoding] [-s] [-d]".format(sys.argv[0]))
else:

	templates_file = "config.py"
	encoding = "utf-8"
	path_to_mystem = "../mystem/mystem"
	text_file = sys.argv[1] #"../texts/input.txt"
	show_sentences = False
	debug = False

	encoding = get_argument("-e") or encoding
	path_to_mystem = get_argument("-m") or path_to_mystem
	templates_file = get_argument("-t") or templates_file
	if '-s' in sys.argv:
		show_sentences = True

	if '-d' in sys.argv:
		debug = True

	config = SourceFileLoader("config", templates_file).load_module()

	if config.templates_list is None:
		raise Exception("Please specify correct template file")


	text = mystem.parse(mystem.run(text_file, path_to_mystem, encoding))
	for sentence in text:
		has_any = False
		for pattern in templates.extract([sentence], config.templates_list):

			for category, words in pattern.items():
				words = set(words)
				if len(words) >= 2:
					if not has_any:
						has_any = True
						if show_sentences:
							print("\n")
							if debug:
								for word in sentence:
									print(word)
							else:
								print(' '.join([word['text'] for word in sentence]))
						print('== Extracted meeting ==')
					print(category, ':', set(words))


