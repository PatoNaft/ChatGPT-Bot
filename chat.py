from tkinter import *
import customtkinter
import openai
import os
import pickle

#Initiate App
root = customtkinter.CTk()
root.title("ChatGPT Bot")
root.geometry('600x600')
root.iconbitmap('ai_lt.ico') #https://tkinter.com/ai_lt.ico

#Set Color Scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


# Submit to ChatGPT
def speak():
	if chat_entry.get():
		# Define our filename
		filename = "api_key"
		try:
			if os.path.isfile(filename):
				# Open the file
				input_file = open(filename, 'rb')

				# Load the data from the file into a variable
				stuff = pickle.load(input_file)

				# Query ChatGPT
				# Define our API Key to ChatGPT
				openai.api_key = stuff

				# Create an instance
				openai.Model.list()

				# Define our Query / Response
				response = openai.Completion.create(
					model = "text-davinci-003",
					prompt = chat_entry.get(),
					temperature = 0,
					max_tokens = 60,
					top_p = 1.0,
					frequency_penalty = 0.0,
					presence_penalty = 0.0,
					)
			
				my_text.insert(END, (response["choices"][0]["text"]).strip())
				my_text.insert(END, "\n\n")

			else:
				# Create the file
				input_file = open(filename, 'wb')
				# Close the file
				input_file.close()
				#Error message - you need an api key
				my_text.insert(END, "\n\nYou Need an API Key To Talk With ChatGPT. get one here: \nhttps://beta.openai.com/account/api-keys")

		except Exception as e:
			my_text.insert(END, f"\n\n There was an error\n\n{e}")		
			# Do something
			pass
	else:
		my_text.insert(END, "\n\nHey! You Forgot to Type Anything")	

#Clear The Screens
def clear():
	# Clear The Main Text Box
	my_text.delete(1.0, END)
	# Clear the query entry widget
	chat_entry.delete(0, END)

# Do API Stuff
def key():
	# Define our filename
	filename = "api_key"

	try:
		if os.path.isfile(filename):
			# Open the file
			input_file = open(filename, 'rb')

			# Load the data from the file into a variable
			stuff = pickle.load(input_file)

			# Output stuff to our entry box
			api_entry.insert(END, stuff)
		else:
			# Create the file
			input_file = open(filename, 'wb')
			# Close the file
			input_file.close()
	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")		

# Resize App Larger
	root.geometry('600x750')
	# Reshow API Frame
	api_frame.pack(pady=30)


# Save the API Key
def save_key():
	# Define our file name
	filename = "api_key"

	try:
		# Open file
		Output_file = open(filename, 'wb')


		# Actually add the data to the file
		pickle.dump(api_entry.get(), Output_file)

		# Delete Entry Box
		api_entry.delete(0, END)
		
		# Hide API Frame - Smaller
		api_frame.pack_forget()
		root.geometry('600x600')
	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")	

#Create Text Frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

#Add Text Widget to Get ChatGPT Responses
my_text = Text(text_frame,
	bg="#343638",
	width=65,
	bd=1,
	fg="#d6d6d6",
	relief="flat",
	wrap=WORD,
	selectbackground="#1f538d")
my_text.grid(row=0, column=0)

#Create a scroll bar for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
	command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

# Add the scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)





# Entry Wideget to Type Text to ChatGPT
chat_entry = customtkinter.CTkEntry(root,
	placeholder_text="Type text to ChatGPT....",
	width=535,
	height=50,
	border_width=2)
chat_entry.pack(pady=10)

# Create Button Frame
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

# Create submit buttons
submit_button = customtkinter.CTkButton(button_frame,
	text="Speak to ChatGPT",
	command=speak)
submit_button.grid(row=0, column=0, padx=25)

# Create clear buttons
clear_button = customtkinter.CTkButton(button_frame,
	text="Clear Response",
	command=clear)
clear_button.grid(row=0, column=1, padx=35)

# Create API buttons
api_button = customtkinter.CTkButton(button_frame,
	text="Update API Key",
	command=key)
api_button.grid(row=0, column=2, padx=25)

# Add API Key Frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

# Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
	placeholder_text="Enter Your API Key",
	width=350, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)	

# Add API Button
api_save_button = customtkinter.CTkButton(api_frame,
	text="Save Key",
	command=save_key)
api_save_button.grid(row=0, column=1, padx=10)	




root.mainloop()