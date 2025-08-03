import os
import re


# ANSI color codes
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def find_markdown_links():
    # Get all markdown files in current directory
    md_files = [f for f in os.listdir(".") if f.endswith(".md")]

    # Create mapping of filenames without extension to full filenames
    filename_map = {os.path.splitext(f)[0].lower(): f for f in md_files}

    results = {}

    # Go through each markdown file
    for md_file in md_files:
        links = []

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

            # Look for potential references to other files
            for name in filename_map:
                # Skip self-references
                if name == os.path.splitext(md_file)[0].lower():
                    continue

                # Look for the filename (case insensitive) in the content
                pattern = rf"\b{re.escape(name)}\b"
                matches = list(re.finditer(pattern, content.lower()))

                filtered_matches = []
                for match in matches:
                    # Check if the match is already wrapped in [[]]
                    start_pos = match.start()
                    end_pos = match.end()

                    # Check if there are [[ before and ]] after the match
                    is_already_linked = (
                        start_pos >= 2
                        and end_pos + 2 <= len(content)
                        and content[start_pos - 2 : start_pos] == "[["
                        and content[end_pos : end_pos + 2] == "]]"
                    )

                    if not is_already_linked:
                        filtered_matches.append(match)

                if filtered_matches:
                    # Store both the target file and the match positions
                    links.append((filename_map[name], filtered_matches, content))

        if links:
            results[md_file] = links

    return results


if __name__ == "__main__":
    links = find_markdown_links()

    # Print results and handle user confirmation
    for source, targets in links.items():
        # print(f"\n{Colors.CYAN}In {Colors.BOLD}{source}{Colors.RESET}:")

        with open(source, "r", encoding="utf-8") as f:
            content = f.read()

        for target_file, matches, original_content in targets:
            print(
                f"\n{Colors.CYAN}In {Colors.BOLD}{source}{Colors.RESET} {Colors.GREEN}found potential references to {Colors.BOLD}{target_file}{Colors.RESET}:"
            )

            for match in matches:
                # Get surrounding context (150 chars before and after)
                start = max(0, match.start() - 150)
                end = min(len(original_content), match.end() + 150)
                context = original_content[start:end]

                # Color the reference word in the contexnt
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
                    # Replace the matched text with [[text]]
                    original_word = original_content[match.start() : match.end()]
                    content = content.replace(original_word, f"[[{original_word}]]")

        # Write the modified content back to the file
        with open(source, "w", encoding="utf-8") as f:
            f.write(content)
