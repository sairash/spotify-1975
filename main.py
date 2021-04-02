import keyboard
import time
import os
from win32gui import GetWindowText, GetForegroundWindow
from pygame import mixer
import datetime
import threading
import webbrowser
import sys
from prettytable import PrettyTable
import random
#import Finished


#os change
os.system("Cls") #clears screen
os.system("title Geet -cli") #change title

#extra
commandTable = PrettyTable(["Command", "Info",'Example']) #for hint table
rainbow_colors = ['#FF0900', '#FF7F00', ' #FFEF00', '#00F11D', ' #0079FF', ' #A800FF'] #for rainbow colored prints
valid_hex = '0123456789ABCDEF'.__contains__ #constrains for printing colors
typing_time = 0.05 #typing speed
selected = 1 #selected
rainbow_loop_after = 2 #rainbow new color after ? loops
rainbow_currently_at=0 #global rainbow value


#printing Info in the screen
home_info_array = ['[Enter]/ Play -- To play previously played song. -- play','F-[Path] -- To enter a new path. -- f-C:/Users/natur/Downloads/Music','Git -- To go to Github Page -- git', 'Mail -- To mail the creator -- mail'] #hints
home_about_array = ['A Command line interface mp3 player with many features.','Experimantal project (Created in a day).','Hit [Enter] to play previous played File.', 'Type Dir of music file to play from that file.'] #shown at the home page
info_array = ['press [Space] To Play or Pause','Press [<-] [->] (horizontal arrow keys) to control volume.', 'Press [^] [v] (vertical arrow keys) to browse through file and press [Enter] to play', 'Press [L] to loop forever.', 'Press [R] to randomly play song.'  , 'Press [E] / [Esc] to Exit.', 'Press [G] to go to Github'] #info shown while playing audio

#music data
music_path='' #path of going to be played audio
music_in_file=[] #all music files name is stored here
currently_playing = 'f.mp3' #currently playing audio
currently_playing_index = 0 #currently playing audio index with ref to music_in_file[]
volume_level= 0.7 #volume of music player
music_length = '0:03:19' #music length of currently playing audio

#geetdata
browse_pointer_position = 0 #where the pointer is with ref to music_in_file[] 
loop_forever = False #loops the audio forever
randomize_music = False # randomize audio
is_pause = False #audio paused?
notExit = True #does the user want to exit the program

#terminal size
col = '150' #width
lines = '41' #height

#logo
geet_logo_txt = open('geet.txt','r') #read file
geet_logo_split = geet_logo_txt.read().split('\n') #change to array
geet_logo_txt.close() #close file

#project git page
def githubPage():
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		webbrowser.open_new('https://github.com/sairash/geet') #open browser


#mail the creator
def mailME():
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		webbrowser.open_new('mailto:nation.ance@gmail.com') #open browser


#change terminal size
def terminal_size():
	os.system('mode con: cols='+col+' lines='+lines+'') #change size of terminal
	return(col,lines) #return value


#clean the hex code
def clean_hex(data):
	return ''.join(filter(valid_hex, data.upper())) #better hex code


#Print Colors
def printC(text, color='#ffffff', end='\n'):
	hexint = int(clean_hex(color), 16) #get int of hexcode
	print("\x1B[38;2;{};{};{}m{}\x1B[0m".format(hexint>>16, hexint>>8&0xFF, hexint&0xFF, text),end=end) #prints color in the cmd window


#Print Animation
def printA(text, end='\n',fore_color='#ffffff',back_color='#000000'):
	start_typing=False 
	back_hex_int = int(clean_hex(fore_color), 16) #chnage to hex
	fore_hex_int = int(clean_hex(back_color), 16) #chnage to hex
	text = text+end #add text with end data
	for character in text:
		if character==':': #initaial
			start_typing = not start_typing #change started value
		else:
			if start_typing: #if initiated
				sys.stdout.write("\x1B[48;2;{};{};{}m\x1B[38;2;{};{};{}m{}\x1B[0m".format(fore_hex_int >> 16, fore_hex_int >> 8 & 0xFF, fore_hex_int & 0xFF, back_hex_int >> 16, back_hex_int >> 8 & 0xFF, back_hex_int & 0xFF, character)) #type characters
				sys.stdout.flush()
				time.sleep(typing_time) #wait before printing another characters
			else:
				print(' ',end='') #Middle without typing


