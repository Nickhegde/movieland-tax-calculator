


def modify(test):
    test["Month"] = 2
    return
    


def main():
    test_obj = {
        "Month": 1,
        "GrossIncome": 1000
    }
    modify(test_obj)
    print(test_obj)

main()