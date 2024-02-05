import objects
import tkinter
import customtkinter
import os
import sys
from tkinter import filedialog

added_video_widgets = []
downloading_video_widgets = []
downloaded_video_widgets = []
paused_video_widgets = []

added_frame_scrolled = [0]
downloading_frame_scrolled = [0]
downloaded_frame_scrolled = [0]

def set_theme(main_bg=None,
              object_fg=None, object_fg_hover=None, object_border=None,object_border_hover=None, object_txt=None, object_txt_2=None,
              entry_fg=None, entry_bd=None,
              btn_bg=None, btn_txt=None,
              line_fg=None):
    
    global object_bg
    
    
    global object_text
    global object_text_2
    
    global object_main
    global object_main_hover
    
    global object_bd
    global object_bd_hover
    
    root.configure(bg=main_bg)
    head_frame.configure(fg_color=main_bg, bg_color=main_bg)
    url_entry.configure(bg_color=main_bg, fg_color=entry_fg, border_color=entry_bd)
    add_video_btn.configure(bg_color=main_bg)
    download_path_button.configure(bg_color=main_bg, fg_color=main_bg)
    
    head_frame_2.configure(fg_color=btn_bg, bg_color=main_bg)
    added_btn.set_theme(normal_color=btn_bg, hover_color=btn_bg, clicked_color=btn_bg,
                        bg_color=btn_bg, text_color=btn_txt)
    downloading_btn.set_theme(normal_color=btn_bg, hover_color=btn_bg, clicked_color=btn_bg,
                        bg_color=btn_bg, text_color=btn_txt)
    downloaded_btn.set_theme(normal_color=btn_bg, hover_color=btn_bg, clicked_color=btn_bg,
                        bg_color=btn_bg, text_color=btn_txt)
    line_1.configure(bg=line_fg)
    line_2.configure(bg=line_fg)
    
    body_frame.configure(fg_color=main_bg, bg_color=main_bg)
    
    added_frame.set_theme(fg_color=main_bg, bg_color=main_bg)
    downloading_frame.set_theme(fg_color=main_bg, bg_color=main_bg)
    downloaded_frame.set_theme(fg_color=main_bg, bg_color=main_bg)
    
    object_bg = main_bg
    
    
    object_text = object_txt
    object_text_2 = object_txt_2
    
    object_main = object_fg
    object_main_hover = object_fg_hover
    object_bd = object_border
    object_bd_hover = object_border_hover
    
    for widget in added_video_widgets:
        try:
            widget.set_theme(fg_color=object_fg, bg_color=main_bg, fg_color_hover=object_main_hover,
                             text_color=object_text, text_color_2=object_text_2,
                             bd_color=object_bd ,bd_color_hover=object_bd_hover)
        except:
            pass
    
    for widget in downloading_video_widgets :
        try:
            widget.set_theme(fg_color=object_fg, fg_color_hover=object_fg_hover,
                             bg_color=main_bg, text_color=object_text,
                             bd_color=object_bd, bd_color_hover=object_bd_hover)
        except:
            pass
    for widget in downloaded_video_widgets:
        try:
            widget.set_theme(fg_color=object_fg, fg_color_hover=object_fg_hover, 
                             bg_color=main_bg, text_color=object_text, 
                             bd_color=object_bd, bd_color_hover=object_bd_hover)
        except:
            pass
        
    credits_menu.set_theme(border_color=object_bd, fg_color=object_fg,
                           bg_color=main_bg,text_color=object_text)
    
    credits_btn.configure(bg_color=main_bg, fg_color=main_bg, hover_color=main_bg, text_color=object_text)

#root
root = customtkinter.CTk()
root.title("YouTube Downloader")
root.iconbitmap("src/icon/main.ico")
root.geometry("960x500")
root.configure(bg="#3C3A3A")
root.minsize(960,500)
root.minsize(960,500)
root.attributes("-alpha",1)



