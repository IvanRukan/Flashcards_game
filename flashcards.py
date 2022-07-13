import json
import argparse


def add():
    global logs
    print(f'The card:')
    logs += '\nThe card:'
    term = input()
    logs += f'\n{term}'
    if term in terms:
        while term in terms:
            print(f'The term "{term}" already exists. Try again:')
            logs += f'\nThe term "{term}" already exists. Try again:'
            term = input()
            logs += f'\n{term}'
    print(f'The definition of the card:')
    logs += '\nThe definition of the card:'
    hardest_cards[term] = 0
    definition = input()
    logs += f'\n{definition}'
    if definition in terms.values():
        while definition in terms.values():
            print(f'The definition "{definition}" already exists. Try again:')
            logs += f'\nThe definition "{definition}" already exists. Try again:'
            definition = input()
            logs += f'\n{definition}'
    terms[term] = definition
    print(f'The pair ("{term}":"{definition}") has been added.')
    logs += f'\nThe pair ("{term}":"{definition}") has been added.'


def ask():
    global logs
    print('How many times to ask?')
    logs += '\nHow many times to ask?'
    amount = int(input())
    logs += f'\n{str(amount)}'
    iterator = (each for each in terms.items())
    for _ in range(amount):
        try:
            pair = next(iterator)
        except StopIteration:
            iterator = (each for each in terms.items())
            pair = next(iterator)
        print(f'Print the definition of "{pair[0]}"')
        logs += f'\nPrint the definition of "{pair[0]}"'
        answer = input()
        logs += f'\n{answer}'
        if answer == pair[1]:
            print('Correct!')
            logs += '\nCorrect!'
        else:
            hardest_cards[pair[0]] += 1
            for possible_term in terms.keys():
                if terms[possible_term] == answer:
                    print(
                        f'Wrong. The right answer is "{pair[1]}", but your definition is correct for "{possible_term}" card')
                    logs += f'\nWrong. The right answer is "{pair[1]}", but your definition is correct for "{possible_term}" card'
                    break
            else:
                print(f'Wrong. The right answer is "{pair[1]}".')
                logs += f'\nWrong. The right answer is "{pair[1]}".'


def remove():
    global logs
    print('Which card?')
    logs += '\nWhich card?'
    removable = input()
    logs += f'\n{removable}'
    try:
        terms.pop(removable)
        print('The card has been removed')
        logs += '\nThe card has been removed'
    except KeyError:
        print(f"Can't remove \"{removable}\": there is no such card.")
        logs += f"\nCan't remove \"{removable}\": there is no such card."


def importer():
    global logs
    print('File name')
    logs += '\nFile name'
    name = input()
    logs += f'\n{name}'
    try:
        with open(name, 'r') as json_file:
            loaded_cards = json.load(json_file)
            print(f'{len(loaded_cards)} cards have been loaded')
            logs += f'\n{len(loaded_cards)} cards have been loaded'
            terms.update(loaded_cards)
    except FileNotFoundError:
        print('File not found')
        logs += '\nFile not found'


def export():
    global logs
    print('File name')
    logs += '\nFile name'
    name = input()
    logs += f'\n{name}'
    with open(name, 'w') as json_file:
        json.dump(terms, json_file)
        print(f'{len(terms)} cards have been saved')
        logs += f'\n{len(terms)} cards have been saved'


def log():
    print('File name:')
    name = input()
    with open(name, 'w') as logging_file:
        logging_file.write(logs)
    print('The log has been saved')


def hardest_card():
    global logs
    if sum(sorted(hardest_cards.values())) == 0:  # multiple errors + updating import and export
        print('There are no cards with errors')
        logs += '\nThere are no cards with errors'
    elif len(sorted(hardest_cards.values())) == 1 or sorted(hardest_cards.values())[-1] != sorted(hardest_cards.values())[-2]:
        wrong_answers = sorted(hardest_cards.values())[-1]
        needed_term = ''
        for term in hardest_cards.keys():
            if hardest_cards[term] == wrong_answers:
                needed_term = term
                break
        print(f'The hardest card is {needed_term}. You have {hardest_cards[needed_term]} errors answering it.')
        logs += f'\nThe hardest card is {needed_term}. You have {hardest_cards[needed_term]} errors answering it.'
    else:
        cards_string = 'The hardest cards are '
        hardest = sorted(hardest_cards.values())[-1]
        for term in hardest_cards.keys():
            if hardest_cards[term] == hardest:
                cards_string += f'"{term}", '
        cards_string = cards_string.rstrip(', ')
        print(cards_string)
        logs += f'\n{cards_string}'


def reset():
    global hardest_cards, logs
    hardest_cards = dict.fromkeys(hardest_cards, 0)
    print('Card statistics have been reset')
    logs += '\nCard statistics have been reset'


def command_line():
    global logs
    if args.import_from:
        with open(args.import_from, 'r') as json_file:
            new_cards = json.load(json_file)
            terms.update(new_cards)
            print(f'{len(new_cards)} cards have been loaded')
            logs += f'\n{len(new_cards)} cards have been loaded'
            hardest_cards.update(dict.fromkeys(new_cards, 0))
    if args.export_to:
        with open(args.export_to, 'w') as json_file:
            json.dump(terms, json_file)
            print(f'{len(terms)} cards have been saved')
            logs += f'\n{len(terms)} cards have been saved'


terms = {}
logs = ''
hardest_cards = {}
parser = argparse.ArgumentParser()
parser.add_argument('--import_from')
parser.add_argument('--export_to')
args = parser.parse_args()
if args.import_from:
    command_line()
print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats)')
logs += '\nInput the action (add, remove, import, export, ask, exit, log, hardest card, reset stats)'
user_input = input()
logs += f'\n{user_input}'
while user_input != 'exit':
    if user_input == 'add':
        add()
    elif user_input == 'remove':
        remove()
    elif user_input == 'import':
        importer()
    elif user_input == 'export':
        export()
    elif user_input == 'ask':
        ask()
    elif user_input == 'log':
        log()
    elif user_input == 'hardest card':
        hardest_card()
    elif user_input == 'reset stats':
        reset()
    print()
    logs += '\n'
    print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats)')
    logs += '\nInput the action (add, remove, import, export, ask, exit, log, hardest card, reset stats)'
    user_input = input()
    logs += f'\n{user_input}'
else:
    if args.export_to:
        command_line()
    else:
        print('Bye bye!')
        logs += '\nBye bye!'
