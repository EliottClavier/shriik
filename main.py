from src.ascii_converter import AsciiConverter
import sys

def main():
    try:
        ascii_converter = AsciiConverter()
        ascii_converter.launch_workflow(sys.argv[1], "ascii_image")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
