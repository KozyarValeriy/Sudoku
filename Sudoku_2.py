import copy, random

def sudoku_solution(sudoku_first, n):
    ''' Функция для решения судоку
      На вход подается:
        sudoku_first  - матрица с целыми числами,
        n             - разрядность судоку.
      Возвращает:
        sudoku_result - решенное судоку, либо заполненое списками с лопустимыми значениями. 
    '''
    empty_cell = [x for x in range(1, 10)]
    adress_empty_cell = []
    sudoku_result = sudoku_first.copy()
    for row_numb in range(n):
        for col_numb in range(n):
            if sudoku_result[row_numb][col_numb] == 0:
                sudoku_result[row_numb][col_numb] = empty_cell.copy()
                adress_empty_cell.append([row_numb, col_numb])
    sudoku_result, result, adress_empty_cell = find_pass_cell(sudoku_result, adress_empty_cell, n)
    if not result:
        print_sudoku(sudoku_result)
        sudoku_result, result = try_predict(adress_empty_cell, sudoku_result, n, 20, 3, 1)
        if not result:
            sudoku_result, result = try_predict(adress_empty_cell, sudoku_result, n, 100, 9, 1)
    return sudoku_result    

def print_sudoku(sudoku):
    for row in sudoku:
        for item in row:
            print(item, end=' ')
        print()    
    
def find_pass_cell(sudoku_result, adress_empty_cell, n):
    ''' Функция для заполнения пустых ячеек.
      На вход подается:
        sudoku_result     - матрица судоку с целыми числами,
        adress_empty_cell - адреса пустых ячеек в судоку.
      Возвращает:
        sudoku_result     - решенное судоку, либо заполненое списками с лопустимыми значениями;
        result            - True если судоку решена, иначе False;
        adress_empty_cell - массив адресов пустых ячеек.        
    '''
    result = True
    k = 0 # переменная для счетчика выхода из цикла
    len_adress_mas = len(adress_empty_cell)
    while len_adress_mas > 0:
        prev_len_adress_mas = len_adress_mas 
        for adress in adress_empty_cell:
            if len(sudoku_result[adress[0]][adress[1]]) == 0:
                break  
            sudoku_result = search_by_square(sudoku_result, adress, n)
            sudoku_result = search_by_row(sudoku_result, adress, n)
            sudoku_result = search_by_col(sudoku_result, adress, n)            
        for i in range(len(adress_empty_cell) - 1, -1, -1):       
            if len(sudoku_result[adress_empty_cell[i][0]][adress_empty_cell[i][1]]) == 1:
                (sudoku_result[adress_empty_cell[i][0]]
                              [adress_empty_cell[i][1]]) = (sudoku_result[adress_empty_cell[i][0]]
                                                                         [adress_empty_cell[i][1]][0])
                del adress_empty_cell[i]
        len_adress_mas = len(adress_empty_cell)
        if prev_len_adress_mas == len_adress_mas:
            k += 1
        else:
            k = 0
        if k > 5:
            result = False
            #print('Нет выхода из цикла While\n')
            break
    return sudoku_result, result, adress_empty_cell

def search_by_square(sudoku_result, adress, n):
    ''' Функция для поиска пересечений в квадрате
      На вход подается:
        sudoku_result - матрица судоку с целыми числами,
        adress        - адреса пустой ячееки;
        n             - разрядность судоку.
      Возвращает:
        sudoku_result - решенное судоку, либо заполненое списками с лопустимыми значениями.
    '''
    square_adress = [0, 0]
    if adress[0] - 3 < 0:
        square_adress[0] = 0
    elif adress[0] - 6 < 0:
        square_adress[0] = 1
    else:
        square_adress[0] = 2

    if adress[1] - 3 < 0:
        square_adress[1] = 0
    elif adress[1] - 6 < 0:
        square_adress[1] = 1
    else:
        square_adress[1] = 2          
    #print('Номер квадрата', square_adress)
    #print('--------------')
    #print(sudoku_result)
    for row in range(3 * square_adress[0], 3 * square_adress[0] + 3):
        for col in range(3 * square_adress[1], 3 * square_adress[1] + 3):
            if (type(sudoku_result[row][col]) != type(list()) and
                sudoku_result[row][col] in sudoku_result[adress[0]][adress[1]]):
                del sudoku_result[adress[0]][adress[1]][
                        sudoku_result[adress[0]][adress[1]].index(sudoku_result[row][col])]
    return sudoku_result

def search_by_row(sudoku_result, adress, n):
    ''' Функция для поиска пересечений в строке
      На вход подается:
        sudoku_result - матрица судоку с целыми числами,
        adress        - адреса пустой ячееки;
        n             - разрядность судоку.
      Возвращает:
        sudoku_result - решенное судоку, либо заполненое списками с лопустимыми значениями.
    '''
    for col in range(0, n):
        if (type(sudoku_result[adress[0]][col]) != type(list()) and
            sudoku_result[adress[0]][col] in sudoku_result[adress[0]][adress[1]]):
            del sudoku_result[adress[0]][adress[1]][
                    sudoku_result[adress[0]][adress[1]].index(sudoku_result[adress[0]][col])]  
    return sudoku_result

