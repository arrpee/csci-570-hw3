from timeit import default_timer

DELTA = 30
ALPHA = {}
ALPHA["A"] = {"A": 0, "C": 110, "G": 48, "T": 94}
ALPHA["C"] = {"A": 110, "C": 0, "G": 118, "T": 48}
ALPHA["G"] = {"A": 48, "C": 118, "G": 0, "T": 110}
ALPHA["T"] = {"A": 94, "C": 48, "G": 110, "T": 0}


def read_input_file(filename="input.txt"):
    with open(filename) as f:
        inp = f.read().splitlines()

    split = None
    for i in range(1, len(inp)):
        try:
            int(inp[i])
        except Exception as e:
            split = i
            break

    return (
        inp[0],
        [int(x) for x in inp[1:split]],
        inp[split],
        [int(x) for x in inp[1 + split :]],
    )


def generate_string(base_str, arr):
    if not arr:
        return base_str

    gen_string = base_str
    for i in arr:
        gen_string = gen_string[: i + 1] + gen_string + gen_string[i + 1 :]

    assert len(gen_string) == (2 ** len(arr)) * len(base_str)

    return gen_string


def align_strings(s1, s2):
    dp = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]

    for i in range(len(s1) + 1):
        dp[i][0] = i * DELTA

    for i in range(len(s2) + 1):
        dp[0][i] = i * DELTA

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            dp[i][j] = min(
                dp[i - 1][j - 1] + ALPHA[s1[i - 1]][s2[j - 1]],
                dp[i - 1][j] + DELTA,
                dp[i][j - 1] + DELTA,
            )

    aligned_string = []
    l1 = len(s1) - 1
    l2 = len(s2) - 2
    while l1 != 0 and l2 != 0:
        if dp[l1][l2] == dp[l1 - 1][l2 - 1] + ALPHA[s1[l1]][s2[l2]]:
            aligned_string.append(s1[l1])
            l1 -= 1
            l2 -= 1
        elif dp[l1][l2] == dp[i - 1][j] + DELTA:
            aligned_string.append("_")
            l1 -= 1
        else:
            aligned_string.append("_")
            l2 -= 1

    if l1:
        for i in range(l1, -1, -1):
            aligned_string.append(s1[i])
    elif l2:
        for i in range(l2, -1, -1):
            aligned_string.append(s2[i])

    aligned_string.reverse()
    return "".join(aligned_string)


def write_output_file(s, time_taken, memory_used, filename="output.txt"):
    with open(filename, "w") as f:
        f.write(s[:50])
        f.write("\n")
        f.write(s[-50:])
        f.write("\n")
        f.write(f"{time_taken:.3f}")
        f.write("\n")
        f.write(f"{memory_used}")


if __name__ == "__main__":

    start = default_timer()

    base_str1, indices1, base_str2, indices2 = read_input_file()

    string1 = generate_string(base_str1, indices1)
    string2 = generate_string(base_str2, indices2)

    output_string = align_strings(string1, string2)

    memory_used = 0
    time_taken = default_timer() - start

    write_output_file(output_string, time_taken, memory_used)