#make animatable
def make_animateable(string,center=True):
	string_to_return = ':'+string+':' #add : to make it animatable
	if center: #want text at center?
		return(string_to_return.center(int(console_x))) #adds spaces to make it look like it is in the center
	else:
		return(string_to_return) #returns without adding spaces


#make a string colorful
def print_rainbow_colors_loop(string):
	global rainbow_currently_at #global value
	currently_in_function = 0 #change data per function call
	for letter in string: #per letter string
		printC(letter, color=rainbow_colors[rainbow_currently_at], end='') #print color
		#change rainbow color
		if currently_in_function % 2 == 0:
			rainbow_currently_at += 1
			if rainbow_currently_at % 6 == 0:
				rainbow_currently_at = 0
		currently_in_function += 1


#welcome page input command
def take_input_command_home():
	global music_in_file, music_path , currently_playing, total_music_in_file #global variables
	while True:
		command = input('\033[4mGeet\033[0m: > ').lower() #input command
		#checking commnd
		if command == 'hint':
			for info in home_info_array: #reading hint array
				all_info = info.split(' -- ') #spliting for data
				commandTable.add_row(all_info) #adding to the table

			print(commandTable) #showing table
		elif command == 'git':
			printA(make_animateable('Opening browser:',center=False), fore_color='#000000', back_color='#00F11D') #print info with animation
			githubPage() #show git page
		elif command == 'mail':
			printA(make_animateable('Opening browser:',center=False), fore_color='#000000', back_color='#00F11D') #print info with animation
			mailME() #show mail page
		elif command == '' or command == 'play':
			song_data = open('data.txt','r') #opening database xD
			song_data_split = song_data.read().split('\n') #split the data
			song_data.close() #closing database to clear memory
			if len(song_data_split)==0:
				print('\033[4mGeet\033[0m: > No Data Please Specify a path using p-[Path] command') #if nothing in db ask to give data
			else:
				music_path = song_data_split[0] #putting path data to music_path
				currently_playing = song_data_split[1] #putting currently playing data from database
				for root, subdirs, files in os.walk(song_data_split[0]): #go through the path to get every audio file
					for file in files:
						if os.path.splitext(file)[1].lower() in ('.mp3', '.wav', '.ogg', '.xm', '.mod'): #select only audio file
							music_in_file.append(file) #audiofile appended to playable list
				total_music_in_file = len(music_in_file)
				break #break the loop
		elif command[0] == 'f':
			number_of_files = 0
			printA(make_animateable('Wait going through files! ',center=False), fore_color='#000000', back_color='#00F11D') #animating info
			path=command[2:] #getting everything after 2 element
			for root, subdirs, files in os.walk(path): #go through the path to get every audio file
				for file in files:
					if os.path.splitext(file)[1].lower() in ('.mp3', '.wav', '.ogg', '.xm', '.mod'): #select only audio file
						music_in_file.append(file) #audiofile appended to playable list
						number_of_files +=1
			if number_of_files > 0:
				first_file = music_in_file[0] #putting the first element in first file to add at currently playing
				print(path, first_file)
				#writing data to database
				song_data = open('data.txt','w')
				music_path = path
				song_data.write(path)
				song_data.write('\n')
				song_data.write(first_file)
				song_data.close()
				currently_playing = first_file #adding to currently playing
				total_music_in_file = len(music_in_file) #total music in file added
				break #break the loop
			else:
				printA(make_animateable('No Playable Audiofile found. ',center=False), fore_color='#ffffff', back_color='#ff0000') #animating info
				print('',end='')
		else:
			printA(make_animateable('Invalid command: ',center=False), fore_color='#ffffff', back_color='#ff0000') #animating info
			print('',end='')


