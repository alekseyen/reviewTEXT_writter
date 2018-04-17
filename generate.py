"""
Скрипт создаёт текст на основе модели, которую вы создали
с помощью {train.py} и указанной вами длины - length.
!Причем все синтаксические средства опускаются!

Особенности программы(кратко):
Для того чтобы подобрать слово следующее слово:
    а) Состовляем массив из всех слов которые идут после
текущего умноженного на соответстующую частоту
    б) random.choice'ом выбираем какое слово должно идти
после текущего

Пример:
model: а б - 2,  а в - 2
Массив из которого будет выбираться случ. слово:
{б, б, в, в}

@author: Подкидышев Алексей
@email: alexp2019@gmail.com
"""

import argparse
import random
import sys


def next_words(pair_of_all_words, curW):
    """Находит следующее после curW слово,
     но если нач. слова нет - кидает exeption"""

    arr = [(i.split())[1] for i in pair_of_all_words if i.split()[0] == curW
           for j in range(int(i.split()[2]))]
    if len(arr) != 0:
        return random.choice(arr)
    else:
        # Если curW - поледнее слово в нашем списке,
        #  то след. слово берем рандомно
        if (str.split(pair_of_all_words
                      [len(pair_of_all_words) - 1]))[1] == curW:

            return str.split(''.join(
                pair_of_all_words[random.randint(0, 1)]))[random.randint(0, 1)]
        else:
            # Выкидываем исключение если начального слова нет в списке
            exit(256)
            print(curW)
            raise ValueError('К сожалению такого слово в списках нет')


def generate_text(model, seed, length, finalTextFile):
    'Метод генерирующий словосочетания, на основе модели'
    pair_of_all_words = model.readlines()
    if seed == '' or seed is None:
        seed = (random.choice(pair_of_all_words)).split()[0]

    'Изначально curW == seed'
    curW = seed

    for i in range(length):
        finalTextFile.write(curW + ' ')
        curW = next_words(pair_of_all_words, curW)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Cоставляет текст')

    parser.add_argument('--model', type=str,
                        help='Путь для загрузки модели')
    parser.add_argument('--seed', type=str,
                        help='НЕОБЯАТЕЛЬНО!'
                             ' Начальное слово')
    parser.add_argument('--length', type=int,
                        help='Длина'
                             ' последовательности слов')
    parser.add_argument('--output', default='', type=str,
                        help='Вывод текста')

    args = parser.parse_args()

    with open(args.model, 'r', encoding="utf8") as file:
        if args.output == '':
            generate_text(file, args.seed, args.length, sys.stdout)
        else:
            with open(args.output, 'w', encoding="utf8") as output:
                generate_text(file, args.seed, args.length, output)

    print('\n')
    print(' "{}" TEXT generation is'
          ' completed successfully'.format(args.output))
