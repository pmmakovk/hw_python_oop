from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE = ('Тип тренировки: {training_type}; ' 
               'Длительность: {duration_h:.3f} ч.; '
               'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    training_type: str
    duration_h: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        data_1 = self.training_type
        data_2 = self.duration_h
        data_3 = self.distance
        data_4 = self.speed
        data_5 = self.calories
        return self.MESSAGE.format(training_type=data_1, duration_h=data_2,
                                   distance=data_3, speed=data_4,
                                   calories=data_5)


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    TIME_COEFF = 60

    action: int
    duration_h: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        total_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return total_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration_h
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message_training = InfoMessage(self.__class__.__name__,
                                       self.duration_h,
                                       self.get_distance(),
                                       self.get_mean_speed(),
                                       self.get_spent_calories())
        return message_training


class Running(Training):
    """Тренировка: бег."""
    CAL_COEFF_1 = 18
    CAL_COEFF_2 = 20

    def get_spent_calories(self) -> float:
        calories = ((self.CAL_COEFF_1 * self.get_mean_speed()
                    - self.CAL_COEFF_2) * self.weight / self.M_IN_KM
                    * (self.TIME_COEFF * self.duration_h))
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CAL_COEFF_3 = 0.035
    CAL_COEFF_4 = 0.029

    height: float

    def get_spent_calories(self) -> float:
        calories = ((self.CAL_COEFF_3 * self.weight
                    + (self.get_mean_speed()**2 // self.height)
                    * self.CAL_COEFF_4 * self.weight)
                    * (self.TIME_COEFF * self.duration_h))
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CAL_COEFF_5 = 1.1

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        speed = (self.length_pool
                 * self.count_pool / self.M_IN_KM / self.duration_h)
        return speed

    def get_spent_calories(self) -> float:
        calories = (self.get_mean_speed() + self.CAL_COEFF_5) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_type:
        return 'Неизвестный тип тренировки'
    else:
        training_obj = training_type[workout_type](*data)
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
