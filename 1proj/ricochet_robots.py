# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 18:
# 93744 Nuno Carvalho
# 93739 Miguel Silva

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys
import math
import random


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
        self.robots = {}

        #init board
        for x in range(size):
            self.board.append([])
            for y in range(size):
                self.board[x].append([])
                self.board[x][y] = {"robot":None, "barriers":[]}

                if x == 0:
                    self._set_barrier("u", (x,y))
                if x == self.size - 1:
                    self._set_barrier("d", (x,y))
                if y == 0:
                    self._set_barrier("l", (x,y))
                if y == self.size - 1:
                    self._set_barrier("r", (x,y))

        #append robots
        for r, pos in robots:
            self._set_robot(r, self.__position_in(pos))

        #append target
        t, pos = target
        self._set_target(t, self.__position_in(pos))

        #append barriers
        for b, pos in barriers:
            self._set_barrier(b, self.__position_in(pos))
            if b == "u":
                self._set_barrier("d", self.__position_in(self.__position_change(pos, "u")))
            if b == "d":
                self._set_barrier("u", self.__position_in(self.__position_change(pos, "d")))
            if b == "l":
                self._set_barrier("r", self.__position_in(self.__position_change(pos, "l")))
            if b == "r":
                self._set_barrier("l", self.__position_in(self.__position_change(pos, "r")))

    def __position_change(self, position, direction):
        """ Returns the translated position according to the input direction """
        if direction == "u":
            return (position[0] - 1, position[1])
        if direction == "d":
            return (position[0] + 1, position[1])
        if direction == "l":
            return (position[0], position[1] - 1)
        if direction == "r":
            return (position[0], position[1] + 1)

    def __position_out(self, position):
        return (position[0] + 1, position[1] + 1)

    def __position_in(self, position):
        return (position[0] - 1, position[1] - 1)

    def __get_position(self, position):
        x, y = position
        return self.board[x][y]

    def _get_barriers(self, position):
        return self.__get_position(position)["barriers"]

    def _get_robot(self, position):
        return self.__get_position(position)["robot"]

    def get_target(self):
        return self.target[0], self.__position_out(self.target[1])

    def _set_barrier(self, barrier, position):
        self.__get_position(position)["barriers"].append(barrier)

    def _set_robot(self, robot, position):
        self.__get_position(position)["robot"] = robot
        self.robots[robot] = position

    def _set_target(self, target, position):
        self.target = target, position

    def _reset_robot(self, position):
        robot = self._get_robot(position)
        self.__get_position(position)["robot"] = None
        self.robots[robot] = None

    def _valid_action(self, position, direction):
        aux_pos = self.__position_change(position, direction)
        if direction not in self._get_barriers(position) and self._get_robot(aux_pos) == None:
            return True                
        return False

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """     
        return self.__position_out(self.robots[robot])
    

    def robot_valid_actions(self, robot):
        """ Devolve as possiveis ações do robô passado como argumento. """
        pos = self.__position_in(self.robot_position(robot))

        possible_actions = ("u", "d", "l", "r")

        actions = [(robot, ac) for ac in possible_actions if self._valid_action(pos, ac)]

        return actions


    def robot_action(self, action):
        robot, direction = action
        position = self.__position_in(self.robot_position(robot))
        self._reset_robot(position)

        while(self._valid_action(position, direction)):
            position = self.__position_change(position, direction)
        
        self._set_robot(robot, position)

    def robot_check_target(self):
        tg = self.get_target()
        return tg[1] == self.robot_position(tg[0])


def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
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

        random.shuffle(actions)
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
        color, target_pos = node.state.board.get_target()
        robot_pos = node.state.board.robot_position(color)
        #return math.sqrt(math.pow((target_pos[0] - robot_pos[0]), 2) + math.pow((target_pos[1] - robot_pos[1]), 2)) # euclidian distance
        return abs(target_pos[0] - robot_pos[0]) + abs(target_pos[1] - robot_pos[1]) # manhathan distance



if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    board = parse_instance(sys.argv[1])

    problem = RicochetRobots(board)

    # Obter o nó solução usando a procura A*:
    solution_node = astar_search(problem)

    print(solution_node.solution)
    #result_state = problem.result(initial_state)
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
