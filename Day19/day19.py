def segment_line(line, words):
    """
    Counts the number of ways the given string `line` can be segmented into a sequence of words
    from the set `words`. Uses dynamic programming.

    Time Complexity: O(n^2)
    Space: O(n + 1) for the array storing the counts up to each index point
    """
    n = len(line)

    # match_counts[i] stores the number of ways line[0:i] can be segmented.
    match_counts = [0] * (n + 1)

    # Base case: there is only one way to segment an empty string.
    match_counts[0] = 1

    # Loop over each end index.
    for i in range(1, n + 1):
        # Check all possible starts for a word ending at i.
        for j in range(i):
            # Get the substring from the start up to, but not including the end.
            substring = line[j:i]

            # The substring can only be placed at a valid start - match_counts[j] > 0 means
            # that the prefix up to the start has one or more complete segmentations.
            if match_counts[j] > 0 and substring in words:
                # Add the prior segmentation count to the count at i. This will keep count of the
                # number of ways line[0:i] can be segmented.
                match_counts[i] += match_counts[j]

    # Return the number of ways the line can be segmented.
    return match_counts[n]


valid_line_count = 0
valid_combination_count = 0

with open('Day19/input.txt', 'r') as f:
    words = set(word.strip() for word in f.readline().split(','))
    f.readline()
    for count in [segment_line(line, words) for line in [line.rstrip() for line in f.readlines()]]:
        if count > 0:
           valid_line_count += 1
           valid_combination_count += count

print(f'Day 19 Part 1: {valid_line_count}')
print(f'Day 19 Part 2: {valid_combination_count}')
