import win11toast
import moviepy.editor as mpe
import pytube
from pytube import request as pytube_request
import tkinter
import os
import threading
from urllib import request
import time
from PIL import Image , ImageDraw 
import webbrowser
import pyautogui
import customtkinter



def PASS():
    pass

def PASS_E(e):
    pass

def checkFileName(path):
    splited = path.split(".")
    file_name ,extenstion = ".".join(splited[0:-1]),splited[-1]
    generate_file_name = file_name
    i = 2
    while os.path.exists(generate_file_name+"."+extenstion):
        generate_file_name = file_name + " ({})".format(i)
        i += 1
    return generate_file_name + "." + extenstion

def convertData(s,with_decimal):
    datas = ["B","KB","MB","GB","TB","PB","EB"]
    index= 0
    
    while len(str(int(s))) > 2 and (index+1) < len(datas) :
        s = s /1024
        index += 1
    if with_decimal == True:
        val = str(round(s,1)) + " " + datas[index]
    else:
        val = str(int(s)) + " " + datas[index]
    return val

def replaceFileName(url:str):
    filename = url
    replaces = ["\\","/",":",'"',"?","<",">","|","*"]
    for re in replaces:
        filename = filename.replace(re,"~")
    return filename

def fix_len(val:str, leng:int, side:str="->"):
    if side=="->":
        return val+(leng-len(val))*"  "
    else:
        return(leng-len(val))*"  " +val

class customButton(customtkinter.CTkButton):
    def __init__(self ,text ,image_normal ,image_hover ,image_clicked ,**kwargs):
        super().__init__(**kwargs)
        
        self.text = text
        self.image_normal = tkinter.PhotoImage(file=image_normal)
        self.image_hover = tkinter.PhotoImage(file=image_hover)
        self.image_clicked = tkinter.PhotoImage(file=image_clicked)
        
        self.set_normal()
    def set_normal(self):
        self.configure(state="normal")
        self.configure(image=self.image_normal ,text=self.text)
        
        def _button_normal(e):
            self.configure(image=self.image_normal ,text=self.text)
            
        def _button_hover(e):
            self.configure(image=self.image_hover ,text=self.text)
        self.bind("<Enter>" ,_button_hover)
        self.bind("<Leave>" ,_button_normal)
            
    def set_clicked(self):
        self.configure(state="disabled")
        self.configure(image=self.image_clicked ,text=self.text)
        
        def _button_normal(e):
            self.configure(image=self.image_clicked ,text=self.text)
        def _button_hover(e):
            self.configure(image=self.image_clicked ,text=self.text)
        self.bind("<Enter>" ,_button_hover)
        self.bind("<Leave>" ,_button_normal)

class customButton_2(customtkinter.CTkButton):
    def __init__(self ,text="" ,normal_color=None ,hover_color=None ,clicked_color=None ,**kwargs):
        super().__init__(**kwargs)
        
        self.text = text
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.clicked_color = clicked_color
        
        self.set_normal()

    def set_normal(self):
        self.place(y=15)
        #self.configure(state="normal")
        self.configure(fg_color=self.normal_color ,text=self.text, text_font=("inter",15,"normal"))
        
        def _button_normal(e):
            self.configure(fg_color=self.normal_color ,text=self.text, text_font=("inter",15,"normal"))
            
        def _button_hover(e):
            self.configure(fg_color=self.hover_color ,text=self.text ,text_font=("inter",17,"normal"))
        self.bind("<Enter>" ,_button_hover)
        self.bind("<Leave>" ,_button_normal)
        
            
    def set_clicked(self):
        self.place(y=12)
        #self.configure(state="disabled")
        self.configure(fg_color=self.clicked_color ,text=self.text ,text_font=("inter",17,"bold"))
        
        def _button_normal(e):
            self.configure(fg_color=self.clicked_color ,text=self.text ,text_font=("inter",17,"bold"))
        def _button_hover(e):
            self.configure(fg_color=self.clicked_color ,text=self.text ,text_font=("inter",17,"bold"))
        self.bind("<Enter>" ,_button_hover)
        self.bind("<Leave>" ,_button_normal)
    
    def set_theme(self ,normal_color ,hover_color ,clicked_color, bg_color, text_color):
        self.configure(bg_color=bg_color, fg_color=normal_color, text_color=text_color)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.clicked_color = clicked_color
    


class scrollableFrame(customtkinter.CTkFrame):
    def __init__(self, master ,fg_color=None  ,**kwargs):
        super().__init__(master, fg_color=fg_color ,bg_color=fg_color,**kwargs)
        self.master = master

        self.mainCanvas = tkinter.Canvas(master=self ,
                                         bg=fg_color ,
                                         scrollregion=(0,0,0,0) ,
                                         highlightthickness=0)
    
        self.verticalScroller = customtkinter.CTkScrollbar(master=self ,
                                                           command=self.mainCanvas.yview ,
                                                           orientation='vertical' ,
                                                           fg_color=fg_color ,bg_color=fg_color)
        self.verticalScroller.place(relheight=1 ,relx=1 ,x=-13 ,width=15)
        #maincanvas sync with scrollabars
        self.mainCanvas.configure(yscrollcommand=self.verticalScroller.set)

        #create top frame for all widget 
        self.outputFrame = customtkinter.CTkFrame(master=self.mainCanvas ,
                                                  height=0 ,
                                                  fg_color=fg_color ,bg_color=fg_color)
        self.mainCanvas.create_window((0,0) ,window=self.outputFrame,anchor='nw')
        self.mainCanvas.place(relwidth=1 ,relheight=1 ,width=-25)
        
     
        #self.masterFrame.bind('<Configure>' ,self.__configure)
        self.configureWinfo(height=self.mainCanvas.winfo_height())
        
        
    def configureWinfo(self,width=None,height=None):
        if width==None:
            width = self.mainCanvas.winfo_width()
        if height==None:
            height = self.outputFrame.winfo_height()
        self.mainCanvas.configure(scrollregion=(0,0,width,height))
        self.mainCanvas.configure(height=height ,width=width)
        self.outputFrame.configure(width=width,height=height)
        
    def set_theme(self, fg_color=None, bg_color=None):
        self.configure(fg_color=fg_color, bg_color=bg_color)
        self.mainCanvas.configure(bg=fg_color)
        self.verticalScroller.configure(bg_color=bg_color, fg_color=bg_color)
        self.outputFrame.configure(bg_color=bg_color, fg_color=fg_color)
    

