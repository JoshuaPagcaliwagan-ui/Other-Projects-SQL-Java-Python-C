# Group Jazzy J's Members
# John Benedict G. Calimlim
# Joshua O. Pagcaliwagan
# Sophia Jeanine V. Untalan

import mariadb  # import mariadb module for database connection
import sys  # import sys module for system-specific parameters and functions
from getpass import getpass  # import getpass for secure password input
from datetime import datetime  # import datetime for date operations
import re  # regex pattern matching for input validation

# function to connect to mariadb database
def create_connection():
    try:
        conn = mariadb.connect(  # establish a connection to the database
            user="project",  # set the username for the database
            password="project",  # set the password for the database
            host="localhost",  # set the host to localhost
            database="127project"  # specify the database name
        )
        return conn  # return the connection object
    except mariadb.Error as e:  # handle any connection errors
        print(f"Error connecting to MariaDB Platform: {e}")  # print error message
        sys.exit(1)  # exit the program with an error code

# function for user login
def login():
    student_number = input("Enter Student Number: ")  # prompt user for student number
    password = getpass("Enter Password: ")  # prompt user for password securely
    
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object for executing queries
    
    try:
        # check if student number and password match in the database
        cursor.execute("SELECT * FROM member WHERE student_number = ? AND password = ?", (student_number, password))
        member = cursor.fetchone()  # fetch the first matching record
        
        if member:  # if a matching record is found
            print(f"Welcome {member[2]} {member[4]}!")  # greet the user with their name
            return student_number  # return the student number for session
        else:  # if no matching record is found
            print("Invalid credentials")  # inform user of invalid credentials
            return None  # return None to indicate failure
            
    except mariadb.Error as e:  # handle any errors during login
        print(f"Error during login: {e}")  # print error message
        return None  # return None to indicate failure
    finally:
        cursor.close()  # close the cursor to free resources
        conn.close()  # close the database connection

