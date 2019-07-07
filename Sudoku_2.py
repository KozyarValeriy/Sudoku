import copy
import random

class Sudoku():
    def __init__(self, sudoku, size=9):
        ''' Class sudoku
        Arguments:
        sudoku -- sudoku,
        result -- whether the solved Sudoku,
        adress_empty_cell -- cell addresses with a pass number
        size -- digit capacity of sudoku.
        '''
        self.sudoku = sudoku
        self.result = False
        self.adress_empty_cell = []
        self.size = size

    def __getitem__(self, index):
        return self.sudoku[index]    

    def __str__(self):
        string_sudoku = ''
        for row in self.sudoku:
            string_sudoku += '[' 
            for item in row:
                string_sudoku += (str(item) + ', ')
            string_sudoku = string_sudoku.rstrip()
            string_sudoku = string_sudoku[0:len(string_sudoku)-1]
            string_sudoku += ']\n'
        return string_sudoku

    def solution(self):
        ''' Method to solve sudoku       
        Changes the object itself
        '''
        self.find_empty_adress()           
        self._find_pass_cell()
        if not self.result:
            self._try_predict()

    def find_empty_adress(self):
        empty_cell = [x for x in range(1, self.size + 1)]
        for row_numb in range(self.size):
            for col_numb in range(self.size):
                if self[row_numb][col_numb] == 0:
                    self[row_numb][col_numb] = empty_cell.copy()
                    self.adress_empty_cell.append([row_numb, col_numb])    

    def _find_pass_cell(self):
        ''' Function to fill empty cells '''
        # Variable for exit from loop
        self.counter = 0
        len_adress_mas = len(self.adress_empty_cell)
        while len_adress_mas > 0:
            prev_len_adress_mas = len_adress_mas 
            for adress in self.adress_empty_cell:
                if not self[adress[0]][adress[1]]:
                    break
                self._search_by_square(adress)
                self._search_by_row(adress)
                self._search_by_col(adress)
            for i in range(len(self.adress_empty_cell) - 1, -1, -1):       
                if len(self[self.adress_empty_cell[i][0]][self.adress_empty_cell[i][1]]) == 1:
                    (self[self.adress_empty_cell[i][0]]
                         [self.adress_empty_cell[i][1]]) = (self[self.adress_empty_cell[i][0]]
                                                                [self.adress_empty_cell[i][1]][0])
                    del self.adress_empty_cell[i]
            len_adress_mas = len(self.adress_empty_cell)
            if prev_len_adress_mas == len_adress_mas:
                self.counter += 1
            else:
                self.counter = 0
            if self.counter > 5:
                break
        else:
            self.result = True

    def _search_by_square(self, adress):
        ''' Function to find matches in a square ''' 
        square_size = int(self.size ** 0.5)
        square_adress = [adress[0] // square_size, adress[1] // square_size]    
        for row in range(square_size * square_adress[0], square_size * square_adress[0] + square_size):
            for col in range(square_size * square_adress[1], square_size * square_adress[1] + square_size):
                if (not isinstance(self[row][col], list) and
                        self[row][col] in self[adress[0]][adress[1]]):
                    del self[adress[0]][adress[1]][self[adress[0]][adress[1]].index(self[row][col])]   
    
    def _search_by_row(self, adress):
        ''' Function to find matches in a row '''
        for col in range(self.size):
            if (not isinstance(self[adress[0]][col], list) and 
                    self[adress[0]][col] in self[adress[0]][adress[1]]):
                del self[adress[0]][adress[1]][self[adress[0]][adress[1]].index(self[adress[0]][col])]  

    def _search_by_col(self, adress):
        ''' Function to find matches in a column '''
        for row in range(self.size):
            if (not isinstance(self[row][adress[1]], list) and 
                    self[row][adress[1]] in self[adress[0]][adress[1]]):
                del self[adress[0]][adress[1]][self[adress[0]][adress[1]].index(self[row][adress[1]])]  

    def _try_predict(self, iteration=20, lenth=3, volume_pred=1):
        ''' Function to solve with substitution
        Arguments:
        iteration -- number of iterations allowed to solve Sudoku;
        lenth -- maximum length of unknown values to assume
        volume_pred -- the number of predictions at a time.
        '''    
        # Dictionary to remember which elements have already been substituted
        d = dict(zip([tuple(adress) for adress in self.adress_empty_cell], 
                     [list() for x in range(len(self.adress_empty_cell))]))
        count = 0
        for i in range(iteration):
            temp_sudoku = Sudoku(copy.deepcopy(self.sudoku))
            temp_sudoku.adress_empty_cell = copy.deepcopy(self.adress_empty_cell)
            random.shuffle(temp_sudoku.adress_empty_cell)
            for adress in temp_sudoku.adress_empty_cell:
                if (len(temp_sudoku[adress[0]][adress[1]]) <= lenth and #len(d[tuple(adress)]) < lenth and
                    len(temp_sudoku[adress[0]][adress[1]]) > len(d[tuple(adress)])):
                    d[tuple(adress)].append(temp_sudoku[adress[0]][adress[1]][len(d[tuple(adress)])])
                    temp_sudoku[adress[0]][adress[1]] = d[tuple(adress)][-1]
                    del temp_sudoku.adress_empty_cell[temp_sudoku.adress_empty_cell.index(adress)]
                    count += 1
                    if count >= volume_pred:
                        break

            temp_sudoku._find_pass_cell()
            if temp_sudoku.result:
                self.sudoku = temp_sudoku.sudoku
                self.result = True
                self.adress_empty_cell = []
                print('The solution was found in %d iterations' % (i))
                break
        else:
            print('For %d iterations the solution was not found' % (iteration))
        print('--------------------')

def test(complexity):
    if complexity == 'Easy':
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
        sudoku = Sudoku(sudoku)
        sudoku.solution()
        print(sudoku)
    elif complexity == 'Medium':
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
        sudoku = Sudoku(sudoku)
        sudoku.solution()
        print(sudoku)
    elif complexity == 'Hard':        
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
        sudoku = Sudoku(sudoku)
        sudoku.solution()
        print(sudoku)
    elif complexity == 'Extreme':
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
        sudoku = Sudoku(sudoku)
        sudoku.solution()
        print(sudoku)
    
if __name__ == '__main__':
    test('Easy')
    print('\n---------------------------\n')    
    test('Medium')
    print('\n---------------------------\n')
    test('Hard')
    print('\n---------------------------\n')
    test('Extreme')

'''    
sudoku = []
n = 9 #Размерность судоку
print('Введите чила построчно, разделяя пробелом.')
print('Пустые ячейки заполняйте нулями.')


for i in range(n):
    #Ввод данных через пробел
    sudoku.append(list(int(x) for x in input().split()))
'''

