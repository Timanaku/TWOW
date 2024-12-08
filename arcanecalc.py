import tkinter as tk
from tkinter import ttk

buffs = {
    "berserking": 1.10,
    "arcane_power": 1.35,
    "accelerated_arcana": 1.05,
    "mind_quickening_gem": 1.33
}

def calculate_total_haste(selected_buffs, gear_haste_percentages):
    total_haste = 1.0
    for buff in selected_buffs:
        if buff in buffs:
            total_haste *= buffs[buff]
    for gear_haste in gear_haste_percentages:
        total_haste *= (1.0 + gear_haste)
    return total_haste

def calculate_missiles(H):
    total_cast_time = (5 / H) + 1
    missile_interval = 0.95 / H
    missiles_floored = int((5 + H) / 0.95)
    missiles_unfloored = (5 + H) / 0.95
    deadzone = total_cast_time - (missiles_floored * missile_interval)
    return {
        "total_cast_time": total_cast_time,
        "missiles_floored": missiles_floored,
        "missiles_unfloored": missiles_unfloored,
        "deadzone": deadzone
    }

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


root = tk.Tk()
root.iconbitmap('AP.ico')
root.title("Haste & Missiles Calculator")

buff_frame = ttk.LabelFrame(root, text="Select Buffs")
buff_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

buff_vars = {}
row_index = 0
for buff_name in buffs.keys():
    var = tk.IntVar()
    c = ttk.Checkbutton(buff_frame, text=buff_name.replace("_", " ").title(), variable=var)
    c.grid(row=row_index, column=0, sticky="w")
    buff_vars[buff_name] = var
    row_index += 1


gear_frame = ttk.LabelFrame(root, text="Gear Haste (comma-separated in %)")
gear_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

gear_haste_entry = ttk.Entry(gear_frame, width=30)
gear_haste_entry.grid(row=0, column=0, padx=5, pady=5)

calc_button = ttk.Button(root, text="Calculate", command=on_calculate)
calc_button.grid(row=2, column=0, pady=10)

results_frame = ttk.LabelFrame(root, text="Results")
results_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

haste_label = ttk.Label(results_frame, text="Haste: N/A")
haste_label.grid(row=0, column=0, sticky="w")

cast_time_label = ttk.Label(results_frame, text="Total Cast Time: N/A")
cast_time_label.grid(row=1, column=0, sticky="w")

missiles_floored_label = ttk.Label(results_frame, text="Missiles (floored): N/A")
missiles_floored_label.grid(row=2, column=0, sticky="w")

missiles_unfloored_label = ttk.Label(results_frame, text="Missiles (unfloored): N/A")
missiles_unfloored_label.grid(row=3, column=0, sticky="w")

deadzone_label = ttk.Label(results_frame, text="Deadzone: N/A")
deadzone_label.grid(row=4, column=0, sticky="w")

root.mainloop()
