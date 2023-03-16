class LyricsProcessing:
    def __init__(self, filepath: str = 'lyric/11次心跳 - 火箭少女101.txt', encoding: str = 'utf-8'):
        self.filepath = filepath
        self.select_number_of_first_line = 2
        self.encoding = encoding

    def get_output_filename(self, select_number_of_first_line: int = 2, filetype: str = 'txt'):
        self.select_number_of_first_line = select_number_of_first_line
        with open(self.filepath, 'r', encoding=self.encoding) as file:
            lines = file.readlines()[:select_number_of_first_line]

        file_title = '_'.join([line.split(':')[-1].strip('\n')
                              for line in lines])
        self.output_filename = f"{file_title}.{filetype}"
        return self.output_filename

    def get_word_index(self, word_list: list, sentence: str):
        word_index_list = list()
        prev = 0
        for word in word_list:
            index = sentence.index(word)
            sentence = sentence[index:]
            word_index_list.append(index + prev)
            prev = index + prev
        return word_index_list

    def output_file(self, filename: str = ""):
        if filename == "":
            filename = self.output_filename

        filename, filetype = filename.split('.')
        counter = 1

        for key, val in self.data.items():
            with open(f"{filename}_{counter:05}.{filetype}", 'w', encoding=self.encoding) as output_file:
                output_file.write(f"{key}\n")
                for s, e, w in val:
                    output_file.write(f"<{s}> <{e}> {w}\n")
            counter += 1

    def parser(self):
        with open(self.filepath, 'r', encoding=self.encoding) as file:
            data = file.readlines()[self.select_number_of_first_line:]

        self.data = dict()

        for line in data:
            sentence_begin_time = line.split('<')[0]
            sentence_data = line.strip('\n').split(']')[-1]

            word_list = list()
            for dirty_word in sentence_data.split(')'):
                clean_word = dirty_word.split('<')[0].strip()
                word_list.append(clean_word)

            word_list = word_list[1:]

            dirty_start_time = sentence_data.split('>')
            start_time = list()

            for time in dirty_start_time:
                clean_start_time = time.split('<')[-1]
                start_time.append(clean_start_time)

            end_time = start_time[1: -1]
            start_time = start_time[:-2]

            sentence_data = list()
            for i in range(len(word_list)):
                if word_list[i] == "":
                    continue
                sentence_data.append(
                    (start_time[i], end_time[i], word_list[i]))

            self.data[sentence_begin_time] = sentence_data


if __name__ == '__main__':
    preProcessing = LyricsProcessing()
    preProcessing.get_output_filename(2)
    preProcessing.parser()
    preProcessing.output_file()
