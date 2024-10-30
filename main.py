"""
Project: "https:www.github.com/gamingoninuslin/PixARKServerManager",
Author(s): ["GamingOnInsulin"],
Description: "This is simple PixARK Server Manager that allows the user easly set the server settings like ports and world map and other sever related settings.",
Version: V1.0.0a,
License: MIT (https://opensource.org/license/mit)
"""
import tkinter as tk
from tkinter import ttk, filedialog
import threading
import subprocess
import os
import queue


class PixArkServerManager:
    def __init__(self, root):
        self.root = root
        self.root.title("PixArk Server Manager")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.icon_path = "./PixARK.ico"
        root.iconbitmap(self.icon_path)
                
    # Server Path and Status
        self.server_path_frame = ttk.Frame(root)
        self.server_path_frame.pack(fill="x", padx=10, pady=10)

        self.server_path_label = ttk.Label(self.server_path_frame, text="Server Path:")
        self.server_path_label.pack(side="left")

        self.server_path_entry = ttk.Entry(self.server_path_frame)
        self.server_path_entry.pack(side="left", fill="x", expand=True)

        self.server_path_button = ttk.Button(self.server_path_frame, text="Set Location", command=self.set_server_path)
        self.server_path_button.pack(side="left")

        self.server_status_label = ttk.Label(self.server_path_frame, text="Server Status: Not Running")
        self.server_status_label.pack(side="left", padx=10)

        # Server Control Buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(fill="x", padx=10, pady=10)

        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start_server)
        self.start_button.pack(side="left")

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_server)
        self.stop_button.pack(side="left")
    
        self.restart_button = ttk.Button(self.button_frame, text="Restart", command=self.restart_server)
        self.restart_button.pack(side="left")

    # Administration Tab
        self.admin_tab = ttk.Notebook(root)
        self.admin_tab.pack(fill="both", expand=True, padx=10, pady=10)

        self.admin_page = ttk.Frame(self.admin_tab)
        self.admin_tab.add(self.admin_page, text="Server Settings")
        
        divider_frame = ttk.Frame(self.admin_page, height=60)
        divider_frame.grid(row=0, column=0, columnspan=2, sticky="ew")  # Adjust row as needed

    
    # server name    
        server_name_label = ttk.Label(self.admin_page, text="Server Name:")
        server_name_label.grid(row=1, column=0, sticky="w", padx=80)
        self.server_name_entry = ttk.Entry(self.admin_page)
        self.server_name_entry.grid(row=1, column=1, sticky="w", ipadx=9)
        self.server_name_entry.insert("", "PixARK Dedicated Server")  #  # default server name
        
    # world name  
        world_name_label = ttk.Label(self.admin_page, text="World Name:")
        world_name_label.grid(row=2, column=0, sticky="w", padx=80)
        self.server_name_var = tk.StringVar()  # Create the StringVar for the dropdown
        self.world_name_dropdown = ttk.Combobox(self.admin_page, textvariable=self.server_name_var, values=("CubeWolrd_Light", "SkyPiea_Light"), state="readonly") # default CubeWorld_Light as world
        self.world_name_dropdown.current(0)
        self.world_name_dropdown.grid(row=2, column=1, sticky="w") 
    
    # password
        password_label = ttk.Label(self.admin_page, text="Password:")
        password_label.grid(row=3, column=0, sticky="w", padx=80)
        self.password_entry = ttk.Entry(self.admin_page)
        self.password_entry.grid(row=3, column=1, sticky="w", ipadx=9) 
        self.password_entry.insert("", "Password123")  # default password
        
    # admin password
        admin_password_label = ttk.Label(self.admin_page, text="Admin Password:")
        admin_password_label.grid(row=4, column=0, sticky="w", padx=80)
        self.admin_password_entry = ttk.Entry(self.admin_page)
        self.admin_password_entry.grid(row=4, column=1, sticky="w", ipadx=9) 
        self.admin_password_entry.insert("", "AdminPassword123")  # default admin password
        
    # number of players
        number_of_players_label = ttk.Label(self.admin_page, text="Number Of Players:")
        number_of_players_label.grid(row=5, column=0, sticky="w", padx=80)
        self.number_of_players_entry = ttk.Entry(self.admin_page)
        self.number_of_players_entry.grid(row=5, column=1, sticky="w", ipadx=9) 
        self.number_of_players_entry.insert(0, "25")  # default number of players
        
    # port    
        port_label = ttk.Label(self.admin_page, text="Port:")
        port_label.grid(row=6, column=0, sticky="w", padx=80)
        self.port_entry = ttk.Entry(self.admin_page)
        self.port_entry.grid(row=6, column=1, sticky="w", ipadx=9)
        self.port_entry.insert(0, "27016")  # Default port


    # Cube Port
        cube_port_label = ttk.Label(self.admin_page, text="Cube Port:")
        cube_port_label.grid(row=7, column=0, sticky="w", padx=80)
        self.cube_port_entry = ttk.Entry(self.admin_page)
        self.cube_port_entry.grid(row=7, column=1, sticky="w", ipadx=9)
        self.cube_port_entry.insert(0, "27017")  # Default cube port
        
    # Querry Port
        querry_port_label = ttk.Label(self.admin_page, text="Querry Port:")
        querry_port_label.grid(row=8, column=0, sticky="w", padx=80)
        self.querry_port_entry = ttk.Entry(self.admin_page)
        self.querry_port_entry.grid(row=8, column=1, sticky="w", ipadx=9)
        self.querry_port_entry.insert(0, "27018")  # Default querry port
        
    # Rcon Port
        rcon_port_label = ttk.Label(self.admin_page, text="Rcon Port:")
        rcon_port_label.grid(row=9, column=0, sticky="w", padx=80)
        self.rcon_port_entry = ttk.Entry(self.admin_page)
        self.rcon_port_entry.grid(row=9, column=1, sticky="w", ipadx=9)
        self.rcon_port_entry.insert(0, "7777")  # Default Rcon port
        
        divider_frame = ttk.Frame(self.admin_page, height=15)
        divider_frame.grid(row=19, column=0, columnspan=2, sticky="ew")  # Adjust row as needed

        # self.console_text = tk.Text(self.admin_page, height=17, width=96, state=tk.DISABLED)
        # self.console_text.grid(row=20, column=0, sticky="nsew", columnspan=2)

    def set_server_path(self):
        server_exe_path = filedialog.askopenfilename(filetypes=[("PixARK Server Executable", "*.exe")])
        self.server_path_entry.delete(0, tk.END)
        self.server_path_entry.insert(0, server_exe_path)

    def start_server(self):
        port = self.port_entry.get()
        cube_port = self.cube_port_entry.get()
        querry_port = self.querry_port_entry.get()
        rcon_port = self.rcon_port_entry.get()
        server_path = self.server_path_entry.get()
        server_name = self.server_name_entry.get()
        world_name = self.world_name_dropdown.current()
        server_pass = self.password_entry.get()
        admin_pass = self.admin_password_entry.get()
        players_no = self.number_of_players_entry.get()
            
        if not os.path.isfile(str(server_path)):
            print(f"Error: PixARKServer.exe not found at {server_path}")
            return
            
        # Build command line arguments based on world selection
        world_map = {
            0: "CubeWorld_Light",
            1: "SkyPiea_Light",
        }
        command_line_args = f"{world_map[world_name]}?listen?MaxPlayers={players_no}?Port={port}?QueryPort={querry_port}?RCONPort={rcon_port}?SessionName={server_name}?ServerAdminPassword={admin_pass}?CULTUREFORCOOKING=en -NoBattlEye -NoHangDetection -CubePort={cube_port} -cubeworld={server_name} -nosteamclient -game -server -log"

        self.server_process = subprocess.Popen([server_path, command_line_args])
        self.server_status_label.config(text="Server Status: Running")
            

        if not os.path.isfile(str(server_path)):
            # Handle case where server_exe is not found
            print(f"Error: PixARKServer.exe not found at {server_path}")
        return

    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            self.server_status_label.config(text="Server Status: Stopped")
        else:
            print("Server is not running")

    def restart_server(self):
        self.stop_server()
        self.start_server()

    def quit(self):
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PixArkServerManager(root)
    root.mainloop()