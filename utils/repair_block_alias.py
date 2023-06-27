import os
import sys
import stat

class LinkRepairer:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def repair_links(self):
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                filepath = os.path.join(root, file)
                if os.path.islink(filepath):
                    link_target = os.readlink(filepath)
                    if not os.path.exists(link_target):
                        print(f"Broken link: {filepath} -> {link_target}")
                        if "/root/.lamden/migrating" in link_target:
                            new_target = link_target.replace("/root/.lamden/migrating", "/root/.lamden/blocks")
                            print(f"Repairing link: {filepath} -> {new_target}")
                            os.unlink(filepath)
                            os.symlink(new_target, filepath)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python repair_block_alias.py <root_directory>")
        sys.exit(1)
        
    root_dir = sys.argv[1]
    repairer = LinkRepairer(root_dir)
    repairer.repair_links()
