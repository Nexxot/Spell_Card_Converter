import math
import xml.etree.ElementTree as ET

MAX_LENGTH = 1000


def print_file(file_path, spells):
    # Create the root element
    compendium = ET.Element("compendium")
    # Iterate over all spells
    for spell_csv in spells:
        # Determine how many cards we need
        cards_needed = 1
        copy_for_counting = list(spell_csv.text)
        while len(copy_for_counting) > 0:
            total_length = 0
            pop_counter = 0
            for paragraph in copy_for_counting:
                if total_length + len(paragraph) < MAX_LENGTH or (
                        len(paragraph) > MAX_LENGTH and total_length == 0):
                    total_length += len(paragraph)
                    pop_counter += 1
                else:
                    break
            for i in range(pop_counter):
                copy_for_counting.pop(0)
            if len(copy_for_counting) > 0:
                cards_needed += 1


        # If we only need 1 card just print everything
        if cards_needed == 1 or len(spell_csv.text) == 1:
            # Create the spell element
            spell = ET.SubElement(compendium, "spell")
            name = ET.SubElement(spell, "name")
            # Create sub-elements for the spell
            level = ET.SubElement(spell, "level")
            school = ET.SubElement(spell, "school")
            time = ET.SubElement(spell, "time")
            ritual = ET.SubElement(spell, "ritual")
            range_element = ET.SubElement(spell, "range")
            components = ET.SubElement(spell, "components")
            duration = ET.SubElement(spell, "duration")
            classes_element = ET.SubElement(spell, "classes")

            # Set text for the values
            level.text = spell_csv.level
            school.text = spell_csv.school
            time.text = spell_csv.time
            ritual.text = spell_csv.ritual
            range_element.text = spell_csv.range_dnd
            components.text = spell_csv.components
            duration.text = spell_csv.duration
            classes_element.text = spell_csv.classes

            # Handle the text and name
            name.text = spell_csv.name
            for paragraph in spell_csv.text:
                text_element = ET.SubElement(spell, "text")
                text_element.text = paragraph
        else:
            current_card = 0
            while current_card < cards_needed or len(spell_csv.text) > 0:
                total_length = 0
                pop_counter = 0

                spell = ET.SubElement(compendium, "spell")
                name = ET.SubElement(spell, "name")
                # Create sub-elements for the spell
                level = ET.SubElement(spell, "level")
                school = ET.SubElement(spell, "school")
                time = ET.SubElement(spell, "time")
                ritual = ET.SubElement(spell, "ritual")
                range_element = ET.SubElement(spell, "range")
                components = ET.SubElement(spell, "components")
                duration = ET.SubElement(spell, "duration")
                classes_element = ET.SubElement(spell, "classes")

                # Set text for the values
                level.text = spell_csv.level
                school.text = spell_csv.school
                time.text = spell_csv.time
                ritual.text = spell_csv.ritual
                range_element.text = spell_csv.range_dnd
                components.text = spell_csv.components
                duration.text = spell_csv.duration
                classes_element.text = spell_csv.classes

                # Handle the text and name
                name.text = spell_csv.name + " [" + str(current_card + 1) + "/" + str(cards_needed) + "]"
                for paragraph in spell_csv.text:
                    if total_length + len(paragraph) < MAX_LENGTH or (
                            len(paragraph) > MAX_LENGTH and total_length == 0):
                        text_element = ET.SubElement(spell, "text")
                        text_element.text = paragraph
                        total_length += len(paragraph)
                        pop_counter += 1
                    else:
                        break
                for i in range(pop_counter):
                    spell_csv.text.pop(0)
                current_card += 1

    # Create an ElementTree object
    tree = ET.ElementTree(compendium)

    # Save the XML to a file
    new_path = file_path.replace("Spells.csv", "Spells.xml")
    tree.write(new_path, encoding="utf-8", xml_declaration=True)
