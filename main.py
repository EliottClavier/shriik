from src.window import Window

def main():
    Window()

    # try:
    #     BrailleConverter()
    #     ascii_converter = AsciiConverter()
    #     if len(sys.argv) > 1:
    #         ascii_converter.launch_workflow(sys.argv[1], "ascii_image")
    #     else:
    #         raise Exception("No image path provided")
    # except Exception as e:
    #     print(e)

if __name__ == "__main__":
    main()
