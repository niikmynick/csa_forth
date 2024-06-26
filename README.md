csa lab 3
========================

- Кобик Никита Алексеевич
- P3224
- ```forth | stack | harv | mc -> hw | instr | struct | stream | mem | cstr | prob2 | cache```
- Базовый вариант

## Язык программирования

```ebnf
program     ::=     { term }

term        ::=     word | number | string | var_def | word_def | condition | for_loop | while_loop

word        ::=     "=" 
                  | "<" 
                  | ">" 
                  | "dup" 
                  | "drop" 
                  | "swap" 
                  | "!" 
                  | "@" 
                  | "?" 
                  | "+" 
                  | "-" 
                  | "*" 
                  | "/" 
                  | "mod" 
                  | "key" 
                  | "." 
                  | "emit" 
                  | ".\"" 
                  | "\"" 
                  | "cr" 
                  | "leave" 
                  | "nop"

number      ::=     { <any of "0-9"> }

string      ::=     "\"" { <any symbols except "\""> } "\""
                  | "\'" { <any symbols except "\'"> } "\'"

var_def     ::=     "variable" var_name [ number "cells allot" ]
var_name    ::=     <any of "a-z A-Z _"> { <any of "a-z A-Z 0-9 _"> }

word_def    ::=     ":" { term } ";"

condition   ::=     "if" { term } [ "else" { term } ] "then"

for_loop    ::=     number number "do" { term } "loop"

while_loop  ::=     "begin" { term } "until" 
```

Примечания:
- Код выполняется последовательно
- Первая указанная команда считается началом программы
- Все переменные и процедуры должны быть объявлены до использования
- В программе не может быть переменных и процедур с одинаковыми именами
- Использование имени процедуры означает переход к ее выполнению, а после завершения - возврат к точке вызова
- Да, вся программа состоит из слов или литералов, разделенных пробелами, но было принято решение выделить несколько структур в описании для более точного определения синтаксиса

## Система команд

Набор инструкций FORTH:
- `=` -- проверить, что два значения со стека равны `[..., a, b] -> [..., -1 | 0]`
- `<` -- проверить, что верхнее значение со стека больше второго `[..., a, b] -> [..., -1 | 0]`
- `>` -- проверить, что верхнее значение со стека меньше второго `[..., a, b] -> [..., -1 | 0]`
- `dup` -- дублировать верхнее значение на стеке данных `[..., a] -> [..., a, a]`
- `drop` -- переместить указатель вершины стека на одну ячейку вниз `[..., a, b] -> [..., a]`
- `swap` -- поменять местами два верхних значения на стеке данных `[..., a, b] -> [..., b, a]` 
- `!` -- вершина стека -> адрес сохранения, второе значение сверху -> значение `[..., value, address] -> [...]`
- `@` -- прочитать ячейку памяти по адресу с вершины стека данных `[..., address] -> [..., value]`
- `?` -- замена последовательности `@ .`, т.е. прочитать ячейку памяти по адресу с вершины стека данных и сохранить для вывода `[..., address] -> [..., value] -> [...]`
- `+` -- сложить два значения с вершины стека `[..., a, b] -> [..., a + b]`
- `-` -- вычесть два значения с вершины стека `[..., a, b] -> [..., a - b]`
- `*` -- умножить два значения с вершины стека `[..., a, b] -> [..., a * b]`
- `/` -- разделить два значения с вершины стека `[..., a, b] -> [..., a // b]`
- `mod` -- положить на стек остаток от деления двух значений с вершины стека `[..., a, b] -> [..., a % b]`
- `not` -- инвертировать значение с вершины стека данных `[..., a] -> [..., not a]`
- `key` -- прочитать символ из потока ввода и положить его на стек `[...] -> [..., chr]`
- `.` -- вывести в поток вывода значение с вершины стека `[..., a] -> [...]`
- `emit` -- вывести в поток вывода значение с вершины стека в виде ASCII символа `[..., a] -> [...]`
- `."` -- вывести последующую строку в поток вывода
- `"` -- закончить вывод строки в поток вывода
- `cr` -- вывести в поток вывода перевод строки
- `leave` -- выйти из цикла
- `nop` -- ничего не делать

