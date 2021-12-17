import tkinter as tk
from mongodb.query_manager import *

def fetch_user(uid, list, found_label):
    list.delete(0, tk.END)
    if uid.get() == '':
        query_id = {}
    else:
        query_id = {'uid': uid.get()}
    res = QueryManager.query_user(query_id)

    found_label['text'] = f'Found {len(res)} results.'

    for i in sorted(res, key=lambda x: int(x['uid'])):
        list.insert(tk.END, f'User ID: {i["uid"]}, Name: {i["name"]}, Region: {i["region"]}')

if __name__ == '__main__':
    app = tk.Tk(className='Article App')
    app.title('Article App')
    app.geometry("800x500")

    user_label = tk.Label(app, text='User ID', font=('bold', 14), pady=20, padx=20)
    user_label.grid(row=0, column=0, sticky=tk.W)

    user_text = tk.StringVar()
    user_entry = tk.Entry(app, textvariable=user_text)
    user_entry.grid(row=0, column=1)

    found_label = tk.Label(app, text='', font=('bold', 14), padx=20)
    found_label.grid(row=2, column=0, sticky=tk.W)

    user_submit = tk.Button(app, text='Submit', fg="grey",
                            command=lambda: fetch_user(user_text, result_list, found_label), pady=5)
    user_submit.grid(row=0, column=2)

    result_list = tk.Listbox(app, height=8, width=50)
    result_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

    app.mainloop()