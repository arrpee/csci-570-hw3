#%%
from tqdm import tqdm
import subprocess
import random
import matplotlib.pyplot as plt


def generate_test_case(
    filename, base_str1_length=4, base_str2_length=4, str1_mods=4, str2_mods=4
):
    base_str1 = []
    for _ in range(base_str1_length):
        base_str1.append(random.choice(["A", "C", "T", "G"]))

    base_str2 = []
    for _ in range(base_str2_length):
        base_str2.append(random.choice(["A", "C", "T", "G"]))

    with open(filename, "w") as f:
        f.write("".join(base_str1))
        f.write("\n")
        for i in range(str1_mods):
            f.write(f"{random.randint(0, ((2 ** (i)) * base_str1_length) -1)}")
            f.write("\n")

        f.write("".join(base_str2))
        f.write("\n")
        for i in range(str2_mods):
            f.write(f"{random.randint(0, ((2 ** (i)) * base_str2_length )-1)}")
            f.write("\n")


if __name__ == "__main__":
    filename = "input.txt"
    base_length = 4

    time_basic = []
    time_efficient = []

    memory_basic = []
    memory_efficient = []

    problem_size = []

    for i in tqdm(range(1, 9)):
        for j in [0, 2]:
            # print((2 ** i) * (base_length + j))
            generate_test_case(filename, base_length + j, base_length + j, i, i)
            problem_size.append(((2 ** i) * (base_length + j)) ** 2)

            output = subprocess.run(
                [
                    "/usr/bin/time",
                    "-l",
                    "python3",
                    "5840387942_6161762888_basic.py",
                    filename,
                ],
                capture_output=True,
                text=True,
            ).stderr

            time, memory = [x.strip() for x in output.splitlines()][:2]
            time_basic.append(float(time[: time.find(" ")]))
            memory_basic.append(int(memory[: memory.find(" ")]) / 1024)

            output = subprocess.run(
                [
                    "/usr/bin/time",
                    "-l",
                    "python3",
                    "5840387942_6161762888_efficient.py",
                    filename,
                ],
                capture_output=True,
                text=True,
            ).stderr

            time, memory = [x.strip() for x in output.splitlines()][:2]
            time_efficient.append(float(time[: time.find(" ")]))
            memory_efficient.append(int(memory[: memory.find(" ")]) / 1024)

    plt.ylabel("Time Taken (s)")
    plt.xlabel("Problem Size (|m| * |n|)")
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    plt.plot(problem_size, time_basic, "o", label="Basic", linestyle="-")
    plt.plot(problem_size, time_efficient, "^", label="Efficient", linestyle="--")
    plt.legend()
    plt.savefig(
        "CPUPlot.jpg", format="jpg", dpi=200, bbox_inches="tight", pad_inches=0.3
    )

    plt.cla()
    plt.ylabel("Memory Used (kb)")
    plt.xlabel("Problem Size (|m| * |n|)")
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    plt.plot(problem_size, memory_basic, "o", label="Basic", linestyle="-")
    plt.plot(problem_size, memory_efficient, "^", label="Efficient", linestyle="--")
    plt.legend()
    plt.savefig(
        "MemoryPlot.jpg", format="jpg", dpi=200, bbox_inches="tight", pad_inches=0.3
    )

# %%
