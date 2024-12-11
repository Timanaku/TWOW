
import tkinter as tk
from tkinter import ttk

# Define buffs and their multipliers. These represent the boost each buff gives.
buffs = {
    "berserking": 1.10,  # Adds 10% haste
    "arcane_power": 1.35,  # Adds 35% damage boost
    "accelerated_arcana": 1.05,  # Adds 5% arcane boost
    "mind_quickening_gem": 1.33  # Adds 33% spell haste
}

# Calculate total haste based on selected buffs and gear percentages
def calculate_total_haste(selected_buffs, gear_haste_percentages):
    total_haste = 1.0
    for buff in selected_buffs:
        if buff in buffs:
            total_haste *= buffs[buff]
    for gear_haste in gear_haste_percentages:
        total_haste *= (1.0 + gear_haste)
    return total_haste

# Calculate missiles and relevant statistics based on haste
def calculate_missiles(H):
    total_cast_time = (5 / H) + 1  # Time to cast with haste
    missile_interval = 0.95 / H  # Time between missile casts
    missiles_floored = int((5 + H) / 0.95)  # Missiles rounded down
    missiles_unfloored = (5 + H) / 0.95  # Missiles as a float
    deadzone = total_cast_time - (missiles_floored * missile_interval)  # Remaining time after missiles
    return {
        "total_cast_time": total_cast_time,
        "missiles_floored": missiles_floored,
        "missiles_unfloored": missiles_unfloored,
        "deadzone": deadzone
    }

# Format buff names for display
def format_buff_name(buff_name):
    return buff_name.replace("_", " ").title()

# Set up initial variables for buffs
def setup_buff_vars():
    return {}

# Create the UI elements for the buff selection
def setup_buff_frame(parent):
    buff_frame = ttk.LabelFrame(parent, text="Select Buffs", style="Custom.TLabelframe")
    buff_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
    buff_vars = setup_buff_vars()
    row_index = 0
    for buff_name in buffs:
        var = tk.IntVar()
        c = ttk.Checkbutton(buff_frame, text=format_buff_name(buff_name), variable=var, style="Custom.TCheckbutton")
        c.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
        buff_vars[buff_name] = var
        row_index += 1
    return buff_frame, buff_vars

# Create the UI for gear haste input
def setup_gear_frame(parent):
    gear_frame = ttk.LabelFrame(parent, text="Gear Haste (comma-separated in %)", style="Custom.TLabelframe")
    gear_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
    gear_haste_entry = ttk.Entry(gear_frame, width=30, style="Custom.TEntry")
    gear_haste_entry.grid(row=0, column=0, padx=10, pady=5)
    return gear_frame, gear_haste_entry

# Create the UI for the results display
def setup_results_frame(parent):
    results_frame = ttk.LabelFrame(parent, text="Results", style="Custom.TLabelframe")
    results_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    haste_label = ttk.Label(results_frame, text="Haste: N/A", style="Custom.TLabel")
    haste_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    cast_time_label = ttk.Label(results_frame, text="Total Cast Time: N/A", style="Custom.TLabel")
    cast_time_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    missiles_floored_label = ttk.Label(results_frame, text="Missiles (floored): N/A", style="Custom.TLabel")
    missiles_floored_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    missiles_unfloored_label = ttk.Label(results_frame, text="Missiles (unfloored): N/A", style="Custom.TLabel")
    missiles_unfloored_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    deadzone_label = ttk.Label(results_frame, text="Deadzone: N/A", style="Custom.TLabel")
    deadzone_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

    return results_frame, haste_label, cast_time_label, missiles_floored_label, missiles_unfloored_label, deadzone_label

# Update the results labels after calculation
def on_calculate():
    selected_buffs = [buff_name for buff_name, var in buff_vars.items() if var.get() == 1]

    gear_input = gear_haste_entry.get().strip()
    gear_haste = []
    if gear_input:
        for gh in gear_input.split(','):
            gh = gh.strip()
            if gh:
                try:
                    val = float(gh) / 100.0
                    gear_haste.append(val)
                except ValueError:
                    pass

    H = calculate_total_haste(selected_buffs, gear_haste)
    results = calculate_missiles(H)

    haste_label.config(text=f"Haste: {int(H*100)}%")
    cast_time_label.config(text=f"Total Cast Time: {results['total_cast_time']:.3f}s")
    missiles_floored_label.config(text=f"Missiles (floored): {results['missiles_floored']}")
    missiles_unfloored_label.config(text=f"Missiles (unfloored): {results['missiles_unfloored']:.3f}")
    deadzone_label.config(text=f"Deadzone: {results['deadzone']:.3f}s")

# Main function to set up and run the UI
def main():
    global root, buff_vars, gear_haste_entry, haste_label, cast_time_label, missiles_floored_label, missiles_unfloored_label, deadzone_label

    root = tk.Tk()
    root.iconbitmap('AP.ico')
    root.title("Haste & Missiles Calculator")

    # Apply custom styles for a dark minimalist look
    style = ttk.Style()
    root.configure(bg="#333333")
    style.configure("Custom.TLabelframe", background="#444444", foreground="#FFFFFF", font=("Arial", 12, "bold"), borderwidth=1, relief="solid")
    style.configure("Custom.TLabel", background="#444444", foreground="#FFFFFF", font=("Arial", 10))
    style.configure("Custom.TCheckbutton", background="#444444", foreground="#FFFFFF", font=("Arial", 10))
    style.configure("Custom.TButton", background="#666666", foreground="#FFFFFF", font=("Arial", 11, "bold"), borderwidth=1, relief="solid")
    style.configure("Custom.TEntry", fieldbackground="#555555", foreground="#FFFFFF", font=("Arial", 10), relief="flat")

    buff_frame, buff_vars = setup_buff_frame(root)
    gear_frame, gear_haste_entry = setup_gear_frame(root)

    calc_button = tk.Button(root, text="Calculate", command=on_calculate, bg="#666666", fg="#FFFFFF", font=("Arial", 11, "bold"), relief="solid", borderwidth=1)
    calc_button.grid(row=2, column=0, pady=10, padx=20)

    results_frame, haste_label, cast_time_label, missiles_floored_label, missiles_unfloored_label, deadzone_label = setup_results_frame(root)

    root.mainloop()

if __name__ == "__main__":
    main()
