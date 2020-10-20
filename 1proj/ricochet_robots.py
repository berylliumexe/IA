# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys


class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas.
        """
        return self.id < other.id


class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    def __init__(self, size, robots, target, barriers):
        self.size = size
        self.board = []
        self.target = ()        

        #init board
        for x in range(size):
            self.board.append([])
            for y in range(size):
                self.board[x].append([])
                self.board[x][y] = {"robot":None, "barriers":[], "target":None}

                if x == 0:
                    self.board[x][y]["barriers"].append("u")
                if x == self.size - 1:
                    self.board[x][y]["barriers"].append("b")
                if y == 0:
                    self.board[x][y]["barriers"].append("l")
                if y == self.size - 1:
                    self.board[x][y]["barriers"].append("r")

        #append robots
        for r, pos in robots:
            self._robot_set_position(r, pos)
        
        #append target
        t, pos = target
        self.board[pos[0] - 1][pos[1] - 1]["target"] = t
        self.target = target

        #append barriers
        for b, pos in barriers:
            self.board[pos[0] - 1][pos[1] - 1]["barriers"].append(b)
            

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y]["robot"] == robot:
                    return (x + 1, y + 1)

    def robot_valid_actions(self, robot):
        """ Devolve as possiveis ações do robô passado como argumento. """
        actions = []

        r_x, r_y = self.robot_position(robot)

        #try up        
        if ("u" not in self.board[r_x - 1][r_y - 1]["barriers"]) and ("b" not in self.board[r_x - 2][r_y - 1]["barriers"]) \
            and (self.board[r_x - 2][r_y - 1]["robot"] == None):

            actions.append((robot, "u"))

        #try bot
        if ("b" not in self.board[r_x - 1][r_y - 1]["barriers"]) and ("u" not in self.board[r_x][r_y - 2]["barriers"]) \
            and (self.board[r_x][r_y - 2]["robot"] == None):

            actions.append((robot, "b"))

        #try left
        if ("l" not in self.board[r_x - 1][r_y - 1]["barriers"]) and ("r" not in self.board[r_x - 1][r_y - 2]["barriers"]) \
            and (self.board[r_x - 1][r_y - 2]["robot"] == None):

            actions.append((robot, "l"))

        #try right
        if ("r" not in self.board[r_x - 1][r_y - 1]["barriers"]) and ("l" not in self.board[r_x - 1][r_y]["barriers"]) \
            and (self.board[r_x - 1][r_y]["robot"] == None):

            actions.append((robot, "r"))
        
        return actions

    def _robot_set_position(self, robot, position):
        x, y = position
        self.board[x - 1][y - 1]["robot"] = robot
    
    def _robot_reset_position(self, position):
        x, y = position
        self.board[x - 1][y - 1]["robot"] = None
    
    def robot_action(self, action):
        robot, pos = action

        self._robot_reset_position(self.robot_position(robot))
        self._robot_set_position(robot, pos)

    """
    def end(self):
        self._robot_reset_position(self.robot_position(self.target[0]))
        self._robot_set_position(*self.target)

    def end_check(self):
        robot_pos = self.robot_position(self.target[0])
    """
    # TODO: outros metodos da classe



def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    # TODO
    size = 0
    robots = []
    target = None
    barriers = []

    num_robots = 4

    with open(filename) as file:
        size = int(file.readline())
        
        #parse robots
        for _ in range(num_robots):
            line = file.readline().split(" ")
            robots.append( (line[0], (int(line[1]), int(line[2])) ))

        #parse target
        line = file.readline().split(" ")
        target = (line[0], (int(line[1]), int(line[2]))) #(color, (x, y))
        
        #parse barriers
        for _ in range(int(file.readline())):
            line = file.readline().rsplit()
            barriers.append( (line[2], (int(line[0]), int(line[1])) ))

    return Board(size, robots, target, barriers)



class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = RRState(board)

        #self.goal = RRState(board)
        #self.goal.board.end()

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []

        robots = ("R", "Y", "G", "B")
        
        for r in robots:
            actions += state.board.robot_valid_actions(r)

        return actions

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """

        new_state = RRState(state.board)

        new_state.board.robot_action(action)

        return new_state

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """

        return 

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    board = parse_instance(sys.argv[1])

    problem = RicochetRobots(board)

    initial_state = RRState(board)

    print(problem.actions(initial_state))
    #result_state = problem.result(initial_state)
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