#welcome page display
def main():
	os.system("Cls") #clearing screen
	for line in geet_logo_split: #for everyline in logo
		print_rainbow_colors_loop(line.center(int(console_x))) #printing logo

	printA(make_animateable(' Welcome To Spotify-1975 a music player in cmd '), back_color='#FFEF00', fore_color='#000000') #animating info
	printA(make_animateable(' To play music press the enter or put in the path and hit enter.'), back_color='#FFEF00', fore_color='#000000') #animating info
	print()
	print('--------------------------------------------------------------About---------------------------------------------------------------'.center(int(console_x)))
	for line in home_about_array: #print every line info
		print("          | "+line+" "*(130-len(line)-3)+"|")

	print('----------------------------------------------------------------------------------------------------------------------------------'.center(int(console_x)))
	print()
	print_rainbow_colors_loop('Creator - Sairash'.center(int(console_x))) #printing rainbow color creator
	print_rainbow_colors_loop('git: https:/www.github.com/sairash/geet'.center(int(console_x))) #printing git link rainbow
	print('\033[4mGeet\033[0m: > "Eg: Hint"') # print hint
	take_input_command_home() #enter command
	music_play() #initial music play 


#init play music
def music_play():
	global music_length_seconds, music_length, currently_playing_index, browse_pointer_position #global variable
	#music player
	mixer.init() #starting the mixer
	print(music_path+currently_playing)
	mixer.music.load(music_path+'/'+currently_playing) #loading the song
	a = mixer.Sound(music_path+'/'+currently_playing) #loading the song for its length
	music_length = str(datetime.timedelta(seconds=int(a.get_length()))) #changing the music length variable 
	music_length_seconds = int(a.get_length())
	# Setting the volume
	mixer.music.set_volume(volume_level) 
	# Start playing the song
	mixer.music.play()
	currently_playing_index = music_in_file.index(currently_playing)
	browse_pointer_position = currently_playing_index


#progress bar
def progressBar(currently_at,total_length,number_of_dash):
	currently_at_percent = int(int(currently_at) * 100/ total_length) #percentage of current position
	should_be_placed_at = int(currently_at_percent/100 * number_of_dash) #percentage of current position with respective to number of dash
	data_to_return = ''
	for x in range(number_of_dash): #putting value
		if x < should_be_placed_at:
			data_to_return += '=' #placing = for already played
		elif x > should_be_placed_at:
			data_to_return += '-' #placing - for remaining music
		else:
			data_to_return += '█' # placing cursor

	return data_to_return #returning string


#play selected selected song
def play_selected_song(number):
	global a, music_length, music_length_seconds, currently_playing_index, currently_playing, browse_pointer_position #global variable
	mixer.music.load(music_path+'/'+music_in_file[number]) #loading the song
	a = mixer.Sound(music_path+'/'+music_in_file[number]) #loading the song for its length
	music_length = str(datetime.timedelta(seconds=int(a.get_length()))) #changing the music length variable 
	music_length_seconds = int(a.get_length())
	# Setting the volume
	mixer.music.set_volume(volume_level)
	# Start playing the song
	mixer.music.play()
	currently_playing_index=number
	currently_playing = music_in_file[currently_playing_index]
	song_data = open('data.txt','w') # writing new in database
	song_data.write(music_path)
	song_data.write('\n')
	song_data.write(currently_playing)
	song_data.close()
	browse_pointer_position= number #changing browser pointer position
	cli_refresh() #refresh gui


#printing cli all music with ... at last
def cli_audio_names(audio_name):
	split_audio_name=audio_name.split('.') #split audio name with .
	audio_name=split_audio_name[:-1] #audio name is everything except last
	audio_name = '.'.join(audio_name) #joining audio name
	extension = split_audio_name[-1] #get extension name
	file_name = ''
	if len(audio_name) > 75:
		file_name = audio_name[:75] + '..' #file name with .. at end
	else:
		file_name = audio_name
	file_name +='.'+extension #adding extension at end
	return file_name #returning string