def search_by_col(sudoku_result, adress, n):
    ''' Функция для поиска пересечений в столбце
      На вход подается:
        sudoku_result - матрица судоку с целыми числами,
        adress        - адреса пустой ячееки;
        n             - разрядность судоку.
      Возвращает:
        sudoku_result - решенное судоку, либо заполненое списками с лопустимыми значениями.
    '''
    for row in range(0, n):
        if (type(sudoku_result[row][adress[1]]) != type(list()) and
            sudoku_result[row][adress[1]] in sudoku_result[adress[0]][adress[1]]):
            del sudoku_result[adress[0]][adress[1]][
                    sudoku_result[adress[0]][adress[1]].index(sudoku_result[row][adress[1]])]  
    return sudoku_result

def try_predict(adress_empty_cell, sudoku_result, n, iteration, lenth=2, volume_pred=1):
    ''' Функция для предположения числа и посдставления в судоку.
      На вход подается:
        adress_empty_cell - адреса пустых ячеек;
        sudoku_result     - нерешенное судоку со списками вместо пустых ячеек;
        n                 - разрядность судоку;
        iteration         - кол-во итераций, допустимых для решения судоку;
        lenth             - при какой длине списка с допустимыми значениями делать предположение;
        volume_pred       - число предсказаний за один раз.
      Возвращает:
        sudoku_result     - решенное судоку, либо заполненое списками с лопустимыми значениями;
        result            - True если судоку решена, иначе False.
    '''    
    # Словарь для запоминания, какие элементы уже подставлялись
    d = dict(zip([tuple(adress) for adress in adress_empty_cell], [list() for x in range(len(adress_empty_cell))]))
    counter = 0
    for i in range(iteration):
        temp_adress = copy.deepcopy(adress_empty_cell)
        temp_sudoku = copy.deepcopy(sudoku_result)
        random.shuffle(temp_adress)
        for adress in temp_adress:
            if (len(temp_sudoku[adress[0]][adress[1]]) <= lenth and len(d[tuple(adress)]) < lenth and
                len(temp_sudoku[adress[0]][adress[1]]) > len(d[tuple(adress)])):
                d[tuple(adress)].append(temp_sudoku[adress[0]][adress[1]][len(d[tuple(adress)])])
                temp_sudoku[adress[0]][adress[1]] = d[tuple(adress)][-1]
                #print('------------------------')
                #print(adress, d[tuple(adress)][-1])
                #print_sudoku(temp_sudoku)
                del temp_adress[temp_adress.index(adress)]
                counter += 1
                if counter >= volume_pred:
                    break
        temp_sudoku, result, temp_adress = find_pass_cell(temp_sudoku, temp_adress, n)
        if result:
            sudoku_result = temp_sudoku
            print('Итерация', i)
            print('ОК!!!')
            break
    else:
        print('За %.d итераций найти решения не получилось!' % (iteration))
    print(d)
    print('--------------------')
    return sudoku_result, result



