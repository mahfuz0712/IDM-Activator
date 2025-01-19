import customtkinter as ctk
import os
import subprocess
import requests

# Globals
IDM_PATH = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
REGISTRY_BACKUP_DIR = os.path.join(os.environ["TEMP"], "IDM_Registry_Backup")


# Helper Functions
def run_command(command):
    """Runs a command and returns its output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()


def check_idm_running():
    """Checks if IDM is running."""
    tasks = run_command(["tasklist", "/FI", "IMAGENAME eq idman.exe"])
    return "idman.exe" in tasks


def kill_idm():
    """Terminates IDM if running."""
    if check_idm_running():
        print("[*] IDM is running. Terminating...")
        run_command(["taskkill", "/F", "/IM", "idman.exe"])


def backup_registry_key(key_path, backup_file):
    """Backs up a registry key."""
    print(f"[*] Backing up registry key: {key_path}")
    result = run_command(["reg", "export", key_path, backup_file, "/y"])
    if result:
        print(f"[+] Backup created: {backup_file}")
    else:
        print(f"[-] Failed to backup: {key_path}")


def delete_registry_key(key_path):
    """Deletes a registry key."""
    print(f"[*] Deleting registry key: {key_path}")
    result = run_command(["reg", "delete", key_path, "/f"])
    if result:
        print(f"[+] Deleted: {key_path}")
    else:
        print(f"[-] Failed to delete: {key_path}")


def add_registry_key(key_path, name, value):
    """Adds or modifies a registry key."""
    print(f"[*] Adding registry key: {key_path}\\{name}")
    result = run_command(["reg", "add", key_path, "/v", name, "/t", "REG_SZ", "/d", value, "/f"])
    if result:
        print(f"[+] Added: {key_path}\\{name}")
    else:
        print(f"[-] Failed to add: {key_path}\\{name}")


def download_file(url, save_path):
    """Downloads a file from the internet."""
    try:
        print(f"[*] Downloading file from {url}")
        response = requests.get(url, stream=True)
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"[+] Downloaded: {save_path}")
    except Exception as e:
        print(f"[-] Failed to download {url}: {e}")


# CustomTkinter Input Form
def get_user_details():
    """Creates a CustomTkinter form for user to input fname, lname, and email."""
    user_details = {}

    def submit():
        user_details["fname"] = fname_entry.get()
        user_details["lname"] = lname_entry.get()
        user_details["email"] = email_entry.get()

        if not user_details["fname"] or not user_details["lname"] or not user_details["email"]:
            error_label.configure(text="All fields are required!", fg_color="red")
        else:
            form.destroy()

    # Create the form window
    form = ctk.CTk()
    form.title("IDM Activation Details")
    form.geometry("400x300")
    form.resizable(False, False)

    # Center the form on the screen
    screen_width = form.winfo_screenwidth()
    screen_height = form.winfo_screenheight()
    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (300 // 2)
    form.geometry(f"400x300+{x}+{y}")

    # Configure grid layout
    form.grid_rowconfigure((0, 1, 2, 3), weight=1)
    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=2)

    # Labels and Entry Fields
    ctk.CTkLabel(form, text="First Name", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    fname_entry = ctk.CTkEntry(form, width=200)
    fname_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(form, text="Last Name", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    lname_entry = ctk.CTkEntry(form, width=200)
    lname_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(form, text="Email", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    email_entry = ctk.CTkEntry(form, width=200)
    email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Error Label
    error_label = ctk.CTkLabel(form, text="", font=("Arial", 12), fg_color="transparent")
    error_label.grid(row=3, column=0, columnspan=2, pady=5)

    # Submit Button
    submit_button = ctk.CTkButton(form, text="Submit", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2, pady=20)

    form.mainloop()
    return user_details


# Main Logic
def main():
    print("[*] Starting IDM Activation Script")

    # Get user details using CustomTkinter
    user_details = get_user_details()

    if not user_details:
        print("[-] User cancelled the operation.")
        return

    fname, lname, email = user_details["fname"], user_details["lname"], user_details["email"]

    # Ensure registry backup directory exists
    os.makedirs(REGISTRY_BACKUP_DIR, exist_ok=True)

    # Check IDM installation
    if not os.path.exists(IDM_PATH):
        print("[-] IDM is not installed. Please install IDM first.")
        return

    # Kill IDM if running
    kill_idm()

    # Backing up registry keys
    backup_registry_key("HKCU\\Software\\DownloadManager", os.path.join(REGISTRY_BACKUP_DIR, "HKCU_Backup.reg"))

    # Clear registry keys
    keys_to_clear = [
        "HKCU\\Software\\DownloadManager\\FName",
        "HKCU\\Software\\DownloadManager\\LName",
        "HKCU\\Software\\DownloadManager\\Email",
        "HKCU\\Software\\DownloadManager\\Serial",
    ]
    for key in keys_to_clear:
        delete_registry_key(key)

    # Add registration details
    print("[*] Applying registration details...")
    add_registry_key("HKCU\\Software\\DownloadManager", "FName", fname)
    add_registry_key("HKCU\\Software\\DownloadManager", "LName", lname)
    add_registry_key("HKCU\\Software\\DownloadManager", "Email", email)
    print(f"[+] Registration applied: {fname} {lname} {email}")

    # Trigger downloads to initialize IDM
    downloads = [
        "https://www.internetdownloadmanager.com/images/idm_box_min.png",
        "https://www.internetdownloadmanager.com/register/IDMlib/images/idman_logos.png",
        "https://www.internetdownloadmanager.com/pictures/idm_about.png",
    ]
    for url in downloads:
        download_file(url, os.path.join(REGISTRY_BACKUP_DIR, os.path.basename(url)))

    print("Activation complete.")


if __name__ == "__main__":
    main()
