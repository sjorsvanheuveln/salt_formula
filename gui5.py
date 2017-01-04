#!/usr/bin/env python

#Zoutformules Tool 1.5
#Sjors van Heuveln
#07-02-2016

#make use of py2exe for .exe compiling

#  LC:	1) Label().place(x=100,y=200) locatiebepaling; other parameters: fg=foreground color, bg=background color
#		2) Label().grid(row=,column=)
#		3) textvariable parameter is required for dynamic variables, e.g. parameter text doesn't allow this (static)

# TODO:	1) Test for bugs due to highscore addition.
#		2) Help functie voor hoe je moet intypen en hoe highscore werkt, 20 vragen en dat je binas niet mag gebruiken.
#		3) Check out py2app!!!! https://pythonhosted.org/py2app/

import sys
import operator
import random
from Tkinter import *

##### FUNCTIONS #####
def but_actie():
	global label_ans
	global correct_number
	global question_number
	global volgende_button
	global again_button
	global result
	global hoofd_menu_button
	global al_gespeeld
	global scores
	global submit_highscore
	global entry_hs
	global result_hs

	#right or wrong?
	if antwoord.get() == thiskey.get():
		label_ans = Label(frmMain, text="Goed")
		correct_number += 1
	else:
		label_ans = Label(frmMain, text="Fout, antwoord moest zijn: " + thiskey.get())

	button.pack_forget()
	question_number += 1

	#exit when number_limit is reached
	if question_number == question_limit:
		label_ans.pack()
		
		al_gespeeld = True

		#check if score is highscore
		scores = load_highscores()
		index_lowest,lowest = min(scores, key = lambda t: t[1])
		if correct_number > lowest:

			message_hs = str(correct_number)+ " correct! Je hebt een highscore, typ je naam in:"
			result_hs = Label(frmMain, text = message_hs)
			result_hs.pack()
			entry_hs = Entry(frmMain, textvariable = player_name)
			entry_hs.pack()
			submit_highscore = Button(frmMain, text='Submit Highscore', command = insert_highscore)
			submit_highscore.pack()

		else:
			message = str(correct_number)+ " uit " + str(question_limit) + " correct!"
			result = Label(frmMain, text = message)
			result.pack()
			again_button = Button(frmMain, text='Oefen nog een keer', command = restart)
			again_button.pack()
			hoofd_menu_button = Button(frmMain, text='Hoofdmenu', command = hoofd_menu)
			hoofd_menu_button.pack()

		return

	
		
	#add volgende button
	volgende_button = Button(frmMain, text='Volgende', command = volgende_actie)
	volgende_button.pack()
	label_ans.pack()

	return 

def insert_highscore():	
	global new_high_score
	global question_number
	global correct_number

	new_high_score = True

	scores.pop(4) #removes the last item in list, which should be lowest as it is an ordered list
	scores.append((player_name.get(),correct_number))

	new_scores = open('./scores.txt', 'w+')
	for item in scores:
		print >> new_scores, item[0] + '\t' + str(item[1])
	new_scores.close()
	question_number = 0
	correct_number = 0
	show_highscore()

	return

def volgende_actie():
	thiskey.set(salt_lib.keys()[random.randint(0,len(salt_lib)-1)])
	question.set(salt_lib[thiskey.get()])

	entry1.delete(0, 'end') #clears entrybox
	volgende_button.destroy()
	label_ans.pack_forget()
	button.pack()
	frmMain.update_idletasks()
	return

def make_salt_library(a,b):
	#reads zout.txt file and creates dictionary from name and chemical notation
	salt_lib = {}
	with open('zouten.txt','r') as f:
		for line in f:
			zout = line.split()
			salt_lib[zout[b]] = zout[a]
	return salt_lib

def restart():
	global question_number
	global correct_number

	hoofd_menu_button.destroy()
	label_ans.pack_forget()
	again_button.destroy()
	result.pack_forget()
	thiskey.set(salt_lib.keys()[random.randint(0,len(salt_lib)-1)])
	question.set(salt_lib[thiskey.get()])
	button.pack()
	question_number = 0
	correct_number = 0
	return

