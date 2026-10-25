import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class CustomPopup:
    def __init__(self, message_text: str):

        # Initialize the popup window
        self.popup = ctk.CTkWidget() if hasattr(ctk, 'CTkWidget') else ctk.CTkToplevel()
        
        # 1. Window Styling & Always-on-Top Configuration
        self.popup.title("Deepfake Detection")
        self.popup.geometry("380x500")
        self.popup.configure(fg_color="#0a1120")  # Dark blue-black background
        self.popup.attributes("-topmost", True)   # Keeps the window always on top
        
        # Optional: Remove standard OS window borders for a cleaner look
        # popup.overrideredirect(True) 

        # 2. Main Container Frame (Adds inner padding)
        main_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # 3. Header Section (Title and Icon placeholder)
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        icon_label = ctk.CTkLabel(header_frame, text="👁", text_color="#ffffff", font=("Arial", 16))
        icon_label.pack(side="left", padx=(0, 8))
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Deepfake Detection", text_color="#00a8e8", font=("Arial", 16))
        subtitle_label.pack(side="left")

        # Divider line
        divider = ctk.CTkFrame(main_frame, fg_color="#334155", height=2)
        divider.pack(fill="x", pady=(0, 20))

        self.passed_text_label = ctk.CTkLabel(main_frame, text=message_text, text_color="#ffffff", width=100,
                                                font=("Arial", 20, "bold"), anchor="w", justify="left")
        self.passed_text_label.pack(fill="x", padx=15, pady=(15, 5))

        # Box showcasing the passed string argument
        display_box = ctk.CTkFrame(main_frame, fg_color="#0f172a", border_color="#1e293b", border_width=1, corner_radius=10, height=300)
        display_box.pack(fill="x", pady=(0, 15))
        display_box.pack_propagate(False)

        self.fig = Figure(figsize=(4, 4), dpi=100)
        self.fig.patch.set_facecolor('#0f172a')
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=display_box)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)

        self.update_chart(0.0)

    def update_chart(self,percent):
            try:
                # 1. Parse and validate the single input number
                val = float(percent)
                if not (0.0 <= val <= 1.0):
                    raise ValueError("Value must be between 0 and 1")
                
                # 2. Calculate the remainder
                remainder = 1.0 - val
                sizes = [val, remainder]
                
                # 3. Define the custom theme colors (Green and Gray)
                colors = ['#28a745', '#e0e0e0'] 
    
                # 4. Redraw the Matplotlib Donut Chart
                self.ax.clear()
                
                # The 'wedgeprops' parameter sets the width of the ring to make it a donut
                wedges, texts = self.ax.pie(
                    sizes, 
                    colors=colors, 
                    startangle=90,          # Starts pointing straight up
                    counterclock=False,     # Moves clockwise like a progress bar
                    wedgeprops={'width': 0.3, 'edgecolor': '#f8f9fa', 'linewidth': 2}
                )
    
                # Add text inside the hole of the donut
                percentage_text = f"{val * 100:.0f}%"
                self.ax.text(0, 0, percentage_text, ha='center', va='center', fontsize=24, weight='bold', color="#FFFEFF")
                
                self.ax.axis('equal')  
                self.canvas.draw()
    
            except ValueError:
                print("Invalid Input", "Please enter a valid decimal number between 0.0 and 1.0")

    def update_message(self, new_text: str):
        if self.popup.winfo_exists():  # Ensures the window is still open before trying to update
            self.passed_text_label.configure(text=new_text)

    def exists(self):
        return self.popup.winfo_exists()

    def destroy(self):
        self.popup.after(100, self.popup.destroy)


# --- Example Usage ---
if __name__ == "__main__":
    # Setup a dummy root window needed by customtkinter to run
    root = ctk.CTk()
    root.withdraw() # Hide the main root window
    
    # Call the function with your custom string
    smy_popup = CustomPopup("Analyzing initial data...")

    root.after(3000,lambda:smy_popup.update_chart(0.5))
    
    root.mainloop()
