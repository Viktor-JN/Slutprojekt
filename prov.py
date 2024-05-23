from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from time import sleep

#tar bort föregående answers.json ifall den finns
if os.path.exists("answers.json"):
  os.remove("answers.json")

#sätter frågorna i variabeln questions så att de kan läsas in som en lisa
with open("questions.json", encoding="utf-8") as f:
    questions = json.load(f)

#Definerar en funktion som gör att endast 1 av svarsalternativen kan vara iklickad
def check(option):
    if(option == 1):
        opt2var.set(0)
        opt3var.set(0)  
        opt4var.set(0)
    elif(option == 2):
        opt1var.set(0)
        opt3var.set(0)
        opt4var.set(0)
    elif(option == 3):
        opt1var.set(0)
        opt2var.set(0)
        opt4var.set(0)
    else:
        opt1var.set(0)
        opt2var.set(0)
        opt3var.set(0)

#skapar en funktion för att spara ner svaren i variabeln questions
def saveAnswer():
    global questionNumber
    with open("answers.json", 'w', encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    if opt1var.get() == 1: #kollar om opt1var är 1
        questions[questionNumber]["answer"] = questions[questionNumber]["A"]
    elif opt2var.get() == 1:
        questions[questionNumber]["answer"] = questions[questionNumber]["B"]
    elif opt3var.get() == 1:
        questions[questionNumber]["answer"] = questions[questionNumber]["C"]
    elif opt4var.get() == 1:
        questions[questionNumber]["answer"] = questions[questionNumber]["D"]
    else:
        questions[questionNumber]["answer"] = ""


#skapar en funktion för att kolla om frågan har blivit bescarad
def hasAnswer():
    global answers
    opt1var.set(0)
    opt2var.set(0)
    opt3var.set(0)
    opt4var.set(0)
    with open("answers.json", 'r', encoding="utf-8") as f:
        answers = json.load(f)
    if answers[questionNumber]["answer"] == answers[questionNumber]["A"]:
        opt1var.set(1)
    elif answers[questionNumber]["answer"] == answers[questionNumber]["B"]:
        opt2var.set(1)
    elif answers[questionNumber]["answer"] == answers[questionNumber]["C"]:
        opt3var.set(1)
    elif answers[questionNumber]["answer"] == answers[questionNumber]["D"]:
        opt4var.set(1)
    else:
        opt1var.set(0)
        opt2var.set(0)
        opt3var.set(0)
        opt4var.set(0)
        
global questionNumber   
questionNumber = 0  #Definerar en variabel för vilken fråga man är på i provet
#Funktion för att gå till nästa fråga
def quesIncrease():
    saveAnswer()
    global questionNumber
    if questionNumber < (len(questions)-1):
        questionNumber+=1
    else:
        pass
    hasAnswer()
    #Ändrar alla texter i fönstret så de är korrekta
    ques.config(text=questions[questionNumber]["Question"])
    opt1.config(text=questions[questionNumber]["A"])
    opt2.config(text=questions[questionNumber]["B"])
    opt3.config(text=questions[questionNumber]["C"])
    opt4.config(text=questions[questionNumber]["D"])
    quesPart.config(text=str(questionNumber+1)+"/20")

#Skapar en funktion för att gå till föregående fråga
def quesDecrease():
    saveAnswer()
    global questionNumber
    if questionNumber > 0:
        questionNumber-=1
    else:
        pass
    hasAnswer()
    #Ändrar alla texter i fönstret så de är korrekta
    ques.config(text=questions[questionNumber]["Question"])
    opt1.config(text=questions[questionNumber]["A"])
    opt2.config(text=questions[questionNumber]["B"])
    opt3.config(text=questions[questionNumber]["C"])
    opt4.config(text=questions[questionNumber]["D"])
    quesPart.config(text=str(questionNumber+1)+"/20")

#skapar funktion som öppnar fönstret för att visa hur många rätt du fick av 20
def open_popup():
    top= Toplevel(root)
    top.geometry("400x100")
    top.title("Resultat")
    Label(top, text= "Du fick "+str(correctAnswers)+" av 20 rätt!", font=("Arial", 30)).pack()
    Button(top, text= "Avsluta", command=lambda:root.destroy()).pack()
    Button(top, text= "Visa svar", command=lambda:showanswers()).pack()

def showanswers():
    questionNumber=0
    shownAnswers= Toplevel(root)
    shownAnswers.geometry("500x700")
    shownAnswers.title("Resultat")
    Label(shownAnswers, text="Dina svar och de rätta svaren", font=("Arial", 25)).pack()
    Scrollb = Scrollbar(shownAnswers)
    Scrollb.pack(side = RIGHT, fill=Y)
    with open("answers.json", 'r', encoding="utf-8") as f:
        answers = json.load(f)
    LiBo = Listbox(shownAnswers, yscrollcommand=Scrollb.set, width=500)
    for i in range(len(answers)):
        #Label(shownAnswers, text="Fråga "+str(answers[questionNumber]["Question"]), font=("Arial", 12)).pack()
        #Label(shownAnswers, text= "Ditt svar: "+str(answers[questionNumber]["answer"])).pack()
        #Label(shownAnswers, text= "Rätt svar: "+str(answers[questionNumber]["key"])).pack()
        LiBo.insert(END, "Fråga "+str(answers[questionNumber]["Question"]))
        LiBo.insert(END, "Rätt svar: "+str(answers[questionNumber]["key"]))
        LiBo.insert(END, "Ditt svar: "+str(answers[questionNumber]["answer"]))
        questionNumber+=1
    LiBo.pack(side=LEFT, fill=BOTH)
    Scrollb.config(command=LiBo.yview)
   
#skapar en funktion som körs när du vill rätta och då avsluta quizzet
def quizEnd():
    global correctAnswers
    saveAnswer()
    correctAnswers = 0
    with open("answers.json", 'r', encoding="utf-8")as f:
        answers = json.load(f)
    with open("answers.json", 'w', encoding="utf-8")as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    sleep(2) #ger tid för att filerna ska läsas in och inget ska bli fel
    for i in range(len(answers)):
        if answers[i]["answer"] == questions[i]["key"]:
            correctAnswers +=1
        else:
            pass
    open_popup()
        
#Sätter upp själva fönstret och fönstrets storlek och titel
root = Tk()
root.title("Teoriprov")
root.geometry("800x600")

quesPart = Label(root, text=str(questionNumber+1)+"/20") #Visar vilken fråga du är på
quesPart.pack(side=TOP, anchor=NW, pady=10, padx=10)
topTitle = ttk.Label(root, anchor="center", padding=10, text="Välkommen till körkortsprovet")#Välkommnar till körkortsprovet
topTitle.pack(pady=10)

#Sätter opt1var och opt2var som variablar inom tkinter
opt1var = IntVar()
opt2var = IntVar()
opt3var = IntVar()
opt4var = IntVar()

#Sätter ut knapparna för fleralternativssvar
#Lambda skapar en funktion som endast stoppar in ett värde i check funktionen för att avmarkera de andra alternativen
ques = Label(root, text=questions[questionNumber]["Question"])
ques.pack(pady=10)
opt1 = Checkbutton(root, text=questions[questionNumber]["A"], variable=opt1var ,command=lambda:check(1))
opt1.pack()
opt2 = Checkbutton(root, text=questions[questionNumber]["B"], variable=opt2var, command=lambda:check(2))
opt2.pack()
opt3 = Checkbutton(root, text=questions[questionNumber]["C"], variable=opt3var, command=lambda:check(3))
opt3.pack()
opt4 = Checkbutton(root, text=questions[questionNumber]["D"], variable=opt4var, command=lambda:check(4))
opt4.pack()

#skapar knappar för att gå fram och tillbaka genom frågorna i provet
btnNext = Button(root, text="-->", command=quesIncrease)
btnNext.pack(pady=10)
btnBack = Button(root, text="<--", command=quesDecrease)
btnBack.pack(pady=10)

#skapar rättaknappen som sedan kör quizEnd funktionen som räknar hur många rätt du fick av 20
btnResult = Button(root, text="Rätta", command=lambda:quizEnd())
btnResult.pack(side=BOTTOM, anchor=SE, padx=10, pady=10)

#startar själva fönstret med allting i
root.mainloop()