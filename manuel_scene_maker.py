class Random_File:
    def __init__(self, file_dir=""):
        self.dir: str = (
            random.choice(list(files.keys())) if file_dir == "" else fav_dirs[file_dir]
        )
        files_in_dir = os.listdir(self.dir)
        if not files_in_dir:
            print("No more files to move...")
            self.path = ""
            self.file = ""
            main_menu() 
        self.file: str = random.choice(files_in_dir)
        self.path: str = f"{self.dir}/{self.file}"

    def rate(self, i=0, count=1):
        """
        Rate a random file and move it to a favorite directory
        Loop until i is equal to count
        """
        if i >= count:
            return
        print(f"\n\b[ {i+1} / {count} ]")
        self.open()
        for fav_i, fav_dir in enumerate(fav_dirs):
            print(f"{fav_i+1}) {fav_dir}")
        feedback: str = input(f"Move to... (1-{len(fav_dirs)}): ")
        rating: int = (
            int(-1 if feedback == "" or not feedback.isdigit() else feedback)
        ) - 1
        if 0 <= rating and rating < len(fav_dirs):
            new_path: str = fav_dirs[rating]
        else:
            new_path: str = "not moved"

        if batch_move:
            Random_File().rate(i + 1, count)
            self.move(new_path)
        else:
            self.move(new_path)
            Random_File().rate(i + 1, count)

    def open(self):
        if not self.path:
            return
        if windows:
            os.startfile(self.path)
        else:
            subprocess.call([linux_image_viewer, self.path])
        print(f"{self.file} in {self.dir}")
        return

    def move(self, new_path):
        if new_path == "not moved":
            print("file not moved")
            return
        shutil.move(self.path, new_path)
        print(f"Moved {self.file} to {new_path}")

