import random
from blackjack_parser import BlackjackParser

class BlackjackGame:
    def __init__(self):
        # Inicializa o parser e as variáveis do jogo
        self.parser = BlackjackParser()
        self.dealer_cards = []
        self.player_cards = []
        self.split_hands = []  # Para armazenar as mãos divididas
        self.total_points = 21
        self.doubled = False  # Para verificar se a aposta foi dobrada

    def start_game(self):
        # Configura o jogo e inicia a interação com o jogador
        self.configure_game()
        self.deal_initial_cards()

        while True:
            self.display_player_hand()
            option = input('Escolha uma ação: hit (comprar carta), double (dobrar aposta), split (dividir mão), hold (parar): ').lower()

            if option == 'hit':
                self.player_cards.append(random.randint(2, 11))
            elif option == 'double':
                self.double_bet()
                break  # Após dobrar a aposta, a rodada acaba
            elif option == 'split' and len(self.player_cards) == 2 and self.player_cards[0] == self.player_cards[1]:
                self.split_hand()
            elif option == 'hold':
                break
            else:
                print('Ação inválida. Tente outra ação.')

        self.calculate_results()

    def configure_game(self):
        # Permite ao jogador alterar a regra de pontos totais do jogo
        change_total_points = input('Deseja mudar o total de 21 pontos de cartas? (s/n): ').lower()

        if change_total_points == 's':
            total_points_value = input('Digite um novo valor de pontos totais: ')

            if total_points_value.isdigit():
                self.total_points = int(total_points_value)
                print(f'Regra definida para {self.total_points} pontos totais')
            else:
                print('Erro: Opção inválida. Portanto a regra continuará sendo 21 pontos totais')
        elif change_total_points == 'n':
            print('Regra permanecida como 21 pontos totais')
        else:
            print('Erro: Opção inválida. Portanto a regra continuará sendo 21 pontos totais')

    def deal_initial_cards(self):
        # Compra cartas para o dealer até que ele tenha uma pontuação perto do limite
        while sum(self.dealer_cards) < self.total_points - 4:
            self.dealer_cards.append(random.randint(2, 11))

        print("Cartas do Dealer: ", self.dealer_cards)

        # Dá duas cartas iniciais ao jogador
        self.player_cards.append(random.randint(2, 11))
        self.player_cards.append(random.randint(2, 11))

    def display_player_hand(self):
        print("\nSuas cartas: ", self.player_cards)

    def double_bet(self):
        print("Você escolheu dobrar a aposta.")
        self.doubled = True
        self.player_cards.append(random.randint(2, 11))
        print("Sua nova carta é:", self.player_cards[-1])

    def split_hand(self):
        print("Você escolheu dividir a mão.")
        self.split_hands.append([self.player_cards[0]])
        self.split_hands.append([self.player_cards[1]])
        self.player_cards = []
        for hand in self.split_hands:
            hand.append(random.randint(2, 11))
            print(f"Nova mão: {hand}")

    def calculate_results(self):
        d_expression = f'dealer={self.total_points}-'
        for i in range(len(self.dealer_cards)):
            if i == 0:
                d_expression += f'{self.dealer_cards[i]}'
            else:
                d_expression += f'+{self.dealer_cards[i]}'

        self.parser.parse(d_expression)

        p_expression = f'player={self.total_points}-'
        for i in range(len(self.player_cards)):
            if i == 0:
                p_expression += f'{self.player_cards[i]}'
            else:
                p_expression += f'+{self.player_cards[i]}'

        self.parser.parse(p_expression)

        print('\n------------------------------------------')
        print('Resultado:\n')

        env = self.parser.env
        if env['dealer'] < 0 and env['player'] < 0:
            print(f'A pontuação de ambos foi maior que {self.total_points}. Ocorreu um empate!!!')
        elif env['dealer'] < 0 and env['player'] >= 0:
            print(f'A pontuação do Dealer foi maior que {self.total_points}. Você ganhou!!!')
        elif env['dealer'] >= 0 and env['player'] < 0:
            print(f'A sua pontuação foi maior que {self.total_points}. Você perdeu!!!')
        elif env['dealer'] < env['player']:
            print('A pontuação do dealer foi maior. Você perdeu!!!')
        elif env['dealer'] > env['player']:
            print('Sua pontuação foi maior que a do Dealer. Você ganhou!!!')
        elif env['dealer'] == env['player']:
            print('A pontuação de ambos é igual. Ocorreu um empate!!!')

        print('------------------------------------------')
        print('Total de cartas:\n')
        print(f'Pontuação do Dealer: {sum(self.dealer_cards)}')
        print(f'Sua pontuação: {sum(self.player_cards)}')
        print('------------------------------------------')

if __name__ == '__main__':
    # Inicia o jogo
    game = BlackjackGame()
    game.start_game()