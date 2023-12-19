import os
import datetime
from functools import wraps


def logger(path):

    def __logger(old_function):

        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            date_row = 'Дата и время вызова функции: ' + str(datetime.datetime.now())
            name_row = 'Имя функции: ' + old_function.__name__
            args_row = ''
            kwargs_row = ''
            if len(args) > 0:
                for arg in args:
                    args_row += str(arg) + ' '
                args_row = 'Аргументы функции: ' + args_row
            if len(kwargs) > 0:
                for key, value in kwargs.items():
                    kwargs_row += key + ':' + str(value) + ' '
                kwargs_row = 'Именованные аргументы: ' + kwargs_row
            result_row = 'Результат работы функции: ' + str(result)
            write_row = date_row + ' ' + name_row + ' ' + args_row + kwargs_row + result_row
            if os.path.exists(path):
                with open(path, 'a', encoding='utf-8') as f:
                    f.write('\n' + write_row)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(write_row)
            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path, encoding='utf-8') as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()