# from pprint import pprint
from random import randint


class CardCell():
    """
    Class representing particular cell

    ...

    Attributes
    ----------
    data : int, str
    matched : boolean

    Methods
    -------
    empty_cell()
        Turns itself to cell with no data

    match_cell()
        Turns cell to matched state with 'X' representation
    """

    def __init__(self, numb=None):
        self.data = numb
        self.matched = False

    def empty_cell(self):
        self.data = None
        self.matched = None

    def match_cell(self):
        self.data = 'X'
        self.matched = True

    def __repr__(self):
        return f'cell[{self.data}]'


class Card():
    """
    Class representing Card object.
    It has responsibillity for manipulating cells
    ...

    Attributes
    ----------
    num : int
    digit_cells_number : int
    matched_cells : int
    width : int
    height : int

    Methods
    -------
    empty_cells_count(axis=None)
        Return number of empty cells axiswise

    card_from_data(data)
        Fills Card with CardCell instances, considering data width and height

    match_card(number, cb, player)
        Check if input number equals any number inside Card.
        If any, calls callback to notify GameLoop instance

    set_digit_cells_number()
        Calculate digit_cells_number(total non-empty cells) from data

    rows()
        Return row's generator

    columns()
        Return column's generator

    """

    def __init__(self, width=None, height=None, data=None):
        self.num = 0
        self.digit_cells_number = None
        self.matched_cells = 0

        if (width and height) is None:
            raise Exception('Cannot be empty')

        else:
            self.width = width
            self.height = height

            # print(f'digit_cells_number {self.digit_cells_number}')

            if not data:
                self.data = [[CardCell(randint(1, 100))
                             for el in range(self.width)]
                             for el in range(self.height)]
            else:
                self.card_from_data(data)

    def empty_cells_count(self, axis=None):
        count = 0

        # simple counter
        if not axis:
            flattened_data = \
                [item for sublist in self.data for item in sublist]

            for el in flattened_data:
                if el.data is None:
                    count += 1

            # return f'total Empty cells {count}'
            return count

        # count rows
        elif axis == 1:
            count = []
            for rw in self.rows:
                count.append([len(list(filter(lambda x: x.data is None, rw)))])

            # return f'total Empty cells in rows {count}'
            return count

        # count columns
        elif axis == 2:
            count = []
            for rw in self.columns:
                count.append(len(list(filter(lambda x: x.data is None, rw))))

            # return f'total Empty cells in columns {count}'
            return count

        else:
            raise Exception('axis must be 1 or 2')

    def card_from_data(self, data):
        data_gen = (CardCell(i) for i in data)
        if self.width*self.height != len(data):
            raise Exception(f'data dont fit to card form: \
                {self.width*self.height}!= {len(data)}')

        self.data = [[next(data_gen)
                     for el in range(self.width)]
                     for el in range(self.height)]

    def match_card(self, number, cb, player):

        for row in self.data:
            for cell in row:
                if cell.data == number:
                    # print(f'\t matched {cell.data} to {number}')
                    cell.match_cell()
                    self.matched_cells += 1

                    # Notify Game to stop
                    if self.matched_cells >= self.digit_cells_number:
                        cb(winner=player)

    def set_digit_cells_number(self):
        self.digit_cells_number = self.width * self.height -\
            self.empty_cells_count()

    @property
    def rows(self):
        return (rw for rw in self.data)

    @property
    def columns(self):
        for i in range(self.width):
            yield [el[i] for el in self.data]

    def __iter__(self):
        return self

    def __next__(self):
        if self.num < self.height:
            num = self.num
            self.num += 1
            return self.data[num]
        else:
            raise StopIteration()

    def __repr__(self):
        output = ''
        for row in self.data:
            output += f'{row} \n'

        return f'{output}'

    def __str__(self):
        output = ''
        for row in self.data:
            output += '|'
            for el in row:
                if el.data and (el.data != 'X'):
                    output += f' {el.data:02} '
                elif el.data == 'X':
                    output += ' XX '
                else:
                    output += '    '

            output += '|\n'

        return f'{output}'
