try:
    VER = open("VER", "r").readlines()[0]
except:
    VER = "??? (Possibly Modified)"

from os import system

def main():
    print("~`   THE UNTOLD ODYSSEY  `~")
    print(f"    {VER}")
    print(f"This script will continue to build the client for your platform. The version of the source code is [{VER}].")

    confirmation = input("Press any key to continue the building process . . . ")

    print("Initializing build process. Please wait as compiling the game may take a moment.")
    
    system("python3 setup.py build_apps")

if __name__ == "__main__":
    main()