class DownloadedVideoObject(customtkinter.CTkFrame):
    def __init__(self,master ,url ,
                thumbnail ,thumbnail_hover,
                title ,channel ,file_size ,
                downloaded_widgets:list ,
                selected_quallity ,
                fg_color=None ,fg_color_hover=None,
                bg_color=None ,
                txt_color = None,
                border_color=None ,border_color_hover=None,
                file_downloaded_path = "" ,
                height=None,
                **kwargs):
        self.alive = True
        self.thumbnail_hover = thumbnail_hover
        self.thumbnail = thumbnail
        self.downloaded_widgets = downloaded_widgets
        self.downloaded_widgets.append(self)
        super().__init__(master.outputFrame ,fg_color=fg_color ,bg_color=bg_color ,border_color=border_color, height=height ,**kwargs)
        self.main_master = master
        self.main_master.configureWinfo(height=len(self.downloaded_widgets)*(height+4))
        
        
        self.fg_color_normal = fg_color
        self.fg_color_hover = fg_color_hover
        self.border_color_normal = border_color
        self.border_color_hover = border_color_hover
        self.height = height
        
        def play_video():
            os.startfile(file_downloaded_path)
        self.thumbnailBtn = customtkinter.CTkButton(master=self ,text="" ,
                                                    image=thumbnail ,
                                                    width=128 ,
                                                    height=72 ,fg_color=fg_color ,bg_color=fg_color ,
                                                    state='disable' ,
                                                    border_width=0, command=play_video)
        def thumbnail_hover_img_set(e):
            self.thumbnailBtn.configure(image=self.thumbnail_hover)
        def thumbnail_img_set(e):
            self.thumbnailBtn.configure(image=self.thumbnail)
            
            
        def pop_up(e):
            if self.alive :
                self.configure(border_color=self.border_color_hover, border_width=2 ,height=self.height+4)
                self.pack(pady=0 ,padx=0 ,fill="x")
                self.thumbnailBtn.place(x=10,y=5)
                #self.set_react(fg_color=self.fg_color_hover)
        def pop_back(e):
            if self.alive:
                self.configure(border_color=self.border_color_normal, border_width=1,height=self.height)
                self.pack(pady=2 ,padx=0 ,fill="x")
                self.thumbnailBtn.place(x=10,y=3)
                #self.set_react(fg_color=self.fg_color_normal)
                
        self.bind("<Enter>",pop_up)
        self.bind("<Leave>",pop_back)
       
        self.thumbnailBtn.bind("<Enter>",thumbnail_hover_img_set)
        self.thumbnailBtn.bind("<Leave>",thumbnail_img_set)
      
        self.titleLabel = tkinter.Label(master=self ,anchor="w" ,
                                        text = "Title : "+title ,
                                        font=('arial',10,'bold') ,
                                        bg=fg_color ,fg=txt_color)
        
    
        self.channelLabel = tkinter.Label(master=self ,font=('arial',8,'bold') ,anchor="w" ,
                                          text = "Channel : "+channel ,
                                          bg=fg_color ,fg=txt_color )
        
    
        self.urlLabel = tkinter.Label(master=self ,anchor="w" ,
                                      text=url ,font=('arial',10) ,
                                      bg=fg_color ,fg=txt_color)
        
        def open_location():
            os.startfile("/".join(file_downloaded_path.split("/")[:-1]))
        self.open_folder_btn_img_normal = "src/download path button/2.png"
        self.open_folder_btn_img_hover = "src/download path button/2.png"
        self.open_folder_btn_img_clicked = "src/download path button/2.png"
        self.open_folder_btn = customButton(master=self ,width=15, height=15,
                                      image_normal=self.open_folder_btn_img_normal ,
                                      image_hover=self.open_folder_btn_img_hover ,
                                      image_clicked=self.open_folder_btn_img_clicked ,
                                      text="" ,bg_color=fg_color ,fg_color=fg_color ,
                                      hover_color=fg_color ,
                                      command=open_location)
        
        self.remove_btn_img_normal = "src/remove button/normal.png"
        self.remove_btn_img_hover = "src/remove button/normal.png"
        self.remove_btn_img_clicked = "src/remove button/normal.png"
        self.removeBtn = customButton(master=self ,
                                      image_normal=self.remove_btn_img_normal ,
                                      image_hover=self.remove_btn_img_hover ,
                                      image_clicked=self.remove_btn_img_clicked ,
                                      text="" ,bg_color=fg_color ,fg_color=fg_color ,
                                      hover_color=fg_color ,
                                      command=self.kill)
        
        self.thumbnailBtn.place(x=10,y=3)
        self.titleLabel.place(x=150,y=8 ,relwidth=0.9 ,width=-150)
        self.channelLabel.place(x=150 ,y=28 ,relwidth=0.8 ,width=-200)
        self.urlLabel.place(x=150 ,y=48 ,relwidth=0.8,width=-200)
        self.open_folder_btn.place(relx=1 ,x=-150 ,y=30)
       
        
        self.removeBtn.place(relx=1,x=-50,y=27 ,height=25 ,width=25)
        
    def set_theme(self, fg_color=None, fg_color_hover=None ,bg_color=None, text_color=None, bd_color=None, bd_color_hover=None):
        self.configure(fg_color=fg_color, bg_color=bg_color, border_color=bd_color)
        self.thumbnailBtn.configure(fg_color=fg_color, bg_color=fg_color, hover_color=fg_color)
        self.channelLabel.configure(bg=fg_color, fg=text_color)
        self.titleLabel.configure(bg=fg_color, fg=text_color)
        self.urlLabel.configure(bg=fg_color, fg=text_color)
        self.open_folder_btn.configure(fg_color=fg_color, bg_color=fg_color, hover_color=fg_color)
        self.removeBtn.configure(bg_color=fg_color ,fg_color=fg_color ,
                                hover_color=fg_color)
        
        self.fg_color_normal = fg_color
        self.fg_color_hover = fg_color_hover
        self.border_color_normal = bd_color
        self.border_color_hover = bd_color_hover

        
    def kill(self):
        self.alive = False
        self.downloaded_widgets.remove(self)
        self.main_master.configureWinfo(height=len(self.downloaded_widgets)*(self.height+4))
        self.pack_forget()
        del self

