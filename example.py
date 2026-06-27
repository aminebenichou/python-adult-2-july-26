def is_authenticated(func):
    def checking():
        print("checking...")
        print("User is authenticated")
        return True
    return checking


@is_authenticated
def displayText():
    print("hello")
    return True



test= displayText()