Набор инструкций ASM:
- `push value` -- положить значение на вершину стека `[...] -> [..., value]`
- `pop` -- переместить указатель вершины стека на одну ячейку вниз `[..., a, b] -> [..., a]`
- `read variable_name` -- прочитать ячейку памяти по адресу переменной `[...] -> [..., value]`
- `read` -- прочитать ячейку памяти по адресу с вершины стека данных `[..., address] -> [..., value]`
- `save address` -- сохранить значение с вершины стека в память по указанному адресу `[..., value] -> [...]`
- `save` -- вершина стека -> адрес сохранения, второе значение сверху -> значение `[..., value, address] -> [...]`
- `swap` -- поменять местами два верхних значения на стеке данных `[..., a, b] -> [..., b, a]` 
- `dup` -- дублировать верхнее значение на стеке данных `[..., a] -> [..., a, a]`
- `comp` -- сравнить два значения со стека `[..., a, b] -> [... -1 | 0 | 1]`
- `jmp` -- безусловный переход на метку
- `jmz` -- переход на метку, если верхнее значение стека == 0 `[..., a] -> [...]`
- `jnz` -- переход на метку, если верхнее значение стека != 0 `[..., a] -> [...]`
- `add` -- сложить два значения с вершины стека `[..., a, b] -> [..., a + b]`
- `sub` -- вычесть два значения с вершины стека `[..., a, b] -> [..., a - b]`
- `mul` -- умножить два значения с вершины стека `[..., a, b] -> [..., a * b]`
- `div` -- разделить два значения с вершины стека `[..., a, b] -> [..., a // b]`
- `inc` -- увеличить значение на вершине стека на 1 `[..., a] -> [..., a + 1]`
- `dec` -- уменьшить значение на вершине стека на 1 `[..., a] -> [..., a - 1]`
- `not` -- инвертировать значение с вершины стека данных `[..., a] -> [..., not a]`
- `ret` -- возврат к точке перехода
- `nop` -- ничего не делать
- `hlt` -- завершить выполнение программы

Примечания:
- Использование операндов со стека подразумевает его изъятие

## Организация памяти

Данные и инструкции имеют разные места хранения, согласно Гарвардской архитектуре 

```
    data memory
+------------------+
| 00 :     in      |
| 01 :     out     |
| 02 :     ...     |
+------------------+

 instruction memory 
+------------------+
| 00 :     ...     |
|          ...     |
| n  :     hlt     |
|    :     ...     |
+------------------+
```

Исходный код транслируется в файл формата json, содержащий две секции - данные и инструкции
- В секции данных указаны используемые переменные и их требуемый размер
- В секции инструкций хранятся индекс инструкции, ее код и операнд

У программиста нет доступа к памяти инструкций

В системе поддерживаются целые знаковые числа (integer), символы (char), строки (string)

Порты ввода-вывода отображаются в память. Для доступа к ним используются обращения к определенным заранее ячейкам в памяти данных

Адресация - прямая, с использованием переменных (подставляется адрес ячейки в памяти данных) и меток (адрес ячейки в памяти инструкций)

Строки представлены в виде массива символов, переменная -- ссылка на первый элемент 
(например, если в переменную `text` записана строка и данные сохранены в ячейках памяти, начиная с 24, то `push text` повлияет на стек данных как `[...] -> [..., 24]`)

## Транслятор

```
python python translator.py <source> <target>
```

Трансляция реализуется в несколько этапов:
- Очистка исходного кода от пустых строк
- Деление кода на термы
- Проверка синтаксиса программы
- Парсинг переменных
- Парсинг инструкций
- Трансляция инструкций в код ассемблера
- Подстановка адресов переменных
- Генерация файла формата json