added_video_count = 1
downloading_video_count = 1
def add_download(added_video_object:objects.AddedVideoObject):
    global downloading_video_count
    globals()["downloading_video_"+str(downloading_video_count)] = objects.DownloadingVideoObject(master=downloading_frame ,
                                                              video_stream_data= added_video_object.video_stream_data ,
                                                              url=added_video_object.url ,
                                                              title=added_video_object.title ,
                                                              selected_quallity=added_video_object.selected_quallity ,
                                                              download_info = added_video_object.download_info ,
                                                              audio_size = added_video_object.audio_size,
                                                              audio_itag=added_video_object.audio_itag,
                                                              thumbnail=added_video_object.thumbnail,
                                                              thumbnail_hover = added_video_object.thumbnail_hover,
                                                              channel=added_video_object.channel ,
                                                              fg_color=object_main ,
                                                              fg_color_hover=object_main_hover,
                                                              bg_color=object_bg ,
                                                              txt_color = object_text ,
                                                              height=80,
                                                              file_download_path=default_download_path ,
                                                              downloading_widgets=downloading_video_widgets ,
                                                              paused_widgets=paused_video_widgets , 
                                                              downloaded_widgets = downloaded_video_widgets,
                                                              downloaded_master = downloaded_frame ,
                                                              corner_radius=10 ,
                                                              border_width=1 ,border_color=object_bd, border_color_hover=object_bd_hover)
    
    globals()["downloading_video_"+str(downloading_video_count)].pack(pady=2 ,padx=0 ,fill="x")
    downloading_video_count += 1
    
    
    
    
def add_video():
    global added_video_count
    url = url_entry.get()
    if (url) :
        globals()["added_video_"+str(added_video_count)] = objects.AddedVideoObject(master=added_frame ,
                                                                    url=url ,
                                                                    fg_color=object_main ,fg_color_hover=object_main_hover,
                                                                    bg_color=object_bg ,
                                                                    txt_color=object_text, txt_color_2=object_text_2,
                                                                    height=80  ,
                                                                    added_widgets=added_video_widgets ,
                                                                    corner_radius=10 ,
                                                                    border_width=1 ,border_color=object_bd, border_color_hover=object_bd_hover,
                                                                    added_frame_scrolled=added_frame_scrolled)
        
        globals()["added_video_"+str(added_video_count)].pack(pady=2 ,padx=0 ,fill="x")
        globals()["added_video_"+str(added_video_count)].downloadBtn.configure(command=lambda video_wiget=globals()["added_video_"+str(added_video_count)]:add_download(video_wiget))
        added_video_count += 1

head_frame = customtkinter.CTkFrame(master=root )
head_frame.place(x=10 ,y=50 ,relwidth=1 ,width=-20 ,height=55)

url_entry = customtkinter.CTkEntry(master=head_frame , height=48, text_font=("inter",12,"normal" ),border_width=3,
                                   placeholder_text="\t\t\t\t    Enter URL" ,)
url_entry.place(relwidth=1 ,width=-260)
 
def show_menu(e):
    url_entry.focus()
    #get x,y pos in window
    x = root.winfo_pointerx()-root.winfo_rootx()
    y = root.winfo_pointery()-root.winfo_rooty()
    #print(x,"x",y)
    
    if url_entry.winfo_width()-x < 70:
        x = url_entry.winfo_width()-70
    copy_paste_menu.place(x=x,y=83)
    
def hide_menu(e):
    mouse_x = root.winfo_pointerx()-root.winfo_rootx()
    mouse_y = root.winfo_pointery()-root.winfo_rooty()
    
    #check mouse pointer on entry or not 
    #if pointer on entry menu will not be hide 
    url_entry_start_x = int(head_frame.place_info()["x"])
    url_entry_end_x = url_entry.winfo_width() + url_entry_start_x
    url_entry_start_y = int(head_frame.place_info()["y"])
    url_entry_end_y = url_entry.winfo_height() + url_entry_start_y
    if not(mouse_x>=url_entry_start_x and mouse_x<=url_entry_end_x and mouse_y>=url_entry_start_y and mouse_y<=url_entry_end_y) : 
        copy_paste_menu.place_forget()
def hide_menu2(e):
    copy_paste_menu.place_forget()


url_entry.bind("<Button-3>",show_menu)
url_entry.bind("<Button-2>",show_menu)
root.bind("<Button-2>",hide_menu)
root.bind("<Button-3>",hide_menu)

url_entry.bind("<Button-1>",hide_menu2)
root.bind("<Button-1>",hide_menu2)
root.bind('<FocusOut>',hide_menu2)



def change_place_holder(e):
    copy_paste_menu.place_forget()
    #print(e.width)
    add_video_btn.focus_set()
    url_entry.configure(placeholder_text=(int(e.width/150))*"\t" + "Enter URL")
url_entry.bind("<Configure>",change_place_holder)


add_video_btn = objects.customButton_2(master=head_frame ,
                                        normal_color="#BF0202" ,
                                        hover_color="#BF0202",
                                        clicked_color="#BF0202" ,
                                        text="Add",
                                        width=150 ,
                                        height=50 ,
                                        fg_color="#3C3A3A" ,
                                        bg_color="#3C3A3A" ,
                                        text_font=("inter",12,"normal"),
                                        command=add_video)
add_video_btn.place(relx=1 ,x=-230 ,y=1)


