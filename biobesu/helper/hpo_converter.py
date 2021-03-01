#!/user/bin/env python3

def read_hpo_obo(hpo_obo):
    """
    Reads the phenotypes from an .obo file.
    :param hpo_obo: the path to the .obo file
    :return: the phenotypes with as key their ID and as value their name
    :rtype: dict
    """
    
    # Strings to identify parts of file.
    match_term = '[Term]'
    match_id = 'id: '
    match_name = 'name: '
    match_synonym = 'synonym: "'

    # Default values for processing.
    phenotypes = {}
    hpo_id = None
    hpo_name = None

    # Goes through the .obo file.
    with open(hpo_obo) as file:
        for line in file:
            # Resets id and name for new phenotype.
            if line.startswith(match_term):
                hpo_id = None
                hpo_name = None
            # Sets id/name when found.
            elif line.startswith(match_id):
                hpo_id = line.lstrip(match_id).strip()
            elif line.startswith(match_name):
                hpo_name = line.lstrip(match_name).strip()
            # Sets a synonym as alternative for name when found on a line.
            elif line.startswith(match_synonym):
                hpo_name = line.lstrip(match_synonym).split('"', 1)[0].strip()

            # If a combination of an id and a name/synonym is stored, saves it to the dictionaries.
            # Afterwards, reset name to None so that it won't be triggered by every line (unless new synonym is found).
            if hpo_id is not None and hpo_name is not None:
                phenotypes[hpo_id] = hpo_name
                hpo_name = None

    return phenotypes
