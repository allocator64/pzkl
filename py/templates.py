

def check_word(word, template):

	# If it's string - then we need exact word
	if type(template) == str:
		if word.get('lex') == template:
			return True
		else:
			return False

	#If it's a list we need all list of attributes to be present in a word
	elif type(template) == list:
		definite_attributes = word.get("gr",{}).get("definite", [])
		alternative_attributes = word.get("gr",{}).get("alternatives", [])

		for attribute in template:
			if attribute not in definite_attributes:

				# We leave only those alternatives that contains needed attribute
				alternative_attributes = [alt for alt in alternative_attributes if attribute in alt]

				# So, if none are left - that means no alternative is acceptable
				# But remember - we are in If brach that didn't find attribute in definite attributes
				# That means there's no attribute present in word
				if len(alternative_attributes) == 0:
					return False
		return True

	elif type(template) == dict:
		if 'required' in template:
			if not check_word(word, template['required']):
				return False

		if 'one_of' in template:
			for subtemplate in template['one_of']:
				if check_word(word, subtemplate):
					return True
		return False
	else:
		return False


def extract_sentence(sentence, template):
	pattern = {}

	# basic templates
	for basic_template in template['basic_templates']:
		occurrences = 0

		for word in sentence:
			passed = False
			lexem = None
			# There can be several variants
			for variant in word.get('analysis', []):
				if check_word(variant, basic_template['template']):
					passed = True
					break

			if passed:
				occurrences += 1

				if basic_template['amount'] == '*' or occurrences <= basic_template['amount']:

					if basic_template.get('category') is not None:
						if basic_template['category'] not in pattern:
							pattern[basic_template['category']] = list()

						pattern[basic_template['category']].append(word['text'])

				else:
					break

		if basic_template.get('required', False) and occurrences == 0:
			return None

	for sequence in template['sequences']:
		sequence_found = False

		for index, first_word in enumerate(sentence):
			sequence_index = 0
			occurrences = 0
			gap = 0
			cache = ""
			word_index = 0
			while word_index + index < len(sentence):
				word = sentence[index + word_index]
				passed = False
				lexem = None

				for variant in word.get('analysis', []):
					if check_word(variant, sequence['list'][sequence_index]['template']):
						passed = True
						lexem = variant['lex']
						break

				if passed:

					occurrences += 1

					if sequence['list'][sequence_index]['amount'] == '*' or occurrences <= sequence['list'][sequence_index]['amount']:
						if not sequence['list'][sequence_index].get('no_cache', False):
							if sequence['list'][sequence_index].get('use_lexem', False):
								cache += lexem + ' '
							else:
								cache += word['text'] + ' '
						word_index += 1
						if sequence_index >= len(sequence['list']) - 1:
							sequence_found = True

					else:
						sequence_index += 1
						occurrences = 0
						gap = 0
						if sequence_index == len(sequence['list']):
							sequence_found = True
							break
				else:
					if occurrences > 0:
						occurrences = 0
						gap = 0
						sequence_index += 1
					else:
						word_index += 1
						gap += 1
						if gap > sequence['list'][sequence_index].get('max_gap', 0):
							break

				if sequence_index == len(sequence['list']):
					break

			if sequence_found:
				if sequence.get('category') is not None:
					if sequence['category'] not in pattern:
						pattern[sequence['category']] = list()
					pattern[sequence['category']].append(cache.strip())
				break

		if not sequence_found and sequence.get('required', False):
			return None

	return pattern


def extract(text, templates):
	extracted = list()
	for sentence in text:
		for template in templates:
			extracted.append(extract_sentence(sentence, template))

	return [e for e in  extracted if e is not None and len(e) > 0]









