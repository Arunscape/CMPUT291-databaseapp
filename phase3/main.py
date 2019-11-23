from query import Query



def main_loop():

    q = Query()

    while True:
        buffer = input("Enter your query")
        
        if buffer == "exit":
            break




if __name__ == "__main__":
    main_loop()