class DownloadingVideoObject(customtkinter.CTkFrame):
    def __init__(self,master ,url ,
                 thumbnail ,thumbnail_hover,
                 title ,channel ,
                 selected_quallity,
                 download_info, audio_size, audio_itag,
                 fg_color ,fg_color_hover,
                 bg_color ,txt_color ,
                 video_stream_data, 
                 downloading_widgets:list ,paused_widgets:list,downloaded_widgets:list ,
                 file_download_path = "" ,
                 downloaded_master=None ,
                 border_color=None ,border_color_hover=None,
                 height=None,**kwargs):
        super().__init__(master.outputFrame ,fg_color=fg_color ,bg_color=bg_color ,border_color=border_color, height=height ,**kwargs)
        
        self.alive = True
        self.alive_2 = True
        self.downloaded_master = downloaded_master
        self.main_master = master
        self.downloading_widgets = downloading_widgets
        self.paused_widgets = paused_widgets
        self.downloading_widgets.append(self)
        self.main_master.configureWinfo(height=len(self.downloading_widgets)*(height+4))
        self.downloaded_widgets = downloaded_widgets
        self.url = url 
        self.thumbnail = thumbnail
        self.thumbnail_hover = thumbnail_hover
        self.title = title
        self.channel = channel 

        self.selected_quallity = selected_quallity
        self.download_info = download_info
        self.audio_size = audio_size
        self.audio_inbuilt_in = ""
        self.audio_itag = audio_itag
        self.height = height
        self.video_stream_data = video_stream_data
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.txt_color = txt_color
        
        self.downloading = True
        self.download_pause = False
        self.download_pause_success = False
        
        self.fg_color_normal = fg_color
        self.fg_color_hover = fg_color_hover
        self.border_color_normal = border_color
        self.border_color_hover = border_color_hover
        self.height = height
        
        def pop_up(e):
            if self.alive_2 :
                self.configure(border_color=self.border_color_hover, border_width=2 ,height=self.height+4)
                self.pack(pady=0 ,padx=0 ,fill="x")
                self.thumbnailBtn.place(x=10,y=5)
                #self.set_react(fg_color=self.fg_color_hover)
        def pop_back(e):
            if self.alive_2:
                self.configure(border_color=self.border_color_normal, border_width=1,height=self.height)
                self.pack(pady=2 ,padx=0 ,fill="x")
                self.thumbnailBtn.place(x=10,y=3)
                #self.set_react(fg_color=self.fg_color_normal)
                
        self.bind("<Enter>",pop_up)
        self.bind("<Leave>",pop_back)

        self.file_download_info = self.download_info[self.selected_quallity]
        self.file_size_conveterd = convertData(self.file_download_info["size"] ,with_decimal=1)
        
        self.file_size = self.file_download_info["size"]
        self.audio_inbuilt_in = self.file_download_info["audio"]
        self.download_type = self.file_download_info["type"]
        
        if self.audio_inbuilt_in:
            self.download_file_name = file_download_path + "/" +  replaceFileName(self.channel + " - " + self.title) + self.file_download_info["ext"]
        else:
            self.download_file_name = file_download_path + "/" +  replaceFileName(self.channel + " - " + self.title) + ".videotmp"
            
        
        #############################################################################
        ############################################################################# wigets
        
        def thumbnail_hover_img_set(e):
            self.thumbnailBtn.configure(image=self.thumbnail_hover)
        def thumbnail_img_set(e):
            self.thumbnailBtn.configure(image=self.thumbnail)
        def open_url():
            webbrowser.open(self.url)

        self.thumbnailBtn = customtkinter.CTkButton(master=self ,text="" ,
                                                    image=self.thumbnail ,
                                                    width=128 ,
                                                    height=72 ,fg_color=fg_color ,bg_color=fg_color ,
                                                    state='disable' ,
                                                    border_width=0,
                                                    command=open_url)
        self.thumbnailBtn.bind("<Enter>",thumbnail_hover_img_set)
        self.thumbnailBtn.bind("<Leave>",thumbnail_img_set)
      
        self.titleLabel = tkinter.Label(master=self ,anchor="w" ,
                                        text = "Title : "+self.title ,
                                        font=('arial',10,'bold') ,
                                        bg=fg_color ,fg=txt_color)
        
    
        self.channelLabel = tkinter.Label(master=self ,font=('arial',8,'bold') ,anchor="w" ,
                                          text = "Channel : "+self.channel ,
                                          bg=fg_color ,fg=txt_color )
        
        self.urlLabel = tkinter.Label(master=self ,anchor="w" ,
                                      text=self.url ,font=('arial',10) ,
                                      bg=fg_color ,fg=txt_color)
        
        self.remove_btn_img_normal = "src/remove button/normal.png"
        self.remove_btn_img_hover = "src/remove button/normal.png"
        self.remove_btn_img_clicked = "src/remove button/normal.png"
        self.removeBtn = customButton(master=self ,
                                      image_normal=self.remove_btn_img_normal ,
                                      image_hover=self.remove_btn_img_hover ,
                                      image_clicked=self.remove_btn_img_clicked ,
                                      text="" ,bg_color=fg_color ,fg_color=fg_color ,
                                      hover_color=fg_color ,
                                      command=self.kill)
        
        
        self.progress_frame = customtkinter.CTkFrame(self ,height=40 ,fg_color=fg_color)
    
    
        self.downloadProgressBar = customtkinter.CTkProgressBar(master=self.progress_frame ,bg_color=fg_color,
                                                                height=8)
        self.downloadProgressBar.set(0)
        self.ResolutionLabel = tkinter.Label(master=self.progress_frame,
                                             text="Quallity : "+self.selected_quallity,
                                             bg=fg_color ,fg=txt_color)
        self.downloadProgressLabel = tkinter.Label(master=self.progress_frame ,
                                                     text="Progress : "+convertData(0,with_decimal=1)\
                                                        +"/"+\
                                                        self.file_size_conveterd ,
                                                     bg=fg_color ,fg=txt_color)
        self.downloadPercentageLabel = tkinter.Label(master=self.progress_frame ,
                                                       text="0%" ,
                                                       bg=fg_color ,fg=txt_color)
        
        self.status_frame = customtkinter.CTkFrame(self ,height=76 ,fg_color=fg_color)
        
        self.pause_button_img_normal = tkinter.PhotoImage(file="src/pause/normal.png")
        self.pause_button_img_hover = tkinter.PhotoImage(file="src/pause/hover.png")
        self.resume_button_img_normal = tkinter.PhotoImage(file="src/resume/normal.png")
        self.resume_button_img_hover = tkinter.PhotoImage(file="src/resume/hover.png")
        self.pause_resume_button = customtkinter.CTkButton(self.status_frame ,text="" ,
                                                           width=15 ,height=15 ,
                                                           fg_color=fg_color ,bg_color=fg_color ,
                                                           hover_color=fg_color)
        self.pauseResumeButtonConfigure("pause")
        self.statusLabel = tkinter.Label(master=self.status_frame ,
                                         text="   Downloading..." ,
                                         bg=fg_color ,fg=txt_color)
    
        self.thumbnailBtn.place(x=10,y=3)
        self.titleLabel.place(x=150,y=8 ,relwidth=0.90 ,width=-150)
        self.channelLabel.place(x=150 ,y=28 ,relwidth=0.43 ,width=-150)
        self.urlLabel.place(x=150 ,y=48 ,relwidth=0.43 ,width=-130)
        
        self.progress_frame.place(y=28 ,relx=0.5 ,relwidth=0.5, width=-170)
        self.downloadProgressBar.pack(fill="x" ,pady=5)
        self.ResolutionLabel.pack(expand=True, fill="both", side="left" ,pady=0)
        self.downloadProgressLabel.pack(expand=True, fill="both", side="left" ,pady=0)
        self.downloadPercentageLabel.pack(expand=True, fill="both", side="left" ,pady=0)
        
        self.status_frame.place(y=25 ,relx=1, x=-170)
        self.pause_resume_button.pack()
        self.statusLabel.pack()
        
        self.removeBtn.place(relx=1,x=-50,y=27 ,height=25 ,width=25)

        threading.Thread(target=self.downloadVideo).start()
        
    def set_theme(self, fg_color=None, fg_color_hover=None ,bg_color=None, text_color=None, bd_color=None, bd_color_hover=None):
        self.configure(fg_color=fg_color, bg_color=bg_color, border_color=bd_color)
        
        self.thumbnailBtn.configure(fg_color=fg_color, bg_color=fg_color, hover_color=fg_color)
        self.channelLabel.configure(bg=fg_color, fg=text_color)
        self.titleLabel.configure(bg=fg_color, fg=text_color)
        self.urlLabel.configure(bg=fg_color, fg=text_color)

        
        self.progress_frame.configure(fg_color=fg_color, bg_color=fg_color)
        self.ResolutionLabel.configure(bg=fg_color, fg=text_color)
        self.downloadProgressLabel.configure(bg=fg_color, fg=text_color)
        self.downloadPercentageLabel.configure(bg=fg_color, fg=text_color)
        
        
        self.status_frame.configure(fg_color=fg_color ,bg_color=fg_color)
        self.pause_resume_button.configure(fg_color=fg_color ,bg_color=fg_color ,
                                            hover_color=fg_color)
        
        
        self.statusLabel.configure(bg=fg_color, fg=text_color)
        self.removeBtn.configure(bg_color=fg_color ,fg_color=fg_color ,
                                hover_color=fg_color)
        
        self.fg_color_normal = fg_color
        self.fg_color_hover = fg_color_hover
        self.border_color_normal = bd_color
        self.border_color_hover = bd_color_hover
        
    def pauseResumeButtonConfigure(self,state):
        if state=="pause":
            self.pause_resume_button.configure(image=self.pause_button_img_normal)
            def pauseBtnHover(e):
                self.pause_resume_button.configure(image=self.pause_button_img_hover)
            def pauseBtnNormal(e):
                self.pause_resume_button.configure(image=self.pause_button_img_normal)
            self.pause_resume_button.bind("<Enter>",pauseBtnHover)
            self.pause_resume_button.bind("<Leave>",pauseBtnNormal)
            
            def pauseTheDownload():
                self.pause_resume_button.configure(command=PASS)
                self.download_pause = True
                self.statusLabel.configure(text="       Pausing...      ")
                while not(self.download_pause_success):
                    time.sleep(0.5)
                    pass
                self.statusLabel.configure(text="        Paused..!      ")
                self.paused_widgets.append(self)
                self.pauseResumeButtonConfigure("resume")  
            self.pause_resume_button.configure(command=threading.Thread(target=pauseTheDownload).start)
            
            
        elif state=="resume":
            self.pause_resume_button.configure(image=self.resume_button_img_normal)
            def resumeBtnHover(e):
                self.pause_resume_button.configure(image=self.resume_button_img_hover)
            def resumeBtnNormal(e):
                self.pause_resume_button.configure(image=self.resume_button_img_normal)
            self.pause_resume_button.bind("<Enter>",resumeBtnHover)
            self.pause_resume_button.bind("<Leave>",resumeBtnNormal)
            
            def resumeTheDownload():
                self.statusLabel.configure(text="   Downloading...")
                self.paused_widgets.remove(self)
                self.download_pause = False
                self.pauseResumeButtonConfigure("pause")
            self.pause_resume_button.configure(command=resumeTheDownload)
            
    def showNotification(self ,state, download_file_name):
        if state == "Download Complete" :
            file_path = os.path.abspath(download_file_name)
            folder_path = "/".join(file_path.split("\\")[0:-1])
            buttons = [
                {'activationType': 'protocol', 'arguments': file_path , 'content': 'Play'},
                {'activationType': 'protocol', 'arguments': folder_path , 'content': 'Open Folder'}
            ]
            win11toast.toast(title=state+"..!" ,app_id="YouTube Downloader" ,icon=os.path.abspath("src\\icon\\main.ico") ,
                            body=file_path.split("\\")[-1] ,
                            buttons=buttons,duration="short")
        else:
            file_path = os.path.abspath(download_file_name)
            folder_path = "/".join(file_path.split("\\")[0:-1])
            win11toast.toast(title=state+"..!" ,app_id="YouTube Downloader" ,icon=os.path.abspath("src\\icon\\main.ico") ,
                            body=file_path.split("\\")[-1], 
                            duration="short")
        
            
    def downloadSuccess(self):
        self.pause_resume_button.pack_forget()
        self.statusLabel.configure(text="Download\nComplete..!")
        time.sleep(0.5)
        self.pack_forget()
        self.set_to_downloaded()
        download_file_name = self.download_file_name
        try:
            threading.Thread(target=self.showNotification,args=("Download Complete",download_file_name)).start()
        except Exception as error:
            print(error)
        self._kill()
        

            
    def set_to_downloaded(self):
        globals()["downloaded_video_"+str(len(self.downloaded_widgets)+1)] =  DownloadedVideoObject(master=self.downloaded_master ,
                                                    url=self.url ,
                                                    thumbnail=self.thumbnail,
                                                    thumbnail_hover=self.thumbnail_hover,
                                                    title=self.title ,channel=self.channel ,
                                                    file_size=self.file_size ,
                                                    selected_quallity=self.selected_quallity,
                                                    file_downloaded_path =self.download_file_name ,
                                                    fg_color=self.fg_color ,
                                                    bg_color=self.bg_color ,
                                                    txt_color = self.txt_color,
                                                    border_color=self.border_color_normal ,
                                                    border_color_hover=self.border_color_hover,
                                                    corner_radius=10 ,
                                                    height=80 ,
                                                    downloaded_widgets = self.downloaded_widgets,
                                                    border_width=1)
        globals()["downloaded_video_"+str(len(self.downloaded_widgets)+1)].pack(pady=1 ,padx=0 ,fill="x")
        
        
    def downloadFailed(self):
        self.pause_resume_button.pack_forget()
        self.statusLabel.configure(text="       Download\n       Failed..!" ,fg="#ff0000" )
        self.paused_widgets.append(self)
        download_file_name = self.download_file_name
        try:
            threading.Thread(target=self.showNotification,args=("Download Failed",download_file_name)).start()
        except Exception as error:
            print(error)
            
    def convert_video_audio(self):
        #old version
        self.pause_resume_button.configure(state="disabled")
        self.statusLabel.configure(text="     Converting...")
        
        video_file = mpe.VideoFileClip(self.download_file_name)
        audio_file = mpe.AudioFileClip(self.download_audio_file_name)
        
        final_file = video_file.set_audio(audio_file)
        final_file_name = checkFileName(".".join(self.download_file_name.split(".")[0:-1]) + ".mp4")
        print("Final File :",final_file_name)
        final_file.write_videofile(final_file_name)
        try:
            video_file.close()
            audio_file.close()
            os.remove(self.download_file_name)
            os.remove(self.download_audio_file_name)
        except:
            pass
        self.download_file_name = final_file_name
        self.downloading = False
        self.downloadSuccess()
        
        
        
        
        """self.pause_resume_button.configure(state="disabled")
        self.statusLabel.configure(text="     Converting...")
        
        sounds = pydub.AudioSegment.from_mp3(self.download_audio_file_name)
        dst_sound = checkFileName(self.download_audio_file_name+".wav")
        sounds.export(dst_sound, format="wav")
        
        final_file_name = checkFileName(".".join(self.download_file_name.split(".")[0:-1]) + ".mp4")
        
        #convert audio to wave
        with open(self.download_audio_file_name, "rb") as inp_f:
            data = inp_f.read()
        os.remove(self.download_audio_file_name)
        with wave.open(self.download_audio_file_name, "wb") as out_f:
            out_f.setnchannels(2)
            out_f.setsampwidth(2) # number of bytes
            out_f.setframerate(44100)
            out_f.writeframesraw(data)
        
        with wave.open(self.download_audio_file_name, 'rb') as audio_file:
            audio_data = audio_file.readframes(audio_file.getnframes())
            audio_params = audio_file.getparams()
        with open(self.download_file_name, 'ab') as video_file:
            video_file.write(audio_data)
        os.rename(self.download_file_name,final_file_name)
        try:
            os.remove(self.download_audio_file_name)
        except:
            pass
        self.download_file_name = final_file_name
        self.downloading = False
        self.downloadSuccess()"""
    
    def audio_only_download(self):
        stream = self.video_stream_data.get_audio_only()
        self.download_audio_file_name = checkFileName(self.download_file_name+".audiotmp")
        print("Audio File :",self.download_audio_file_name)
        with open(self.download_audio_file_name,"wb") as self.audio_file :
            stream = pytube_request.stream(stream.url)
            while 1:
                if self.alive == False:
                    self.downloading = False
                    break
                if self.download_pause :
                    self.download_pause_success = True
                    time.sleep(0.7)
                    continue
                self.download_pause_success = False
                if self.alive == False:
                    self.downloading = False
                    break
                chunk = next(stream, None)
                if self.alive == False:
                    self.downloading = False
                    break
                if chunk:
                    self.audio_file.write(chunk)
                    self.downloded_bytes += len(chunk)
                    self.configureDownloadProgress()
                else:
                    self.audio_file.close()
                    self.convert_video_audio()
                    break
    def downloadVideo(self):
        try:
            self.downloded_bytes = 0
            if self.download_type == "Video":
                stream = self.video_stream_data.get_by_itag(self.file_download_info["itag"])
            elif self.download_type == "Audio":
                stream = self.video_stream_data.get_audio_only()
            
            self.download_file_name = checkFileName(self.download_file_name)
            print("File :",self.download_file_name)
            with open(self.download_file_name,"wb") as self.video_file :
                stream = pytube_request.stream(stream.url)
                while 1:
                    if self.alive == False:
                        self.downloading = False
                        break
                    if self.download_pause :
                        self.download_pause_success = True
                        time.sleep(0.7)
                        continue
                    self.download_pause_success = False
                    if self.alive == False:
                        self.downloading = False
                        break
                    chunk = next(stream, None)
                    if self.alive == False:
                        self.downloading = False
                        break
                    if chunk:
                        self.video_file.write(chunk)
                        self.downloded_bytes += len(chunk)
                        self.configureDownloadProgress()
                    else:
                        if self.audio_inbuilt_in:
                            self.video_file.close()
                            self.downloading = False
                            self.downloadSuccess()
                        else:
                            self.video_file.close()
                            self.audio_only_download()
                        break
        except Exception as error:
            print(error)
            self.downloading = False
            self.downloadFailed()
            
    def configureDownloadProgress(self):
        download_progress = self.downloded_bytes/self.file_size
        self.downloadProgressBar.set(download_progress)
        self.downloadPercentageLabel.configure(text=str(round(download_progress*100,2)) + "%")
        self.downloadProgressLabel.configure(text= "Progress : "+convertData(self.downloded_bytes,with_decimal=1)\
                                                        +"/"+\
                                                        self.file_size_conveterd ,)
    
        
    def _kill(self):
        self.pause_resume_button.configure(state="disabled")
        self.statusLabel.configure(fg="#ff0000",text="     Removing...   ")
        while self.downloading:
            time.sleep(0.5)
        self.alive_2 = False
        self.pack_forget()
        if self in self.paused_widgets:
            self.paused_widgets.remove(self)
        self.downloading_widgets.remove(self)
        self.main_master.configureWinfo(height=len(self.downloading_widgets)*(self.height+4))
        del self
        

    def kill(self):
        self.alive = False
        self.removeBtn.configure(command=PASS)
        self.statusLabel.place_forget()
        threading.Thread(target=self._kill).start()
        

                

