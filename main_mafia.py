import random
from collections import Counter


lobby = ["Name1", "Name2", "Name3", "Name4", "Name5", "Name6", "Name7", "Name8", "Name9", "Name10"]
mafia_kill = []  # list куда записываются выстрелы мафии
list_vote_start = []  # list куда записываются все кто выставлен
l2 = []  # list дополнительный лист для голосования


# Класс создания игроков
class Player:
    def __init__(self, user_name, user_rol, user_box, user_status):
        #self.user_con = user_conn
        self.user_name = user_name
        self.user_rol = user_rol
        self.user_box = user_box
        self.user_status = user_status
        self.user_foll = 0

# ------------------ Функции игрока -------------------
    def user_roll_mafia_shot(self):
        """Выстрел мафии"""
        if self.user_rol == "Дон" or self.user_rol == "Мафия" and self.user_status == 1:
            btn = int(input("Мафия, кого стреляем?")) - 1
            mafia_kill.append(btn)

    def user_roll_don_check(self, p_list):
        """Проверка дона"""
        if self.user_rol == "Дон" and self.user_status == 1:
            btn = int(input("Дон, кто шериф?")) - 1
            if p_list[btn].list_user_roll == "Дон" or p_list[btn].list_user_roll == "Мафия":
                self.user_roll_don_check(p_list)
            else:
                print(p_list[btn].list_user_roll)

    def user_roll_sherif_check(self, p_list):
        """Проверка шерифа"""
        if self.user_rol == "Шериф" and self.user_status == 1:
            btn = int(input("Шериф, кого проверить?")) - 1
            if p_list[btn].list_user_roll == "Шериф":
                self.user_roll_sherif_check(p_list)
            elif p_list[btn].list_user_roll == "Дон":
                print("Игрок является мафией")
            else:
                print(p_list[btn].list_user_roll)

    def user_camera(self):
        """Запуск камеры"""

    def speak_min(self):
        """Минута игрока"""

    def speak_end(self):
        """Завершить речь"""

    @property
    def speak_foll(self):
        """Выкрик игрока"""
        if self.user_foll < 3:
            self.user_foll += 1
        else:
            return "More > 3"
        return self.user_foll

    def want_vote(self, p_list):
        """Выставить на голосование"""
        use_vote = input("Хотите когото выставить? [y/n]")
        if use_vote.lower() == "y":
            use_vote = int(input("Номер игрока кого хотите выставить?")) - 1
            if use_vote in list_vote_start:
                print("Поддерживаете")
            elif p_list[use_vote].user_status == 0:
                print("Данный игрок мертв. Выберите другую кандидатуру")
                self.want_vote(p_list)
            else:
                print("Вы выставили игрока", str(use_vote + 1))
                list_vote_start.append(p_list[use_vote].list_user_box)

    @property
    def list_user_roll(self):
        """Получить роль игрока"""
        return self.user_rol

    @property
    def list_user_name(self):
        """Получить имя игрока"""
        return self.user_name

    @property
    def list_user_box(self):
        """Получить место на котором сидит игрок"""
        return self.user_box

    @property
    def list_user_status(self):
        """Получить статус жизни игрока"""
        return self.user_status


