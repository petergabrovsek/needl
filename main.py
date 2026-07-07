from multi_needle import MultiNeedle


if __name__ == "__main__":
    words_config = [
        # ('Avstrija', 18),
        # ('Belgija', 17),
        # ('Bolgarija', 12),
        # ('Ciper', 12),  #
        # ('Češka', 28),  #!!!!!!!!
        # ('Danska', 22),  #
        # ('Estonija', 18),
        # ('Finska', 15),
        # ('Francija', 16),
        # ('Grčija', 20),
        # ('Hrvaška', 17),
        # ('Irska', 18),
        # ('Italija', 17),  #
        # ('Latvija', 20),
        # ('Litva', 16),
        # ('Luksemburg', 20),
        # ('Madžarska', 15),
        # ('Malta', 24),  #!!!!!!!!
        # ('Nemčija', 20),
        # ('Nizozemska', 12),  #?
        # ('Poljska', 10),
        # ('Portugalska', 17),
        # ('Romunija', 16),
        # ('Slovaška', 18),
        ('Slovenija', 12),
        # ('Španija', 19),
        # ('Švedska', 14),
    ]

    for word, seed in words_config:
        print(word.upper())
        needl = MultiNeedle(30, 42, word, 15, seed=seed)
        if needl.generate():
            needl.print_haystack()
        else:
            print("Failed to generate a puzzle")