class AddedVideoObject(customtkinter.CTkFrame):
    def __init__(self,master:scrollableFrame ,url ,fg_color ,bg_color, fg_color_hover, border_color,border_color_hover ,txt_color, txt_color_2, added_widgets:list ,height ,added_frame_scrolled:list,**kwargs):
        super().__init__(master.outputFrame ,fg_color=fg_color ,bg_color=bg_color ,border_color=border_color,height=height ,**kwargs)
        self.main_master = master
        self.added_widgets = added_widgets
        self.added_widgets.append(self)
        self.main_master.configureWinfo(height=len(self.added_widgets)*(height+4))
        
       
        ############################################################################
        self.url = url
        self.title = ""
        self.channel = ""
        self.thumbnail = ""
        self.thumbnail_hover = ""
        self.selected_quallity = ""
    
        self.alive = True
    
        self.download_info = ""
        
        self.txt_color = txt_color
        self.txt_color_2 = txt_color_2
        self.audio_itag = ""
        self.audio_size = ""
        self.video_stream_data = None
        
        self.fg_color_normal = fg_color
        self.fg_color_hover = fg_color_hover
        self.border_color_normal = border_color
        self.border_color_hover = border_color_hover
        self.height = height
        

        
        def scroll(e):
            """scroll_v = (-1*(e.delta/120))/len(self.added_widgets)
            added_frame_scrolled[0] =  added_frame_scrolled[0] + scroll_v
            print("end_value : ",self.main_master.verticalScroller.end_value)
            print(added_frame_scrolled[0])"""
            """if added_frame_scrolled[0] >= 1 - (2*(1/len(self.added_widgets))):
                added_frame_scrolled[0] = 1 - (2*(1/len(self.added_widgets)))
            elif added_frame_scrolled[0] <= 0:
                adde"""
            """
            self.main_master.mainCanvas.yview("moveto",added_frame_scrolled[0])
            #print("end_value : ",self.main_master.verticalScroller.end_value)
            added_frame_scrolled[0] = self.main_master.verticalScroller.get()
            """
            
        self.main_master.bind_all("<MouseWheel>", scroll)
        
        def pop_up(e):
            if self.alive :
                self.configure(border_color=self.border_color_hover, border_width=2 ,height=self.height+4)
                self.pack(pady=0 ,padx=0 ,fill="x")
                self.thumbnailBtn.place(x=10,y=5)
                #self.set_react(fg_color=self.fg_color_hover)
        def pop_back(e):
            if self.alive:
                self.configure(border_color=self.border_color_normal, border_width=1,height=self.height)
                self.pack(pady=2 ,padx=0 ,fill="x")
                self.thumbnailBtn.place(x=10,y=3)
                #self.set_react(fg_color=self.fg_color_normal)
        
        self.bind("<Enter>",pop_up)
        self.bind("<Leave>",pop_back)
        
        #############################################################################
        ############################################################################# wigets
        def open_url():
            webbrowser.open(self.url)
        self.thumbnailBtn = customtkinter.CTkButton(master=self ,text="" ,width=128 ,
                                                    height=72 ,fg_color=fg_color ,bg_color=fg_color,
                                                    state='disable' ,
                                                    border_width=0  ,
                                                    command=open_url)
        
        
        self.titleLabel = tkinter.Label(master=self ,anchor="w",
                                        font=('arial',10,'bold') ,
                                        bg=fg_color, fg=txt_color )
        
        self.channelLabel = tkinter.Label(master=self,font=('arial',8,'bold')  ,anchor="w",
                                         bg=fg_color, fg=txt_color)
        
        self.ResolutionMenu = customtkinter.CTkComboBox(master=self ,values=["..........","..........",".........."])
        
        self.download_btn_img_normal = "src/download button/normal.png"
        self.download_btn_img_hover = "src/download button/normal.png"
        self.download_btn_img_clicked = "src/download button/normal.png"
        self.downloadBtn = customButton(master=self ,
                                        text="" ,
                                        image_normal=self.download_btn_img_normal ,
                                        image_hover=self.download_btn_img_hover ,
                                        image_clicked=self.download_btn_img_clicked ,
                                        width=20, height=30 ,
                                        bg_color=fg_color ,fg_color=fg_color ,
                                        hover_color=fg_color
                                        )
        
      
        self.urlLabel = tkinter.Label(master=self ,anchor="w",
                                      text=self.url ,font=('arial',10) ,
                                      bg=fg_color ,fg=txt_color)
        
        self.remove_btn_img_normal = "src/remove button/normal.png"
        self.remove_btn_img_hover = "src/remove button/normal.png"
        self.remove_btn_img_clicked = "src/remove button/normal.png"
        self.removeBtn = customButton(master=self ,
                                      image_normal=self.remove_btn_img_normal ,
                                      image_hover=self.remove_btn_img_hover ,
                                      image_clicked=self.remove_btn_img_clicked ,
                                      text="" ,bg_color=fg_color ,fg_color=fg_color ,
                                      hover_color=fg_color ,
                                      command=self.kill)
        
        self.reload_btn_img_normal = "src/reload button/normal.png"
        self.reload_btn_img_hover = "src/reload button/hover.png"
        self.reload_btn_img_clicked = "src/reload button/clicked.png"
        self.reloadBtn = customButton(master=self ,
                                      image_normal=self.reload_btn_img_normal ,
                                      image_hover=self.reload_btn_img_hover ,
                                      image_clicked=self.reload_btn_img_clicked ,
                                      text="" ,bg_color=fg_color ,fg_color=fg_color ,
                                      hover_color=fg_color ,
                                      width=20 ,height=20 ,command=self.loading )
        #self.statusLabel = tkinter.Label(master=self ,
        #                                 bg=fg_color)
        
        
        #############################################################################
        #############################################################################
        #############################################################################
        self.thumbnail_btn_loading_frames = [tkinter.PhotoImage(file='src/loading/5.gif',format = 'gif -index %i' %(i)) for i in range(12)]
        self.thumbnail_btn_loading_frames_index = 0
        self.thumbnail_btn_loading_failed_frame = tkinter.PhotoImage(file="src/loading failed/3.png")
        
        #############################################################################
        #############################################################################
        self.thumbnailBtn.place(x=10,y=3)
        self.titleLabel.place(x=150,y=8 ,relwidth=0.93 ,width=-150)
        self.channelLabel.place(x=150 ,y=28 ,relwidth=0.63 ,width=-150)
        self.urlLabel.place(x=150 ,y=48 ,relwidth=0.63 ,width=-150)
        
        self.ResolutionMenu.place(x=-320,y=30 ,relx=1)
        self.downloadBtn.place(x=-150 ,y=30 ,relx=1)
        #self.reloadBtn.place(x=250 ,y=30 ,relx=0.65)
        #self.statusLabel.place(x=300 ,y=30 ,relx=0.65)
        self.loading_success = False
        self.removeBtn.place(relx=1,x=-50,y=27 ,height=25 ,width=25)
        self.loading()
    
    """def set_react(self, fg_color=None):
        self.configure(fg_color=fg_color)
        self.thumbnailBtn.configure(fg_color=fg_color, bg_color=fg_color, hover_color=fg_color)
        self.downloadBtn.configure(bg_color=fg_color ,fg_color=fg_color ,
                                    hover_color=fg_color)
        self.channelLabel.configure(bg=fg_color)
        self.urlLabel.configure(bg=fg_color)
        self.titleLabel.configure(bg=fg_color)
        self.removeBtn.configure(bg_color=fg_color ,fg_color=fg_color ,
                                hover_color=fg_color)"""
        
    def set_theme(self, fg_color=None ,bg_color=None,fg_color_hover=None, text_color=None,text_color_2=None, bd_color=None,bd_color_hover=None):
        self.configure(fg_color=fg_color, bg_color=bg_color, border_color=bd_color)
        self.thumbnailBtn.configure(fg_color=fg_color, bg_color=fg_color, hover_color=fg_color)
        self.downloadBtn.configure(bg_color=fg_color ,fg_color=fg_color ,
                                    hover_color=fg_color)
        self.urlLabel.configure(bg=fg_color, fg=text_color)
        self.removeBtn.configure(bg_color=fg_color ,fg_color=fg_color ,
                                hover_color=fg_color)
        self.channelLabel.configure(bg=fg_color)
        self.titleLabel.configure(bg=fg_color)
        if self.loading_success :
            self.channelLabel.configure(fg=text_color)
            self.titleLabel.configure(fg=text_color)
        else:
            self.channelLabel.configure(fg=text_color_2)
            self.titleLabel.configure(fg=text_color_2)
    
    
        self.fg_color_normal = fg_color
        self.fg_color_hover = fg_color_hover
        self.border_color_normal = bd_color
        self.border_color_hover = bd_color_hover
        
        
    def select_resolution_E(self,e):
        selected = self.ResolutionMenu.get().split("  :  ")
        self.selected_quallity = selected[1].split(" | ")[0].replace(" ","")
        self.ResolutionMenu.set(selected[1].strip(" "))
        self.downloadBtn.set_normal()
    def select_resolution(self):
        self.selected_quallity = self.supported_reso_and_size[0].split("  :  ")[1].split(" | ")[0].replace(" ","")
        self.ResolutionMenu.set(self.supported_reso_and_size[0].split("  :  ")[1].strip(" "))
        self.downloadBtn.set_normal()
        
    def loading(self):
        self.ResolutionMenu.configure(command=PASS_E)
        self.downloadBtn.set_clicked()
        self.reloadBtn.set_clicked()
        
        self.loading_success = False       
        self.thumbnail_loading_success = False 
        self.title_loading_success = False
        self.channel_loading_success = False
        self.loading_failed = False
        self.loading_dot_count = 2
        
        
        self.channelLabel.configure(fg=self.txt_color_2)
        self.titleLabel.configure(fg=self.txt_color_2)
        self.ResolutionMenu.configure(values=["..........","..........",".........."])
        self.ResolutionMenu.set("..........")
        
        self.urlLabel.configure(fg=self.txt_color)
        #self.statusLabel.configure(fg="#ffffff" ,text="Loading...")
        def loop():
            if not(self.thumbnail_loading_success) :
                self.thumbnailBtn.configure(image=self.thumbnail_btn_loading_frames[self.thumbnail_btn_loading_frames_index])
                self.thumbnail_btn_loading_frames_index += 3                
                if self.thumbnail_btn_loading_frames_index == len(self.thumbnail_btn_loading_frames) :
                    self.thumbnail_btn_loading_frames_index = 0
            if not(self.channel_loading_success) :
                self.channelLabel.configure(text="Channel : "+"."*self.loading_dot_count)
            if not(self.title_loading_success):
                self.titleLabel.configure(text="Title : "+"."*self.loading_dot_count)
            self.loading_dot_count += 1
            if self.loading_dot_count > 7:
                self.loading_dot_count = 0
            if not(self.loading_success) and self.alive and not(self.loading_failed):
                self.after(200,loop)
            else:
                if self.loading_failed :
                    self.thumbnailBtn.configure(image=self.thumbnail_btn_loading_failed_frame)
                    self.channelLabel.configure(text="Channel : ..." ,fg=self.txt_color_2)
                    self.urlLabel.configure(fg="#aaaaaa")
                    self.titleLabel.configure(text="Title : ..." ,fg=self.txt_color_2)
                    #self.statusLabel.configure(fg="#505050" ,text="Loading Failed..!")
                else:
                    self.channelLabel.configure(fg=self.txt_color)
                    self.urlLabel.configure(fg=self.txt_color)
                    self.titleLabel.configure(fg=self.txt_color)
                    #self.statusLabel.configure(text="")
                    self.ResolutionMenu.configure(command=self.select_resolution_E)
                    self.select_resolution()
                self.reloadBtn.configure(command=self.loading)
                self.reloadBtn.set_normal()
        loop()
        threading.Thread(target=self.getVideoInfo).start()
        
    def configureInfo(self,title=None,channel=None,thumbnail=None,resolutions=None,length=None):
        if title != None:
            self.titleLabel.configure(text="Title : "+title)
        if channel != None:
            self.channelLabel.configure(text="Channel : "+channel)
        if thumbnail !=None:
            self.thumbnailBtn.configure(image=thumbnail)
        if resolutions != None :
            self.ResolutionMenu.configure(values=resolutions)
        if length != None:
            pass
        
        
    def getVideoInfo(self):
        try:
            self.video = pytube.YouTube(self.url)
            
            self.title = self.video.title
            self.title_loading_success = True
            self.configureInfo(title=self.title)
            
            self.channel = self.video.author
            self.channel_loading_success = True
            self.configureInfo(channel=self.channel)
            
            self.length = self.video.length
            self.length_loading_success = True
            self.configureInfo(length=self.length)
            
            self.video_stream_data  = self.video.streams
            
            def get_download_info()->dict:
                videos_info = []
                download_info = []
                videos_raw_data = self.video_stream_data.all()
                
                pops = ['fps','vcodec','progressive','acodec']
                for info in videos_raw_data:
                    info = str(info)[9:-1]
                    video_data = {key:value[1:-1] for key,value in (x.split("=") for x in info.split())}
                    for pop in pops:
                        try:
                            video_data.pop(pop)
                        except:
                            pass
                    videos_info.append(video_data)
                    
               
                self.audio_size = self.video_stream_data.get_audio_only().filesize
                audio_info = {"itag":int(0) ,"type":"Audio", "ext":".mp3" ,"audio":True, "video":False,  "res":"128kbps", "size":self.audio_size}
            
                        
                            
                supported_resolutions = []    
                for info in videos_info:
                    if info["type"] == "video" :
                        try:
                            size = self.video_stream_data.get_by_resolution(info["res"]).filesize
                            if info["res"] not in supported_resolutions:
                                supported_resolutions.append(info["res"])
                                download_info.append({"itag":int(info["itag"]) ,"type":"Video", "ext":".mp4" ,"audio":True, "video":True, "res":info["res"], "size":size})
                        except:
                            pass
                    
                
                for info in videos_info:
                    if info["type"] == "video" :
                        try:
                            size = self.video_stream_data.get_by_itag(int(info["itag"])).filesize
                            if info["res"] not in supported_resolutions:
                                supported_resolutions.append(info["res"])
                                download_info.append({"itag":int(info["itag"]) ,"type":"Video", "ext":".mp4" ,"audio":False, "video":True, "res":info["res"], "size":size+self.audio_size})
                        except Exception as error:
                            pass
                
                for i in range(len(download_info)-1):
                    swapped = False
                    for j in range(len(download_info)-i-1):
                        if int(download_info[j]["res"][0:-1]) < int(download_info[j+1]["res"][0:-1]):
                            download_info[j],download_info[j+1] = download_info[j+1],download_info[j]
                            swapped = True
                    if not swapped:
                        break
                   
                download_info.append(audio_info)
    
                final_info = {}
                for info in download_info:
                    final_info[info["res"]] = info
                
                return final_info
            
            
            
            def set_download_info():
                self.supported_reso_and_size = []
                for info in self.download_info:
                    self.supported_reso_and_size.append(self.download_info[info]["type"] + "  :  " + fix_len(info,leng=7,side="<-") + " | "+ convertData(self.download_info[info]["size"], with_decimal=True))
                self.configureInfo(resolutions=self.supported_reso_and_size)
            
            
            self.download_info = get_download_info()
            set_download_info()
    
            def getThumbnail():
                self.thumbnail_url = self.video.thumbnail_url
                self.thumbnail_download_path = checkFileName("temp/" + replaceFileName(self.url) + ".png")
                request.urlretrieve(self.thumbnail_url, self.thumbnail_download_path)
                thumbnail_temp = Image.open(self.thumbnail_download_path)
                
                def add_corners(im, rad):
                    circle = Image.new('L', (rad * 2, rad * 2), 0)
                    draw = ImageDraw.Draw(circle)
                    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
                    alpha = Image.new('L', im.size, 255)
                    w, h = im.size
                    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
                    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
                    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
                    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
                    im.putalpha(alpha)
                    return im
                
                thumbnail_temp = thumbnail_temp.resize((128,94),Image.Resampling.LANCZOS).crop((0,12,128,82))
                thumbnail_temp_corner_rounded = add_corners(thumbnail_temp,6)
                thumbnail_temp_corner_rounded.save(self.thumbnail_download_path)
                self.thumbnail = tkinter.PhotoImage(file=self.thumbnail_download_path)
                
                self.thumbnail_hover = " "

                #hover thumbnail
                thumbnail_hover_temp = Image.open(self.thumbnail_download_path)
                thumbnail_hover_path = ".".join(self.thumbnail_download_path.split(".")[0:-1]) + "-hover." + self.thumbnail_download_path.split(".")[-1] 
                thumbnail_hover_temp = thumbnail_hover_temp.convert("RGB")
                thumbnail_hover_data = thumbnail_hover_temp.getdata()
                thumbnail_hover_data_list = []
                for item in thumbnail_hover_data:
                    item = list(item)
                    for index ,i in enumerate(item):
                        if i+30  < 256 :
                            item[index] = i+30
                        else:
                            item[index] = 255
                    thumbnail_hover_data_list.append(tuple(item))
                   
                thumbnail_hover_temp.putdata(thumbnail_hover_data_list)
                #thumbnail_hover_temp.save(thumbnail_hover_path)
                thumbnail_hover_corner_rounded =add_corners(thumbnail_hover_temp,6)
                thumbnail_hover_corner_rounded.save(thumbnail_hover_path)
                self.thumbnail_hover = tkinter.PhotoImage(file = thumbnail_hover_path)
                
                return (self.thumbnail,self.thumbnail_hover)
            
            self.thumbnail,self.thumbnail_hover = getThumbnail()
            self.thumbnail_loading_success = True
            self.configureInfo(thumbnail=self.thumbnail)
            
            def thumbnail_hover_img_set(e):
                self.thumbnailBtn.configure(image=self.thumbnail_hover)
            def thumbnail_img_set(e):
                self.thumbnailBtn.configure(image=self.thumbnail)
                
            self.thumbnailBtn.bind("<Enter>",thumbnail_hover_img_set)
            self.thumbnailBtn.bind("<Leave>",thumbnail_img_set)
            self.loading_success = True
        except :
            self.loading_failed = True
        
    def kill(self):
        self.alive = False
        self.removeBtn.configure(command=PASS)
        self.pack_forget()
        self.added_widgets.remove(self)
        self.main_master.configureWinfo(height=len(self.added_widgets)*(self.height+4))
        del self
        
        
        
        
