import numpy as np

class lib:
	def __init__(self, lib_id, books, signup, ship):
		self.id = lib_id
		self.books = books
		self.signup = signup
		self.ship = ship

	def __str__(self):
		return "Lib " + str(self.id)


def read_file(filename):
	libs = {}
	with open(filename, 'r') as rf:
		lines = [[int(num) for num in line.strip().split(' ') if num != "" ] for line in rf.readlines()]
		num_book, num_lib, days = lines[0][0], lines[0][1], lines[0][2]
		scores = lines[1]
		books = {i:[] for i, book in enumerate(lines[1])}
		lib_id = 0
		for i in range(2, 2 + num_lib * 2, 2):
			_, lib_signup, lib_ship = lines[i]
			lib_books = lines[i + 1]
			for book in lib_books:
				books[book].append(lib_id)
			libs[lib_id] = lib(lib_id, lib_books, lib_signup, lib_ship)
			lib_id += 1
	return libs, books, scores, days

def lib_score(lib, rm_days):
	if len(lib.books) > 0:
		tmp_scores = [books_value[i] for i in lib.books]
		tot_book = sum(tmp_scores)
		avg_book = tot_book/len(tmp_scores)
		# print("tot:",tot_book, "avg_book:", avg_book)
		return min(avg_book * rm_days * lib.ship, tot_book)
	else:
		return 0

files = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt', 'f_libraries_of_the_world.txt']

file_name = files[3]
libs, books, scores, days = read_file(file_name)
books_value = [scores[k] / len(v) if len(v) > 0 else 0 for k, v in books.items()]
# print("books:", books)
# print("days:", days)
# print("scores:", scores)
# print("books_value:",books_value)
# for lib in libs:
# 	print("lib id:", lib.id)
# 	print("books:", lib.books)
# 	print("signup:", lib.signup)
# 	print("ship:", lib.ship)
# 	lib_score(lib)

out_libs = []

day = 0
while day < days and len(libs) > 0:
	lib_scores = [(lib_id,lib_score(lib, days - day - lib.signup)) for lib_id, lib in libs.items()]
	# print("lib scores:", lib_scores)

	best_lib_id = max(lib_scores, key=lambda x: x[1])[0]
	best_lib = libs[best_lib_id]

	best_lib_books = sorted(best_lib.books, key=lambda x: books_value[x], reverse = True)[:((days - day - best_lib.signup) * best_lib.ship)]
	
	# print("best_lib_id:",best_lib_id, "best_lib:",best_lib)
	if len(best_lib_books) == 0:
		break
	out_libs.append((best_lib_id, best_lib_books))

	for book_id in best_lib_books:
		for lib_id in books[book_id]:
			libs[lib_id].books.remove(book_id)
		books[book_id].remove(best_lib_id)
	libs.pop(best_lib_id, None)

	# print("books:", books)
	# print("libs:", libs)

	day += best_lib.signup

with open("out_" + file_name, 'w') as wf:
	wf.write(str(len(out_libs)) + '\n')
	for lib in out_libs:
		wf.write(str(lib[0]) + " " + str(len(lib[1])) + '\n')
		for i, book in enumerate(lib[1]):
			if i != 0:
				wf.write(" ")
			wf.write(str(book))
		wf.write('\n')












