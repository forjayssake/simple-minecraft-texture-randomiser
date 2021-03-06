from cgitb import text
import os
import sys
import time
import random
import shutil
import zipfile
from argparse import ArgumentParser


class txCreator():

    mode: str  = "random"
    mc_path: str = ""
    tmp_dir: str = ""
    mc_dot_dir: str = ""
    mc_version: str = ""
    extract_dir: str = ""
    blocks_suffix: str = "\\assets\minecraft\\textures\\block"
    texture_files: list = []
    pack_format: int = 8 # default for 1.18x
    pack_json: str = '{"pack": {"pack_format": [format],"description": "[description]"}}'


    def __init__(self, mc_path: str, mc_format: int, mc_mode: str):
        
        if not self.check_directory(mc_path):
            print("Error: " + mc_path + " is not found or is not a directory")
            sys.exit(2)
        self.mc_path = mc_path
        print("Validated Minecraft version directory: " + self.mc_path)

        if mc_mode != None:
            self.mode = mc_mode
        print("Mode: " + self.mode)

        if mc_format != None:
            self.pack_format = mc_format
        print("Using pack format: " + str(self.pack_format))

        self.run()


    def run(self):
        self.fetch_paths(self.mc_path)
        if self.mode == "setup" or self.mode == "random":
            self.setup()
        if self.mode == "random":
            self.randomise()
        if self.mode == "random" or self.mode == "complete":
            self.complete()
 

    def setup(self):
        self.tidy_up()
        self.copy_for_version()


    def randomise(self):
        self.fetch_assets_as_dictionary()
        self.reorder_assets()


    def complete(self):
        self.create_texture_pack()
        self.tidy_up()
        print("Complete")


    def fetch_paths(self, mc_path: str):
        print("Deriving required paths")
        # set the path to the version folder
        path = os.path.normpath(mc_path)
        self.mc_path = path.split(os.sep)
        self.mc_path = mc_path.strip("\\")
        print("normalised mincraft version path: " + self.mc_path)
        
        # set the version of minecraft 
        self.mc_version = os.path.split(self.mc_path)[1]
        print("derived mincraft version: " + self.mc_version)

        # set the path to the .mincraft directory
        path_list = self.mc_path.split(os.sep)
        try:
            mc_index = path_list.index(".minecraft")
            mc_dir_list = path_list[0:mc_index+1]
            self.mc_dot_dir = "\\".join(mc_dir_list)
            print("Path to .minecraft directory: " + self.mc_dot_dir)
        except ValueError as ve:
            print("Error: .minecraft directory cannot be found within supplied mincraft version path.")
            sys.exit(2)

        # set the temp directory to copy the .jar file to
        self.tmp_dir = self.mc_dot_dir + "\\tmp_texturepath"
        print("Temp texture file directory: " + self.tmp_dir)

        self.extract_dir = self.tmp_dir + "\\" + self.mc_version
        

    def check_directory(self, directory: str) -> bool:
        return os.path.isdir(directory)


    def copy_for_version(self):

        # validate and copy jar file
        print("Copying " + self.mc_version + ".jar")
        jar_file = self.mc_path + "\\" + self.mc_version + ".jar"
        if not os.path.isfile(jar_file):
            print("Error: Expected file: " + jar_file + " is not found")
            sys.exit(2)

        os.mkdir(self.tmp_dir)
        shutil.copy(jar_file, self.tmp_dir)

        # extract jar file
        print("Extracting " + self.mc_version + ".jar")
        with zipfile.ZipFile(self.tmp_dir + "\\" + self.mc_version + ".jar", 'r') as zip_ref:
            zip_ref.extractall(self.extract_dir)

        if self.mode == "setup":
            print("Extraction complete. Edit image files in: " + self.extract_dir + "\\assets\\minecraft\\textures as required, and run this command in `complete` mode.")
        

    def fetch_assets_as_dictionary(self):
        self.texture_files = os.listdir(self.extract_dir + self.blocks_suffix)


    def reorder_assets(self):
        blocks_path = self.extract_dir + self.blocks_suffix
        while len(self.texture_files) >= 2:
            flist = random.sample(self.texture_files, 2)
            # rename files in place
            os.rename(blocks_path + "\\" + flist[1], blocks_path + "\\1" + flist[1])

            print("Swapping: " + flist[0] + " with " + flist[1])
            os.rename(blocks_path + "\\" + flist[0], blocks_path + "\\" + flist[1])
            os.rename(blocks_path + "\\1" + flist[1], blocks_path + "\\" + flist[0])
            # remove samples from texture_files
            self.texture_files.remove(flist[0])
            self.texture_files.remove(flist[1])


    def create_texture_pack(self):
        print("Creating: " + self.extract_dir + "\\pack.mcmeta")
        f = open(self.extract_dir + "\\pack.mcmeta","w+")
        content = self.pack_json.replace('[format]', str(self.pack_format))

        if self.mode == "random":
            description = 'Randomised_pack_' + str(time.time())
        elif self.mode == "complete":
            userinp = input("Enter a sensible texture pack name: ")
            description = userinp.replace(" ", "_") + "_" + str(time.time())

        content = content.replace('[description]', description)

        f.write(content)
        f.close()

        print("Compressing texture pack: " + self.extract_dir + "\\" + description + ".zip")

        os.mkdir(self.extract_dir + "\\tmpzip")
        shutil.copytree(self.extract_dir + "\\assets",  self.extract_dir + "\\tmpzip\\assets")
        shutil.copy(self.extract_dir + "\\pack.mcmeta",  self.extract_dir + "\\tmpzip\\pack.mcmeta")

        shutil.make_archive(self.extract_dir + "\\" + description, 'zip', self.extract_dir + "\\tmpzip")

        print("Copying " + self.extract_dir + "\\" + description + ".zip to resourcepacks")
        shutil.copy(self.extract_dir + "\\" + description + ".zip", self.mc_dot_dir + "\\resourcepacks\\" + description + ".zip")


    def tidy_up(self):
        print("Deleting temporary directory if present: " + self.tmp_dir)
        if self.check_directory(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)


if __name__ == "__main__":
    parser = ArgumentParser()
    helptxt = "Required. Full path and directory name of required Minecraft version"
    parser.add_argument("-d", "--directory", dest="mc_dir", help=helptxt, metavar="DIRECTORY")

    helptxt = "Optional. Pack format for required minecraft version. See readme.md for more information. Defaults to 8 for 1.18x"
    parser.add_argument("-f", "--format", dest="mc_format", help=helptxt, metavar="INT")

    helptxt = "Optional. [random, setup, complete]. Create random (default), setup custom, complete custom"
    parser.add_argument("-m", "--mode", dest="mc_mode", help=helptxt, metavar="STRING")

    args = parser.parse_args()
    if args.mc_dir == None:
        print("Missing required argument completely: ")
        parser.print_help()
        sys.exit(2)

    print("attemping to process for: " + args.mc_dir)

    tx_creator = txCreator(args.mc_dir, args.mc_format, args.mc_mode)
    