import templates
import mystem

templates_list = [
	{
		'sequences': [
			{
				"list": [
					{
						'template': 'в',
						'amount': 1,
						'no_cache': True,
					},
					{
						'template': {
							'one_of': [
								['географическое название'],
								['существительное', 'предложный'],
								"Яндекс"
							]
						},
						'amount': '*',
						'max_gap': 1,
						'use_lexem': True,
					}
				],
				"category": "place",
			},
			{
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
		'basic_templates': [
			{
				"template": {
					'one_of': [
						"встречать",
					]
				},
				"amount": '*',
				"category": None,
				"required": True

			}
		]
	}
]

text = mystem.parse(mystem.run())
for pattern in templates.extract(text, templates_list):
	print('== Extracted meeting ==')
	for category, words in pattern.items():
		print(category, ':', words)