def set_download_path():
    global default_download_path
    default_download_path_temp = filedialog.askdirectory()
    if len(default_download_path_temp):
        save_download_path(default_download_path_temp)
        default_download_path = default_download_path_temp

download_path_button =  objects.customButton(master=head_frame ,
                                        image_normal="src/download path button/1.png" ,
                                        image_hover="src/download path button/1.png",
                                        image_clicked="src/download path button/1.png" ,
                                        text="",
                                        width=34 ,
                                        height=34 ,
                                        hover_color=None,
                                        command=set_download_path)
download_path_button.place(relx=1 ,x=-55 ,y=10)
###################################################################################################
###################################################################################################
###################################################################################################

#added button download button
head_frame_2 = customtkinter.CTkFrame(master=root )
head_frame_2.place(x=10 ,y=120 ,relwidth=1, height=60 ,width=-40)


#frame for added download downloaded
body_frame = customtkinter.CTkFrame(master=root ,
                                    )
body_frame.place(y=200 ,x=10 ,relwidth=1,relheight=1 ,height=-212) 

added_frame = objects.scrollableFrame(master=body_frame )
downloading_frame = objects.scrollableFrame(master=body_frame)
downloaded_frame = objects.scrollableFrame(master=body_frame)

def place_frame(frame,button): 
    for button_widget in head_frame_2.winfo_children():
        if type(button_widget) != tkinter.Frame :
            if button_widget != button:
                button_widget.set_normal()
            else:
                button_widget.set_clicked()
    for widgets in body_frame.winfo_children():
        if widgets != frame:
            widgets.place_forget()
    frame.place(x=0 ,y=10 ,relwidth=1 ,relheight=1 ,width=-12 ,height=-20)
    
added_btn = objects.customButton_2(master=head_frame_2 ,
                                 height=30 ,
                                 text_font=("inter",15,"normal")
                                 )

downloading_btn = objects.customButton_2(master=head_frame_2 ,
                                 height=30 ,
                                 text_font=("inter",15,"normal")
                                 )

downloaded_btn = objects.customButton_2(master=head_frame_2 ,
                                 height=30 ,
                                 text_font=("inter",15,"normal")
                                 )

line_1 =  tkinter.Frame(head_frame_2 ,width=1, height=40)
line_1.place(relx=0.33 ,y=10)
line_2 = tkinter.Frame(head_frame_2 ,width=1, height=40)
line_2.place(relx=0.66 ,y=10)

added_btn.configure(command=lambda frame=added_frame:place_frame(frame,added_btn))
downloading_btn.configure(command=lambda frame=downloading_frame:place_frame(frame,downloading_btn))
downloaded_btn.configure(command=lambda frame=downloaded_frame:place_frame(frame,downloaded_btn))

place_frame(added_frame,added_btn)

added_btn.place(x=0 ,y=15 ,relwidth=0.33)
downloading_btn.place(relx=0.33 ,y=15 ,relwidth=0.33)
downloaded_btn.place(relx=0.66 ,y=15 ,relwidth=0.33)


added_temp_frame = customtkinter.CTkFrame(added_frame.outputFrame ,height=1)
downloading_temp_frame = customtkinter.CTkFrame(downloading_frame.outputFrame ,height=1)
downloaded_temp_frame = customtkinter.CTkFrame(downloaded_frame.outputFrame ,height=1)
added_temp_frame.pack(fill="x")
downloading_temp_frame.pack(fill="x")
downloaded_temp_frame.pack(fill="x")
def setWidgetWidth(e):
    added_temp_frame.configure(width=e.width-40)
    downloading_temp_frame.configure(width=e.width-40)
    downloaded_temp_frame.configure(width=e.width-40)
body_frame.bind("<Configure>",setWidgetWidth)


###################################################################################################
###################################################################################################
###################################################################################################


def set_to_default_download_path():
    try:
        path = "C:/Users/{}/Downloads/YT Downloader".format(os.getlogin())
        os.mkdir(path)
    except:
        pass
    save_download_path(path)
    
def path_generate(path:str):
    generate_path = path.replace("\\","/")
    while generate_path[-1]=="/" :
        generate_path = generate_path[:-1]
    return generate_path

def save_download_path(path:str):
    download_path_save_file = open("settings/download_path","w")
    download_path_save_file.write(path)
    download_path_save_file.close()
    
def get_download_path():
    download_path_save_file = open("settings/download_path","r")
    path = download_path_save_file.readline()
    download_path_save_file.close()
    return path


self_exit = False

condition = True
while (condition):
    try:
        default_download_path = get_download_path()
        if os.path.exists(default_download_path) :
            pass
        else:
            try:
                set_to_default_download_path()
                default_download_path = get_download_path()
            except Exception as error:
                print(error)
                self_exit = True
        condition = False
    except FileNotFoundError:
        try:
            setting_file = open("settings/download_path","w")
            setting_file.close()
        except:
            self_exit = True
        condition = True
        
