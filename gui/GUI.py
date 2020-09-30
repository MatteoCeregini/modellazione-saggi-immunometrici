from tkinter import *
import pyglet

from engine.WindowManager import WindowManager


def validate_input(value):
    return value.replace('.', '', 1).isdigit() or value == ''


def validate_input_probability(value):
    return (value.replace('.', '', 1).isdigit() and float(value) <= 1) or value == ''



def set_text(entry, text):
    entry.delete(0, END)
    entry.insert(0, text)


class GUI:
    def __init__(self):
        helvetica = ("Helvetica", 10)
        self.root = Tk()
        self.validate = self.root.register(validate_input)
        self.validate_probability_flat_on = self.root.register(validate_input_probability)
        self.root.title("Modello Computazionale")
        self.root.geometry('550x270')
        self.root.resizable(False, False)

        self.frame_entries = Frame(self.root)
        self.frame_entries.place(x=5, y=10)

        self.frame_button = Frame(self.root)
        self.frame_button.place(x=420, y=50)

        self.frame_radio_buttons = LabelFrame(master=self.root, text="Antibodies generation", font=helvetica)
        self.frame_radio_buttons.place(x=5, y=170)
        self.method = IntVar(value=0)
        self.method_random_radio_button = Radiobutton(self.frame_radio_buttons, text="Random",
                                                      variable=self.method, command=self.update_method_random,
                                                      value="1")
        self.method_random_radio_button.grid(row=0, sticky=W)
        self.method_fab_up_radio_button = Radiobutton(self.frame_radio_buttons, text="End-on, Fab-up (Aligned)",
                                                      variable=self.method, command=self.update_method_fab_up,
                                                      value="2")
        self.method_fab_up_radio_button.grid(row=1, sticky=W)

        self.method_side_on_radio_button = Radiobutton(self.frame_radio_buttons, text="Side-on",
                                                       variable=self.method, command=self.update_method_side_on,
                                                       value="3")
        self.method_side_on_radio_button.grid(row=2, sticky=W)

        self.label_antibodies = Label(self.frame_entries, text="Maximum antibody concentration (ng/cm^2)",
                                      font=helvetica)
        self.label_antibodies.grid(row=0, sticky=W)
        self.entry_antibodies = Entry(self.frame_entries, validate="key", validatecommand=(self.validate, "%P"))
        self.entry_antibodies.grid(row=0, column=1)

        self.label_probability_antibody_flat_on = Label(self.frame_entries,
                                                        text="Probability of generating flat-on antibody (0-1)",
                                                        font=helvetica)
        self.label_probability_antibody_flat_on.grid(row=1, sticky=W)
        self.entry_probability_antibody_flat_on = Entry(self.frame_entries, validate="key",
                                                        validatecommand=(self.validate_probability_flat_on, "%P"))
        self.entry_probability_antibody_flat_on.grid(row=1, column=1)

        self.label_width_surface = Label(self.frame_entries, text="Surface side length (nm)",
                                         font=("Helvetica", 10))
        self.label_width_surface.grid(row=2, sticky=W)
        self.entry_width_surface = Entry(self.frame_entries, validate="key", validatecommand=(self.validate, "%P"))
        self.entry_width_surface.grid(row=2, column=1)

        self.label_height_antibody = Label(self.frame_entries, text="Height antibody (nm)", font=helvetica)
        self.label_height_antibody.grid(row=3, sticky=W)
        self.entry_height_antibody = Entry(self.frame_entries, validate="key", validatecommand=(self.validate, "%P"))
        self.entry_height_antibody.grid(row=3, column=1)

        self.label_diameter_antibody = Label(self.frame_entries, text="Diameter antibody (nm)", font=helvetica)
        self.label_diameter_antibody.grid(row=4, sticky=W)
        self.entry_diameter_antibody = Entry(self.frame_entries, validate="key", validatecommand=(self.validate, "%P"))
        self.entry_diameter_antibody.grid(row=4, column=1)

        self.label_radius_antigen = Label(self.frame_entries, text="Radius antigen (nm)", font=helvetica)
        self.label_radius_antigen.grid(row=5, sticky=W)
        self.entry_radius_antigen = Entry(self.frame_entries, validate="key", validatecommand=(self.validate, "%P"))
        self.entry_radius_antigen.grid(row=5, column=1)

        self.label_distance = Label(self.frame_entries, text="Distance between points", font=helvetica)
        self.label_distance.grid(row=6, sticky=W)
        self.entry_distance = Entry(self.frame_entries, validate="key",
                                    validatecommand=(self.validate, "%P"))
        self.entry_distance.grid(row=6, column=1)

        self.button = Button(self.frame_button, text="Run simulation", command=self.start_simulation, height=2,
                             width=11,
                             font=helvetica)
        self.button.grid(row=0, column=0)

    def update_method_random(self):
        self.method.set(1)

    def update_method_fab_up(self):
        self.method.set(2)

    def update_method_side_on(self):
        self.method.set(3)

    def start_simulation(self):
        if self.method.get() == 1:
            try:
                param = {
                    "method": 'random',
                    "ratio_antibodies": float(self.entry_antibodies.get()),
                    "probability_antibody_flat_on": float(self.entry_probability_antibody_flat_on.get()),
                    "diameter_antibody": float(self.entry_diameter_antibody.get()),
                    "height_antibody": float(self.entry_height_antibody.get()),
                    "width_surface": float(self.entry_width_surface.get()),
                    "radius_antigen": float(self.entry_radius_antigen.get()),
                    "distance_between_points": float(self.entry_distance.get())
                }
                window_manager = WindowManager(param, visible=False)
                pyglet.app.run()

            except ValueError:  # Se si lasce qualche entry vuota la simulazione non può partire
                pass
        elif self.method.get() == 2:
            try:
                param = {
                    "method": 'fab_up',
                    "ratio_antibodies": None,
                    "probability_antibody_flat_on": None,
                    "diameter_antibody": float(self.entry_diameter_antibody.get()),
                    "height_antibody": float(self.entry_height_antibody.get()),
                    "width_surface": float(self.entry_width_surface.get()),
                    "radius_antigen": float(self.entry_radius_antigen.get()),
                    "distance_between_points": None
                }
                window_manager = WindowManager(param, visible=False)
                pyglet.app.run()

            except ValueError:  # Se si lasce qualche entry vuota la simulazione non può partire
                pass
        elif self.method.get() == 3:
            try:
                param = {
                    "method": 'side_on',
                    "ratio_antibodies": None,
                    "probability_antibody_flat_on": None,
                    "diameter_antibody": float(self.entry_diameter_antibody.get()),
                    "height_antibody": float(self.entry_height_antibody.get()),
                    "width_surface": float(self.entry_width_surface.get()),
                    "radius_antigen": float(self.entry_radius_antigen.get())
                }
                window_manager = WindowManager(param, visible=False)
                pyglet.app.run()

            except ValueError:  # Se si lasce qualche entry vuota la simulazione non può partire
                pass

    def run(self):
        self.root.mainloop()
