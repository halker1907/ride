import keyboard
import random
import time
from colorama import Fore

class Game:
    def __init__(self, height, width):
        self.FPS = 5
        self.HEIGHT = height
        self.WIDTH = width
        self.PLAYER_CHAR = '\033[31m' + "▲"
        self.OBSTACLE_CHAR = "◙"
        self.BARRIER_CHAR = "▒"
        self.player_pos = self.HEIGHT - 1
        self.player_lane = 1
        self.obstacles = []
        self.barriers = []
        self.obstacle_counter = 0
        self.score = 0
        self.running = True

    def move_player(self, event):
        if event.name == 'a':
            self.player_lane = max(0, self.player_lane - 1)
        elif event.name == 'd':
            self.player_lane = min(2, self.player_lane + 1)

    def move_obstacles(self):
        for i, obstacle in enumerate(self.obstacles):
            self.obstacles[i] = (obstacle[0] + 1, obstacle[1])
        self.obstacles[:] = [obstacle for obstacle in self.obstacles if obstacle[0] < self.HEIGHT]

    def create_obstacle(self):
        if self.obstacle_counter < 3 and random.randint(0, 9) < 5:
            self.obstacles.append((0, random.randint(0, 2) * 4 + 2))
            self.obstacle_counter += 1
        else:
            self.obstacle_counter = 0

    def move_barriers(self):
        for i, barrier in enumerate(self.barriers):
            self.barriers[i] = (barrier[0] + 1, barrier[1])
        self.barriers[:] = [barrier for barrier in self.barriers if barrier[0] < self.HEIGHT]

    def create_barrier(self):
        self.barriers.extend([(0, 0), (0, self.WIDTH)])

    def check_collision(self):
        for obj in self.obstacles + self.barriers:
            if obj[0] == self.player_pos and obj[1] == 2 + 4 * self.player_lane:
                return True
        return False

    def draw_player(self):
        print(f"\033[{self.player_pos};{2 + 4 * self.player_lane}H{self.PLAYER_CHAR}", end="")

    def menu(self):
        print(Fore.GREEN + "Привет! Выбери один из вариантов и нажми на его номер клавишей.")
        print("╔══════════════════╗")
        print("╠═1. Начать игру═══╣")
        print("╚══════════════════╝")
        print("╔════════════════════╗")
        print("╠═2. Выйти из игры═══╣")
        print("╚════════════════════╝")
        print("╔═════════════╗")
        print("╠═3. Помощь═══╣")
        print("╚═════════════╝")
        key = keyboard.read_key()
        while True:
            if key == '1':
                self.running = True
                break
            elif key == '2':
                self.running = False
                break
            elif key == '3':
                print(Fore.YELLOW + "Добро пожаловать в игру! Сдесь находится нобольшая сводка правил для тебя.")
                print("Таким значком изображены бортики - ▒ (в них въезжать нельзя, иначе проиграешь)")
                print("Вот так изоражены препятствия - ◙ (в них въезжать нельзя, иначе проиграешь)")
                print("▲ - это Ты")
                print("Для управления используются клавиши - 'A' и 'D' ")
                print("Если вы запустили игру с русской расскладкой, то переключите расскладку на ENG и перезапустите игру(иначе она не будет работать)")
                print("Хорошей игры, и наилучших результатов!")
                input('Для того что бы начать игру, нажмите ENTER')
                break

    def run(self):
        keyboard.on_press(self.move_player)
        self.menu()
        while self.running:
            print("\033[2J")

            self.move_obstacles()
            self.create_obstacle()

            self.move_barriers()
            self.create_barrier()

            self.draw_player()
            for obstacle in self.obstacles:
                print(f"\033[{obstacle[0]};{obstacle[1]}H{self.OBSTACLE_CHAR}", end="")

            for barrier in self.barriers:
                print(f"\033[{barrier[0]};{barrier[1]}H{self.BARRIER_CHAR}", end="")

            if self.check_collision():
                self.running = False
            elif any(barrier[0] == self.player_pos and barrier[1] == 2 + 4 * self.player_lane for barrier in self.barriers):
                self.running = False

            print(f"\033[1;0HСчёт: {self.score}")
            self.score += 1

            time.sleep(0.3)

        print(f"\033[22;0HИгра окончена! Твой счёт: {self.score}")


if __name__ == "__main__":
    game = Game(20, 11)
    game.run()