if self_exit :
    sys.exit(0)
###################################################################################################
###################################################################################################
###################################################################################################


def terminate_app():
    for widget in downloading_video_widgets :
        if widget.alive :
            widget.kill()
    for widget in added_video_widgets :
        widget.kill()
    def loop():
        if len(downloading_video_widgets) != 0:
            root.after(1000,loop)
        else:
            root.destroy()
    loop()

root.protocol("WM_DELETE_WINDOW", terminate_app)



def updaing_ui_status():
    added_btn.configure(text="Added ("+ str(len(added_video_widgets)) + ")")
    downloading_btn.configure(text="Downloading ("+ str(len(downloading_video_widgets)-len(paused_video_widgets)) +  "/" +str(len(downloading_video_widgets)) + ")")
    downloaded_btn.configure(text="Downloaded ("+str(len(downloaded_video_widgets)) + ")")
    root.after(500,updaing_ui_status)
updaing_ui_status()


def save_theme(theme:str):
    open("settings/theme","w").write(theme)

def set_ash_theme():
    save_theme("ash")
    dark_theme_btn.configure(text_color="#FFFFFF", fg_color="#909090", hover_color="#909090", bg_color="#343638")
    ash_theme_btn.configure(text_color="#FFFFFF", fg_color="#909090", hover_color="#909090", bg_color="#343638")
    theme_label.configure(fg="#FFFFFF",bg="#343638")
    
    copy_paste_menu.set_theme(fg_color="#606060",bg_color="#343638", border_color="#707070",line_fg="#909090", text_color="#ffffff", hover_color="#606060")
    
    set_theme(main_bg="#343638",
          object_fg="#505050",object_fg_hover="#4d4b4b", object_border="#cccccc", object_border_hover="#ffffff", object_txt="#ffffff", object_txt_2="#858585",
          entry_fg="#343638", entry_bd="#565b5e",
          btn_bg="#d9d9d9", btn_txt="#494949",
          line_fg="#000000")
    
def set_dark_theme():
    save_theme("dark")
    dark_theme_btn.configure(text_color="#FFFFFF", fg_color="#303030", hover_color="#303030", bg_color="#101010")
    ash_theme_btn.configure(text_color="#FFFFFF", fg_color="#303030", hover_color="#303030", bg_color="#101010")
    theme_label.configure(fg="#FFFFFF",bg="#101010")
    
    copy_paste_menu.set_theme(fg_color="#252525",bg_color="#101010", border_color="#454545" ,line_fg="#353535", text_color="#aaaaaa", hover_color="#353535")
    
    set_theme(main_bg="#101010",
          object_fg="#151515",object_fg_hover="#252525", object_border="#555555",object_border_hover="#999999", object_txt="#cccccc", object_txt_2="#353535",
          entry_fg="#101010", entry_bd="#404040", 
          btn_bg="#202020", btn_txt="#ffffff",
          line_fg="#ffffff")
theme_label = tkinter.Label(master=root, text="Theme  :  ")
theme_label.place(relx=1 ,y=2, x=-160)
dark_theme_btn = customtkinter.CTkButton(master=root, text="Dark", command=set_dark_theme, height=20, width=45)
dark_theme_btn.place(relx=1 ,y=2, x=-50)
ash_theme_btn = customtkinter.CTkButton(master=root, text="Ash", command=set_ash_theme, height=20, width=45)
ash_theme_btn.place(relx=1 ,y=2, x=-100)


    
copy_paste_menu = objects.copy_paste_menu(master=root)

#credits for 
credits_btn = customtkinter.CTkButton(master=root, width=1, height=1, text="~", text_font=("arial",12,"bold"))
credits_btn.place(relx=1, rely=1, x=-26, y=-23)
credits_menu = objects.credits_menu(master=root)
def show_credits(e):
    credits_menu.place(relx=1, rely=1, x=-195, y=-83, width=180, height=65)
def hide_credits(e):
    credits_menu.place_forget()
credits_btn.bind("<Enter>", show_credits)
credits_btn.bind("<Leave>", hide_credits)

#configure theme , 
try:
    f = open("settings/theme","r")
    f.close()
except:
    f = open("settings/theme","w")
    f.close()
if open("settings/theme","r").read() == "dark":
    set_dark_theme()
else:
    set_ash_theme()




root.mainloop()

#clear temp files
for file in ["temp/" + file for file in os.listdir("temp")] :
    try:
        os.remove(file)
    except:
        pass
    

os._exit(1)