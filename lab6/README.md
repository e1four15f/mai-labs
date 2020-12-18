# Лабораторная работа 6
![version](https://img.shields.io/badge/Python-3.8-blue)
![version](https://img.shields.io/badge/numpy-1.19.2-yellowgreen)


## Задание
Дан пустой двухмерный массив `A` размера `NxM` и список двухмерных массивов, где `n<N` и `m<M`, со значением цены.\
Необходимо написать алгоритм упаковки маленький массивов в `A`, при условии максимизации цены.\
Посчитать метрики


## Ход работы
Реализован следующий алгоритм:
1. Из списка двухмерных массивов перебираем все подмножества - кандидаты решения задачи
2. Сортируем кандидатов по цене, если общая площадь кандидата больше вместимости `A`, то откидываем
3. Проверяем для каждого кандидата можно ли его поместить в массив `A`, использую kd-tree подобный алгоритм\
[Описание алгоритма](https://blackpawn.com/texts/lightmaps/)\
![](https://blackpawn.com/texts/lightmaps/diag01.jpg)
![](https://blackpawn.com/texts/lightmaps/diag02.jpg)
![](https://blackpawn.com/texts/lightmaps/diag03.jpg)
![](https://blackpawn.com/texts/lightmaps/diag04.gif)

## Пример работы:
### Найдено решение
![Alt Text](resource/solution.png)
### Вывод метрик
![Alt Text](resource/metrics.png)

