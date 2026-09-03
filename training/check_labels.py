from pathlib import Path
from collections import Counter

label_folder = Path("data/train/labels")

counter = Counter()

for label_file in label_folder.glob("*.txt"):

    with open(label_file, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            class_id = int(line.split()[0])

            counter[class_id] += 1

print("Class distribution:")
print()

for class_id, count in sorted(counter.items()):

    print(
        f"Class ID {class_id}: {count} objects"
    )