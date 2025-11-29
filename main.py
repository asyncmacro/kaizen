import os
import shutil
import re

# --- CONFIGURATION ---
BASE_DIR = os.getcwd()
NEW_ROOT_NAME = "Helicon"
NEW_ROOT = os.path.join(BASE_DIR, NEW_ROOT_NAME)

# --- DIRECTORY STRUCTURE SETUP ---
DIRS_TO_CREATE = [
    "000 - Inbox",
    "100 - Knowledge Graph/110 - Computer Science",
    "100 - Knowledge Graph/120 - Web Development",
    "100 - Knowledge Graph/130 - Design & Product",
    "200 - Personal Growth/210 - Languages",
    "200 - Personal Growth/220 - History & Politics",
    "300 - Projects & Areas/310 - Active Projects",
    "300 - Projects & Areas/320 - Continuous Areas",
    "400 - The Library/410 - Videos",
    "400 - The Library/420 - Articles",
    "900 - System/910 - Templates",
    "900 - System/920 - Prompts",
    "900 - System/990 - Archive",
]


def create_structure():
    if not os.path.exists(NEW_ROOT):
        os.makedirs(NEW_ROOT)
    for d in DIRS_TO_CREATE:
        path = os.path.join(NEW_ROOT, d)
        if not os.path.exists(path):
            os.makedirs(path)


# --- ZETTELKASTEN CLASSIFICATION LOGIC ---
def get_zettel_dest(filename):
    """Classifies Zettelkasten notes based on keywords."""
    fn_lower = filename.lower()

    # 210 - Languages
    if re.search(r"korean|gerund|prepositional", fn_lower):
        return "200 - Personal Growth/210 - Languages"

    # 130 - Design & Product
    if re.search(r"design thinking|double diamond", fn_lower):
        return "100 - Knowledge Graph/130 - Design & Product"

    # 110 - Computer Science (Theory, Complexity, SQL, Algo)
    # Note: Tree shaking is often tooling, but per previous context was mapped to CS/Theory
    if re.search(r"complexity|sql|tree shaking", fn_lower):
        return "100 - Knowledge Graph/110 - Computer Science"

    # 120 - Web Development (Default for Hono, React, JS, HTML, etc.)
    return "100 - Knowledge Graph/120 - Web Development"


# --- MAIN MOVE LOGIC ---
def move_item(src_path, dest_rel_path):
    """Moves a file or folder to the destination inside Helicon."""
    if not os.path.exists(src_path):
        return

    dest_path = os.path.join(NEW_ROOT, dest_rel_path)

    # If moving a directory (like a Project folder), handle potential conflicts
    if os.path.isdir(src_path):
        final_dest = os.path.join(dest_path, os.path.basename(src_path))
        if os.path.exists(final_dest):
            print(f"Skipping {src_path} -> Directory already exists in destination.")
        else:
            shutil.move(src_path, dest_path)
            print(f"Moved Dir:  {os.path.basename(src_path)} -> {dest_rel_path}")

    # If moving a file
    elif os.path.isfile(src_path):
        shutil.move(src_path, dest_path)
        print(f"Moved File: {os.path.basename(src_path)} -> {dest_rel_path}")


def process_migration():
    print("--- Starting Migration to Helicon Structure ---")

    # 1. 0 - Inbox -> 000 - Inbox
    src = os.path.join(BASE_DIR, "0 - Inbox")
    if os.path.exists(src):
        for f in os.listdir(src):
            move_item(os.path.join(src, f), "000 - Inbox")

    # 2. 1 - Map Of Contents -> 120 - Web Development (MOCs sit with content)
    src = os.path.join(BASE_DIR, "1 - Map Of Contents")
    if os.path.exists(src):
        for f in os.listdir(src):
            move_item(
                os.path.join(src, f), "100 - Knowledge Graph/120 - Web Development"
            )

    # 3. 2 - Source Notes -> 410 - Videos (Assuming source notes are mostly video/tutorial based on file list)
    src = os.path.join(BASE_DIR, "2 - Source Notes")
    if os.path.exists(src):
        for f in os.listdir(src):
            # Differentiate if needed, but based on 'Source - Youtube', default to Videos
            move_item(os.path.join(src, f), "400 - The Library/410 - Videos")

    # 4. 3 - Zettelkasten -> Split into 110, 120, 130, 210
    src = os.path.join(BASE_DIR, "3 - Zettelkasten")
    if os.path.exists(src):
        for f in os.listdir(src):
            if f.startswith("."):
                continue  # Skip hidden files

            dest_folder = get_zettel_dest(f)
            move_item(os.path.join(src, f), dest_folder)

    # 5. 4 - Areas -> 320 - Continuous Areas
    src = os.path.join(BASE_DIR, "4 - Areas")
    if os.path.exists(src):
        for f in os.listdir(src):
            move_item(
                os.path.join(src, f), "300 - Projects & Areas/320 - Continuous Areas"
            )

    # 6. 5 - Projects -> 310 - Active Projects
    src = os.path.join(BASE_DIR, "5 - Projects")
    if os.path.exists(src):
        for f in os.listdir(src):
            # This handles directories like 'PixlFlow' and 'Advanced TypeScript'
            move_item(
                os.path.join(src, f), "300 - Projects & Areas/310 - Active Projects"
            )

    # 7. 7 - Prompts -> 920 - Prompts
    src = os.path.join(BASE_DIR, "7 - Prompts")
    if os.path.exists(src):
        for f in os.listdir(src):
            move_item(os.path.join(src, f), "900 - System/920 - Prompts")

    # 8. 9 - Unsorted -> Split (Articles -> 420, Templates -> 910)
    src_unsorted = os.path.join(BASE_DIR, "9 - Unsorted")

    # Handle Articles
    src_articles = os.path.join(src_unsorted, "Articles")
    if os.path.exists(src_articles):
        for f in os.listdir(src_articles):
            move_item(os.path.join(src_articles, f), "400 - The Library/420 - Articles")

    # Handle Templates
    src_templates = os.path.join(src_unsorted, "Templates")
    if os.path.exists(src_templates):
        for f in os.listdir(src_templates):
            move_item(os.path.join(src_templates, f), "900 - System/910 - Templates")

    print("\n--- Migration Complete ---")
    print(f"Your files are now in the '{NEW_ROOT_NAME}' folder.")
    print(
        "Please verify the files. If satisfied, you can delete the empty '0 - Inbox', '1 - Map...', etc. folders."
    )


if __name__ == "__main__":
    create_structure()
    process_migration()
