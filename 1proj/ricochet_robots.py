# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 18:
# 93744 Nuno Carvalho
# 93739 Miguel Silva

from search import Problem, Node, astar_search, compare_searchers, iterative_deepening_search, recursive_best_first_search, bidirectional_search, depth_first_graph_search, depth_first_tree_search
from utils import manhattan_distance, euclidean_distance, hamming_distance
import sys
import math
import random
from timeit import default_timer as timer

from multiprocessing import Manager, cpu_count, Process

ROBOTS = ("Y", "B", "G", "R")

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

    def __hash__(self):
        return hash(self.board)
    
    def __eq__(self, other):
        return self.board == other.board
    
class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    def __init__(self, size, robots, target, barriers, parsed=False, simplified=False):
        self._size = size
        self._target = ()
        self._robots = {}
        self._barriers = {}
        self.simplified = simplified

        #append robots
        for pos in robots:
            self._set_robot(robots[pos], pos)

        #append target
        t, pos = target
        self._set_target(t, pos)

        #append barriers
        for pos in barriers:
            for b in barriers[pos]:
                self._set_barrier(b, pos)

                if parsed:
                    if b == "u":
                        self._set_barrier("d", self.__position_change(pos, "u"))
                    if b == "d":
                        self._set_barrier("u", self.__position_change(pos, "d"))
                    if b == "l":
                        self._set_barrier("r", self.__position_change(pos, "l"))
                    if b == "r":
                        self._set_barrier("l", self.__position_change(pos, "r"))

        if parsed:
            for x in range(1, size +  1):
                self._set_barrier("l", (x, 1))
                self._set_barrier("r", (x, self._size))

            for y in range(1, size + 1):
                self._set_barrier("u", (1, y))
                self._set_barrier("d", (self._size, y))

    def __hash__(self):
        if self.simplified:
            return hash((self.robot_position(self.get_target()[0])))
        else:
            return hash((self.robot_position(r) for r in ROBOTS))


    def __eq__(self, other):
        if self.simplified:
            r = self.get_target()[0]
            return self.robot_position(r) == other.robot_position(r)
        else:
            return all(self.robot_position(r) == other.robot_position(r) for r in ROBOTS)

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

    #getters
    def _get_barriers(self, position):
        try:
            return self._barriers[position]
        except KeyError:
            return []

    def _get_robot(self, position):
        try:
            return self._robots[position]
        except KeyError:
            return None

    def _set_barrier(self, barrier, position):
        try:
            self._barriers[position].append(barrier)
        except KeyError:
            self._barriers[position] = []
            self._barriers[position].append(barrier)

    def get_target(self):
        return self._target

    #setters
    def _set_robot(self, robot, position):
        self._robots[position] = robot

    def _set_target(self, target, position):
        self._target = target, position

    def _reset_robot(self, position):
        del self._robots[position]

    def _valid_action(self, position, direction):
        aux_pos = self.__position_change(position, direction)
        if self.simplified:
            return direction not in self._get_barriers(position)
        else:
            return direction not in self._get_barriers(position) and \
                    self._get_robot(aux_pos) == None

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """     
        for r in self._robots:
            if self._robots[r] == robot:
                return r

    def robot_valid_actions(self, robot):
        """ Devolve as possiveis ações do robô passado como argumento. """
        pos = self.robot_position(robot)

        pa = ["r", "d", "l", "u"]
        
        actions = [(robot, ac) for ac in pa if self._valid_action(pos, ac)]

        return actions


    def robot_action(self, action):
        robot, direction = action
        position = self.robot_position(robot)
        
        self._reset_robot(position)
        
        if self.simplified:
            if self._valid_action(position, direction):
                position = self.__position_change(position, direction)
        else:
            while self._valid_action(position, direction):
                position = self.__position_change(position, direction)

        self._set_robot(robot, position)
    
    def check_finish(self):
        tg = self.get_target()
        return tg[1] == self.robot_position(tg[0])
    
def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    size = 0
    robots = {}
    barriers = {}
    target = None

    num_robots = 4

    with open(filename) as file:
        size = int(file.readline())

        #parse robots
        for _ in range(num_robots):
            line = file.readline().split(" ")
            robots[(int(line[1]), int(line[2]))] = line[0]

        #parse target
        line = file.readline().split(" ")
        target = (line[0], (int(line[1]), int(line[2]))) #(color, (x, y))

        #parse barriers
        for _ in range(int(file.readline())):
            line = file.readline().rsplit()
            try:
                barriers[(int(line[0]), int(line[1]))].append(line[2])
            except KeyError:
                barriers[(int(line[0]), int(line[1]))] = []
                barriers[(int(line[0]), int(line[1]))].append(line[2])


    return Board(size, robots, target, barriers, True)


class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = RRState(board)

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """

        actions = []
        for r in ROBOTS:
            actions += state.board.robot_valid_actions(r)

        return actions

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        b = state.board
    
        new_board = Board(b._size, b._robots, b._target, b._barriers)
        new_board.robot_action(action)

        return RRState(new_board)

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """

        return state.board.check_finish()

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        b = node.state.board
        
        simplified_problem = SimplifiedRicochetRobots(b)
        solution_node = recursive_best_first_search(simplified_problem)

        aux = 0
        counter = 0

        if solution_node != None:
            for s in solution_node.solution():
                if s[1] != aux:
                    aux = s[1]
                    counter += 1
        else:
            counter = 3
        return counter

class SimplifiedRicochetRobots(RicochetRobots):
    def __init__(self, board: Board):
        self.initial = RRState(board)

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        robot = state.board.get_target()[0]

        actions = state.board.robot_valid_actions(robot)
        return actions

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        b = state.board
    
        new_board = Board(b._size, b._robots, b._target, b._barriers, simplified=True)
        new_board.robot_action(action)

        return RRState(new_board)
    
    def h(self, node: Node):
        b = node.state.board
        robot_pos = b.robot_position(b.get_target()[0])
        target_pos = b.get_target()[1]

        return manhattan_distance(robot_pos, target_pos)

def output(node):
    print(len(node.solution()))

    for s in node.solution():
        print(f"{s[0]} {s[1]}")

if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    board = parse_instance(sys.argv[1])

    problem = RicochetRobots(board)

    solution_node = recursive_best_first_search(problem)

    output(solution_node)
