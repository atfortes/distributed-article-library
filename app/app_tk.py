import tkinter as tk
from mongodb.query_manager import *
from mongodb.collection import *

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

        self.pages = (
            StartPage,
            UserPage,
            CreateUserPage,
            ArticlePage,
            ReadPage
        )

        for F in self.pages:
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
            uids = uid.get().split(',')
            query_id = {'uid': {'$in': uids}}
        res = QueryManager.query_user(query_id)

        if len(res) == 1:
            found_label['text'] = f'Found 1 result.'
        else:
            found_label['text'] = f'Found {len(res)} results.'

        for i in sorted(res, key=lambda x: int(x['uid'])):
            list.insert(tk.END, f'User ID: {i["uid"]}, Name: {i["name"]}, Region: {i["region"]}, Gender: {i["gender"]}')

    def create_user(self, tkVars):
        QueryManager.insert_user({
            'id': f'u{tkVars[0]}',
            'timestamp': Collection.get_current_timestamp(),
            'uid': tkVars[0],
            'name': tkVars[1],
            'gender': tkVars[2],
            'email': tkVars[3],
            'phone': tkVars[4],
            'dept': tkVars[5],
            'grade': tkVars[6],
            'language': tkVars[7],
            'region': tkVars[8],
            'role': tkVars[9],
            'preferTags': tkVars[10],
            'obtainedCredits': tkVars[11]
        })


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

        read_button = tk.Button(buttons, text="Reads",
                                command=lambda: controller.show_frame(ReadPage), font=LARGE_FONT)
        read_button.pack(side=tk.LEFT)


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

        user_submit = tk.Button(top_frame, text='Submit',
                                command=lambda: controller.fetch_user(user_text, result_list, found_label),
                                pady=5, padx=20)
        user_submit.pack(side=tk.LEFT)

        found_label = tk.Label(self, text='', font=('bold', 14), padx=20)
        found_label.pack()

        result_list = tk.Listbox(self, height=8, width=50)
        result_list.pack()

        buttons = tk.Frame(self)
        buttons.pack(pady=10)

        create_user_button = tk.Button(buttons, text="Create user",
                           command=lambda: controller.show_frame(CreateUserPage))
        create_user_button.pack(side=tk.LEFT)

        edit_user_button = tk.Button(buttons, text="Edit user",
                            command=lambda: controller.show_frame(ArticlePage))
        edit_user_button.pack(side=tk.LEFT)

        delete_user_button = tk.Button(buttons, text="Delete user",
                            command=lambda: controller.show_frame(ArticlePage))
        delete_user_button.pack(side=tk.LEFT)

        back_button = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        back_button.pack(side=tk.BOTTOM, pady=30)


class CreateUserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Create User", font=LARGE_FONT, fg='blue')
        label.pack(pady=10, padx=10)

        tkVars = []

        frame = tk.Frame(self)
        frame.pack()
        user_label = tk.Label(frame, text='User ID', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        uid = tk.StringVar()
        tkVars += [uid]
        user_entry = tk.Entry(frame, textvariable=uid)
        user_entry.pack(side=tk.LEFT)

        user_label = tk.Label(frame, text='Name', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        name = tk.StringVar()
        tkVars += [name]
        user_entry = tk.Entry(frame, textvariable=name)
        user_entry.pack(side=tk.RIGHT)

        frame = tk.Frame(self)
        frame.pack()
        user_label = tk.Label(frame, text='Gender', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        gender = tk.StringVar()
        tkVars += [gender]
        user_entry = tk.Entry(frame, textvariable=gender)
        user_entry.pack(side=tk.LEFT)

        user_label = tk.Label(frame, text='Email', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        email = tk.StringVar()
        tkVars += [email]
        user_entry = tk.Entry(frame, textvariable=email)
        user_entry.pack(side=tk.RIGHT)

        frame = tk.Frame(self)
        frame.pack()
        user_label = tk.Label(frame, text='Phone', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        phone = tk.StringVar()
        tkVars += [phone]
        user_entry = tk.Entry(frame, textvariable=phone)
        user_entry.pack(side=tk.LEFT)

        user_label = tk.Label(frame, text='Department', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        dept = tk.StringVar()
        tkVars += [dept]
        user_entry = tk.Entry(frame, textvariable=dept)
        user_entry.pack(side=tk.RIGHT)

        frame = tk.Frame(self)
        frame.pack()
        user_label = tk.Label(frame, text='Grade', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        grade = tk.StringVar()
        tkVars += [grade]
        user_entry = tk.Entry(frame, textvariable=grade)
        user_entry.pack(side=tk.LEFT)

        user_label = tk.Label(frame, text='Language', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        language = tk.StringVar()
        tkVars += [language]
        user_entry = tk.Entry(frame, textvariable=language)
        user_entry.pack(side=tk.RIGHT)

        frame = tk.Frame(self)
        frame.pack()
        user_label = tk.Label(frame, text='Region', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        region = tk.StringVar()
        tkVars += [region]
        user_entry = tk.Entry(frame, textvariable=region)
        user_entry.pack(side=tk.LEFT)

        user_label = tk.Label(frame, text='Role', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        role = tk.StringVar()
        tkVars += [role]
        user_entry = tk.Entry(frame, textvariable=role)
        user_entry.pack(side=tk.RIGHT)

        frame = tk.Frame(self)
        frame.pack()
        user_label = tk.Label(frame, text='Tags', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        tags = tk.StringVar()
        tkVars += [tags]
        user_entry = tk.Entry(frame, textvariable=tags)
        user_entry.pack(side=tk.LEFT)

        user_label = tk.Label(frame, text='Credits', font=('bold', 14), pady=20, padx=20)
        user_label.pack(side=tk.LEFT)
        credits = tk.StringVar()
        tkVars += [credits]
        user_entry = tk.Entry(frame, textvariable=credits)
        user_entry.pack(side=tk.RIGHT)

        user_submit = tk.Button(self, text='Submit',
                                command=lambda: controller.create_user(list(map(lambda x: x.get(), tkVars))),
                                pady=5, padx=20)
        user_submit.pack()

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()


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


class ReadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Reads", font=LARGE_FONT, fg='blue')
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
