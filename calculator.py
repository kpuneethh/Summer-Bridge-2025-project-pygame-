#!/usr/bin/env python

def calc_grade(test1, test2, hmw, attendance, total_pts):
    extra = 0

    if(test1 >= 95 and attendance == 100):
        extra = 10
    
    grade = (test1 + hmw + test2 + attendance + extra) / total_pts

    return grade

def main():
    print("Grade Calculator v2")

    midterm = 98
    homework = 100
    final = 97
    partic = 99
    total_points = 400

    print("Final Grade: " + str(calc_grade(midterm, homework, final, partic, total_points)))

if __name__ == "__main__":
        main()



