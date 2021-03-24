'''
Задача-1
У вас есть файл из нескольких строк. Нужно создать генератор который будет построчно выводить строки из вашего файла.
При вызове итерировании по генератору необходимо проверять строки на уникальность.
Если строка уникальна, тогда ее выводим на экран, если нет - скипаем
'''
def reader(file_name):
    for line in open(file_name, "r"):
        yield line

file_name = "LCD1602_chars.txt"
my_reader = reader(file_name)
uniq = []
for line in my_reader:
    if line not in uniq:
        uniq.append(line)
        print(line)


'''
вариация задачи: определение уникальных неповторяющихся строк
'''
def reader(file_name):
    for line in open(file_name, "r"):
        yield line

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


'''
Задача-2:
представим есть файл с логами, его нужно бессконечно контролировать
на предмет возникнования заданных сигнатур.

Необходимо реализовать пайплайн из корутин, который подключается к существующему файлу
по принципу команды tail, переключается в самый конец файла и с этого момента начинает следить
за его наполнением, и в случае возникнования запиcей, сигнатуры которых мы отслеживаем -
печатать результат

Архитектура пайплайна

                   --------
                  /- grep -\
dispenser(file) <- - grep - -> pprint
                  \- grep -/
                   --------

Как только в файл запишется что-то содержащее ('python', 'is', 'great') мы сможем это увидеть
'''
import time     # если не спать в follow(), можно убрать

# обертка
def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap

# отслеживаем на предмет содержания сигнатуры
@coroutine
def grep(pattern,target):
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)

# печатем строку с сигнатурой
@coroutine
def printer():
    while True:
        line = (yield)
        print(line)

# раздаем задачи поиска нескольких сигнатур
@coroutine
def dispenser(targets):
    while True:
        item = (yield)
        for target in targets:
            target.send(item)

# подключаемся в конец файла; спим, если не нашли сигнатуры
def follow(thefile, target):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)


if __name__ == '__main__':
    f_open = open('log.txt')
    follow(f_open,
           dispenser([
               grep('python', printer()),
               grep('is', printer()),
               grep('great', printer()),
           ])
           )


'''
Задача-3 (упрощенный вариант делаете его если задача 2 показалась сложной)
Вам нужно создать pipeline (конвеер, подобие pipeline в unix https://en.wikipedia.org/wiki/Pipeline_(Unix)).
Схема пайплайна :
source ---send()--->coroutine1------send()---->coroutine2----send()------>sink
Все что вам нужно сделать это выводить сообщение о том что было получено на каждом шаге и обработку ошибки GeneratorExit.
Например: Ваш source (это не корутина, не генератор и прочее, это просто функция ) в ней опpеделите цикл из 10 элементов
которые будут по цепочке отправлены в каждый из корутин и в каждом из корутин вызвано сообщение о полученном элементе.
После вызова .close() вы должны в каждом из корутин вывести сообщение что работа завершена.
'''
def source(volume):
    print('starting...')
    coro1 = coroutine1()
    coro2 = coroutine2()
    next(coro1)
    next(coro2)
    i = 1
    while i <= volume:
        coro1.send(i)
        coro2.send(i)
        i += 1

def coroutine1():
    print('Coroutine1 starts')
    try:
        while True:
            x = yield
            print(f'Coroutine1 got {x}')
    except GeneratorExit:
        print('Coroutine1.GeneratorExit: Goodbye')
        coroutine1().close()
        print('Coroutine1 was closed')

def coroutine2():
    print('Coroutine2 starts')
    try:
        while True:
            y = yield
            print(f'Coroutine2 got {y}')
    except GeneratorExit:
        print('Coroutine2.GeneratorExit: Goodbye')
        coroutine2().close()
        print('Coroutine2 was closed')


if __name__ == '__main__':
    source(10)


