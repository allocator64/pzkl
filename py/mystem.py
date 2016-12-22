import os
import sys
import subprocess
import json

_translations = {

#Части речи
	"A": "прилагательное",
	"ADV": "наречие",
	"ADVPRO": "местоименное наречие",
	"ANUM": "числительное-прилагательное",
	"APRO": "местоимение-прилагательное",
	"COM": "часть композита - сложного слова",
	"CONJ": "союз",
	"INTJ": "междометие",
	"NUM": "числительное",
	"PART": "частица",
	"PR": "предлог",
	"S": "существительное",
	"SPRO": "местоимение-существительное",
	"V": "глагол",

#Время (глаголов)
	"наст": "настоящее",
	"непрош": "непрошедшее",
	"прош": "прошедшее",

#Падеж
	"им": "именительный",
	"род": "родительный",
	"дат": "дательный",
	"вин": "винительный",
	"твор": "творительный",
	"пр": "предложный",
	"парт": "партитив",
	"местн": "местный",
	"зват": "звательный",

#Число
	"ед": "единственное число",
	"мн": "множественное число",

#Репрезентация и наклонение глагола
	"деепр": "деепричастие",
	"инф": "инфинитив",
	"прич": "причастие",
	"изъяв": "изьявительное наклонение",
	"пов": "повелительное наклонение",

#Форма прилагательных
	"кр": "краткая форма",
	"полн": "полная форма",
	"притяж": "притяжательные прилагательные",

#Степень сравнения
	"прев": "превосходная",
	"срав": "сравнительная",

#Лицо глагола
	"1-л": "первое лицо",
	"2-л": "второе лицо",
	"3-л": "третье лицо",

#Род
	"муж": "мужской род",
	"жен": "женский род",
	"сред": "средний род",

#Вид
	"несов": "несовершенный",
	"сов": "совершенный",

#Залог
	"действ": "действительный залог",
	"страд": "страдательный залог",

#Одушевленность
	"од": "одушевленное",
	"неод": "неодушевленное",

#Переходность
	"пе": "переходный глагол",
	"нп": "непереходный глагол",

#Прочие обозначения
	"вводн": "вводное слово",
	"гео": "географическое название",
	"затр": "образование формы затруднено",
	"имя": "имя",
	"искаж": "искаженная форма",
	"мж": "общая форма мужского и женского рода",
	"обсц": "обсценная лексика",
	"отч": "отчество",
	"прдк": "предикатив",
	"разг": "разговорная форма",
	"редк": "редко встречающееся слово",
	"сокр": "сокращение",
	"устар": "устаревшая форма",
	"фам": "фамилия",
}



def run(file_name='../texts/input.txt', mystem='../mystem/mystem', encoding='utf-8'):
	return subprocess.check_output([mystem, '-igd', '--format', 'json', file_name]).decode(encoding)


def _parse_gramems(gramems):
	if gramems != "":
		parsed = dict()
		parsed['definite'] = []
		parsed['alternatives'] = []

		gramems = gramems.split('=')
		attributes = gramems[0].split(',')
		variants = gramems[1].strip('()').split('|')

		if len(variants) == 1:
			attributes += variants[0].split(',')

		for attribute in attributes:
			if attribute in _translations:
				parsed['definite'].append(_translations[attribute])

		if len(variants) > 1:
			for variant in variants:
				parsed['alternatives'].append([ _translations[x] for x in variant.split(',') if x in _translations ])

		return parsed

	else:
		return {}


def parse(output):
	sentences = []
	for line in output.split('\n'):
		try:
			sentence = json.loads(line)
			for word in sentence:
				for alternative in word.get("analysis",[]):
					if "gr" in alternative:
						alternative["gr"] = _parse_gramems(alternative["gr"])
			sentences.append(sentence)
		except json.decoder.JSONDecodeError:
			pass
	return sentences


