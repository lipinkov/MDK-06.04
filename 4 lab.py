import datetime

def parse_time(time_str):
    hours, minutes = map(int, time_str.strip().split(':'))
    return datetime.time(hour=hours, minute=minutes)

def minutes_difference(t1, t2):
    return (t1.hour * 60 + t1.minute) - (t2.hour * 60 + t2.minute)

def check_rules(current_time, scheduled_time, method):
    reminders = []
    diff_until = minutes_difference(scheduled_time, current_time)
    if 0 < diff_until <= 15:
        reminders.append("Скоро наступит время приема лекарства.")
    if abs(minutes_difference(current_time, scheduled_time)) <= 5:
        if method.lower() == "до еды":
            reminders.append("Принимайте лекарство за 30 минут до еды.")
        elif method.lower() == "после еды":
            reminders.append("Принимайте лекарство после еды.")
        elif method.lower() == "независимо от еды":
            reminders.append("Сейчас время для приема лекарства.")
    diff_after = minutes_difference(current_time, scheduled_time)
    if diff_after > 30:
        reminders.append("Вы пропустили прием лекарства. Пожалуйста, примите его как можно скорее или свяжитесь с врачом.")
    return reminders

def main():
    print("Система напоминаний о приеме лекарств (экспертная система на основе продукционных правил)")
    scheduled_time_str = input("Введите запланированное время приема лекарства (в формате ЧЧ:ММ, например, 08:00): ")
    scheduled_time = parse_time(scheduled_time_str)
    method = input("Введите способ приема лекарства ('до еды', 'после еды', 'независимо от еды'): ").strip()
    current_time = datetime.datetime.now().time()
    print("Текущее системное время:", current_time.strftime("%H:%M"))
    reminders = check_rules(current_time, scheduled_time, method)
    if reminders:
        print("\nНапоминания:")
        for msg in reminders:
            print(" -", msg)
    else:
        print("\nНа данный момент напоминаний нет.")

if __name__ == "__main__":
    main()
