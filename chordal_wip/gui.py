import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
import chordal_wip.scales as cw


class MyBoxLayout(BoxLayout):
    # Init infinte keywords
    def __init__(self, **kwargs):
        # Init BoxLayout parent class
        super(MyBoxLayout, self).__init__(**kwargs)

        # Stack drop down and chord grid vertically
        self.orientation = "vertical"

        # Add dropdown for triads/7ths selection
        self.spinner_chord_type = Spinner(
            text="Chord Type",  # default text
            values=("triads", "7ths"),  # Options
            size_hint=(0.2, 0.1),  # relative height and width,
            pos_hint={"center_x": 0.5},  # position param
        )

        # TODO: Clean up here, make tidy blocks for each widget, mv add_widget to back
        # Set the default value to "triads" (first valid option)
        self.spinner_chord_type.text = "7ths"

        # Call method when drop down is used
        self.spinner_chord_type.bind(text=self.on_spinner_select)

        # Add widget to layout
        self.add_widget(self.spinner_chord_type)

        # Add GridLayout for chords
        # TODO: Add logic to expand grid depending on n_chords
        self.grid = GridLayout(cols=2)

        # TODO: Name should be big, below add roman numerals and chord degree name
        # place holder text
        self.chord_labels = [
            Label(text="Chord_1"),
            Label(text="Chord_2"),
            Label(text="Chord_3"),
            Label(text="Chord_4"),
        ]

        # Add label to grid
        for label in self.chord_labels:
            self.grid.add_widget(label)

        # Add grid to layout
        self.add_widget(self.grid)

        self.spinner_root = Spinner(
            text="C",
            values=cw.Scale("C", "ionian").ALL_NOTES,  #
            size_hint=(0.2, 0.1),
        )
        self.add_widget(self.spinner_root)
        self.spinner_mode = Spinner(
            text="ionian",
            values=list(cw.Scale("C", "ionian").scales_dict.keys()),  #
            size_hint=(0.2, 0.1),
        )
        self.add_widget(self.spinner_mode)

        self.generate_button = Button(
            text="Go",
            size_hint=(0.5, 0.1),  #
        )
        self.generate_button.bind(on_press=self.call_progression)
        self.add_widget(self.generate_button)

        # TODO: Add all add_widgets here

        # Init progression
        self.progression = None
        self.call_progression(None)

    def call_progression(self, instance):
        """Generate a new chord progression based on current selections.

        Creates a new chord progression using the selected root note and mode,
        then updates the displayed chords.

        Args:
            instance: The button instance that triggered this method (unused).
        """
        # Get scale and chord
        root_note = self.spinner_root.text
        mode = self.spinner_mode.text
        scale = cw.Scale(root_note, mode)
        chord = cw.Chord(scale)

        # Create progression
        progression = cw.MarkovChordProgression(n_chords=4, chord=chord)
        self.progression = progression.progression

        # Update labels
        self.on_spinner_select(self.spinner_chord_type, self.spinner_chord_type.text)

    def on_spinner_select(self, spinner, text):
        """Update chord labels when the chord type spinner selection changes.

        Extracts the selected chord type (triads or 7ths) from the progression
        DataFrame and updates the displayed chord labels.

        Args:
            spinner: The spinner widget that triggered this method (unused).
            text: The selected value from the spinner ('triads' or '7ths').
        """
        # Check if p exists, else do nothing
        if self.progression is not None:
            chords = self.progression[text].tolist()  # Get triads or 7ths
            for i, label in enumerate(self.chord_labels):
                # handles not replacing place holders when n_chords < 4
                if i < len(chords):
                    label.text = chords[i]


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == "__main__":
    MyApp().run()