class copy_paste_menu(customtkinter.CTkFrame):
    def __init__(self, master=None, width=100, height=125, border_width=1,
                 btn_width=90, btn_height=26):
        
        super().__init__(master=master ,width=width, height=height, border_width=border_width)

        def select_all():
            pyautogui.hotkey("ctrl","a")
            #place_info = self.place_info()
            #x = int(place_info["x"])
            #y = int(place_info["y"])
            self.place_forget()
            #self.place(x=x+5,y=y+5)
                        
        def cut():
            pyautogui.hotkey("ctrl","x")
            self.place_forget()
        def copy():
            pyautogui.hotkey("ctrl","c")
            self.place_forget()
        def paste():
            pyautogui.hotkey("ctrl","v")
            self.place_forget()
            
        
        commands = [select_all, cut, copy, paste]
        place_y = [3,34,65,96]
        texts = ["Select All", "Cut", "Copy", "Paste"]
        for i in range(4):
            customtkinter.CTkButton(self, text=texts[i], width=btn_width, height=btn_height, command=commands[i]).place(y=place_y[i], x=5)

        place_y = [31,62,93]
        for i in range(3):
            tkinter.Frame(self, width=80, height=1).place(y=place_y[i], x=10)
            
    
    
    def set_theme(self, fg_color="#252525", text_color="#999999",hover_color="#353535",border_color="#454545",
                 bg_color="#", line_fg="#353535"):
        self.configure(bg_color=bg_color, fg_color=fg_color ,border_color=border_color)
        for widget in self.winfo_children():
            if type(widget) == customtkinter.CTkButton:
                widget.configure(fg_color=fg_color, bg_color=fg_color, hover_color=hover_color, text_color=text_color)
            if type(widget) == tkinter.Frame:
                widget.configure(bg=line_fg)



