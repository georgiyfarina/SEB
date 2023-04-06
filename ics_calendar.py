import ics


if __name__ == '__main__':


    # Replace 'example.ics' with the name of your ICS file

    with open('C://Users//Gabri//Documents//scuola//SUPSI//SecondoAnno//ProgettoSupsiSEB//SEB//data//icalexport.ics') as file:
        calendar = ics.Calendar(file.read())

    print(calendar)
    for event in calendar.events:
        print(f"Event: {event.name}")
        print(f"{event.categories}")
        print(f"{event.extra}")
        print(f"Starts: {event.begin}")
        print(f"Ends: {event.end}")
        print("-" * 20)


