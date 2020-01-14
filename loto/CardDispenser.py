from Card import Card
from random import shuffle, choice


class CardDispenser():
    """
    Class creating particular Card with provided set of rules

    ...

    Attributes
    ----------
    card_rows : int
    card_columns : int
    total_cells : int
    row_max_empties : int
    col_max_empties : int

    Methods
    -------
    set_rules(rules=None))
        Seting rules for Card

    get_proper_card()
        Return final card state

    apply_constraints(card=None)
        Helper function to get_proper_card()

    try_empty_columnwise(card, column)
        Helper function to get_proper_card().
        deleting random cell at each column

    try_empty(card)
        Helper function to get_proper_card()
        deleting random cells to meet constraints

    make_empty_card()
        Generate empty card with specific form

    """

    def __init__(self):
        self.card_rows = None
        self.card_columns = None
        self.total_cells = None
        self.row_max_empties = None
        self.col_max_empties = None

    def set_rules(self, rules=None):
        self.card_rows = rules['rows']
        self.card_columns = rules['columns']
        self.total_cells = self.card_rows * self.card_columns
        self.row_max_empties = rules['row_max_empties']
        self.col_max_empties = rules['col_max_empties']

    def get_proper_card(self):
        # get random 3 out of 9 variants for each column
        empty_card = self._make_empty_card()

        for i, col in enumerate(empty_card.columns, 1):
            all_variants = [el for el in range(10*(i-1)+1, 10*i)]
            shuffle(all_variants)
            picked = all_variants[:self.card_rows]
            picked = sorted(picked)

            for i, col_i in enumerate(col):
                col_i.data = picked[i]

        proper_card = self._apply_constraints(empty_card)
        proper_card.set_digit_cells_number()

        return proper_card

    def _apply_constraints(self, card=None):

        max_empty_cells = \
            self.total_cells \
            - (self.card_columns - self.row_max_empties) * self.card_rows

        while card.empty_cells_count() < max_empty_cells:

            # each column must have at least one Empty
            for col_i in card.columns:
                self._try_empty_columnwise(card, col_i)

            self._try_empty(card)

        return card

    def _try_empty_columnwise(self, card, column):
        random_row = choice(range(self.card_rows))
        old_value = column[random_row].data
        column[random_row].empty_cell()

        if (max(card.empty_cells_count(axis=1))[0] > self.row_max_empties) or \
                (max(card.empty_cells_count(axis=2)) > self.col_max_empties):
            column[random_row].data = old_value
            self._try_empty_columnwise(card, column)

    def _try_empty(self, card):
        random_col = choice(range(self.card_columns))
        random_row = choice(range(self.card_rows))

        old_value = card.data[random_row][random_col].data
        card.data[random_row][random_col].empty_cell()

        if (max(card.empty_cells_count(axis=1))[0] > self.row_max_empties) or \
                (max(card.empty_cells_count(axis=2)) > self.col_max_empties):
            card.data[random_row][random_col].data = old_value
            self._try_empty(card)

    def _make_empty_card(self):
        empties = [None for i in range(self.total_cells)]
        return Card(self.card_columns, self.card_rows, empties)
