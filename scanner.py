import re


class scanner():

    def __init__(self):
        self.set_state('START')
        self.tokens = []
        self.other_state = False

    def set_state(self, state):
        for key in self.STATES:
            self.STATES[key] = False
        self.STATES[state] = True

    def get_state(self, state):
        return self.STATES[state]

    def scan(self, input_file='tiny.txt'):
        input_text = self.read_file(input_file)
        token = ''
        for char in input_text:
            if self.get_state('START'):
                if self.is_symbol(char):
                    self.set_state('DONE')
                elif char == ' ':
                    self.set_state('START')
                    continue
                elif char == '{':
                    self.set_state('IN_COMMENT')
                elif self.is_num(char):
                    self.set_state('IN_NUM')
                elif self.is_identifier(char):
                    self.set_state('IN_ID')
                elif self.is_colon(char):
                    self.set_state('IN_ASSIGN')

            elif self.get_state('IN_COMMENT'):
                if char == '}':
                    self.set_state('DONE')
                else:
                    self.set_state('IN_COMMENT')

            elif self.get_state('IN_NUM'):
                if self.is_num(char):
                    self.set_state('IN_NUM')
                elif char == ' ':
                    self.set_state('DONE')
                else:
                    self.set_state('OTHER')

            elif self.get_state('IN_ID'):
                if self.is_identifier(char) or self.is_num(char):
                    self.set_state('IN_ID')
                elif char == ' ':
                    self.set_state('DONE')
                else:
                    self.set_state('OTHER')

            elif self.get_state('IN_ASSIGN'):
                if char == '=':
                    self.set_state('DONE')
                else:
                    self.set_state('OTHER')

            if not self.get_state('OTHER'):
                token += char

            if self.get_state('OTHER'):
                self.set_state('DONE')
                self.other_state = True

            if self.get_state('DONE'):
                self.categorize(token)
                if self.other_state:
                    token = char
                    if self.is_colon(char): self.set_state('IN_ASSIGN')
                    if self.is_comment(char): self.set_state('IN_COMMENT')
                    if self.is_num(char): self.set_state('IN_NUM')
                    if self.is_identifier(char): self.set_state('IN_ID')
                    if self.is_symbol(char):
                        self.categorize(char)
                        token = ''
                        self.set_state('START')
                    self.other_state = False
                else:
                    token = ''
                self.set_state('START')

    def categorize(self, token):
        if token[-1:] == ' ': token = token[0:-1]
        if self.is_identifier(token):
            if token in self.Reserved_Words:
                self.tokens.append([token, token.upper()])
            else:
                self.tokens.append([token, 'IDENTIFIER'])
        elif self.is_num(token):
            self.tokens.append([token, 'NUMBER'])
        elif token in self.Special_Symbols:
            self.tokens.append([token, self.Special_Symbols[token]])
        elif self.is_comment(token):
            self.tokens.append([token, 'COMMENT'])

    def is_identifier(self, token):
        return token.isidentifier()

    def is_num(self, token):
        return token.isdigit()

    def is_colon(self, c):
        return True if c == ':' else False

    def is_symbol(self, token):
        symbol = ['+', '-', '*', '/', '=', '<', '>', '(', ')', ';']
        return True if token in symbol else False

    def is_comment(self, token):
        return True if re.match(r'^{.+}$', token) else False

    def read_file(self, fileName):
        with open(fileName, 'r') as f:
            input_text = f.read()
            input_text = input_text.replace('\n', ' ')
            input_text += ' '
            return input_text

    def output(self):
        with open('output.txt', 'w') as f:
            f.write('{},{}\n'.format('Token value', 'Token Type'))
            for token in self.tokens:
                f.write('{},{}\n'.format(token[0], token[1]))

    Reserved_Words = ['else', 'end', 'if', 'repeat', 'then', 'until', 'read', 'write']

    STATES = {
        'START': False,
        'IN_COMMENT': False,
        'IN_ID': False,
        'IN_NUM': False,
        'IN_ASSIGN': False,
        'DONE': False,
        'OTHER': False
    }

    Special_Symbols = {
        '+': 'Plus',
        '-': 'Minus',
        '*': 'Multiplication',
        '/': 'Division',
        ':': 'Colon',
        '=': 'Equal',
        ':=': 'Assignment',
        '>': 'Greater_than',
        '<': 'Less_than',
        ';': 'Semicolon',
        '(': 'Right_parenthesis',
        ')': 'Left_parenthesis'
    }
