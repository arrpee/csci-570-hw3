def generate_string(base_str, arr):
    if not arr:
        return base_str

    gen_string = base_str
    for i in arr:
        gen_string = gen_string[: i + 1] + gen_string + gen_string[i + 1 :]
    return gen_string


if __name__ == "__main__":

    with open("input.txt") as f:
        inp = f.read().splitlines()

    split = None
    for i in range(1, len(inp)):
        try:
            int(inp[i])
        except Exception as e:
            split = i
            break

    string1 = generate_string(inp[0], [int(x) for x in inp[1:split]])
    string2 = generate_string(inp[split], [int(x) for x in inp[1 + split :]])

