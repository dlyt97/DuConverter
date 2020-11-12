from tkinter import *
import tkinter as tk
import ctypes
from PIL import ImageTk
from moviepy.editor import *
import threading
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter import ttk
import os

import win32gui, win32con



class DuEncoder(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.CODEC = ''

        #self.minimize_console()

        self.controls()
        self.states()
        self.commands()

    def minimize_console(self):
        print('hide console')
        ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )

    def minimize_window(self):
        self.wm_state('iconic')

    def export_file(self):

        if self.CODEC == '':
            if not self.var_cb_codecs.get() == 'libvpx':
                self.extension_EXPORT_FILE = [("MP4 files", "*.mp4"),
                                              ("MOV files", "*.mov"),
                                              ("MKV files", "*.mkv")]
                self.export_path = str(asksaveasfile(
                    filetypes=self.extension_EXPORT_FILE,
                    defaultextension=self.extension_EXPORT_FILE))
            if self.var_cb_codecs.get() == 'libvpx':
                self.extension_EXPORT_FILE = [("WEBM files", "*.webm")]
                self.export_path = str(asksaveasfile(
                    filetypes=self.extension_EXPORT_FILE,
                    defaultextension=self.extension_EXPORT_FILE))

        if not self.CODEC == '':
            self.export_path = str(asksaveasfile(
                    filetypes=self.extension_EXPORT_FILE,
                    defaultextension=self.extension_EXPORT_FILE))

        print(self.export_path)

        self.variable_EXPORT_PATH = ''

        for var in self.export_path.split()[1:-2]:
            string = str(var).replace("name='", "").replace("'", "")

            string = str(string)

            self.variable_EXPORT_PATH = string

        print(self.variable_EXPORT_PATH)

        if not self.variable_EXPORT_PATH == '':

            self.buttons[2]['state'] = 'normal'
            self.buttons[2].update()

            self.buttons[1]['state'] = 'disabled'
            self.buttons[1].update()

            self.labels[1]['text'] = str(os.path.basename(self.variable_EXPORT_PATH))
            self.labels[1].update()
        else:
            print('Nisi izabrao putanju za izvoz video fajla...')

    def import_file(self):
        files = ([("MP4 files", "*.mp4"),
                  ("MOV files", "*.mov"),
                  ("MKV files", "*.mkv"),
                  ("Webm files", "*.webm")])

        self.IMPORT_PATH = askopenfilename(title='Import path?', filetypes=files)

        if not self.IMPORT_PATH == '':
            self.buttons[1]['state'] = 'normal'
            self.buttons[1].update()

            self.buttons[0]['state'] = 'disabled'
            self.buttons[0].update()

            print(self.IMPORT_PATH)

            self.buttons[0]['state'] = 'disabled'
            self.buttons[0].update()

            self.buttons[1]['state'] = 'normal'
            self.buttons[1].update()

            self.labels[0]['text'] = str(os.path.basename(self.IMPORT_PATH))
            self.labels[0].update()

            self.var_input_FPS.set(str(VideoFileClip(self.IMPORT_PATH).fps))  # FPS

            VIDEO_FILE_SIZE = int((float(os.path.getsize(self.IMPORT_PATH) / pow(1024, 1)) * 8) / VideoFileClip(self.IMPORT_PATH).duration)
            self.var_input_Bitrate.set(str(VIDEO_FILE_SIZE))

            self.input_FPS['state'] = 'normal'
            self.input_FPS.update()

            self.cbox_codecs['state'] = 'normal'
            self.cbox_codecs.update()

            self.input_Bitrate['state'] = 'normal'
            self.input_Bitrate.update()

            self.cbox_audio_fps['state'] = 'normal'
            self.cbox_audio_fps.update()

            self.cbox_audio_Bitrate['state'] = 'normal'
            self.cbox_audio_Bitrate.update()

            # self.cb_log_file['state'] = 'normal'
            # self.cb_log_file.update()

            # Source info -> LabelFrame
            self.source_info()
        else:
            print('Nisi uvezao video fajl...')

    def encoder_Thread(self):
        threadObj = threading.Thread(target=lambda: self.encoder())
        threadObj.start()

    def encoder(self):
        self.buttons[2]['state'] = 'disabled'
        self.buttons[2].update()

        def disabled_state_Settings_tab():
            self.input_FPS['state'] = 'disabled'
            self.input_FPS.update()
            self.cbox_codecs['state'] = 'disabled'
            self.cbox_codecs.update()
            self.input_Bitrate['state'] = 'disabled'
            self.input_Bitrate.update()
            self.cbox_audio_fps['state'] = 'disabled'
            self.cbox_audio_fps.update()
            self.cbox_audio_Bitrate['state'] = 'disabled'
            self.cbox_audio_Bitrate.update()
            self.cb_log_file['state'] = 'disabled'
            self.cb_log_file.update()
        disabled_state_Settings_tab()

        try:
            self.clip = VideoFileClip(self.IMPORT_PATH, audio=True)
        except:
            print('Video ne moze da ucita !!!')

        print('FPS', self.var_input_FPS.get())
        print('CODEC', self.var_cb_codecs.get())
        print('Bitrate', self.var_input_Bitrate.get())
        print('Audio fps', self.var_cb_audio_fps.get())
        print('Audio bitrate', self.var_cb_audio_Bitrate.get())
        print('Log file', self.var_cb_log_file.get())

        self.FILE = ''
        self.FOLDER = ''
        self.FULL_PATH = ''
        self.CODEC = ''

        if self.var_cb_codecs.get() == 'mpeg4':
            self.CODEC = 'mpeg4'
            self.FILE = os.path.basename(self.variable_EXPORT_PATH).\
                replace('.webm', '.mp4')
            self.FOLDER = os.path.dirname(self.variable_EXPORT_PATH)
            self.FULL_PATH = self.FOLDER + '/' + self.FILE
        if self.var_cb_codecs.get() == 'libx264':
            self.CODEC = 'libx264'
            self.FILE = os.path.basename(self.variable_EXPORT_PATH).\
                replace('.webm', '.mp4')
            self.FOLDER = os.path.dirname(self.variable_EXPORT_PATH)
            self.FULL_PATH = self.FOLDER + '/' + self.FILE
        if self.var_cb_codecs.get() == 'nvenc_h264':
            self.CODEC = 'nvenc_h264'
            self.FILE = os.path.basename(self.variable_EXPORT_PATH).\
                replace('.webm', '.mp4')
            self.FOLDER = os.path.dirname(self.variable_EXPORT_PATH)
            self.FULL_PATH = self.FOLDER + '/' + self.FILE
        if self.var_cb_codecs.get() == 'hevc':
            self.CODEC = 'hevc'
            self.FILE = os.path.basename(self.variable_EXPORT_PATH).\
                replace('.webm', '.mp4')
            self.FOLDER = os.path.dirname(self.variable_EXPORT_PATH)
            self.FULL_PATH = self.FOLDER + '/' + self.FILE
        if self.var_cb_codecs.get() == 'hevc_nvenc':
            self.CODEC = 'hevc_nvenc'
            self.FILE = os.path.basename(self.variable_EXPORT_PATH).\
                replace('.webm', '.mp4')
            self.FOLDER = os.path.dirname(self.variable_EXPORT_PATH)
            self.FULL_PATH = self.FOLDER + '/' + self.FILE
        if self.var_cb_codecs.get() == 'libvpx':
            self.CODEC = 'libvpx'
            self.FILE = os.path.basename(self.variable_EXPORT_PATH).\
                replace('.mov', '.webm').\
                replace('.mkv', '.webm').\
                replace('.mp4', '.webm')
            self.FOLDER = os.path.dirname(self.variable_EXPORT_PATH)
            self.FULL_PATH = self.FOLDER + '/' + self.FILE

        print('FULL PATH', self.FULL_PATH)
        print('CODEC', self.CODEC)

        try:
            #self.destroy()  # zatvara prozor kada se konvertuje video...

            #self.minimize_window()
            
            log_file = bool(self.var_cb_log_file.get())

            self.clip.subclip(0, int(self.clip.duration)).write_videofile(
                str(self.FULL_PATH),
                fps=int(float(self.var_input_FPS.get())),
                codec=str(self.CODEC),
                bitrate=str(self.var_input_Bitrate.get())+'k',
                audio_fps=int(self.var_cb_audio_fps.get()),
                audio_bitrate=str(self.var_cb_audio_Bitrate.get())+'k',
                write_logfile=True)
        except:
            print(f'Ne moze da konvertuje {os.path.basename(self.variable_EXPORT_PATH)} fajl')

    def states(self):
        for x in range(1, 3):
            self.buttons[x]['state'] = 'disabled'
            self.buttons[x].update()

        self.input_FPS['state'] = 'disabled'
        self.input_FPS.update()

        self.cbox_codecs['state'] = 'disabled'
        self.cbox_codecs.update()

        self.input_Bitrate['state'] = 'disabled'
        self.input_Bitrate.update()

        self.cbox_audio_fps['state'] = 'disabled'
        self.cbox_audio_fps.update()

        self.cbox_audio_Bitrate['state'] = 'disabled'
        self.cbox_audio_Bitrate.update()

        self.cb_log_file['state'] = 'disabled'
        self.cb_log_file.update()

    def commands(self):
        print('commands')

        self.buttons[0]['command'] = lambda: self.import_file()
        self.buttons[1]['command'] = lambda: self.export_file()
        self.buttons[2]['command'] = lambda: self.encoder_Thread()

        # Izbor trenutno kodeka
        self.choose_item_from_cbox_CODEC()

        # Izbor trenutno audia u Hz-ima
        self.choose_item_from_cbox_Audio_FPS()

        self.cb_log_file['command'] = lambda: self.on_off_write_log_file()

    def controls(self):
        print('controls')

        self.FONT = ('Calibri', 15, 'bold')
        self.BG_COLOR = 'steel blue'
        self.FG_COLOR = 'white'
        self.WIDTH = 16
        self.PAD_X = 10
        self.PAD_Y = 5


        self.tabControl = ttk.Notebook(self)  # Create Tab Control

        self.tab_Media = ttk.Frame(self.tabControl)  # Create a tab

        self.tabControl.add(self.tab_Media, text="Media")  # use the tk constants
        self.tabControl.pack(fill='both', expand=True)  # Pack to make visible

        self.media_FRAME = Frame(self.tab_Media)
        self.media_FRAME.pack(expand=0, fill="both")  # Pack to make visible

        self.buttons = []
        self.btn_names = ['Import', 'Export', 'Start']
        self.labels = []

        for x in range(3):
            button = Button(self.media_FRAME, text='')
            button['font'] = self.FONT
            button['bg'] = self.BG_COLOR
            button['fg'] = self.FG_COLOR
            button['width'] = self.WIDTH
            button['text'] = self.btn_names[x]
            button.grid(row=x, column=0, padx=self.PAD_X, pady=self.PAD_Y)
            self.buttons.append(button)

            if not x == 2:
                label = Label(self.media_FRAME, text='')
                label['font'] = self.FONT
                #label['bg'] = 'gray24'
                label['fg'] = 'black'
                label['width'] = self.WIDTH
                label.grid(row=x, column=1, padx=self.PAD_X, pady=self.PAD_Y)
                self.labels.append(label)

        self.tab_video_Settings = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.tab_video_Settings, text='Settings')  # Add the tab
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible

        self.labels_tabSettings = []
        self.lbl_Settings_names = ['FPS', 'Codec', 'Bitrate(Kbps)', 'Audio FPS(Hz)',
                                   'Audio bitrate(Kbps)', 'Write log file']
        self.box_tabSettings = []

        for x in range(6):
            label = Label(self.tab_video_Settings)
            label['font'] = self.FONT
            label['bg'] = self.BG_COLOR
            label['fg'] = self.FG_COLOR
            label['width'] = self.WIDTH
            label['text'] = str(self.lbl_Settings_names[x])
            label.grid(row=x, column=0, padx=self.PAD_X, pady=self.PAD_Y)
            self.labels_tabSettings.append(label)

        self.var_input_FPS = StringVar()
        self.input_FPS = Entry(self.tab_video_Settings,
                               width=self.WIDTH,
                               textvariable=self.var_input_FPS,
                               font=self.FONT,
                               bg=self.BG_COLOR,
                               fg=self.FG_COLOR)
        self.input_FPS.grid(row=0, column=1, padx=self.PAD_X, pady=self.PAD_Y)

        self.var_cb_codecs = StringVar()
        self.cbox_codecs = ttk.Combobox(
            self.tab_video_Settings,
            width=self.WIDTH, font=self.FONT,
            textvariable=self.var_cb_codecs
        )

        # Adding combobox drop down list
        self.cbox_codecs['values'] = ('mpeg4',
                                      'libx264',
                                      'nvenc_h264',
                                      'hevc',
                                      'hevc_nvenc',
                                      'libvpx')

        self.cbox_codecs.grid(row=1, column=1, padx=self.PAD_X, pady=self.PAD_Y)
        self.cbox_codecs.current([1])

        self.var_input_Bitrate = StringVar()
        self.input_Bitrate = Entry(self.tab_video_Settings,
                               width=self.WIDTH,
                               textvariable=self.var_input_Bitrate,
                               font=self.FONT,
                               bg=self.BG_COLOR,
                               fg=self.FG_COLOR)
        self.input_Bitrate.grid(row=2, column=1, padx=self.PAD_X, pady=self.PAD_Y)


        self.var_cb_audio_fps = StringVar()
        self.cbox_audio_fps = ttk.Combobox(
            self.tab_video_Settings,
            width=self.WIDTH, font=self.FONT,
            textvariable=self.var_cb_audio_fps
        )

        # Adding combobox drop down list
        self.cbox_audio_fps['values'] = (22000,
                                      44100,
                                      48000)

        self.cbox_audio_fps.grid(row=3, column=1, padx=self.PAD_X, pady=self.PAD_Y)
        self.cbox_audio_fps.current(2)

        self.var_cb_audio_Bitrate= StringVar()
        self.cbox_audio_Bitrate = ttk.Combobox(
            self.tab_video_Settings,
            width=self.WIDTH, font=self.FONT,
            textvariable=self.var_cb_audio_Bitrate
        )

        # Adding combobox drop down list
        self.cbox_audio_Bitrate['values'] = (128, 160, 192, 256, 320, 384)

        self.cbox_audio_Bitrate.grid(row=4, column=1, padx=self.PAD_X, pady=self.PAD_Y)
        self.cbox_audio_Bitrate.current(2)

        self.var_cb_log_file = BooleanVar()
        self.cb_log_file = Checkbutton(self.tab_video_Settings,
                                       text='Log file',
                                       var=self.var_cb_log_file,
                                       font=self.FONT,
                                       width=self.WIDTH)
        self.cb_log_file.grid(row=5, column=1, padx=self.PAD_X, pady=self.PAD_Y)

        self.lf_source_file = LabelFrame(self.tab_Media, text="Source:", width=200, height=200)
        self.lf_source_file['font'] = self.FONT
        self.lf_source_file['bg'] = 'steel blue'
        self.lf_source_file['fg'] = 'white'
        self.lf_source_file.pack(expand=1, fill="both")

        source_frame_FONT = ('Arial', 15, 'bold')

        self.lbl_video_name = Label(self.tab_Media, text='Source: ')
        self.lbl_video_name['font'] = source_frame_FONT
        self.lbl_video_name.place(in_=self.lf_source_file, x=5, y=5)

        self.lbl_res_video = Label(self.tab_Media, text='Resolution: ')
        self.lbl_res_video['font'] = source_frame_FONT
        self.lbl_res_video.place(in_=self.lf_source_file, x=5, y=45)

        self.lbl_fps_video = Label(self.tab_Media, text='FPS: ')
        self.lbl_fps_video['font'] = source_frame_FONT
        self.lbl_fps_video.place(in_=self.lf_source_file, x=5, y=90)

        self.lbl_duration_video = Label(self.tab_Media, text='Duration: ')
        self.lbl_duration_video['font'] = source_frame_FONT
        self.lbl_duration_video.place(in_=self.lf_source_file, x=5, y=140)

        self.lbl_fileSize = Label(self.tab_Media, text='File size: ')
        self.lbl_fileSize['font'] = source_frame_FONT
        self.lbl_fileSize.place(in_=self.lf_source_file, x=5, y=190)

    def source_info(self):
        print('source info')

        # Source ->  Video name
        self.lbl_video_name['text'] = 'Source: ' + os.path.basename(self.IMPORT_PATH)
        self.lbl_video_name.update()

        # Source -> Video resolution
        width = VideoFileClip(self.IMPORT_PATH).size[0]
        height = VideoFileClip(self.IMPORT_PATH).size[1]
        self.lbl_res_video['text'] = 'Resolution: ' + str(str(width)+'x'+str(height))
        self.lbl_res_video.update()

        # Source -> Video FPS
        self.lbl_fps_video['text'] = 'FPS: ' + str(VideoFileClip(self.IMPORT_PATH).fps)
        self.lbl_fps_video.update()

        # Source -> Video duration
        def video_duration():
            v_duration = VideoFileClip(self.IMPORT_PATH).duration
            self.lbl_duration_video['text'] = 'Duration:  {0} seconds'.format(v_duration)
            self.lbl_duration_video.update()
        video_duration()

        # Source file size
        def file_size():
            F_SIZE = os.path.getsize(self.IMPORT_PATH)

            BYTES_TO_MEGABYTES = float(F_SIZE / pow(1024, 2))

            ROUND_NUMBER = round(BYTES_TO_MEGABYTES, 3)

            F_SIZE = str(ROUND_NUMBER) + 'MB'

            self.lbl_fileSize['text'] = 'File size: ' + F_SIZE
            self.lbl_fileSize.update()
        file_size()

    def choose_item_from_cbox_Audio_FPS(self):
        def choose_Item(eventObject):
            self.CURRENT_AUDIO_FPS = eventObject.widget.get()
            print(self.CURRENT_AUDIO_FPS)

        self.cbox_audio_fps.bind("<<ComboboxSelected>>", choose_Item)

    def choose_item_from_cbox_CODEC(self):

        self.extension_EXPORT_FILE = ''
        self.CURRENT_CODEC = ''

        def choose_Item(eventObject):
            self.CURRENT_CODEC = eventObject.widget.get()
            print(self.CURRENT_CODEC)

            if not self.CURRENT_CODEC == 'libvpx':
                self.extension_EXPORT_FILE = [("MP4 files", "*.mp4"),
                                              ("MOV files", "*.mov"),
                                              ("MKV files", "*.mkv")]
            if self.CURRENT_CODEC == 'libvpx':
                self.extension_EXPORT_FILE = [("WEBM files", "*.webm")]

        self.cbox_codecs.bind("<<ComboboxSelected>>", choose_Item)

    def choose_audio_bitrate(self):
        print('Audio bitrate')
        def choose_Item(eventObject):
            self.CURRENT_AUDIO_BITRATE = eventObject.widget.get()
            print(self.CURRENT_AUDIO_BITRATE)

        self.cbox_audio_Bitrates.bind("<<ComboboxSelected>>", choose_Item)

    def on_off_write_log_file(self):
        self.var_cb_log_file.set(True)
        
        self.var_cb_log_file['state'] = 'disabled'
        self.var_cb_log_file.update()
    
        variable = self.var_cb_log_file.get()
        print(variable)

        if variable == True:
            self.var_cb_log_file.set(True)
        if variable == False:
            self.var_cb_log_file.set(False)

def gui():
    app = DuEncoder()
    
    try:
        app.title('DuConverter')
    except:
        print('Error','title method')
        
    try:
        app.iconbitmap(r'DuEncoder_icon.ico')
    except:
        print('Error','iconbitmap method')
        
    try:
        app.resizable(False, False)
    except:
        print('Error','resizable method')
        
    try:
        app.geometry('400x450')
    except:
        print('Error','geometry method')
        
    try:
        app.configure(bg="gray24")
    except:
        print('Error','configure method')
        
    app.mainloop()
gui()
