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
                    self._set_barrier("u", (x,y))
                if x == self.size - 1:
                    self._set_barrier("b", (x,y))
                if y == 0:
                    self._set_barrier("l", (x,y))
                if y == self.size - 1:
                    self._set_barrier("r", (x,y))

        #append robots
        for r, pos in robots:
            self._set_robot(r, pos)
        
        #append target
        t, pos = target
        self._set_target(t, pos)

        #append barriers
        for b, pos in barriers:
            x, y = pos
            self._set_barrier(b, (x,y))

    def __position(self, position):
        return position[0] - 1, position[1] -1

    def __get_position(self, position):
        x, y = self.__position(position)
        return self.board[x][y]

    def _get_barriers(self, position):
        return self.__get_position(position)["barriers"]
    
    def _get_robot(self, position):
        return self.__get_position(position)["robot"]
    
    def _get_target(self, position):
        return self.__get_position(position)["target"]

    def _set_barrier(self, barrier, position):
        self.__get_position(position)["barriers"].append(barrier)

    def _set_robot(self, robot, position):
        self.__get_position(position)["robot"] = robot

    def _set_target(self, target, position):
        self.__get_position(position)["target"] = target
        self.target = position, target
    
    def _reset_robot(self, position):
        self.__get_position(position)["robot"] = None
            

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        
        for x in range(self.size):
            for y in range(self.size):
                if self._get_robot((x, y)) == robot:
                    return (x + 1, y + 1)

    def robot_valid_actions(self, robot):
        """ Devolve as possiveis ações do robô passado como argumento. """
        actions = []

        r_x, r_y = self.__position(self.robot_position(robot))

        #try up        
        if ("u" not in self._get_barriers((r_x, r_y))) and ("b" not in self._get_barriers((r_x - 1, r_y))) \
            and (self._get_robot((r_x - 1, r_y)) == None):

            actions.append((robot, "u"))

        #try bot
        if ("b" not in self._get_barriers((r_x, r_y))) and ("u" not in self._get_barriers((r_x + 1, r_y - 1))) \
            and (self._get_robot((r_x + 1, r_y - 1)) == None):

            actions.append((robot, "b"))

        #try left
        if ("l" not in self._get_barriers((r_x, r_y))) and ("r" not in self._get_barriers((r_x, r_y - 1))) \
            and (self._get_robot((r_x, r_y - 1)) == None):

            actions.append((robot, "l"))

        #try right
        if ("r" not in self._get_barriers((r_x, r_y))) and ("l" not in self._get_barriers((r_x , r_y + 1))) \
            and (self._get_robot((r_x, r_y + 1)) == None):

            actions.append((robot, "r"))
        
        return actions
    
    
    def robot_action(self, action):
        robot, pos = action

        self._reset_robot(self.robot_position(robot))
        self._set_robot(robot, pos)

    def robot_check_target(self):
        x, y = self.__position(self.robot_position(self.target[0]))
        return self._get_target((x,y)) == self._get_robot((x,y))


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

        return state.board.robot_check_target()        

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
