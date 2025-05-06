import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CsvData
import random
import string
from .email_server import send_email, send_email_to_admin
import subprocess

# CSRF exemption for testing (for non-browser clients)
sudo_password = "guderian120"  



def generate_temp_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))



@csrf_exempt
def handle_csv_upload(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        error_lst = []
        csv_file = request.FILES['csv_file']

        # Read CSV using pandas
        try:
            # Load the CSV into a DataFrame
            df = pd.read_csv(csv_file)

            # Initialize a list to hold rows as dictionaries
            rows_data = []

            # Iterate through rows and append each row as a dictionary
            for index, row in df.iterrows():
                row_dict = row.to_dict()  # Convert the row to a dictionary
                rows_data.append(row_dict)

            # Return the rows data as a JSON response
            for data in rows_data:
                row = {key.strip(): value.strip() if isinstance(value, str) else value for key, value in data.items()}
                print(row, 'rowwwww')
                username = row.get('username', "")
                full_name = row.get('full_name', "").split(' ')
                department = row.get('department', "")
                email = row.get('email', "")
                temp_password = generate_temp_password()
                print(full_name)

                cmd = f"sudo -S useradd -m -G {department} -c {'-'.join(full_name)} {username}"
                cmd = cmd.split(' ')
                print(f"Running command: {cmd}")
                process = subprocess.Popen(
                        cmd,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )
                    # stdout, stderr = process.communicate(self.sudo_password + '\n')
                stdout, stderr = process.communicate(sudo_password + '\n')
                print('proces stage run', process.returncode)
                if process.returncode == 0:
                    print(f"Successfully created user {username} with passwword {temp_password}")

                        # 2. Set a temporary password
                    passwd_cmd = f"echo '{username}:{temp_password}' | sudo -S chpasswd"
                    passwd_process = subprocess.Popen(
                        passwd_cmd,
                        stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            universal_newlines=True
                    )
                    passwd_stdout, passwd_stderr = passwd_process.communicate(sudo_password + '\n')

                    if passwd_process.returncode != 0:
                        print(f"Error setting password for {username}: {passwd_stderr.strip()}")
                        error_lst.append(f"Error setting password for {username}: {passwd_stderr.strip()}\n")
                        # 3. Force password change on first login
                        continue

                        # 3. Force password change on first login
                    chage_cmd = f"sudo -S chage -d 0 {username}"
                    chage_process = subprocess.Popen(
                            chage_cmd.split(),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                    chage_stdout, chage_stderr = chage_process.communicate(sudo_password + '\n')

                    if chage_process.returncode != 0:
                        print(f"Error forcing password change: {chage_stderr.strip()}")
                        error_lst.append(f"Error forcing password change for {username}: {chage_stderr.strip()}\n")
                        continue

                        # 4. Send email with temporary password
                    if email:
                        print(f"Sending credentials to {email}...")
                        send_email(email," ".join(full_name), username, temp_password)

                        print(f"Successfully processed user {username}")
                else:
                    print(f"Error creating user {username}: {stderr.strip()}")
                    error_lst.append(f"Error creating user {username}: {stderr.strip()}\n")
                    continue  
            print(error_lst)
            return JsonResponse({"message": "CSV processed successfully!", "data": rows_data}) if not error_lst else JsonResponse({"error": "Errors occurred during processing", "details": error_lst}, status=400)
        

        except Exception as e:
            return JsonResponse({"error": f"Failed to read CSV: {str(e)}"}, status=400)

    return JsonResponse({"error": "No CSV file provided"}, status=400)