# function to show user profile
def view_profile(student_number):
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("SELECT * FROM member WHERE student_number = ?", (student_number,))  # query to get member info
        result = cursor.fetchone()  # fetch the first matching record
        
        if result:  # if a profile is found
            print("\n--- PROFILE ---")  # print profile header
            print(f"Student Number: {result[0]}")  # show student number
            print(f"Name: {result[2]} {result[3] or ''} {result[4]}")  # show full name
            print(f"Degree Program: {result[5]}")  # show degree program
            print(f"Gender: {result[6] or 'N/A'}")  # show gender
            print(f"Batch Year: {result[7]}")  # show batch year
        else:  # if no profile found
            print("Profile not found.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during profile retrieval
        print(f"Error fetching profile: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# function to show student organizations
def view_organizations(student_number):
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("""
            SELECT o.organization_name, ms.semester, ms.academic_year, ms.membership_status, ms.member_role, ms.committee
            FROM membership ms
            JOIN organization o ON ms.organization_id = o.organization_id
            WHERE ms.student_number = ?
            ORDER BY ms.academic_year DESC, ms.semester
        """, (student_number,))  # execute the query with the student number
        
        results = cursor.fetchall()  # fetch all organization records
        
        print("\n--- YOUR ORGANIZATIONS ---")  # print header for organizations
        if results:  # if organizations are found
            print(f"{'Organization':<25} {'Semester':<15} {'Year':<10} {'Status':<12} {'Role':<15} {'Committee':<15}")  # print column headers
            print("-" * 100)  # print separator line
            for org in results:  # loop through each organization record
                organization = org[0] or 'N/A'
                semester = org[1] or 'N/A'
                year = org[2] or 'N/A'
                status = org[3] or 'N/A'
                role = org[4] or 'N/A'
                committee = org[5] or 'N/A'
                print(f"{organization:<25} {semester:<15} {year:<10} {status:<12} {role:<15} {committee:<15}")
        else:
            print("No organizations found.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during organization retrieval
        print(f"Error fetching organizations: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# function to show student fees
def view_fees(student_number):
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        # get unpaid fees for the current student from the database
        cursor.execute("""
            SELECT f.fee_reference_number, o.organization_name, f.semester, f.due_date, f.amount_due
            FROM fee f
            JOIN membership ms ON f.student_number = ms.student_number AND f.organization_id = ms.organization_id
            JOIN organization o ON ms.organization_id = o.organization_id
            LEFT JOIN payment p ON f.fee_reference_number = p.fee_reference_number
            WHERE ms.student_number = ?
            AND p.payment_reference_number IS NULL;

        """, (student_number,))  # execute the query with the student number
        
        fees = cursor.fetchall()  # fetch all fee records
        
        if fees:  # if there are unpaid fees
            print("\n--- UNPAID FEES ---")  # print header for unpaid fees
            print(f"{'Ref No':<12} {'Organization':<20} {'Semester':<15} {'Due Date':<12} {'Amount':<10}")  # print column headers
            print("-" * 75)  # print separator line
            for fee in fees:  # loop through each fee record
                due_date_str = fee[3].strftime("%Y-%m-%d") if fee[3] else "N/A"
                print(f"{fee[0]:<12} {fee[1]:<20} {fee[2]:<15} {due_date_str:<12} {fee[4]:<10}")  # print fee details
        else:  # if no unpaid fees found
            print("No unpaid fees found for this student.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during fee retrieval
        print(f"Error fetching fees: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# function to change user password
def change_password(student_number):
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        # Get current password for verification
        current_password = getpass("Enter current password: ")
        
        # Verify current password
        cursor.execute("SELECT password FROM member WHERE student_number = ?", (student_number,))
        stored_password = cursor.fetchone()
        
        if not stored_password or stored_password[0] != current_password:
            print("Current password is incorrect.")
            return
        
        # Get new password
        while True:
            new_password = getpass("Enter new password: ")
            if not new_password.strip():
                print("Password cannot be empty.")
                continue
            
            confirm_password = getpass("Confirm new password: ")
            if new_password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue
            
            break
        
        # Update password in database
        cursor.execute("UPDATE member SET password = ? WHERE student_number = ?", 
                      (new_password, student_number))
        
        conn.commit()
        print("Password changed successfully!")
        
    except mariadb.Error as e:
        print(f"Error changing password: {e}")
    finally:
        cursor.close()
        conn.close()

# function for membership operations (basic structure)
def manage_membership(student_number):
    print("\n--- MEMBERSHIP MANAGEMENT ---")  # print membership management header
    print("[1] View All Organizations")  # option to view all organizations
    print("[2] View Organization Members")  # option to view members of an organization
    print("[3] View Executive Committee Members")  # option to view executive members
    print("[4] View Alumni Members")  # option to view alumni members
    print("[5] View Presidents History")  # option to view past presidents
    print("[6] Add Membership") # option to add membership to a student
    print("[7] View Organization Status Percentage") # option to view percentage per membership status
    print("[0] Back to Main Menu")  # option to return to the main menu
    choice = input("Choose an option: ")  # get user choice
    
    if choice == '1':  # if user wants to view all organizations
        view_all_organizations()  # call function to view all organizations
    elif choice == '2':  # if user wants to view organization members
        view_organization_members()  # call function to view organization members
    elif choice == '3':  # if user wants to view executive members
        view_executive_members()  # call function to view executive members
    elif choice == '4':  # if user wants to view alumni
        view_alumni_members()  # call function to view alumni members
    elif choice == '5':  # if user wants to view presidents history
        view_presidents_history()  # call function to view presidents history
    elif choice == '6': # if user wants to add a membership
        add_membership() # call function for add membership
    elif choice == '7': # if user wants to view percentage of active vs inactive members
        view_percentages() # call function for view percentages
    elif choice == '0':  # if user wants to go back to the main menu
        return  # exit the function
    else:  # if invalid choice
        print("Invalid choice.")  # inform user

# function to view all organizations
def view_all_organizations():
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("SELECT organization_id, organization_name, academic_year, semester FROM organization ORDER BY organization_name")  # query to get all organizations
        rows = cursor.fetchall()  # fetch all organization records
        
        if rows:  # if organizations exist
            print("\n--- ALL ORGANIZATIONS ---")  # print header for all organizations
            print(f"{'ID':<5} {'Name':<40} {'Academic Year':<15} {'Semester':<15}")  # print column headers
            print("-" * 70)  # print separator line
            for row in rows:  # loop through each organization record
                semester = row[3] or 'N/A'  # get semester or 'N/A' if not available
                year = row[2] or 'N/A'  # get academic year or 'N/A' if not available
                org_name = row[1][:27] + "..." if len(row[1]) > 40 else row[1]
                print(f"{row[0]:<5} {org_name:<40} {year:<15} {semester:<15}")
        else:  # if no organizations found
            print("No organizations found.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during organization retrieval
        print(f"Error fetching organizations: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# function to view organization members
def view_organization_members():
    org_id = input("Enter Organization ID: ")  # prompt user for organization ID
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("""
            SELECT m.student_number, m.first_name, m.last_name, ms.member_role, ms.membership_status, 
                   m.gender, m.degree_program, m.batch_year, ms.committee
            FROM member m
            JOIN membership ms ON m.student_number = ms.student_number
            JOIN organization o ON ms.organization_id = o.organization_id
            WHERE o.organization_id = ?
            ORDER BY ms.member_role, m.last_name
        """, (org_id,))  # execute the query with the organization ID
        
        rows = cursor.fetchall()  # fetch all member records
        
        if rows:  # if members are found
            print(f"\n--- MEMBERS OF ORGANIZATION {org_id} ---")  # print header for organization members
            print(f"{'Student#':<12} {'Name':<25} {'Role':<15} {'Status':<12} {'Gender':<8} {'Program':<20} {'Batch':<6} {'Committee':<15}")  # print column headers
            print("-" * 125)  # print separator line
            for row in rows:  # loop through each member record
                student_number = row[0] or 'N/A'
                name = f"{row[1] or ''} {row[2] or ''}".strip() or 'N/A'
                role = row[3] or 'N/A'
                status = row[4] or 'N/A'
                gender = row[5] or 'N/A'
                program = row[6] or 'N/A'
                batch = row[7] or 'N/A'
                committee = row[8] or 'N/A'
                # Print results
                print(f"{student_number:<12} {name:<25} {role:<15} {status:<12} {gender:<8} {program:<20} {batch:<6} {committee:<15}")
        else:
            print("No members found for this organization.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during member retrieval
        print(f"Error fetching members: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# function to view executive committee members
def view_executive_members():
    org_id = input("Enter Organization ID: ")  # prompt user for organization ID
    academic_year = input("Enter Academic Year (e.g., 2024-2025): ")  # prompt user for academic year
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("""
            SELECT m.student_number, m.first_name, m.last_name, ms.member_role, ms.committee, ms.semester
            FROM member m
            JOIN membership ms ON m.student_number = ms.student_number
            WHERE ms.organization_id = ? 
                AND ms.academic_year = ?
                AND ms.committee = 'Executive'
            ORDER BY 
                CASE ms.member_role
                    WHEN 'President' THEN 1
                    WHEN 'Vice President' THEN 2
                    WHEN 'Secretary' THEN 3
                    WHEN 'Treasurer' THEN 4
                    ELSE 5
                END, 
                ms.semester,
                m.last_name
        """, (org_id, academic_year))  # execute the query with the organization ID and academic year
        
        rows = cursor.fetchall()  # fetch all executive member records
        
        if rows:  # if executive members are found
            print(f"\n--- EXECUTIVE COMMITTEE - ORGANIZATION {org_id} ({academic_year}) ---")  # print header
            print(f"{'Student#':<12} {'Name':<25} {'Role':<20} {'Committee':<15} {'Semester':<15}")  # print column headers
            print("-" * 90)  # print separator line
            for row in rows:  # loop through each executive member record
                name = f"{row[1]} {row[2]}"  # concatenate first and last name
                print(f"{row[0]:<12} {name:<25} {row[3]:<20} {row[4]:<15} {row[5]:<15}")  # print executive member details
        else:  # if no executive members found
            print(f"No executive members found for organization {org_id} in academic year {academic_year}.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during executive member retrieval
        print(f"Error fetching executive members: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# function to view alumni members
def view_alumni_members():
    org_id = input("Enter Organization ID: ")  # prompt user for organization ID
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("""
            SELECT m.student_number, m.first_name, m.last_name, ms.member_role, 
                   ms.academic_year, m.batch_year, m.degree_program
            FROM member m
            JOIN membership ms ON m.student_number = ms.student_number
            WHERE ms.organization_id = ? AND ms.membership_status = 'alumni'
            ORDER BY m.batch_year, m.last_name
        """, (org_id,))  # execute the query with the organization ID
        
        rows = cursor.fetchall()  # fetch all alumni member records
        
        if rows:  # if alumni members are found
            print(f"\n--- ALUMNI MEMBERS - ORGANIZATION {org_id} ---")  # print header
            print(f"{'Student#':<12} {'Name':<25} {'Last Role':<15} {'Year Active':<12} {'Batch':<6} {'Program':<20}")  # print column headers
            print("-" * 95)  # print separator line
            for row in rows:  # loop through each alumni member record
                name = f"{row[1]} {row[2]}"  # concatenate first and last name
                print(f"{row[0]:<12} {name:<25} {row[3]:<15} {row[4]:<12} {row[5]:<6} {row[6]:<20}")  # print alumni member details
        else:  # if no alumni members found
            print("No alumni members found for this organization.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during alumni member retrieval
        print(f"Error fetching alumni members: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# function to view presidents history
def view_presidents_history():
    org_id = input("Enter Organization ID: ")  # prompt user for organization ID
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("""
            SELECT m.student_number, m.first_name, m.last_name, ms.academic_year, 
                   ms.semester, ms.membership_status
            FROM member m
            JOIN membership ms ON m.student_number = ms.student_number
            WHERE ms.organization_id = ? AND ms.member_role = 'President'
            ORDER BY ms.academic_year DESC, 
                     CASE ms.semester
                         WHEN '1st Semester' THEN 1
                         WHEN '2nd Semester' THEN 2
                         WHEN 'Midyear' THEN 3
                         ELSE 4
                     END DESC
        """, (org_id,))  # execute the query with the organization ID
        
        rows = cursor.fetchall()  # fetch all president records
        
        if rows:  # if presidents are found
            print(f"\n--- PRESIDENTS HISTORY - ORGANIZATION {org_id} (Current to Past) ---")  # print header
            print(f"{'Student#':<12} {'Name':<25} {'Academic Year':<15} {'Semester':<15} {'Status':<12}")  # print column headers
            print("-" * 85)  # print separator line
            for row in rows:  # loop through each president record
                name = f"{row[1]} {row[2]}"  # concatenate first and last name
                print(f"{row[0]:<12} {name:<25} {row[3]:<15} {row[4]:<15} {row[5]:<12}")  # print president details
        else:  # if no presidents found
            print("No presidents found for this organization.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during president retrieval
        print(f"Error fetching presidents: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# CRUD operations for members 

# helper functions for input validations using regex
def validate_student_number(sn):
    return re.fullmatch(r"\d{4}-\d{5}", sn)

def validate_batch_year(by):
    return re.fullmatch(r"\d{4}", by)

def prompt_nonempty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("This field is required.")

# Add member function
def add_member():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        while True:
            student_number = input("Student Number (XXXX-XXXXX): ").strip()
    
            if not validate_student_number(student_number):
                print("Invalid format. Please enter as XXXX-XXXXX.")
                continue  # Ask again
    
            # Check if student_number already exists
            cursor.execute("SELECT 1 FROM member WHERE student_number = ?", (student_number,))
            if cursor.fetchone():
                print("This student number already exists. Please use a different one.")
                continue  

            break
        
        # Get password from user
        password = getpass("Password: ")
        if not password:
            print("Password cannot be empty.")
            return

        # Get fields for member
        first_name = prompt_nonempty("First Name: ")
        middle_name = input("Middle Name (optional): ") or None
        last_name = prompt_nonempty("Last Name: ")
        degree_program = prompt_nonempty("Degree Program: ")

        gender = input("Gender (optional): ").strip().lower() or None

        # Initially get batch year input from student, extracts from student number is input is invalid for enhanced UX
        while True:
            batch_year = input("Batch Year (YYYY): ").strip()
            if validate_batch_year(batch_year):
                break
            else:
                # Extract the batch year from student number
                extracted_year = student_number.split('-')[0]
                if validate_batch_year(extracted_year):
                    print(f"Invalid input. Using batch year from student number: {extracted_year}")
                    batch_year = extracted_year
                    break
                else:
                    print("Invalid batch year and unable to extract from student number.")
        
        # Insert query for adding members
        cursor.execute("""
            INSERT INTO member (student_number, password, first_name, middle_name, last_name, degree_program, gender, batch_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_number, password, first_name, middle_name, last_name, degree_program, gender, batch_year))

        conn.commit()
        print("Member added successfully.")
    except mariadb.Error as e:
        print(f"Error adding member: {e}")
    finally:
        cursor.close()
        conn.close()

# Update function for member
def update_member():
    # Get and validate student numbers
    student_number = input("Enter Student Number to update (XXXX-XXXXX): ").strip()
    if not validate_student_number(student_number):
        print("Invalid student number format. Use XXXX-XXXXX.")
        return

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Query to check if student number exists
        cursor.execute("SELECT * FROM member WHERE student_number = ?", (student_number,))
        existing = cursor.fetchone()
        if not existing:
            print("Member not found.")
            return

        # Edit specific member fields, leave field as blank if user wish to keep existing details
        print("Leave fields blank to keep current value.")
        password = getpass("New Password: ") or existing[1]
        first_name = input("New First Name: ") or existing[2]
        middle_name = input("New Middle Name: ") or existing[3]
        last_name = input("New Last Name: ") or existing[4]
        degree_program = input("New Degree Program: ") or existing[5]
        gender = input("New Gender: ").strip().lower() or existing[6]
        batch_year = input("New Batch Year (YYYY): ") or existing[7]

        # If invalid batch year, updating is cancelled
        if not validate_batch_year(batch_year):
            print("Invalid batch year. Update canceled.")
            return

        # Query for updating member details
        cursor.execute("""
            UPDATE member
            SET password = ?, first_name = ?, middle_name = ?, last_name = ?, degree_program = ?, gender = ?, batch_year = ?
            WHERE student_number = ?
        """, (password, first_name, middle_name, last_name, degree_program, gender, batch_year, student_number))

        conn.commit()
        print("Member updated successfully.")
    except mariadb.Error as e:
        print(f"Error updating member: {e}")
    finally:
        cursor.close()
        conn.close()

# Delete function for member
def delete_member():

    # Query to check if student number exists
    student_number = input("Enter Student Number to update (XXXX-XXXXX): ").strip()
    if not validate_student_number(student_number):
        print("Invalid student number format. Use XXXX-XXXXX.")
        return

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check if student number input is valid
        if not validate_student_number(student_number):
            print("Invalid student number format.")
            return

        # Confirm to user if they wish to delete the specified member, case insensitive
        confirm = input(f"Are you sure you want to delete member {student_number}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion cancelled.")
            return

        # delete related records
        cursor.execute("DELETE FROM payment WHERE student_number = ?", (student_number,))
        cursor.execute("DELETE FROM fee WHERE student_number = ?", (student_number,))
        cursor.execute("DELETE FROM membership WHERE student_number = ?", (student_number,))
        cursor.execute("DELETE FROM member WHERE student_number = ?", (student_number,))

        conn.commit()
        print("Member and related records deleted successfully.")
    except mariadb.Error as e:
        print(f"Error deleting member: {e}")
    finally:
        cursor.close()
        conn.close()

# Search function for member
def search_member():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Search for a term e.g. a part of a student number, name, or degree program
        search_term = input("Enter student number, name, or degree program: ").strip()
        if not search_term:
            print("Search term cannot be empty.")
            return

        # Expression value for like operator
        like_term = f"%{search_term}%"

        # Uses like operator to filter and search through members given some details
        cursor.execute("""
            SELECT student_number, first_name, middle_name, last_name, degree_program, batch_year
            FROM member
            WHERE student_number LIKE ? OR
                  first_name LIKE ? OR
                  middle_name LIKE ? OR
                  last_name LIKE ? OR
                  degree_program LIKE ?
        """, (like_term, like_term, like_term, like_term, like_term))

        results = cursor.fetchall()
        
        # Print results if exists
        if results:
            print(f"\n{'Student #':<12} {'Name':<30} {'Degree Program':<25} {'Batch Year'}")
            print("-" * 75)
            for row in results:
                full_name = f"{row[1]} {row[2] or ''} {row[3]}"
                print(f"{row[0]:<12} {full_name:<30} {row[4]:<25} {row[5]}")
        else:
            print("No members found.")
    except mariadb.Error as e:
        print(f"Error searching members: {e}")
    finally:
        cursor.close()
        conn.close()

# function for adding membership
def add_membership():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Validate student_number
        while True:
            student_number = input("Student Number (XXXX-XXXXX): ").strip()
            if not validate_student_number(student_number):
                print("Invalid format. Use XXXX-XXXXX.")
                continue
            cursor.execute("SELECT 1 FROM member WHERE student_number = ?", (student_number,))
            if not cursor.fetchone():
                print("No member found with that student number.")
                continue
            break

        # Validate organization_id exists 
        while True:
            try:
                org_id = int(input("Organization ID: ").strip())
                cursor.execute("SELECT 1 FROM organization WHERE organization_id = ?", (org_id,))
                if not cursor.fetchone():
                    print("No organization found with that ID.")
                    continue
                break
            except ValueError:
                print("Organization ID must be an integer.")

        # Academic Year format check 
        while True:
            academic_year = input("Academic Year (e.g., 2024-2025): ").strip()
            if re.fullmatch(r"\d{4}-\d{4}", academic_year):
                break
            print("Invalid format. Use YYYY-YYYY.")

        # Semester validation
        valid_semesters = ['1st Semester', '2nd Semester', 'Midyear']
        while True:
            semester = input("Semester (1st Semester / 2nd Semester / Midyear): ").strip()
            if semester in valid_semesters:
                break
            print("Invalid semester. Choose from:", ', '.join(valid_semesters))

        # Check for duplicate using composite PK
        cursor.execute("""
            SELECT 1 FROM membership
            WHERE student_number = ? AND organization_id = ? AND academic_year = ? AND semester = ?
        """, (student_number, org_id, academic_year, semester))
        if cursor.fetchone():
            print("This membership already exists.")
            return

        # Other fields
        membership_status = prompt_nonempty("Membership Status: ").lower()
        member_role = input("Member Role (optional): ").strip() or None
        committee = input("Committee (optional): ").strip() or None

        # Insert into membership record
        cursor.execute("""
            INSERT INTO membership (
                student_number, organization_id, academic_year, semester,
                membership_status, member_role, committee
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_number, org_id, academic_year, semester, membership_status, member_role, committee))

        conn.commit()
        print("Membership added successfully.")

    except mariadb.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function, where given a time period in semesters, calculates the percentage of active vs inactive students during 
# that time period
def view_percentages():
    # Get organization id input
    print("\nView Percentage of Active vs Inactive Members")
    org_id = input("Enter Organization ID: ").strip()
    
    try:
        # Prompt user for the number of past semesters to include in computing the percentages
        semester_count = int(input("In the past how many semesters: ").strip())
    except ValueError:
        print("Invalid number entered for semester count.")
        return

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Subquery to get the most recent semesters given semester_count number of semesters
        # Ordered by academic year and semester
        cursor.execute("""
            SELECT academic_year, semester 
            FROM membership 
            WHERE organization_id = ?
            GROUP BY academic_year, semester
            ORDER BY academic_year DESC, 
                     CASE semester
                         WHEN '1st Semester' THEN 1
                         WHEN '2nd Semester' THEN 2
                         WHEN 'Midyear' THEN 3
                         ELSE 4
                     END
            LIMIT ?
        """, (org_id, semester_count))

        recent_terms = cursor.fetchall()
        if not recent_terms:
            print("No recent semester data found for this organization.")
            return

        # Create term keys to match using lists for filtering
        recent_keys = [(row[0], row[1]) for row in recent_terms]

        # Dynamically create WHERE clause conditions for each (year, semester)
        conditions = " OR ".join(["(academic_year = ? AND semester = ?)"] * len(recent_keys))
        values = []
        for key in recent_keys:
            values.extend(key)

        # Query to count membership statuses excluding 'alumni' and calculate percentages
        # Percentage is computed against total count within the specified terms
        cursor.execute(f"""
            SELECT membership_status,
                   COUNT(*) AS count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM membership 
                   WHERE organization_id = ? AND ({conditions}) AND membership_status != 'alumni'), 2) AS percentage
            FROM membership
            WHERE organization_id = ? AND ({conditions}) AND membership_status != 'alumni'
            GROUP BY membership_status
        """, [org_id] + values + [org_id] + values)

        rows = cursor.fetchall()
         # Display results
        if rows:
            print(f"\nActive vs Inactive Members for Organization {org_id} (last {semester_count} semesters):")
            print(f"{'Status':<20} {'Count':<10} {'Percentage':<10}")
            print("-" * 40)
            for row in rows:
                print(f"{row[0]:<20} {row[1]:<10} {row[2]:<10}%")
        else:
            print("No data found for the selected range.")
    
    # Handle errors
    except mariadb.Error as e:
        print(f"Error displaying active vs inactive percentage: {e}")
    finally:
        cursor.close()
        conn.close()

# function to serve as menu in managing members
def manage_members():
    while True:
        print("\n=== MEMBERS MANAGEMENT ===")
        print("[1] Add Member")
        print("[2] Edit Member")
        print("[3] Delete Member")
        print("[4] Search Member")
        print("[0] Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
             add_member()
        elif choice == '2':
            update_member()
        elif choice == '3':
            delete_member()
        elif choice == '4':
            search_member()
        elif choice == '0':
            return
        else:
            print("Invalid choice, please try again!")


def manage_fees():
    while True:
        print("\n--- FEES & PAYMENTS MANAGEMENT ---")
        print("FEE MANAGEMENT:")
        print(" 1. View Unpaid Fees by Organization")
        print(" 2. View Payment Summary")
        print(" 3. View Late Payments")
        print(" 4. View Member with Highest Debt")
        print(" 5. Add Fee")
        print(" 6. Edit Fee")
        print(" 7. Delete Fee")
        print(" 8. Search Fee")
        print(" 9. Add Payment")
        print("10. Edit Payment")
        print("11. Delete Payment")
        print("12. Search Payment")
        print("13. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == '1':
            view_unpaid_fees_by_org()
        elif choice == '2':
            view_payment_summary()
        elif choice == '3':
            view_late_payments()
        elif choice == '4':
            view_highest_debt_member()
        elif choice == '5':
            add_fee()
        elif choice == '6':
            edit_fee()
        elif choice == '7':
            delete_fee()
        elif choice == '8':
            search_fee()
        elif choice == '9':
            add_payment()
        elif choice == '10':
            edit_payment()
        elif choice == '11':
            delete_payment()
        elif choice == '12':
            search_payment()
        elif choice == '13':
            break
        else:
            print("Invalid choice. Please try again.")



# function to view unpaid fees by organization
def view_unpaid_fees_by_org():
    org_id = input("Enter Organization ID: ")  # prompt user for organization ID
    semester = input("Enter Semester (1st Semester/2nd Semester/Midyear): ")  # prompt user for semester
    academic_year = input("Enter Academic Year (e.g., 2024-2025): ")  # prompt user for academic year
    
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("""
            SELECT m.student_number, m.first_name, m.last_name, f.due_date, f.amount_due
            FROM member m
            JOIN membership ms ON m.student_number = ms.student_number
            JOIN organization o ON ms.organization_id = o.organization_id
            JOIN fee f ON f.student_number = ms.student_number AND f.organization_id = o.organization_id
            LEFT JOIN payment p ON 
                p.fee_reference_number = f.fee_reference_number 
                AND p.student_number = m.student_number 
                AND p.organization_id = o.organization_id 
            WHERE p.paid_date IS NULL 
            AND ms.academic_year = ? 
            AND f.semester = ?
            AND o.organization_id = ?
            ORDER BY f.due_date
        """, (academic_year, semester, org_id))  # execute the query with parameters
        
        rows = cursor.fetchall()  # fetch all unpaid fee records
        
        if rows:  # if unpaid fees exist
            print(f"\n--- UNPAID FEES FOR ORG {org_id} - {semester} {academic_year} ---")  # print header for unpaid fees
            print(f"{'Student#':<12} {'Name':<25} {'Due Date':<12} {'Amount':<10}")  # print column headers
            print("-" * 65)  # print separator line
            total_unpaid = 0  # initialize total unpaid amount
            for row in rows:  # loop through each unpaid fee record
                name = f"{row[1]} {row[2]}"  # concatenate first and last name
                due_date_str = row[3].strftime("%Y-%m-%d") if row[3] else "N/A"  # format due date
                print(f"{row[0]:<12} {name:<25} {due_date_str:<12} {row[4]:<10.2f}")  # print fee details
                total_unpaid += float(row[4])  # accumulate total unpaid amount
            print("-" * 65)  # print separator line
            print(f"{'TOTAL UNPAID:':<49} {total_unpaid:<10.2f}")  # print total unpaid amount
        else:  # if no unpaid fees found
            print("No unpaid fees found.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during unpaid fee retrieval
        print(f"Error fetching unpaid fees: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# function to view payment summary
def view_payment_summary():
    org_id = input("Enter Organization ID: ")  # prompt user for organization ID
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("""
            SELECT
                SUM(CASE WHEN p.payment_reference_number IS NULL THEN f.amount_due ELSE 0 END) AS total_unpaid,
                SUM(CASE WHEN p.payment_reference_number IS NOT NULL THEN p.amount_paid ELSE 0 END) AS total_paid
            FROM fee f
            LEFT JOIN payment p ON f.fee_reference_number = p.fee_reference_number 
                AND f.student_number = p.student_number 
                AND f.organization_id = p.organization_id
            WHERE f.organization_id = ?
        """, (org_id,))  # execute the query with the organization ID
        result = cursor.fetchone()  # fetch the result
        
        if result:  # if payment data is found
            total_unpaid = result[0] or 0  # get total unpaid amount or set to 0 if None
            total_paid = result[1] or 0  # get total paid amount or set to 0 if None
            print(f"\n--- PAYMENT SUMMARY FOR ORGANIZATION {org_id} ---")  # print header for payment summary
            print(f"Total Paid: {total_paid:.2f}")  # print total paid amount
            print(f"Total Unpaid: {total_unpaid:.2f}")  # print total unpaid amount
            print(f"Total Amount: {(total_paid + total_unpaid):.2f}")  # print total amount (paid + unpaid)
        else:  # if no payment data found
            print("No payment data found.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during payment summary retrieval
        print(f"Error fetching payment summary: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

def view_late_payments():
    org_id = input("Enter Organization ID: ")  # prompt user for organization ID
    semester = input("Enter Semester (1st Semester/2nd Semester/Midyear): ")  # prompt user for semester
    year = input("Enter Year (e.g., 2024): ")  # prompt user for year
    
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("""
            SELECT p.student_number, m.first_name, m.last_name, p.payment_reference_number, 
                   p.paid_date, f.due_date, DATEDIFF(p.paid_date, f.due_date) AS days_late
            FROM payment p
            JOIN fee f ON p.fee_reference_number = f.fee_reference_number 
                AND p.student_number = f.student_number 
                AND p.organization_id = f.organization_id
            JOIN member m ON p.student_number = m.student_number
            WHERE p.organization_id = ?
              AND f.semester = ?
              AND YEAR(f.due_date) = ?
              AND p.paid_date > f.due_date
            ORDER BY days_late DESC
        """, (org_id, semester, year))  # execute query with parameters
        
        rows = cursor.fetchall()  # fetch all late payment records
        
        if rows:  # if late payments exist
            print(f"\n--- LATE PAYMENTS - ORG {org_id} ({semester} {year}) ---")  # print header
            print(f"{'Student#':<12} {'Name':<25} {'Payment Ref':<15} {'Paid Date':<12} {'Due Date':<12} {'Days Late':<12}")  # print column headers
            print("-" * 100)  # print separator line
            for row in rows:  # loop through each late payment record
                name = f"{row[1]} {row[2]}"  # concatenate first and last name
                paid_date_str = row[4].strftime("%Y-%m-%d") if row[4] else "N/A"
                due_date_str = row[5].strftime("%Y-%m-%d") if row[5] else "N/A"
                print(f"{row[0]:<12} {name:<25} {row[3]:<15} {paid_date_str:<12} {due_date_str:<12} {row[6]:<12}")  # print late payment details
        else:  # if no late payments found
            print("No late payments found for the specified criteria.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during late payment retrieval
        print(f"Error fetching late payments: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

def view_highest_debt_member():
    org_id = input("Enter Organization ID: ")  # prompt user for organization ID
    semester = input("Enter Semester (1st Semester/2nd Semester/Midyear): ")  # prompt user for semester
    
    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object
    
    try:
        cursor.execute("""
            SELECT f.student_number, m.first_name, m.last_name, 
                   SUM(f.amount_due - IFNULL(p.amount_paid, 0)) AS total_debt
            FROM fee f
            LEFT JOIN payment p ON f.fee_reference_number = p.fee_reference_number 
                AND f.student_number = p.student_number 
                AND f.organization_id = p.organization_id
            JOIN member m ON f.student_number = m.student_number
            WHERE f.organization_id = ?
              AND f.semester = ?
            GROUP BY f.student_number
            HAVING total_debt > 0
            ORDER BY total_debt DESC
        """, (org_id, semester))  # execute query with organization ID and semester
        
        rows = cursor.fetchall()  # fetch debt records
        
        if rows:  # if debt records exist
            print(f"\n--- TOP 5 MEMBERS WITH HIGHEST DEBT - ORG {org_id} ({semester}) ---")  # print header
            print(f"{'Rank':<6} {'Student#':<12} {'Name':<25} {'Total Debt':<12}")  # print column headers
            print("-" * 60)  # print separator line
            for i, row in enumerate(rows, 1):  # loop through each debt record with rank
                name = f"{row[1]} {row[2]}"  # concatenate first and last name
                print(f"{i:<6} {row[0]:<12} {name:<25} {row[3]:<12.2f}")  # print debt details with rank
        else:  # if no debt found
            print("No outstanding debt found for this organization and semester.")  # inform user
            
    except mariadb.Error as e:  # handle any errors during debt retrieval
        print(f"Error fetching highest debt members: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection

# function to add a new fee
def add_fee():
    ref_no = input("Enter Fee Reference Number: ")  # prompt for fee reference number
    student_no = input("Enter Student Number: ")  # prompt for student number
    org_id = input("Enter Organization ID: ")  # prompt for organization ID
    semester = input("Enter Semester: ")  # prompt for semester
    amount_due = float(input("Enter Amount Due: "))  # prompt for amount due
    due_date = input("Enter Due Date (YYYY-MM-DD): ")  # prompt for due date

    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object

    try:
        cursor.execute("""
            INSERT INTO fee (fee_reference_number, student_number, organization_id, semester, amount_due, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ref_no, student_no, org_id, semester, amount_due, due_date))  # insert fee data into database

        conn.commit()  # save changes to the database
        print("Fee successfully added.")  # inform user of success
    except mariadb.Error as e:  # handle any errors during insert
        print(f"Error adding fee: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection


# function to edit an existing fee
def edit_fee():
    ref_no = input("Enter Fee Reference Number to Edit: ").strip()  # prompt user for fee reference number
    new_amount = float(input("Enter New Amount Due: "))  # prompt for new amount
    new_due_date = input("Enter New Due Date (YYYY-MM-DD): ")  # prompt for new due date

    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object

    try:
        # check if the fee exists first
        cursor.execute("SELECT 1 FROM fee WHERE fee_reference_number = ?", (ref_no,))
        if cursor.fetchone():  # if the fee exists
            cursor.execute("""
                UPDATE fee
                SET amount_due = ?, due_date = ?
                WHERE fee_reference_number = ?
            """, (new_amount, new_due_date, ref_no))  # update fee
            conn.commit()  # save changes to the database
            print("Fee successfully updated.")  # always show success if row exists
        else:
            print("Fee not found.")  # inform user if fee doesn't exist
    except mariadb.Error as e:  # handle any errors during update
        print(f"Error updating fee: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection


# function to delete a fee
def delete_fee():
    ref_no = input("Enter Fee Reference Number to Delete: ").strip()  # prompt user for fee reference number

    conn = create_connection()  # create a database connection
    cursor = conn.cursor()  # create a cursor object

    try:
        # check if the fee exists first
        cursor.execute("SELECT 1 FROM fee WHERE fee_reference_number = ?", (ref_no,))
        if cursor.fetchone():  # if the fee exists
            cursor.execute("""
                DELETE FROM fee
                WHERE fee_reference_number = ?
            """, (ref_no,))  # delete fee from the database
            conn.commit()  # save changes to the database
            print("Fee successfully deleted.")  # inform user of success
        else:
            print("Fee not found.")  # inform user if fee does not exist
    except mariadb.Error as e:  # handle any errors during delete
        print(f"Error deleting fee: {e}")  # print error message
    finally:
        cursor.close()  # close the cursor
        conn.close()  # close the database connection


def search_fee():
    keyword = input("Enter Student Number or Fee Reference Number to Search: ")  # search keyword

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT f.fee_reference_number, f.student_number, m.first_name, m.last_name, 
                   f.organization_id, f.semester, f.amount_due, f.due_date
            FROM fee f
            JOIN member m ON f.student_number = m.student_number
            WHERE f.student_number = ? OR f.fee_reference_number = ?
        """, (keyword, keyword))  # search by student or ref number

        rows = cursor.fetchall()
        if rows:
            print(f"\n--- SEARCH RESULTS ---")
            print(f"{'Ref#':<8} {'Student#':<12} {'Name':<25} {'OrgID':<8} {'Semester':<15} {'Amount':<10} {'Due Date':<12}")
            print("-" * 90)
            for row in rows:
                name = f"{row[2]} {row[3]}"
                due_date_str = row[7].strftime("%Y-%m-%d") if row[7] else "N/A"
                print(f"{row[0]:<8} {row[1]:<12} {name:<25} {row[4]:<8} {row[5]:<15} {row[6]:<10.2f} {due_date_str:<12}")
        else:
            print("No matching fee records found.")
    except mariadb.Error as e:
        print(f"Error searching fees: {e}")
    finally:
        cursor.close()
        conn.close()

def add_payment():
    print("\n--- ADD PAYMENT ---")
    payment_ref = input("Enter Payment Reference Number: ")
    fee_ref = input("Enter Fee Reference Number: ")
    student_no = input("Enter Student Number: ")
    org_id = input("Enter Organization ID: ")
    amount_paid = float(input("Enter Amount Paid: "))
    paid_date = input("Enter Paid Date (YYYY-MM-DD): ")

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check if the fee exists and get the current amount_due
        cursor.execute("""
            SELECT amount_due FROM fee
            WHERE fee_reference_number = ? AND student_number = ? AND organization_id = ?
        """, (fee_ref, student_no, org_id))
        fee = cursor.fetchone()

        if not fee:
            print("Fee record not found. Please check the inputs.")
            return

        current_due = float(fee[0])
        if amount_paid > current_due:
            print(f"Cannot pay more than the due amount ({current_due:.2f}).")
            return

        # Optional: check if a payment already exists for this fee
        cursor.execute("""
            SELECT * FROM payment
            WHERE fee_reference_number = ? AND student_number = ? AND organization_id = ?
        """, (fee_ref, student_no, org_id))
        existing_payment = cursor.fetchone()

        if existing_payment:
            print("Payment for this fee already exists.")
            return

        # Insert payment record
        cursor.execute("""
            INSERT INTO payment (
                payment_reference_number, fee_reference_number, student_number,
                organization_id, amount_paid, paid_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (payment_ref, fee_ref, student_no, org_id, amount_paid, paid_date))

        # Update the fee's amount_due
        new_due = current_due - amount_paid
        cursor.execute("""
            UPDATE fee
            SET amount_due = ?
            WHERE fee_reference_number = ? AND student_number = ? AND organization_id = ?
        """, (new_due, fee_ref, student_no, org_id))

        conn.commit()
        print(f"Payment of {amount_paid:.2f} successfully recorded.")
        print(f"Remaining amount due: {new_due:.2f}")

    except mariadb.Error as e:
        print(f"Error adding payment: {e}")
    finally:
        cursor.close()
        conn.close()


def edit_payment():
    payment_ref = input("Enter Payment Reference Number to Edit: ").strip()
    new_amount = float(input("Enter New Amount Paid: "))
    new_paid_date = input("Enter New Paid Date (YYYY-MM-DD): ")

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check if payment exists
        cursor.execute("SELECT 1 FROM payment WHERE payment_reference_number = ?", (payment_ref,))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE payment
                SET amount_paid = ?, paid_date = ?
                WHERE payment_reference_number = ?
            """, (new_amount, new_paid_date, payment_ref))
            conn.commit()
            print("Payment successfully updated.")
        else:
            print("Payment not found.")
    except mariadb.Error as e:
        print(f"Error updating payment: {e}")
    finally:
        cursor.close()
        conn.close()

def delete_payment():
    payment_ref = input("Enter Payment Reference Number to Delete: ").strip()

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check if payment exists
        cursor.execute("SELECT 1 FROM payment WHERE payment_reference_number = ?", (payment_ref,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM payment WHERE payment_reference_number = ?", (payment_ref,))
            conn.commit()
            print("Payment successfully deleted.")
        else:
            print("Payment not found.")
    except mariadb.Error as e:
        print(f"Error deleting payment: {e}")
    finally:
        cursor.close()
        conn.close()

def search_payment():
    keyword = input("Enter Student Number or Payment Reference Number to Search: ").strip()

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT p.payment_reference_number, p.student_number, m.first_name, m.last_name, 
                   p.organization_id, p.amount_paid, p.paid_date, p.fee_reference_number
            FROM payment p
            JOIN member m ON p.student_number = m.student_number
            WHERE p.student_number = ? OR p.payment_reference_number = ?
        """, (keyword, keyword))

        rows = cursor.fetchall()
        if rows:
            print(f"\n--- SEARCH RESULTS ---")
            print(f"{'PayRef#':<10} {'Student#':<12} {'Name':<25} {'OrgID':<8} {'Amount':<10} {'Paid Date':<12} {'Fee Ref#':<10}")
            print("-" * 90)
            for row in rows:
                name = f"{row[2]} {row[3]}"
                paid_date_str = row[6].strftime("%Y-%m-%d") if row[6] else "N/A"
                print(f"{row[0]:<10} {row[1]:<12} {name:<25} {row[4]:<8} {row[5]:<10.2f} {paid_date_str:<12} {row[7]:<10}")
        else:
            print("No matching payment records found.")
    except mariadb.Error as e:
        print(f"Error searching payments: {e}")
    finally:
        cursor.close()
        conn.close()

# function for the main menu
def main_menu(student_number):
    while True:
        print("\n=== MAIN MENU ===")
        print("\n=== PROFILE ===")
        print("[1] View Your Profile")
        print("[2] View Your Organizations")
        print("[3] View Your Unpaid Fees")
        print("[4] Change Your Password")
        print("\n=== MANAGEMENT ===")
        print("[5] Membership Management")
        print("[6] Fees Management")
        print("[7] Members Management")
        print("\n=== SIGN OUT ===")
        print("[8] Logout")  
        print("[0] Exit")   
        choice = input("Choose an option: ")

        if choice == '1':
            view_profile(student_number)
        elif choice == '2':
            view_organizations(student_number)
        elif choice == '3':
            view_fees(student_number)
        elif choice == '4':
            change_password(student_number) 
        elif choice == '5':
            manage_membership(student_number) 
        elif choice == '6':
            manage_fees() 
        elif choice == '7':
            manage_members()
        elif choice == '8':  
            print("Logging out...")
            main()  
        elif choice == '0':  
            print("Goodbye!")
            sys.exit(0)  
        else:
            print("Invalid choice. Please try again.")

def main():
    print("=== STUDENT ORGANIZATION PORTAL ===")
    student_number = login()
    if student_number:
        main_menu(student_number)

if __name__ == "__main__":
    main()
