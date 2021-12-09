#%%
from tqdm import tqdm
import subprocess
import random
import matplotlib
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

    for i in tqdm(range(2, 11)):
        for j in [1, 0]:
            generate_test_case(filename, base_length, base_length, i, i - j)
            problem_size.append(
                ((2 ** i) * (base_length)) + (2 ** (i - j)) * (base_length)
            )

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

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_ylabel("Time Taken (s)")
    ax.set_xlabel("Problem Size (|m| + |n|) [plotted on a log scale]")
    ax.set_xscale("log")
    ax.set_xticks(problem_size)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.plot(problem_size, time_basic, "o", label="Basic", linestyle="-")
    ax.plot(problem_size, time_efficient, "^", label="Efficient", linestyle="--")
    for (psize, data) in zip(problem_size, time_basic):

        plt.annotate(
            f"{data}s",  # this is the text
            (psize, data),  # these are the coordinates to position the label
            textcoords="offset points",  # how to position the text
            xytext=(0, -12),  # distance from text to points (x,y)
            ha="center",
        )

    for (psize, data) in zip(problem_size, time_efficient):

        plt.annotate(
            f"{data}s",  # this is the text
            (psize, data),  # these are the coordinates to position the label
            textcoords="offset points",  # how to position the text
            xytext=(0, 12),  # distance from text to points (x,y)
            ha="center",
        )
    plt.legend()
    plt.savefig(
        "CPUPlot.jpg", format="jpg", dpi=200, bbox_inches="tight", pad_inches=0.3
    )

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_ylabel("Memory Used (kb)")
    ax.set_xlabel("Problem Size (|m| + |n|) [plotted on a log scale]")
    ax.set_xscale("log")
    ax.set_xticks(problem_size)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.plot(problem_size, memory_basic, "o", label="Basic", linestyle="-")
    ax.plot(problem_size, memory_efficient, "^", label="Efficient", linestyle="--")
    for (psize, data) in zip(problem_size, memory_basic):
        label = f"{data/1024:.0f}Mb"

        plt.annotate(
            label,  # this is the text
            (psize, data),  # these are the coordinates to position the label
            textcoords="offset points",  # how to position the text
            xytext=(0, 12),  # distance from text to points (x,y)
            ha="center",
        )
    for (psize, data) in zip(problem_size, memory_efficient):
        label = f"{data/1024:.0f}Mb"

        plt.annotate(
            label,  # this is the text
            (psize, data),  # these are the coordinates to position the label
            textcoords="offset points",  # how to position the text
            xytext=(0, -12),  # distance from text to points (x,y)
            ha="center",
        )
    plt.legend()
    plt.savefig(
        "MemoryPlot.jpg", format="jpg", dpi=200, bbox_inches="tight", pad_inches=0.3
    )

# %%