#check whether to display L or not
def get_loop_forever():
	if loop_forever:
		return 'L'
	else:
		return ' '


#check whether to display R or not
def get_randomize_music():
	if randomize_music:
		return 'R'
	else:
		return ' '


#when music finishes what to do?
def on_music_finished():
	if loop_forever:
		mixer.music.play() # play the same music again
	elif randomize_music:
		play_selected_song(random.randint(1,total_music_in_file-1)) #get random number from 1 to total music data in music_in_file array
	else:
		play_next = currently_playing_index+1 #else play next in the list
		if play_next >= total_music_in_file:
			play_selected_song(0)
		else:
			play_selected_song(play_next)


#for exit when [e] or [Esc] is pressed
def exit():
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		global notExit #global variable
		notExit = False #end thread job


#when [Space] is pressed
def space():
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		global is_pause #global varaible
		if is_pause:
			mixer.music.unpause() #unpause music
			is_pause = False #change to opposite
		else:
			mixer.music.pause() #pause music 
			is_pause = True #change to opposite
		cli_refresh() #refresh gui


#when [L] is pressed
def loop_forever_function():
	global loop_forever
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		loop_forever = not(loop_forever) #change to opposite
		cli_refresh() #refresh gui


#when [R] is pressed
def randomize_music_function():
	global randomize_music
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		randomize_music = not(randomize_music) #change to opposite
		cli_refresh() #refresh gui


#when [^] is pressed
def volumeUp():
	global volume_level #global value
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		if volume_level < .9: #if less than 1[max]
			volume_level += .1 #change value
			mixer.music.set_volume(volume_level) #change volume
			cli_refresh() #refresh gui


def volumeDown():
	global volume_level #global value
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		if volume_level > 0: #if greater than 0 [min]
			volume_level -= .1 #change value
			mixer.music.set_volume(volume_level) #change volume
			cli_refresh() #refresh gui


def browseUp():
	global browse_pointer_position #global value
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		if browse_pointer_position <= 0:  #if less than 0 [min]
			browse_pointer_position = 0 #set position 0
		else: #if greater than 0 [min]
			browse_pointer_position -=1 #set position -1
		
		cli_refresh() #refresh gui


def browseDown():
	global browse_pointer_position #global value
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		if browse_pointer_position+1 >= total_music_in_file: #if less than total music in array [max]
			browse_pointer_position = total_music_in_file - 1 #set position total music in array -1
		else:#if greater than total music in array [max]
			browse_pointer_position +=1 #set position +1
		
		cli_refresh() #refresh gui


def file_select_enter():
	if GetWindowText(GetForegroundWindow()) == 'Geet -cli': #check window name
		input('Loading... ') #delete enter [important]
		play_selected_song(browse_pointer_position) #playing music at browse position


#gets keypress
def initiate_keyborde_logic():
	keyboard.add_hotkey('g', githubPage) #detects keypress
	keyboard.add_hotkey('l', loop_forever_function) #detects keypress
	keyboard.add_hotkey('r', randomize_music_function) #detects keypress
	keyboard.add_hotkey('e', exit) #detects keypress
	keyboard.add_hotkey('esc', exit) #detects keypress
	keyboard.add_hotkey('space', space) #detects keypress
	keyboard.add_hotkey('left', volumeDown) #detects keypress
	keyboard.add_hotkey('right',volumeUp) #detects keypress
	keyboard.add_hotkey('up', browseUp) #detects keypress
	keyboard.add_hotkey('down', browseDown) #detects keypress
	keyboard.add_hotkey('enter', file_select_enter) #detects keypress


