def main():

    inputs = []
    flag = False
    index = 0
    while(not flag):

        inputs.append(input("Enter a/the next task or type done to exit: "))
        if "done" in inputs:
            flag = True
            inputs.remove("done")
        else:
            index = index + 1
    
    for x in inputs:
        print(x)

main()