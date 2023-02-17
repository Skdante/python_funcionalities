def divide(num1, num2):
    try:
        return num1/num2
    except ZeroDivisionError:
        return 0

while True:
    try:
        op1 = int(input("introduce el primer numero."))
        op2 = int(input("introduce el segundo numero."))
        break
    except:
        input("Agrega valores correctos, please")

print(divide(op1,op2))