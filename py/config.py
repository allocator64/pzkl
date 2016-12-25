
# list of templates, each is applied consequently to a given sentence
templates_list = [
	{
		# Complex templates for category. Each of them is a NER of sorts.
		# Idea is to search for sequences of words that can be described by sequence of word templates
		# Tou think of this as an some form of regexp
		'sequences': [
			{
				# So here is the list. Each template must be fullfilled for sequence of words to be returned.
				# If template is not present in the sentence — None is returned

				################################################################
				# Passing examples:            # Output                        #
				################################################################
				# - В ресторане                # - ресторан                    #
				# - В Яндексе                  # - яндекс                      #
				# - В Москве                   # - москва                      #
				################################################################
				"list": [
					{
						# Simplest template:
						# Lexem must be 'в'
						'template': 'в',
						# Amount of consequent words to search for is 1
						'amount': 1,
						# This option points out that this word will not be present in the returned sequence
						'no_cache': True,
					},
					{
						# Here is a more complex template
						'template': {
							# Word must fullfill at least one of the templates included in 'one_of' list
							'one_of': [
								# This is a list of traits. All of them must be present in word's list of traits
								# So, first option for second word in this template is to have trait 'географическое название'
								['географическое название'],
								# Same here, second option for second word in this template is to have both traits: 'существительное', 'предложный'
								['существительное', 'предложный'],
								# Third option we saw earlier — it's like 'в' — third option for second word is to be 'Яндекс' or 'Яндекса' or any of the derivative of 'Яндекс'
								"Яндекс"
							]
							# Word must fullfill all of the templates included in 'required'
							# It's only purpose is to find exact words in the exact form, as listed in the example below
							#'required': [
							#	'власть',
							#	['предложный']
							#]
						},
						# here is the most interesting part. This is a qualifier for amount with same semantic as '+' in regexp.
						# So this subtemplate will be searched until we find word that doesn't fall for it. Then — that word is passed to the next subtemplate
						'amount': '*',

						# This is maximum amount of non-template words that can appear between previous subtemplate and current one.
						# Note, that templates words are processed in order from 1st to last 
						'max_gap': 1,
						# This option points out that word will be returned in lexem form, not in the form it appeared in the sentence
						# Example: in the sentence 'встретились в ресторане' word 'ресторане' is falls for current subtemplate, but returned word will be 'ресторан'
						'use_lexem': True,
					}
				],
				# this is a category descriptor of this template in the output
				"category": "place",
			},
			{

				################################################################
				# Passing examples:            # Output                        #
				################################################################
				# - С другом                   # - друг                        #
				# - С Борисом Алексеевичем     # - борис алексеевич            #
				# - С ним                      # - он                          #
				################################################################
				"list": [
					{
						'template': 'c',
						'amount': 1,
						'no_cache': True,
					},
					{
						'template': {
							'one_of': [
								["имя", "творительный"],
								["фамилия", "творительный"],
								["отчество", "творительный"],
								["местоимение-существительное", "творительный", "одушевленное"],
								['существительное', 'творительный', "одушевленное"],
							]
						},
						'amount': '*',
						'max_gap': 1,
						'use_lexem': True,
					}
				],
				"category": "actors",
			},
			{
				################################################################
				# Passing examples:            # Output                        #
				################################################################
				# - Встретил Васю              # - вася                        #
				# - Встретил Аню Иванову       # - аня иванова                 #
				# - встретили его              # - он                          #
				################################################################
				"list": [
					{
						'template': 'встречать',
						'amount': 1,
						'no_cache': True,
					},
					{
						'template': {
							'one_of': [
								["имя", "винительный"],
								["фамилия", "винительный"],
								["отчество", "винительный"],
								["местоимение-существительное", "винительный", "одушевленное"],
								['существительное', 'винительный', "одушевленное"],
							]
						},
						'amount': '*',
						'max_gap': 1,
						'use_lexem': True,
					}
				],
				"category": "actors",
			},
			{
				################################################################
				# Passing examples:            # Output                        #
				################################################################
				# - Вася встретил [друга       # - вася                        #
				# - Аня Иванова встретила      # - аня иванова                 #
				# - он встретил                # - он                          #
				################################################################
				"list": [
					{
						'template': {
							'one_of': [
								["имя", "именительный"],
								["фамилия", "именительный"],
								["отчество", "именительный"],
								["местоимение-существительное", "именительный", "одушевленное"],
								["существительное", "именительный", "одушевленное"],
							]
						},
						'amount': '*',
					},
					{
						'template': "встречать",
						'amount': 1,
						'no_cache': True,
						'max_gap': 3,
					}
				],
				"category": "actors",
			},
			{
				################################################################
				# Passing examples:            # Output                        #
				################################################################
				# - пошли на паром             # - паром                       #
				# - идем на спектакл           # - спектакль                   #
				################################################################
				"list": [
					{
						'template': 'пойти',
						'amount': 1,
						'no_cache': True
					},
					{
						'template': {
							'one_of': [
								"в",
								"к",
								"на"
							]
						},
						'amount': 1,
						'max_gap': 3,
						'no_cache': True
					},
					{
						'template': {
							'one_of': [
								['географическое название'],
								['существительное', 'винительный'],
								"Яндекс"
							]
						},
						'amount': '*',
						'max_gap': 1,
						'use_lexem': True,
					}
				],
				"category": "place",
			}
		],

		# This is a simplified version of the above - only one template (so - only one Named Entity)
		'basic_templates': [
			{
				"template": {
					'one_of': [
						"встречать",
					]
				},
				# Semantic is the same is '+' in regexp if required option is True, and '*' if not
				"amount": '*',
				# If no category is specified - words will not be present in the output
				"category": None,
				"required": True

			}
		]
	}
]