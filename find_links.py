import os
import re
import argparse


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def find_markdown_links(vault_path):
    md_files = [f for f in os.listdir(vault_path) if f.endswith(".md")]
    filename_map = {os.path.splitext(f)[0].lower(): f for f in md_files}
    results = {}

    for md_file in md_files:
        links = []
        with open(os.path.join(vault_path, md_file), "r", encoding="utf-8") as f:
            content = f.read()

        # Find all existing wikilinks
        existing_links = set()
        for match in re.finditer(r"\[\[(.+?)\]\]", content):
            existing_links.add(match.group(1).split("|")[0].lower())

        # Remove YAML frontmatter
        if content.startswith("---"):
            end_of_frontmatter = content.find("---", 3)
            if end_of_frontmatter != -1:
                content = content[end_of_frontmatter + 3 :]

        for name in filename_map:
            if name == os.path.splitext(md_file)[0].lower() or name in existing_links:
                continue

            pattern = rf"\b{re.escape(name)}\b"
            matches = list(re.finditer(pattern, content.lower()))

            if matches:
                links.append((filename_map[name], matches, content))

        if links:
            results[md_file] = links

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find potential links in an Obsidian vault."
    )
    parser.add_argument("vault_path", help="The path to the Obsidian vault.")
    args = parser.parse_args()

    links = find_markdown_links(args.vault_path)

    for source, targets in links.items():
        with open(os.path.join(args.vault_path, source), "r", encoding="utf-8") as f:
            content = f.read()

        for target_file, matches, original_content in targets:
            print(
                f"\n{Colors.CYAN}In {Colors.BOLD}{source}{Colors.RESET} {Colors.GREEN}found potential references to {Colors.BOLD}{target_file}{Colors.RESET}:"
            )

            for match in matches:
                start = max(0, match.start() - 150)
                end = min(len(original_content), match.end() + 150)
                context = original_content[start:end]

                match_in_context = match.start() - start
                colored_context = (
                    context[:match_in_context]
                    + f"{Colors.GREEN}{context[match_in_context : match_in_context + match.end() - match.start()]}{Colors.RESET}"
                    + context[match_in_context + match.end() - match.start() :]
                )

                print(
                    f"\n{Colors.YELLOW}Context:{Colors.RESET} \n...{colored_context}..."
                )
                confirm = input(
                    f"{Colors.MAGENTA}Convert this reference to a link? (y/n):{Colors.RESET} "
                )

                if confirm.lower() == "y":
                    original_word = original_content[match.start() : match.end()]
                    content = content.replace(original_word, f"[[{original_word}]]")

        with open(os.path.join(args.vault_path, source), "w", encoding="utf-8") as f:
            f.write(content)
