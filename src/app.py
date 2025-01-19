import customtkinter as ctk
import subprocess
import os


# Function to center the window
def center_window(win, width, height):
    """Centers the window on the screen."""
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')





def show_popup(title, message, success=True):
    """Displays a popup message using CustomTkinter."""
    popup = ctk.CTkToplevel()
    popup.title(title)
    popup.geometry("300x150")
    center_window(popup, 300, 150)

    label = ctk.CTkLabel(popup, text=message, font=("Arial", 14))
    label.pack(pady=20)

    color = "green" if success else "red"
    label.configure(fg_color=color)

    ok_button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
    ok_button.pack(pady=10)


def activator_1_function():
    """Function to run IAS.exe and check for successful activation."""
    try:
        # Path to the IAS.cmd file
        current_dir = os.getcwd()  # or specify the directory explicitly
        ias_path = os.path.join(current_dir, "IAS.cmd")

        # Check if the .cmd file exists
        if not os.path.exists(ias_path):
            show_popup("Error", f"File not found: {ias_path}", success=False)
            return

        # Run the IAS.cmd file and capture the output
        result = subprocess.run(
            ["cmd.exe", "/c", ias_path],  # The "/c" flag tells cmd.exe to run the command and then terminate
            capture_output=True,
            text=True
        )

        # Check if the success message is in the output and if the command ran successfully
        if result.returncode == 0 and "The IDM Activation process has been completed" in result.stdout:
            # If IAS.cmd is successful, proceed to check for AS.exe
            as_path = os.path.join(current_dir, "AS.exe")
            
            if not os.path.exists(as_path):
                show_popup("Error", f"File not found: {as_path}", success=False)
                return

            # Run the AS.exe file and capture the output
            result = subprocess.run(
                [as_path],
                capture_output=True,
                text=True
            )
            
            # Check if the success message is in the AS.exe output
            if result.returncode == 0 and "Activation complete" in result.stdout:
                show_popup("Success", "IDM Activated Successfully!", success=True)
            else:
                show_popup("Error", "Activation failed in AS.exe.", success=False)
                print(f"Error Output from AS.exe: {result.stderr}")  # Optionally print stderr for debugging
        else:
            show_popup("Error", "Activation failed. Please check the logs.", success=False)
            print(f"Error Output from IAS.cmd: {result.stderr}")  # Optionally print stderr for debugging

    except Exception as e:
        show_popup("Error", f"An error occurred: {str(e)}", success=False)
        print(f"Exception: {str(e)}")  # Optionally print the exception for debugging
# Initialize the customtkinter window
window = ctk.CTk()
window.title("IDM Activator")

# Set window dimensions
window_width = 400
window_height = 300

# Center the window on the screen
center_window(window, window_width, window_height)

# Create a tab view
tabview = ctk.CTkTabview(window, width=400, height=300)
tabview.pack(fill="both", expand=True)

# Add Activator Tab
activator_tab = tabview.add("Activators")

# Create the button in the "Activators" tab
button_activator_1 = ctk.CTkButton(activator_tab, text="Activate", command=activator_1_function)

# Place button in the center of the activator tab
button_activator_1.place(relx=0.5, rely=0.4, anchor='center')

# Add Developer Info Tab
developer_tab = tabview.add("Developer Info")

# Add labels for the developer info in the "Developer Info" tab
software_name_label = ctk.CTkLabel(developer_tab, text="IDM Activator", font=("Arial", 14))
version_label = ctk.CTkLabel(developer_tab, text="Version: 1.0.1", font=("Arial", 14))

# Place the developer info labels in the developer tab
software_name_label.pack(pady=10)
version_label.pack(pady=10)

# Start the main loop
window.mainloop()