## Модель процессора

```
python python machine.py <source> <input> <target>
```

```text
Control Unit

                  n & z flags
        +--------------------> +-----------------------+ --- > +------+
        |   +----------------> |  Instruction Decoder  |       | Tick |      
        |   |   +------------> +-------+---+---+-------+ < --- +------+ 
        |   |   | instruction          |   ^   |
+-------+---+---+-------+              |   |   |
|      Data Path        | <------------+   |   +-------------------------------+
+-----------------------+  flow signals    |                                   |
                                           |                                   v
                               +-----------+-----------+       +---------------+-------+
                               |   Microcode  Memory   | < --- | M Instruction Pointer |
                               +-----------------------+       +-----------------------+ 
```

```text
Data Path
      

 rs_write        rs_read                                                                                                                
+-----------------------+                                                                                                          
|     Return  Stack     | < --------------------+                                                                                          
+-------+---------------+                       |                                                                                          
        |                                       |                                                                                       
        |       +-----------------------+       |                                                      
        |       | +1                    |       |                                      instruction                  
        v       v                       |       |                im_read                    |                      
+-------+-------+-------+       +-------+-------+-------+       +-----------------------+   v   +-----------------------+ 
|          MUX          | --- > |  Instruction Pointer  | --- > |  Instruction  Memory  | --- > |     Control  Unit     | 
+-------+---+---+-------+       +-----------+-----------+       +-----------------------+       +-------+-------+-------+                  sel
        ^   ^   ^                latch_ip   |                                                           ^       ^                           |
        |   |   |                           |                                                    N flag |       | Z flag                    v                    dm_write        dm_read
        |   |   +---------------------------|-------------------------------------------------- +-------+-------+-------+       +-----------+-----------+       +-----------------------+ --- > +-----------------------+ 
       sel  |                               |                                      signal --- > |          ALU          | --- > |          MUX          | --- > |      Data  Memory     |       |      I/O Devices      |
            |                               |                               +-----------------> +-------+-------+-------+       +-----------+-----------+       +---------------+-------+ < --- +-----------------------+
            |                               |                               |                           |       |                           ^                                   |
            |                               +-----------------> +-----------+-----------+ <-------------+       +-----------------------+   |   +-------------------------------+
            |                                                   |          MUX          |                                               |   |   | 
            |                                         sel --- > +-----------------------+ <-------------+       +-----------------------|---+   |
            |                                                                                           |       |                       v       v
            |                                                                                   +-------+-------+-------+ --- > +-------+-------+-------+ 
            +---------------------------------------------------------------------------------- |      Data   Stack     |       |          MUX          | < --- sel
                                                                                                +-----------------------+ < --- +-----------------------+
                                                                                                ds_write         ds_read
```

Описание реализации:
- Процесс моделирования отслеживается по тактам
- Программа выполняется последовательно
- Остановка программы происходит:
  - при выполнении команды `hlt`
  - при обращении к несуществующей ячейке памяти
  - при возникновении ошибки во время выполнения (например, деление на 0)
- Переполнение стека или памяти в данной реализации не предусмотрено
- Доступ к памяти инструкций осуществляется по адресу в специальном регистре instruction pointer


Набор инструкций:

| Инструкция | Количество тактов |
|:----------:|:-----------------:|
|    push    |         1         |
|    dup     |         1         |
|    pop     |         1         |
|    read    |      2 или 3      |
|    comp    |         4         |
|    jmp     |         1         |
|    jmz     |      1 или 2      |
|    jnz     |      1 или 2      |
|    add     |         4         |
|    sub     |         4         |
|    mul     |         4         |
|    div     |         4         |
|    inc     |         3         |
|    dec     |         3         |
|    swap    |         4         |
|    save    |      2 или 3      |
|   return   |         2         |
|    nop     |         1         |
|    halt    |         1         |