def main():
	global button
	global entry1
	global q_label
	
	#labels and buttons
	thiskey.set(salt_lib.keys()[random.randint(0,len(salt_lib)-1)])
	question.set(salt_lib[thiskey.get()])

	q_label = Label(frmMain, textvariable = question)
	entry1 = Entry(frmMain, textvariable = antwoord)
	button = Button(frmMain, text='Check Antwoord', command = but_actie)

	#place elements
	q_label.pack()
	entry1.pack()
	button.pack()
	return

def formule_actie():
	global salt_lib

	salt_lib = make_salt_library(0,1)
	formules.destroy()
	namen.destroy()
	highscores.destroy()
	empty_label.pack_forget()
	main()
	return

def namen_actie():
	global salt_lib

	salt_lib = make_salt_library(1,0)
	formules.destroy()
	namen.destroy()
	highscores.destroy()
	empty_label.pack_forget()
	main()
	return

def hoofd_menu():
	global formules
	global namen
	global highscores
	global empty_label
	global new_high_score
	global al_gespeeld

	if al_gespeeld == True:
		#removes main question architecture
		hoofd_menu_button.destroy()
		label_ans.pack_forget()

		#this ifelse is required as there no again button when a new highscore is made
		if new_high_score == False:
			again_button.destroy()
			result.pack_forget()
		else:
			new_high_score = False

		
		q_label.pack_forget()
		entry1.destroy()
		al_gespeeld = False

	if al_highscore == True:
		score_name_label.destroy()
		score_value_label.destroy()
		hoofd_menu_button.destroy()

	formules = Button(frmMain,text="Formule Oefeningen", command=formule_actie)
	namen = Button(frmMain,text="Namen Oefeningen", command=namen_actie)
	highscores = Button(frmMain,text="Highscores", command=show_highscore)
	empty_label = Label(frmMain, text="")
	formules.pack()
	namen.pack()
	empty_label.pack()
	highscores.pack()

	return

def show_highscore():
	global al_highscore
	global score_name_label
	global score_value_label
	global hoofd_menu_button
	global new_high_score

	al_highscore = True
	score_list_names = ''
	score_list_values = ''
	scores = load_highscores()

	for i in range(0,len(scores)):
		score_list_names = score_list_names + scores[i][0] + '\n'
		score_list_values = score_list_values + str(scores[i][1]) + '\n'
	score_list_names = 'NAAM\n' + score_list_names 
	score_list_values = 'SCORE\n' + score_list_values

	if new_high_score == True:
		#if enter this window after new highscore is made
		submit_highscore.pack_forget()
		entry_hs.destroy()
		result_hs.pack_forget()
		label_ans.pack_forget()
		entry1.destroy()
		q_label.pack_forget()
		
	else:
		formules.pack_forget()
		namen.pack_forget()
		empty_label.pack_forget()
		highscores.pack_forget()

	score_name_label = Label(frmMain, text=score_list_names)
	score_value_label = Label(frmMain, text=score_list_values)
	score_name_label.place(x=100,y=60)
	score_value_label.place(x=300,y=60)

	hoofd_menu_button = Button(frmMain, text='Hoofdmenu', command = hoofd_menu)
	hoofd_menu_button.place(relx=0.5,rely=0.8,anchor=CENTER)

	return
	
def load_highscores():
	scores = {}
	with open('scores.txt','r') as f:
		for line in f:
			data = line.split('\t')
			scores[data[0]] = int(data[1].rstrip())

	scores = list(reversed(sorted(scores.items(), key=lambda x:x[1])))
	f.close()
	return scores

##### MAIN ####
frmMain = Tk() #object
antwoord = StringVar()
question = StringVar()
thiskey = StringVar()
player_name = StringVar()

question_number = 0
correct_number = 0
question_limit = 20
al_gespeeld = False
al_highscore = False
new_high_score = False

#setup
frmMain.geometry('450x250+400+200') #syntax: ('width, heigth, xstart, ystart')
frmMain.title('Zoutformules Tool v1.5')
label = Label(frmMain, text="Zoutformules v1.5 voor HAVO/VWO Scheikunde\nMaak 20 vragen, get a highscore!\n\n")
label.pack()

hoofd_menu()

#run window
frmMain.mainloop()
