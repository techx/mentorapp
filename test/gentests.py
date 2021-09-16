import csv
import io
import random
from string import ascii_letters


possible_emails = ['vishruti721@gmail.com', 'vishruti@mit.edu', 'azhang581@gmail.com', 'awzhang@mit.edu']

team_commitment = ['1: My mentor will answer questions through discord/slack but do not have time for calls', '2: My mentor will answer questions and schedule zoom calls whenever I am available', '3: My mentor should be available throughout the day to answer questions and receive calls', '4: My mentor should be willing to stay up all night with my team!']

mentor_commitment = ['1: I will answer questions through discord/slack but do not have time for calls', '2: I will answer questions and schedule zoom calls whenever I am available', '3: I am available throughout the day to answer questions and receive calls', '4: I’m willing to stay up all night with my team!']

expertise = ['Frontend', 'Backend', 'Data Science / Machine Learning', 'App / Mobile Dev', 'Hardware / IoT']

virtual = ['In person', 'Virtual']


def gen_random_name():
    n = random.randint(1, 10)
    a = (''.join(random.choice(ascii_letters) for i in range(n)))
    return a

def gen_random_team():
    n = random.randint(1, 4)
    names = []
    for i in range(n):
        names.append(gen_random_name())
    team = (','.join(names))
    return team

def gen_random_commitment(option):
    n = random.randint(0, 3)
    return team_commitment[n] if option == 'team' else mentor_commitment[n]

def gen_random_interest():
    n = random.randint(1, 5)
    a = random.sample(expertise, k=n)
    return (', '.join(a))

def get_random_email():
    return random.choice(possible_emails)

def gen_in_person_virtual():
    return random.choice(virtual)


def generate_team_csv(n):
    filename = "team3.csv"
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        
        csvwriter.writerow(['Timestamp', 'What is your name?', 'Who are the rest of your team members?', 'What is the primary email contact for your team? ', 'What level of commitment would you like in a mentor?', 'Which area do you predict your project will be in? (This is not binding)', 'Is your team accepted to attend in person or virtually?'])
        for i in range(n):
            csvwriter.writerow(['lol', gen_random_name(), gen_random_team(), get_random_email(), gen_random_commitment('team'), gen_random_interest(), gen_in_person_virtual()])
        

def generate_mentor_csv(n):
    filename = "mentor3.csv"
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(['Timestamp', 'What is your name?', 'What is your email?', 'What\'s your level of commitment throughout the weekend?', 'What\'s your area of expertise?', 'Are you accepted to attend in person or virtually?'])
        for i in range(n):
            csvwriter.writerow(['lol', gen_random_name(), get_random_email(), gen_random_commitment('mentor'), gen_random_interest(), gen_in_person_virtual()])   


generate_team_csv(250)
generate_mentor_csv(100)