def test():
    '''Функция для тестирования алгоритма'''
    print('Easy sudoku')
    sudoku = [[2, 0, 1, 0, 0, 0, 0, 8, 0],  #[2, 4, 1, 3, 9, 7, 6, 8, 5]
              [9, 7, 0, 0, 8, 0, 0, 1, 0],  #[9, 7, 3, 6, 8, 5, 4, 1, 2]
              [0, 0, 6, 0, 2, 0, 3, 0, 9],  #[8, 5, 6, 4, 2, 1, 3, 7, 9]
              [3, 6, 4, 9, 1, 0, 5, 2, 0],  #[3, 6, 4, 9, 1, 8, 5, 2, 7]
              [5, 8, 0, 2, 4, 0, 1, 9, 6],  #[5, 8, 7, 2, 4, 3, 1, 9, 6]
              [0, 9, 0, 7, 0, 0, 8, 0, 4],  #[1, 9, 2, 7, 5, 6, 8, 3, 4]
              [0, 0, 0, 8, 7, 2, 9, 6, 3],  #[4, 1, 5, 8, 7, 2, 9, 6, 3]
              [0, 0, 0, 1, 3, 0, 0, 5, 0],  #[6, 2, 9, 1, 3, 4, 7, 5, 8]
              [7, 0, 0, 5, 6, 0, 2, 4, 1]]  #[7, 3, 8, 5, 6, 9, 2, 4, 1]
    sudoku_result = sudoku_solution(sudoku, 9)
    print_sudoku(sudoku_result)
    print('------------------------------------')    
    print('Medium sudoku')
    sudoku = [[0, 6, 5, 0, 0, 4, 0, 9, 0],  #[7, 6, 5, 8, 2, 4, 1, 9, 3]
              [1, 0, 0, 0, 0, 0, 0, 0, 4],  #[1, 3, 2, 7, 9, 5, 6, 8, 4]
              [8, 0, 0, 0, 0, 1, 0, 0, 0],  #[8, 4, 9, 3, 6, 1, 7, 5, 2]
              [0, 0, 0, 2, 0, 3, 0, 0, 9],  #[6, 7, 1, 2, 8, 3, 5, 4, 9]
              [0, 0, 0, 1, 0, 6, 3, 0, 7],  #[9, 8, 4, 1, 5, 6, 3, 2, 7]
              [0, 5, 3, 4, 0, 9, 0, 0, 0],  #[2, 5, 3, 4, 7, 9, 8, 1, 6]
              [0, 9, 7, 6, 0, 0, 0, 0, 0],  #[5, 9, 7, 6, 4, 8, 2, 3, 1]
              [0, 0, 6, 5, 0, 0, 0, 7, 8],  #[4, 1, 6, 5, 3, 2, 9, 7, 8]
              [3, 0, 8, 9, 0, 0, 4, 0, 5]]  #[3, 2, 8, 9, 1, 7, 4, 6, 5]
    sudoku_result = sudoku_solution(sudoku, 9)
    print_sudoku(sudoku_result)
    print('------------------------------------')
    print('Hard sudoku')
    sudoku = [[0, 0, 4, 0, 0, 6, 0, 0, 9],  #[0, 0, 4, 0, 0, 6, 0, 0, 9]
              [0, 8, 0, 0, 9, 0, 0, 2, 0],  #[0, 8, 0, 0, 9, 0, 0, 2, 0]
              [0, 0, 0, 0, 1, 0, 0, 0, 8],  #[0, 0, 0, 0, 1, 0, 0, 0, 8]
              [1, 0, 0, 0, 0, 0, 0, 0, 6],  #[1, 0, 0, 0, 0, 0, 0, 0, 6]
              [0, 0, 0, 0, 0, 0, 0, 4, 0],  #[0, 0, 0, 0, 0, 0, 0, 4, 0]
              [9, 0, 0, 0, 0, 7, 0, 5, 0],  #[7, 0, 0, 0, 0, 7, 0, 5, 0]
              [2, 0, 0, 5, 0, 0, 3, 0, 0],  #[2, 0, 0, 5, 0, 0, 3, 0, 0]
              [0, 6, 7, 0, 8, 0, 0, 0, 0],  #[0, 6, 7, 0, 8, 0, 0, 0, 0]
              [0, 1, 0, 0, 0, 3, 2, 0, 0]]  #[0, 1, 0, 0, 0, 3, 2, 0, 0]
    sudoku_result = sudoku_solution(sudoku, 9)
    print_sudoku(sudoku_result)
    print('------------------------------------')
    print('Extreme sudoku')
    sudoku = [[0, 9, 0, 6, 0, 0, 8, 0, 0],  #[0, 9, 0, 6, 0, 0, 8, 0, 0]
              [0, 0, 0, 5, 0, 3, 4, 0, 0],  #[0, 0, 0, 5, 0, 3, 4, 0, 0]
              [8, 0, 7, 0, 0, 0, 6, 1, 0],  #[8, 0, 7, 0, 0, 0, 6, 1, 0]
              [0, 0, 0, 0, 5, 0, 0, 0, 7],  #[0, 0, 0, 0, 5, 0, 0, 0, 7]
              [0, 0, 0, 7, 9, 0, 1, 0, 0],  #[0, 0, 0, 7, 9, 0, 1, 0, 0]
              [0, 0, 0, 0, 0, 6, 3, 0, 0],  #[0, 0, 0, 0, 0, 6, 3, 0, 0]
              [0, 7, 0, 0, 0, 0, 0, 2, 0],  #[0, 7, 0, 0, 0, 0, 0, 2, 0]
              [0, 4, 0, 0, 0, 0, 0, 0, 0],  #[0, 4, 0, 0, 0, 0, 0, 0, 0]
              [2, 0, 3, 0, 6, 1, 0, 0, 4]]  #[2, 0, 3, 0, 6, 1, 0, 0, 4]
    sudoku_result = sudoku_solution(sudoku, 9)
    print_sudoku(sudoku_result)
    
if __name__ == '__main__':
    test()
    
sudoku = []
n = 9 #Размерность судоку
print('Введите чила построчно, разделяя пробелом.')
print('Пустые ячейки заполняйте нулями.')

'''
for i in range(n):
    #Ввод данных через пробел
    sudoku.append(list(int(x) for x in input().split()))
'''