#display music player gui
def cli_refresh():
	if str(datetime.timedelta(seconds=int(mixer.music.get_pos()/1000))) == music_length: #check if music finished
		on_music_finished() #on music finished
	console_x, console_y=terminal_size() #get and make terminal size
	#print logo
	for line in geet_logo_split:
		print_rainbow_colors_loop(line.center(int(console_x))) #print in rainbow color
	print_rainbow_colors_loop(datetime.datetime.now().strftime("%H:%M:%S").center(int(console_x))) #print clock in rainbow colors
	print()
	print('---------------------------------------------------------------Open---------------------------------------------------------------'.center(int(console_x)))
	#print all music and select
	if(browse_pointer_position+10 >= total_music_in_file): #for ending
		for music in range(total_music_in_file-10,total_music_in_file):
			if music == browse_pointer_position:
				file_name = cli_audio_names(music_in_file[music]+' <') #if index is same as browse pointer position
			else:
				file_name = cli_audio_names(music_in_file[music]) #if index is not same
			if music_in_file[music] == currently_playing: #if index of music in array is same as currently playing
				print("          | ",end='')
				printC(file_name,color='#ffff00',end='')
				printC(" "*(130-len(file_name)-3),color='#ff0000',end='')
				print("|")
			else:
				print("          | "+file_name+" "*(130-len(file_name)-3)+"|") #if not same as currently playing
	else:
		for music in range(browse_pointer_position,browse_pointer_position+10): #not for ending
			if music == browse_pointer_position:
				file_name = cli_audio_names(music_in_file[music]+' <') #if index is same as browse pointer position
			else:
				file_name = cli_audio_names(music_in_file[music]) #if index is not same
			if music_in_file[music] == currently_playing: #if index of music in array is same as currently playing
				print("          | ",end='')
				printC(file_name,color='#ffff00',end='')
				printC(" "*(130-len(file_name)-3),color='#ff0000',end='')
				print("|")
			else:
				print("          | "+file_name+" "*(130-len(file_name)-3)+"|") #if not same as currently playing
	print('----------------------------------------------------------------------------------------------------------------------------------'.center(int(console_x)))



	print('--------------------------------------------------------------Lyrics--------------------------------------------------------------'.center(int(console_x)))
	lyrics_comming_soon='Lyrics Comming Soon'
	print("          | "+lyrics_comming_soon+" "*(130-len(lyrics_comming_soon)-3)+"|") #lyrics display area

	for music in range(4):
		file_name = ''
		print("          | "+file_name+" "*(130-len(file_name)-3)+"|")

	print('----------------------------------------------------------------------------------------------------------------------------------'.center(int(console_x)))

	print('---------------------------------------------------------------Info---------------------------------------------------------------'.center(int(console_x)))
	for info in info_array:
		print("          | "+info+" "*(130-len(info)-3)+"|")

	print('----------------------------------------------------------------------------------------------------------------------------------'.center(int(console_x)))


	print()
	print_rainbow_colors_loop('Creator - Sairash'.center(int(console_x))) #creator with rainbow colors display
	if (is_pause):
		print(' ► {1}  {2} {0}    ◄) {3}  {5}  {4}'.format(music_length,datetime.timedelta(seconds=int(mixer.music.get_pos()/1000)), progressBar(int(mixer.music.get_pos()/1000), music_length_seconds,46), progressBar(int(volume_level*100), 100,10),get_loop_forever(),get_randomize_music()).center(int(console_x))) #if paused is true controller
	else:
		print('▐▐ {1}  {2} {0}    ◄) {3}  {5}  {4}'.format(music_length,datetime.timedelta(seconds=int(mixer.music.get_pos()/1000)), progressBar(int(mixer.music.get_pos()/1000), music_length_seconds,46), progressBar(int(volume_level*100), 100,10),get_loop_forever(),get_randomize_music()).center(int(console_x))) #if not paused controller


#command line interface
def cli():
	while notExit:
		cli_refresh()
		time.sleep(1)


#console_window
console_x, console_y = terminal_size() #resize and get height and length
os.system("title Geet -cli") #change title just incase

main() #welcome Screen
cli_thread = threading.Thread(target=cli) #intiating parellel processing in gui
cli_thread.start() #gui start

initiate_keyborde_logic() #adding keypress logics

cli_thread.join() #when pressed ends program