class GameMafia:
    # Игровая логика
    def __init__(self, lobby):
        self.rols = ["Мирный житель", "Мирный житель", "Мирный житель", "Мирный житель", "Мирный житель",
                     "Мирный житель", "Мафия", "Мафия", "Дон", "Шериф"]  # Роли которые есть в игре
        self.lobby = lobby
        random.shuffle(self.rols)

        # Создаем объекты игроков
        self.player = [Player(self.lobby[i], self.rols[i], i, user_status=1) for i in range(len(lobby))]

        print("self.players:", self.player)
        print("lobby:", self.lobby)
        # cnt = -1
        # for i in lobby:
        #     cnt += 1
        #     self.player.append(Player(i[0], i[1], self.rols[cnt], cnt, user_status=1))

        self.count_night = 0  # Подсчет ночей
        self.game_over = 0  # Переменная для проверки, закончена игра или нет
        self.speak_count = 0  # Переменная для передачи речи на следующий круг

        # Переменная для проверки, если голосование было 1 раз, то переголосование, если 2 раза, то подъем
        self.vote_count = 0
        self.vote_count_v2 = 0  # Вспомогательная переменная для голосования

        #self.night()

        """Анимация раздачи карт, потом self.night"""

    @property
    def list_user(self):
        """Получаем список игроков"""
        return self.player

    def check_game_over(self):
        """Функция для проверки окончания игры"""
        if self.count_night > 0:
            count_mafia = 0
            count_citizen = 0
            for i in self.list_user:
                if i.list_user_status == 1:
                    if i.user_rol == "Мафия" or i.user_rol == "Дон":
                        count_mafia += 1
                    if i.user_rol == "Мирный житель" or i.user_rol == "Шериф":
                        count_citizen += 1
            if count_mafia == count_citizen:
                self.game_over = 1

    def day(self):
        """Игровое поле: День"""

        if self.count_night > 1:
            # Проверка, все ли черные игроки выстрелили в одного игрока
            if all(mafia_kill[i] == mafia_kill[i + 1] for i in range(len(mafia_kill) - 1)) and self.list_user[
                                                                                mafia_kill[0]].list_user_status == 1:
                print("Ночью был убит игрок", mafia_kill[0] + 1)
                self.list_user[mafia_kill[0]].speak_min()
                self.list_user[mafia_kill[0]].user_status = 0  # Игрок убит, присваиваем игроку статус Dead
                self.check_game_over()  # Проверяем закончилась ли игра
            else:
                print("Мафия промахнулась")
        mafia_kill.clear()

        if self.game_over == 0:  # Если игра не окончена ->
            # Речи игроков
            if self.speak_count > 10:
                self.speak_count = 0

            for i in self.list_user[self.speak_count:]:
                if i.list_user_box <= self.speak_count and i.list_user_status == 0:
                    self.speak_count += 1
                else:
                    break

            for i in self.list_user[self.speak_count:]:
                if i.list_user_status == 1:
                    print("Речь игрока", i.user_name)
                    #self.time_speak_user(i)

            for i in self.list_user[:self.speak_count]:
                if i.list_user_status == 1:

                    print("Речь игрока", i.user_name)
                    #self.time_speak_user(i)

            self.speak_count += 1
            self.vote()
        else:
            print("Game Over")
            exit()
            return

    def vote(self):
        """Голосование"""
        # Если круг 0, то при одной кандидатуре голосование не проводится
        if self.count_night == 1 and len(list_vote_start) <= 1 and self.vote_count == 0:
            self.night()

        # Если были промахи, то будет заголосован тот кто выставлен
        if len(list_vote_start) == 1 and self.count_night > 0:
            print("Был заголосован", list_vote_start[0] + 1)
            self.list_user[list_vote_start[0]].user_status = 0
            self.night()

        if len(list_vote_start) == 0:  # Если никто не выставлен
            print("На голосование никто не выставлен")
            self.night()

        lst = sorted(list_vote_start)  # Сортируем список кто на голосовании
        list_players_vote = []
        print("На голосование выставлены:", lst)

        # Спрашиваем у игроков за кого они голосуют
        for i in self.list_user:
            if i.list_user_status == 1:
                btn = int(input("За кого хотите проголосовать?")) - 1
                list_players_vote.append(btn)  # Записываем голоса игроков

        count_vote = Counter(list_players_vote)  # Считаем голоса
        list_vote_start.clear()
        for k, v in count_vote.items():  # Сравниваем голоса за кандидатов
            if v == max(count_vote.values()):
                list_vote_start.append(k)
                if self.vote_count_v2 == 0:
                    l2.append(k)

        lst = sorted(list_vote_start)
        self.vote_count += 1
        self.vote_count_v2 += 1

        lst_ugadayka = []

        for i in self.list_user:
            if i.list_user_status == 1:
                lst_ugadayka.append(i)

        # Если первое голосование и голоса пошли поровну
        if lst == sorted(l2) and self.vote_count == 1 and len(lst) > 1:
            print("Попил")
            self.vote()
        elif lst == sorted(l2) and self.vote_count == 2:  # Если второе голосование и голоса пошли поровну
            l3 = []
            count_alive = 0
            for i in self.list_user:
                if i.list_user_status == 1:
                    count_alive += 1
                    btn = input("Хотите поднять? [y/n]")
                    l3.append(btn)
            c = Counter(l3)

            if len(lst_ugadayka) == len(l2):
                print("Подъем не возможен")
            elif c["y"] > (count_alive / 2):  # Проверяем достаточно ли голосов для подьема
                print("Вас подняли")
                for i in self.list_user:
                    for x in lst:
                        if i.user_box == x:
                            print("Прощальная ", i.user_name)
                            self.list_user[x].user_status = 0
                            self.check_game_over()
                l3.clear()
            else:
                print("Голосов не достаточно")
        elif len(lst) == 1:  # Если 1 игрок получил больше голосов
            print("Был заголосован", lst[0] + 1)
            self.list_user[lst[0]].user_status = 0

        # Если попил изменился, но все еще есть кандидаты с одинаковым кло-вом голосов
        if len(lst) != len(l2) and len(lst) != 1:
            print("Новый попил")
            self.vote_count = 0
            self.vote_count_v2 = 0
            l2.clear()
            self.vote()

        lst.clear()
        lst_ugadayka.clear()
        self.night()

    def night(self):
        """Игровое поле: Ночь"""
        self.check_game_over()
        if self.game_over == 1:
            print("Game Over")
            exit()
            return

        # Очищаем все что использовали
        list_vote_start.clear()
        l2.clear()
        self.vote_count = 0
        self.vote_count_v2 = 0

        if self.count_night > 0:  # Если была уже договорка

            # Ночные действия игроков в зависимости от роли
            for i in self.list_user:  # Стрельба мафии
                if i.list_user_status == 1:
                    i.user_roll_mafia_shot()

            for i in self.list_user:  # Проверка дона
                if i.list_user_status == 1:
                    i.user_roll_don_check(self.list_user)

            for i in self.list_user:  # Проверка шерифа
                if i.list_user_status == 1:
                    i.user_roll_sherif_check(self.list_user)
        else:
            print(self.list_user)
            print("Dogovorka")
        self.count_night += 1
        self.day()


if __name__ == "__main__":
    GameMafia()
