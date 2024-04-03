block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    """
    Takes a whole markdown document and splits into distinct blocks.
    Strip any leading or trailing whitspaces from each block.
    It should remove empty blocks.

    """
    blocks = markdown.split("\n\n")
    filtered_blocks = [block.strip() for block in blocks if block.strip() != '']
    return filtered_blocks


def match_upto_dot(s):
    for i, c in enumerate(s):
        if c == '.':
            return s[:i], i
    return s, -1


def is_ordered_list(raw_block):
    input_lines = raw_block.split("\n")
    start = 1  # Ordered lists start with 1

    for raw_line in input_lines:
        line = raw_line.strip()
        digit_str, dot_idx = match_upto_dot(line)

        try:
            digit = int(digit_str)
            # Check if the digit matches the expected sequence number, and
            # ensure the dot immediately follows the digit with no spaces
            if digit == start and dot_idx == len(digit_str):
                start += 1  # Increment for the next expected number
            else:
                return False
        except ValueError:
            return False

    return True

def is_heading(raw_block):
    line = raw_block.strip()
    if line.startswith("#"):
        count = len(line) - len(line.lstrip('#'))
        if 1 <= count <= 6 and line[count:].startswith(' '):
            return True
    return False


def block_to_block_type(md_block):
    """
    Heading starts with 1-6 #
    Code blocks must start with 3 backticks and end with 3 backticks.
    Every line in a quote block must start with a > character.
    Every line in an unordered list block must start with a * or - character.
    Every line in an ordered list block must start with a number followed by a . character. The number must start at 1 and increment by 1 for each line.
    If none of the above conditions are met, the block is a normal paragraph.
    """
    is_unordered_list = lambda s: all(line.strip()[0] == '*' or line.strip()[0] == '-' for line in s.split("\n") if line.strip())
    is_code = lambda s:  s.strip().startswith("```") and s.strip().endswith("```")
    is_quote = lambda s: all(line.strip()[0] == '>' for line in s.split("\n") if line.strip())


    if is_ordered_list(md_block):
        return block_type_ordered_list
    if is_unordered_list(md_block):
        return block_type_unordered_list
    if is_code(md_block):
        return block_type_code
    if is_heading(md_block):
        return block_type_heading
    if is_quote(md_block):
        return block_type_quote
    else:
        return block_type_paragraph
