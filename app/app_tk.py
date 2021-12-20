import tkinter as tk
from mongodb.query_manager import *

HUGE_FONT = ("Verdana", 100)
LARGE_FONT = ("Verdana", 26)
MEDIUM_FONT = ("Verdana", 18)


class ArticleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("800x500")
        self.title('Article App')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, UserPage, ArticlePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def fetch_user(self, uid, list, found_label):
        list.delete(0, tk.END)
        if uid.get() == '':
            query_id = {}
        else:
            uids = uid.get().split(' ')
            query_id = {'uid': {'$in': uids}}
        res = QueryManager.query_user(query_id)

        found_label['text'] = f'Found {len(res)} results.'

        for i in sorted(res, key=lambda x: int(x['uid'])):
            list.insert(tk.END, f'User ID: {i["uid"]}, Name: {i["name"]}, Region: {i["region"]}, Gender: {i["gender"]}')


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Article App", font=HUGE_FONT, fg='blue')
        label.pack(pady=10, padx=10)

        buttons = tk.Frame(self)
        buttons.pack()

        user_button = tk.Button(buttons, text="Users",
                           command=lambda: controller.show_frame(UserPage), font=LARGE_FONT)
        user_button.pack(side=tk.LEFT)

        articles_button = tk.Button(buttons, text="Articles",
                            command=lambda: controller.show_frame(ArticlePage), font=LARGE_FONT)
        articles_button.pack(side=tk.LEFT)


class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Users", font=LARGE_FONT, fg='blue')
        label.pack(pady=10, padx=10)

        top_frame = tk.Frame(self)
        top_frame.pack()

        user_label = tk.Label(top_frame, text='User ID', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)

        user_text = tk.StringVar()
        user_entry = tk.Entry(top_frame, textvariable=user_text)
        user_entry.pack(side=tk.LEFT)

        user_submit = tk.Button(top_frame, text='Submit', fg="grey",
                                command=lambda: controller.fetch_user(user_text, result_list, found_label), pady=5)
        user_submit.pack(side=tk.LEFT)

        found_label = tk.Label(self, text='', font=('bold', 14), padx=20)
        found_label.pack()

        result_list = tk.Listbox(self, height=8, width=50)
        result_list.pack()

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(side=tk.BOTTOM, pady=30)


class ArticlePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Articles", font=LARGE_FONT, fg='blue')
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(UserPage), font=MEDIUM_FONT)
        button2.pack()

if __name__ == '__main__':
    app = ArticleApp()
    app.mainloop()