class credits_menu(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width=1, border_color="Red")
        
        """
        UI Designed By: Soorya
        Programmed By: Thisal
        """
        l11 = customtkinter.CTkLabel(master=self, text="UI Designed By" ,justify="left", width=100)
        l11.grid(row=1, column=1, pady=2, padx=2)
        l12 = customtkinter.CTkLabel(master=self, text=":" ,justify="left", width=5)
        l12.grid(row=1, column=2)
        l13 = customtkinter.CTkLabel(master=self, text="Soorya" ,justify="left", width=60, text_font=("arial",10,"bold"))
        l13.grid(row=1, column=3)
        
        l21 = customtkinter.CTkLabel(master=self, text="Coded By" ,justify="left", width=100)
        l21.grid(row=2, column=1, pady=0)
        l22 = customtkinter.CTkLabel(master=self, text=":" ,justify="left", width=5)
        l22.grid(row=2, column=2)
        l23 = customtkinter.CTkLabel(master=self, text="Thisal" ,justify="left", width=60, text_font=("arial",10,"bold"))
        l23.grid(row=2, column=3)
        self.labels = [l11, l12, l13, l21, l22, l23]
        
        
    def set_theme(self, border_color, fg_color, bg_color, text_color):
        self.configure(border_color=border_color, fg_color=fg_color, bg_color=bg_color)
        for label in self.labels:
            label.configure(fg_color=fg_color, bg_color=fg_color, text_color=text_color)
        
        
        