team_number = 0
person_number = 0
student_id = 0
canvas_id = 1000
with open("MyExampleContacts.csv", "w") as my_csv_file:
    my_csv_file.write("LastName,FirstName,Email,StudentID,CanvasId,Team\n")
    for i in range(350):
        person_number += 1
        canvas_id += 1
        if i % 5 == 0:
            team_number += 1
            person_number = 1

        last_name = f"Team{team_number}"
        first_name = f"Person{person_number}"
        email = f"{last_name}{first_name}@ucdavis.edu"
        out_line = f"{last_name},{first_name},{email},{student_id},{canvas_id},{team_number}\n"
        my_csv_file.write(out_line)
