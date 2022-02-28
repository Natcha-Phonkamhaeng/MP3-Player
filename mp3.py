# created 5 Feb 2022
'''
1. fix delete song when press forward and backward button
2. delete multiple songs
*** 3. fixing slider song
4. create label when music's been paused

'''

from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os, time
from pygame import mixer
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

mixer.init()

root = Tk()
root.geometry('390x380+2000+100')
root.title('MP3 Player')


class Main_Frame:

	def __init__(self, master):
		self.frame = Frame(master)
		self.menu_bar = Menu(master)
	
		self.open = Menu(self.menu_bar, tearoff=0)
		self.open.add_command(label='Add Songs', command=self.add_songs)
		self.open.add_command(label='Exit', command= lambda : master.quit())
		self.menu_bar.add_cascade(label='Open', menu=self.open)
		
	def add_songs(self):
		
		filetypes = (('mp3 files', '*.mp3'), ('wav files', '*.wav'), )

		# select multiple songs
		self.songs_path = filedialog.askopenfilenames(title='Choose Songs to Play', filetypes=filetypes)
		
		for song in self.songs_path:
			self.song_dir, self.song_name = os.path.split(song)
			img_btn.song_box.insert(END, self.song_name)	
					
			
class Img_Btn(Main_Frame):

	def __init__(self, master):
		super().__init__(master)

		self.play_img = PhotoImage(file='Assets/play.png')		
		self.fwd_img = PhotoImage(file='Assets/forward.png')		
		self.bck_img = PhotoImage(file='Assets/back.png')		
		self.stop_img = PhotoImage(file='Assets/stop.png')		
		self.pause_img = PhotoImage(file='Assets/pause.png')
		self.song_box = Listbox(self.frame, bg='black', fg='white', selectbackground='green', width=50, height=13)
		self.unpause = mixer.music.get_busy() # return True
		
	def draw(self):
		self.frame.pack(fill='both', expand=True)

		self.song_box.place(x=45, y=20)

		self.bck = Button(self.frame, image=self.bck_img, borderwidth=0, command=self.backward)
		self.bck.place(x=50, y=250)

		self.play = Button(self.frame, image=self.play_img, borderwidth=0, command=self.play)
		self.play.place(x=110, y=250)

		self.pause = Button(self.frame, image=self.pause_img, borderwidth=0, command=self.pause)
		self.pause.place(x=170, y=250)

		self.stop = Button(self.frame, image=self.stop_img, borderwidth=0, command=self.stop)
		self.stop.place(x=230, y=250)
		
		self.fwd = Button(self.frame, image=self.fwd_img, borderwidth=0, command=self.forward)
		self.fwd.place(x=290, y=250)

		self.song_time = Label(self.frame, text='00:00 of 00:00', relief=GROOVE, bd=1,  anchor=E)
		self.song_time.pack(fill=X, side=BOTTOM, ipady=3)

		self.slider_label = Label(self.frame, text='00:00')
		self.slider_label.pack(side=BOTTOM)

		self.slider = ttk.Scale(self.frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=290)
		self.slider.pack(side=BOTTOM)

	def play(self):				
		self.songs_selected = self.song_box.get(ACTIVE)		
		mixer.music.load(os.path.join(main_frame.song_dir, self.songs_selected))		
		mixer.music.play(loops=-1)

		# time_slider = time.strftime('%M:%S', time.gmtime(self.slider.get()//1000))
		self.slider_label.config(text=int(self.slider.get()))

		def time_show():
			try:
				cur_selection = img_btn.song_box.curselection()[0]
				last_selection = img_btn.song_box.get(cur_selection)
				current_time = mixer.music.get_pos() // 1000
				# change to time format
				time_elapsed = time.strftime('%M:%S', time.gmtime(current_time))
				# use Mutagen to scan the length of song, converting to song directory
				song_directory = os.path.join(main_frame.song_dir, last_selection)
				song_length = MP3(song_directory)
				song_length = song_length.info.length
				# change song_length to time format
				song_length_format = time.strftime('%M:%S', time.gmtime(song_length))
				self.song_time.config(text=f'{time_elapsed} of {song_length_format}')
				self.song_time.after(1000, time_show)
			except IndexError:
				print('song playing is deleted, raising index error')
		
		time_show()		
		
	def stop(self):
		mixer.music.stop()

	def pause(self):
		if self.unpause: #return True -->if mixer get busy, music is playing (unpause)
			mixer.music.unpause()
		if not self.unpause:
			mixer.music.pause()
		self.unpause = not self.unpause # set to run if false statement

	def forward(self):
		selection = self.song_box.curselection() # return tuple (0,) (1,) (2,) ....
		next_selection = 0

		if len(selection) > 0: # make sure we have to select some song
			current_selection = selection[0]			
			self.song_box.selection_clear(selection) # clear whatever we select
			if current_selection < self.song_box.size()-1: #song_box.size is number of songs in playlist
				next_selection = current_selection + 1

		self.song_box.activate(next_selection)
		self.song_box.selection_set(next_selection)
		
		self.next_song = self.song_box.get(ACTIVE) # return name of song
		mixer.music.load(os.path.join(main_frame.song_dir, self.next_song))
		mixer.music.play(loops=-1)

	def backward(self):
		selection = self.song_box.curselection() # return tuple (0,) (1,) (2,) ....
		last_selection = 0

		if len(selection) > 0: # make sure we have to select some song
			current_selection = selection[0]			
			self.song_box.selection_clear(selection) # clear whatever we select
			if current_selection < self.song_box.size(): #song_box.size is number of songs in playlist
				last_selection = current_selection - 1

		self.song_box.activate(last_selection)
		self.song_box.selection_set(last_selection)
		
		last_song = self.song_box.get(ACTIVE)
		mixer.music.load(os.path.join(main_frame.song_dir, last_song))
		mixer.music.play(loops=-1)


def delete_song(event):	
	try:
		# return interger
		cur_selection = img_btn.song_box.curselection()[0]
		# return nam of song
		last_selection = img_btn.song_box.get(cur_selection)
		# condition to check we select at least 1 song
		if cur_selection >= 0:
			try:
				# if song playing is about to be deleted
				if last_selection == img_btn.songs_selected:	
					img_btn.song_box.delete(img_btn.song_box.curselection())
					mixer.music.stop()
				# else if we tend to delete another song
				elif last_selection != img_btn.songs_selected:
					img_btn.song_box.delete(img_btn.song_box.curselection())					
			# except block catching the error if we open the app, try to delete without playing any song
			except AttributeError:
				print('no songs playing')
	except IndexError:
		print('no song selected')
	
def main():	
	# main_frame.draw_win()
	img_btn.draw()
	img_btn.song_box.bind('<Delete>', delete_song)
	
	
	root.bind('<Escape>', lambda x: root.quit())
	root.mainloop()

main_frame = Main_Frame(root)
img_btn = Img_Btn(root)
root.config(menu=main_frame.menu_bar)

if __name__=='__main__':
	main()













