class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'''Тип тренировки: {self.training_type}; \
Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; \
Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}.''')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        total_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return total_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message_training = InfoMessage(self.__class__.__name__,
                                       self.duration,
                                       self.get_distance(),
                                       self.get_mean_speed(),
                                       self.get_spent_calories())
        return message_training


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action, duration, weight):                                   
        super().__init__(action, duration, weight)                 

    def get_spent_calories(self) -> float:
        cal_coeff_1 = 18
        cal_coeff_2 = 20
        calories = ((cal_coeff_1 * self.get_mean_speed() - cal_coeff_2)
        * self.weight / self.M_IN_KM * (60 * self.duration))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        cal_coeff_3 = 0.035
        cal_coeff_4 = 0.029
        calories = (cal_coeff_3 * self.weight
		+ (self.get_mean_speed()**2 // self.height)
		* cal_coeff_4 * self.weight) * (60 * self.duration)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = (self.length_pool
        * self.count_pool / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        cal_coeff_5 = 1.1
        calories = (self.get_mean_speed() + cal_coeff_5) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    training_obj = training_dict[workout_type](*data)
    return training_obj


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
