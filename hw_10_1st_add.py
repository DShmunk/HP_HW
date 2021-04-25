'''
вариация задачи: определение уникальных неповторяющихся строк
'''
def reader(file_name):
    for line in open(file_name, "r"):
        yield line


def run_reader():
    file_name = "LCD1602_chars.txt"
    my_reader = reader(file_name)
    uniq = {}
    for line in my_reader:
        if line not in uniq:
            uniq[line] = 1
        else:
            uniq[line] += 1
    for k, v in uniq.items():
        if v == 1: print(k)
    return uniq


if __name__ == "__main__":
    run_reader()