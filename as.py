names = ["Ліза", "Віка", "Артем", "Олексій", "Джон Порк", "Давід", "Тімоха", "Джек", "Оля", "Діма", "Тарас", "Надя", "Иаков", "Ніколь", "Нюща" ]
with open("names.txt", "w", encoding = "utf 8") as file:
    file.write("")
for name in names:
    with open("names.txt", "a", encoding = "utf 8") as file:
        file.write(name + "/n")