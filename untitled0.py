import csv

a = open("Mathdata.csv", "a", newline="")
f = ["ID", "math_q", "expected", "key_press"]
b = csv.DictWriter(a, fieldnames=f)
b.writerow({"ID":"abc", "math_q":"ghg", "expected":"lklk", "key_press":"a"})
a.close()