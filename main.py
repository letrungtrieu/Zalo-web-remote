import tkinter as tk
from tkinter import ttk, messagebox
from util import *
from zalo import Zalo

ZALO_THREAD:list[Zalo] = []

def show_actions_window(id):
    item = tree.item(id)
    action_window = tk.Toplevel(root)
    action_window.title("Actions")

    # Thiết lập kích thước cho cửa sổ phụ
    action_window_width = 300
    action_window_height = 350

    # Lấy kích thước và vị trí của cửa sổ chính
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    # Tính vị trí để cửa sổ phụ nằm giữa cửa sổ chính
    x = root_x + (root_width - action_window_width) // 2
    y = root_y + (root_height - action_window_height) // 2

    action_window.geometry(f"{action_window_width}x{action_window_height}+{x}+{y}")

    # Frame cho các nút
    button_frame = tk.Frame(action_window)
    button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    tk.Button(button_frame, text="Start", command=lambda: start_action(action_window,id)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Stop", command=lambda: stop_action(action_window,item)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete", command=lambda: delete_action(action_window,id)).pack(side=tk.LEFT, padx=5)

    # Frame cho các trường nhập liệu
    input_frame = tk.Frame(action_window)
    input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # Group Name
    tk.Label(input_frame, text="Group Name").pack(side=tk.TOP, fill=tk.X)
    group_name_entry = tk.Entry(input_frame)
    group_name_entry.pack(side=tk.TOP, fill=tk.X)
    group_name_entry.insert(0, item['values'][0])

    # Member Start ID
    tk.Label(input_frame, text="Member Start ID").pack(side=tk.TOP, fill=tk.X)
    member_start_id_entry = tk.Entry(input_frame)
    member_start_id_entry.pack(side=tk.TOP, fill=tk.X)
    member_start_id_entry.insert(0, item['values'][1])

    # Member End ID
    tk.Label(input_frame, text="Member End ID").pack(side=tk.TOP, fill=tk.X)
    member_end_id_entry = tk.Entry(input_frame)
    member_end_id_entry.pack(side=tk.TOP, fill=tk.X)
    member_end_id_entry.insert(0, item['values'][2])

    # Message
    tk.Label(input_frame, text="Message").pack(side=tk.TOP, fill=tk.X)
    message_entry = tk.Entry(input_frame)
    message_entry.pack(side=tk.TOP, fill=tk.X)
    message_entry.insert(0, item['values'][3])

    # Sleep
    tk.Label(input_frame, text="Sleep").pack(side=tk.TOP, fill=tk.X)
    sleep_entry = tk.Entry(input_frame)
    sleep_entry.pack(side=tk.TOP, fill=tk.X)
    sleep_entry.insert(0, item['values'][4])
    
    # Profile
    tk.Label(input_frame, text="Profile").pack(side=tk.TOP, fill=tk.X)
    profile_entry = tk.Entry(input_frame)
    profile_entry.pack(side=tk.TOP, fill=tk.X)
    profile_entry.insert(0, item['values'][5])

    # Nút Lưu (nếu cần)
    save_button = tk.Button(action_window, text="Save", command=lambda: save_action(action_window, id, group_name_entry.get(), member_start_id_entry.get(), member_end_id_entry.get(), message_entry.get(), sleep_entry.get(), profile_entry.get()))
    save_button.pack(side=tk.BOTTOM, pady=10)

def get_zalo(item)->Zalo:
    for zalo in ZALO_THREAD:
        if zalo.profile == item['values'][5]:
            return zalo

def start_action(action_window:tk.Toplevel, item_id):
    # Implement start action
    item = tree.item(item_id)
    zalo:Zalo = get_zalo(item)
    ZALO_THREAD.remove(zalo)
    zalo = Zalo(tree, item_id,*item['values'])
    ZALO_THREAD.append(zalo)
    zalo.start()
    if action_window:
        action_window.destroy()
    print(f"Start Action for {item['values']}")

def stop_action(action_window:tk.Toplevel, item):
    # Implement stop action
    zalo:Zalo = get_zalo(item)
    if zalo is not None:
        zalo.stop()
        ZALO_THREAD.remove(zalo)
    action_window.destroy()
    print(f"Stop Action for {item['values']}")

def delete_action(action_window:tk.Toplevel, id):
    # Implement delete action
    item = tree.item(id)
    stop_action(action_window, item)
    tree.delete(id)
    save_config(tree)
    action_window.destroy()
    print(f"Delete Action for {item['values']}")

def save_action(action_window:tk.Toplevel, id, group_name, member_start_id, member_end_id, message, sleep, profile):
    item = tree.item(id)
    if item['values'][5] != profile and get_zalo(item):
        messagebox.showerror("Profile conflict","Profile đã được sử dụng")
        action_window.destroy()
        return
    tree.item(id, values=(group_name, member_start_id, member_end_id, message, sleep, profile))
    action_window.destroy()
    save_config(tree)


def add_item():
    id = tree.insert('', tk.END, values=('', 0, 0, '', 120, ''))
    show_actions_window(id)

def start_all():
    for item_id in tree.get_children():
        start_action(None,item_id)

def stop_all():
    for v in ZALO_THREAD:
        v.stop()
        ZALO_THREAD.remove(v)

def create_ui():
    global root, tree
    root = tk.Tk()
    root.title("Zalo Automation")
    root.geometry("640x480")

    style = ttk.Style(root)
    style.theme_use("default")

    style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'), background="#D3D3D3", foreground='black')
    style.configure("Treeview", font=('Calibri', 10), background="#D3D3D3", foreground='black')

    tree = ttk.Treeview(root, columns=('GroupName', 'MemberStartID', 'MemberEndID', 'Message', 'Sleep', 'Profile'), show='headings')
    tree.heading('GroupName', text='Group Name')
    tree.heading('MemberStartID', text='Start ID')
    tree.heading('MemberEndID', text='End ID')
    tree.heading('Message', text='Message')
    tree.heading('Sleep', text='Sleep')
    tree.heading('Profile', text='Profile')
    

    tree.column('GroupName', width=120, stretch=tk.YES, anchor='center')
    tree.column('MemberStartID', width=90, stretch=tk.YES, anchor='center')
    tree.column('MemberEndID', width=90, stretch=tk.YES, anchor='center')
    tree.column('Message', width=150, stretch=tk.YES, anchor='center')
    tree.column('Sleep', width=80, stretch=tk.YES, anchor='center')
    tree.column('Profile', width=120, stretch=tk.YES, anchor='center')

    config = read_config()
    for profile, details in config.items():
        item_id = tree.insert('', tk.END, values=(details['group_name'], details['member_start_id'], details['member_end_id'], details['msg'], details['sleep'], details['profile']))
        ZALO_THREAD.append(Zalo(tree, item_id, **details))


    tree.bind('<<TreeviewSelect>>', lambda event: show_actions_window(tree.selection()[0]))
    tree.pack(expand=True, fill='both')

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
    
    add_button = tk.Button(button_frame, text="ADD", command=add_item)  # Cần thực hiện chức năng thêm mới
    add_button.pack(side=tk.TOP, fill=tk.X)
    
    start_all_button = tk.Button(button_frame, text="START ALL", command=start_all)  # Cần thực hiện chức năng thêm mới
    start_all_button.pack(side=tk.TOP, fill=tk.X)
    
    stop_all_button = tk.Button(button_frame, text="STOP ALL", command=stop_all)  # Cần thực hiện chức năng thêm mới
    stop_all_button.pack(side=tk.TOP, fill=tk.X)

    root.mainloop()

if __name__ == '__main__':
    create_ui()
