from enum import Enum
import re
import csv

import file_printer


class School(Enum):
    Abjuration = "A"
    Conjuration = "C"
    Divination = "D"
    Enchantment = "EN"
    Evocation = "EV"
    Illusion = "I"
    Necromancy = "N"
    Transmutation = "T"


class Spell:
    ritual = ""

    def __init__(self, name, source, level, casting_time, duration, school, range_dnd, components, classes,
                 optional_variant_classes, text, at_higher_levels):
        self.text = []
        self.paragraph_lengths = []
        # Create the name of the Spell by combing the name and adding the source in brackets
        self.name = name + " (" + source + ")"
        # Set the level to the first letter of level unless it's a cantrip then it gets set to 0
        self.level = 0 if level == "Cantrip" else level[0]
        # Check if the spell is a ritual if that's the case, note it and remove (ritual) from the string
        if " (ritual)" in school:
            self.ritual = "true"
            school = school.replace(" (ritual)", "")
        # Get the abbreviation of each school from the enum
        self.school = School[school].value
        # Copy the casting time
        self.time = casting_time
        # Copy the duration
        self.duration = duration
        # Copy the range
        self.range_dnd = range_dnd
        # Copy the components unless there is a material one, in that case cut the description of what specifically
        self.components = components[:8] if " M " in components else components
        # Copy both classes and optional classes if present
        self.classes = classes if optional_variant_classes == "" else classes + " ," + optional_variant_classes
        # Split the text when there is a line break and put it in a list and add the higher level description
        Spell.text = []
        Spell.paragraph_lengths = []
        for match in re.findall(r'\.\w', text):
            self.text.append(text[:text.find(match) + 1])
            text = text[text.find(match) + 1:]
        self.text.append(text)
        for index, paragraph in enumerate(self.text):
            if len(paragraph) > file_printer.MAX_LENGTH:
                split_paragraph = split_string_at_sentence_middle(paragraph)
                self.text.pop(index)
                self.text.insert(index, split_paragraph[1])
                self.text.insert(index, split_paragraph[0])
        self.text.append(at_higher_levels[1:])
        # Document how long each paragraph is and remove all empty ones
        for paragraph in self.text:
            if len(paragraph) > 0:
                self.paragraph_lengths.append(len(paragraph))
            else:
                self.text.remove(paragraph)

    def __str__(self):
        return "Name: " + self.name + "\nLevel: " + str(self.level) + "\nSchool: " + self.school + "\nTime: " + str(
            self.time) + "\nRitual: " + str(self.ritual) + "\nRange: " + str(self.range_dnd) + "\nComponents: " + str(
            self.components) + "\nDuration: " + str(self.duration) + "\nClasses: " + str(
            self.classes) + "\nText: " + str(self.text) + "\nTextLength: " + str(self.paragraph_lengths)


def read_spells(path):
    list_of_spells = []
    file_path = path
    with open(file_path, "r", encoding='utf8') as spells:
        csv_reader = csv.reader(spells)
        next(csv_reader)
        for row in csv_reader:
            list_of_spells.append(
                Spell(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
    spells.close()
    return list_of_spells


def split_string_at_sentence_middle(input_string):
    # Find the middle index
    middle_index = len(input_string) // 2

    # Find the nearest sentence-ending punctuation around the middle index
    punctuation = ['.', '!', '?']
    for i in range(middle_index, 0, -1):
        if input_string[i] in punctuation:
            middle_index = i + 1  # Include the punctuation in the second part
            break

    # Split the string
    first_part = input_string[:middle_index]
    second_part = input_string[middle_index:]

    return first_part, second_part
