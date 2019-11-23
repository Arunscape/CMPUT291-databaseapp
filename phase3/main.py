from query import Query


def main_loop():

    q = Query()

    while True:
        buffer = input("Enter your command: ")

        if buffer == "exit":
            break
        elif buffer == "output=brief":
            pass
        elif buffer == "output=full":
            pass

        # maybe this can return a list of query objects
        # so, like we have a Query data class with the parsed terms.
        # e.g. Query(type=date, prefix='date <=', term='2019/11/20')
        queries = parse(buffer)

        for q in queries:
            result = q.process(q)
            print(result)

    q.close_db()


if __name__ == "__main__":
    main_loop()
