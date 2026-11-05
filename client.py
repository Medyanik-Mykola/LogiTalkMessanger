from customtkinter import *
from socket import *
from threading import *

client_socket = socket(AF_INET, SOCK_STREAM)
is_connected = False

HOST = "5.tcp.eu.ngrok.io"
PORT = 29726

try:
    client_socket.connect((HOST, PORT))
    is_connected = True
    print("Ви успішно приєднались до сервера!")
except:
    print("Помилка підключення до сервера(")

window = CTk()
window.geometry("500x400")
window.title("LogiTalk")

from PIL import Image
background = Image.open("image.png")
background_ctk =  CTkImage(light_image=background, size=(window.winfo_width(), window.winfo_height()))

my_username = "Гість"

window.menu_visible = False

def showLeftSideMenu():
    if window.menu_visible == True:
        sidebar_frame.pack_forget()
        window.menu_visible = False
        btn_menu.configure(text="▶")
    else:
        sidebar_frame.pack(side="left", fill="y", before=main_frame)
        window.menu_visible = True
        btn_menu.configure(text="◀")

def add_message (message_text, align="right"):
    msg_label = CTkLabel(
        chat,
        text=message_text,
        corner_radius=8,
        fg_color= "#1f6aa5" if align == "right" else "#333333",
        padx=10, pady=5,
        text_color="white"
    )

    anchor = "e" if align == "right" else "w"
    msg_label.pack(anchor=anchor, pady=5, padx=10)

    chat._parent_canvas.yview_moveto(1.0)

def send_message(event=None):
    if is_connected == False:
        return

    message = message_input.get()

    if message.strip():
        add_message(f"Ви: {message}", align="right")

        full_message = f"{my_username}: {message}"

        client_socket.sendall(full_message.encode("utf-8"))
        message_input.delete(0, "end")

def changeTheme():
    theme = get_appearance_mode()
    if theme == "Dark":
        set_appearance_mode("Light")
    else:
        set_appearance_mode("Dark")

sidebar_frame = CTkFrame(window, width=150, corner_radius=0)
sidebar_frame.pack_propagate(False)

name_label = CTkLabel(sidebar_frame, text="Гість",)
name_label.pack()

changeName_ent = CTkEntry(sidebar_frame, placeholder_text="Enter name...")
changeName_ent.pack()

def change_username ():
    global my_username
    new_name = changeName_ent.get()
    if new_name.strip():
        my_username = new_name
        changeName_ent.delete(0, "end")
        name_label.configure(text=my_username)
    

savenamebtn = CTkButton(sidebar_frame, text="Save name", command=change_username,)
savenamebtn.pack(padx=10, pady=10)

changeThemeBtn = CTkButton(sidebar_frame, text="Change theme", command=changeTheme)
changeThemeBtn.pack(padx=10, pady=(35, 0))

main_frame = CTkFrame(window, fg_color="transparent")
main_frame.pack(side="left", fill="both", expand=True)

# sidebar_frame.pack(side="left", fill="y", before=main_frame)

btn_menu = CTkButton(main_frame, width=30, text="▶", command=showLeftSideMenu)
btn_menu.pack(anchor="nw", padx=10, pady=10)

chat = CTkScrollableFrame(main_frame)
chat.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

bottom_frame = CTkFrame(main_frame, fg_color="transparent")
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

message_input = CTkEntry(bottom_frame, placeholder_text="Введіть повідомлення...")
message_input.pack(side="left", fill="x", expand=True, padx=5)

message_input.bind("<Return>", send_message)

sendmesaage = CTkButton(bottom_frame, width=80, text="Надіслати", command=send_message)
sendmesaage.pack(side="right")

def receive_messages():
    while is_connected == True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break

            message = data.decode("utf-8")
            window.after(0, lambda m=message: add_message(m, align="left"))
        except:
            print("З'єднання з сервером розірвано")
            break

if is_connected == True:
    receive_thread = Thread(target=receive_messages, daemon=True)
    receive_thread.start()

window.mainloop()





















