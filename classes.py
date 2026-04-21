import uuid
from datetime import datetime, date
from enum import Enum


# ===================== ENUMS =====================

class LessonStatus(Enum):
    PLANNED = "Запланировано"
    COMPLETED = "Проведено"
    CANCELLED = "Отменено"


class RequestStatus(Enum):
    NEW = "Новая"
    IN_PROGRESS = "В обработке"
    APPROVED = "Одобрена"
    REJECTED = "Отклонена"


# ===================== BASE USER =====================

class User:
    def __init__(self, id, login, password, last_name, first_name,
                 middle_name, phone, email):
        self.id = id
        self.login = login
        self.password = password
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.phone = phone
        self.email = email

    def authenticate(self, password):
        if self.password == password:
            print("Авторизация успешна")
            return True
        else:
            print("Неверный пароль")
            return False

    def change_password(self, new_password):
        self.password = new_password
        print("Пароль успешно изменён")

    def __repr__(self):
        return f"<Пользователь {self.login}>"


# ===================== USERS =====================

class Admin(User):

    def register_student(self, student):
        print(f"Ученик {student.first_name} зарегистрирован")

    def block_user(self, user):
        print(f"Пользователь {user.login} заблокирован")

    def enroll_student(self, student, group):
        group.add_student(student)
        print(f"Ученик {student.first_name} записан в группу {group.name}")

    def cancel_enrollment(self, student, group):
        group.remove_student(student)
        print(f"Ученик {student.first_name} удалён из группы {group.name}")

    def send_notification(self, message, users):
        for user in users:
            print(f"Отправлено на {user.email}: {message}")

    def manage_group(self, group):
        print(f"Управление группой {group.name}")


class Teacher(User):

    def conduct_lesson(self, lesson):
        lesson.status = LessonStatus.COMPLETED
        print(f"Занятие {lesson.id} проведено")

    def mark_attendance(self, group):
        print(f"Посещаемость отмечена для группы {group.name}")


class Student(User):
    def __init__(self, id, login, password, last_name, first_name,
                 middle_name, phone, email,
                 birth_date, school,
                 parent_name, parent_phone, parent_email):

        super().__init__(id, login, password, last_name, first_name,
                         middle_name, phone, email)

        self.birth_date = birth_date
        self.school = school
        self.parent_name = parent_name
        self.parent_phone = parent_phone
        self.parent_email = parent_email

    def view_schedule(self, schedule):
        print("Расписание:")
        for lesson in schedule.lessons:
            print(f"{lesson.datetime} — {lesson.status.value}")
        return schedule.lessons


# ===================== CORE CLASSES =====================

class Course:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def add(self):
        print(f"Курс '{self.name}' добавлен")

    def edit(self, name=None, description=None):
        if name:
            self.name = name
        if description:
            self.description = description
        print("Курс обновлён")


class Group:
    def __init__(self, id, name, max_students):
        self.id = id
        self.name = name
        self.max_students = max_students
        self.students = []

    def add_student(self, student):
        if len(self.students) < self.max_students:
            self.students.append(student)
        else:
            raise ValueError("Группа переполнена")

    def remove_student(self, student):
        self.students.remove(student)


class Lesson:
    def __init__(self, id, datetime_value, status=LessonStatus.PLANNED):
        self.id = id
        self.datetime = datetime_value
        self.status = status


class Schedule:
    def __init__(self):
        self.lessons = []

    def get_group_schedule(self, group):
        print(f"Получено расписание для группы {group.name}")
        return self.lessons

    def get_teacher_schedule(self, teacher):
        print(f"Получено расписание для преподавателя {teacher.first_name}")
        return self.lessons


class Request:
    def __init__(self, id, created_at, status=RequestStatus.NEW):
        self.id = id
        self.created_at = created_at
        self.status = status

    def approve(self):
        self.status = RequestStatus.APPROVED
        print("Заявка одобрена")

    def reject(self):
        self.status = RequestStatus.REJECTED
        print("Заявка отклонена")
