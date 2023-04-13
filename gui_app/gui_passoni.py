import os
import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import ttk
from SEB.modules.ics_taker_module.ics_function import ics_taker

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title('SUPSI easy browsing')
        self.geometry(f"{1100}x{580}")

        # main page
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets left
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Custom Links",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.start_app, text="WhatsApp")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.open_link(
            "https://mail.google.com/mail/u/0/#inbox"), text="Gmail")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,
                                                        command=lambda: self.open_link("https://chat.openai.com/chat"),
                                                        text="ChatGPT")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame,
                                                        command=lambda: self.open_link(
                                                            "https://www.icorsi.ch/login/index.php"),
                                                        text="iCorsi")
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame,
                                                        command=lambda: self.open_link(
                                                            "https://portalestudenti.supsi.ch/Account/Login?ReturnUrl=%2FHome%2FIndex"),
                                                        text="Portale Studenti")
        self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame,
                                                        command=lambda: self.open_link(
                                                            "https://webmail.ti-edu.ch/hpronto/"),
                                                        text="Pronto!")

        '''
        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=1, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=1, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=1, pady=20, padx=20, sticky="n")

        # set default values
        # self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        '''

        # Login Page
        self.cover = customtkinter.CTkFrame(master=self, width=1100, height=580, corner_radius=15)
        self.cover.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.frame = customtkinter.CTkFrame(master=self.cover, width=320, height=280, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.log_title = customtkinter.CTkLabel(master=self.frame, text='Login into your SUPSI account',
                                                font=('Century Gothic', 20))
        self.log_title.place(x=20, y=40)

        self.usr_entry = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Username')
        self.usr_entry.place(x=50, y=100)

        self.psw_entry = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Password', show='*')
        self.psw_entry.place(x=50, y=150)

        self.button = customtkinter.CTkButton(master=self.frame, width=220, text='Login', corner_radius=6,
                                              command=self.button_function)
        self.button.place(x=50, y=230)




    def table_creator(self, calendar):
        # table creation
        table_frame = tkinter.Frame(self)
        table_frame.grid(row=2, column=1, sticky="nsew")

        table = ttk.Treeview(table_frame)
        table['columns'] = ('subject', 'date', 'description', 'progress')

        # creation of columns
        width = 200
        table.column("#0", width=0)
        table.column('subject', width=width, anchor='center')
        table.column('date', width=width, anchor='center')
        table.column('description', width=width, anchor='center')
        table.column('progress', width=width, anchor='center')

        # creation of headings
        table.heading('subject', text='subject', anchor='center')
        table.heading('date', text='date', anchor='center')
        table.heading('description', text='description', anchor='center')
        table.heading('progress', text='progress', anchor='center')

        for idx, event in enumerate(calendar.events):
            # inserting data
            table.insert(parent='', index='end', iid=idx, text='',
                         values=(f'{event.name}', f'{event.begin}', f'{event.description}', 'started'))

        table.pack()
    def button_function(self):
        calendar = ics_taker(f'{self.usr_entry.get()}', f'{self.psw_entry.get()}')
        self.table_creator(calendar)
        self.frame.destroy()
        self.cover.destroy()

    def open_link(self, link):
        os.system(f"start {link}")

    def start_app(self):
        os.system("explorer.exe shell:appsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


def main_page_starter():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main_page_starter()
