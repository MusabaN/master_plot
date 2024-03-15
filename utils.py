def insert_line_breaks(label):
    max_len = 5
    # Handling forward slash
    if '/' in label and len(label) > max_len:
        parts = label.split('/')
        # Ensure there are parts to work with and rejoin with a line break
        if len(parts) >= 2:
            return f'{parts[0]} /\n{parts[1]}'
    # Handling spaces
    if ' ' in label and len(label) > max_len:
        parts = label.split(' ')
        # Find the first occurrence where rejoining parts exceeds max_len characters
        for i in range(1, len(parts)):
            if len(' '.join(parts[:i])) > max_len:
                return ' '.join(parts[:i]) + '\n' + ' '.join(parts[i:])
        return label
    return label


# Apply the custom function to each alternative
def adjust_labels(alternatives):
    return [insert_line_breaks(alt) for alt in alternatives]