Примечание: количество тактов в таблице указано без учета времени на выборку инструкции (2 такта)

Набор микрокоманд:
- `rs_write` -- запись IP в стек возврата
- `rs_read` -- чтение с вершины стека возврата
- `ds_write` -- запись в стек данных
- `ds_read` -- чтение с вершины стека данных
- `dm_write` -- запись в память данных в ячейку AR
- `dm_read` -- чтение из памяти данных ячейки AR
- `dm_set_addr` -- установка AR
- `im_read` -- чтение из памяти инструкций ячейки AR
- `im_set_addr` -- установка AR
- `latch_ip` -- защелкивание IP
- `ip_mux_ip` -- выбор IP на мультиплексоре, подключенном к IP
- `ip_mux_ds` -- выбор TODS на мультиплексоре, подключенном к IP
- `ip_mux_rs` -- выбор TORS на мультиплексоре, подключенном к IP
- `ip_mux_alu` -- выбор ALU на мультиплексоре, подключенном к IP
- `ds_mux_ds` -- выбор TODS на мультиплексоре, подключенном к стеку данных
- `ds_mux_dm` -- выбор DM на мультиплексоре, подключенном к стеку данных
- `ds_mux_alu` -- выбор ALU на мультиплексоре, подключенном к стеку данных
- `dm_mux_ds` -- выбор TODS на мультиплексоре, подключенном к памяти данных
- `dm_mux_alu` -- выбор ALU на мультиплексоре, подключенном к памяти данных
- `alu_add` -- операция сложения на операндах в АЛУ
- `alu_sub` -- операция вычитания на операндах в АЛУ
- `alu_div` -- операция деления на операндах в АЛУ
- `alu_mul` -- операция умножения на операндах в АЛУ
- `alu_mod` -- операция mod на операндах в АЛУ
- `alu_comp` -- операция сравнения на операндах в АЛУ
- `alu_invert` -- операция инвертирования на операнде в АЛУ
- `alu_set_a` -- определить левый операнд АЛУ
- `alu_set_b` -- определить правый операнд АЛУ
- `alu_mux_ds` -- выбор TODS на мультиплексоре, подключенном к АЛУ
- `alu_mux_im` -- выбор IM на мультиплексоре, подключенном к АЛУ
- `alu_mux_alu` -- выбор АЛУ на мультиплексоре, подключенном к АЛУ
- `alu_mux_zero` -- выбор 0 на мультиплексоре, подключенном к АЛУ
- `alu_mux_one` -- выбор 1 на мультиплексоре, подключенном к АЛУ
- `halt` -- останов

## Тестирование

```
pytest test.py
```

Тестирование выполняется при помощи golden тестов

CI для Github Actions разделен на две задачи

Lint:
```yaml
name: Python Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install mypy pytest
    - name: Run mypy linter
      run: |
        mypy .
```

Test:
```yaml
name: Python Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest
          pip install pytest-golden
      - name: Run golden tests
        run: |
           pytest test.py
```

Пример проверки исходного кода
```text
pytest test.py
============================= test session starts ==============================
collecting ... collected 5 items

test.py::test_translator_asm_and_machine[golden/test/prob1.yml] 
test.py::test_translator_asm_and_machine[golden/test/cat.yml] 
test.py::test_translator_asm_and_machine[golden/test/prob5.yml] 
test.py::test_translator_asm_and_machine[golden/test/hello_user.yml] 
test.py::test_translator_asm_and_machine[golden/test/hello_world.yml] 

============================== 5 passed in 4.04s ===============================
```

## Статистика

|    Тест     | Инструкций | Исполнено |  Такт  |
|:-----------:|:----------:|:---------:|:------:|
| hello world |     49     |    27     |  362   | 
| hello user  |    139     |    345    |  4966  |
|    prob2    |     80     |   1171    | 16843  |
|     cat     |     34     |    116    |  1686  |
