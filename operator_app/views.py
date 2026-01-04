import os
import pandas as pd
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE_DIR, 'data', 'operator_data.xlsx')


# -------------------
# Operator Form
# -------------------
def operator_form(request):
    if request.method == 'POST':
        new_data = {
            "EMP ID": request.POST.get('emp_id'),
            "NAME": request.POST.get('name'),
            "SHIFT": request.POST.get('shift'),
            "DOJ": request.POST.get('doj'),
            "DOL": request.POST.get('dol'),
            "ST-10": request.POST.get('st10'),
            "ST-15": request.POST.get('st15'),
            "ST-20": request.POST.get('st20'),
            "ST-25": request.POST.get('st25'),
            "ST-30": request.POST.get('st30'),
            "ST-40": request.POST.get('st40'),
            "REMARK": request.POST.get('remark'),
        }

        df = pd.read_excel(EXCEL_PATH)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_excel(EXCEL_PATH, index=False)

        return redirect('dashboard')

    return render(request, 'operator_form.html')


# -------------------
# Custom Admin Login
# -------------------
def admin_login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get('admin_id')
        password = request.POST.get('admin_pass')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')  # redirect to editable dashboard
        else:
            error = "Invalid credentials or not an admin!"
    return render(request, 'admin_login.html', {'error': error})


# -------------------
# Dashboard
# -------------------
def dashboard(request):
    df = pd.read_excel(EXCEL_PATH)
    total_manpower = len(df)

    search_query = request.GET.get('search', '').strip()
    filtered_df = df.copy()

    if search_query:
        filtered_df = filtered_df[
            filtered_df['EMP ID'].astype(str).str.contains(search_query, case=False, na=False) |
            filtered_df['NAME'].astype(str).str.contains(search_query, case=False, na=False)
        ]

    filtered_df.insert(0, 'SR_NO', range(1, len(filtered_df) + 1))

    filtered_df = filtered_df.rename(columns={
        "EMP ID": "EMP_ID",
        "ST-10": "ST10",
        "ST-15": "ST15",
        "ST-20": "ST20",
        "ST-25": "ST25",
        "ST-30": "ST30",
        "ST-40": "ST40",
    })

    records = filtered_df.to_dict(orient='records')

    return render(request, 'dashboard.html', {
        'records': records,
        'total_manpower': total_manpower,
        'search_query': search_query,
        'is_admin': request.user.is_authenticated and request.user.is_staff
    })


# -------------------
# Edit Operator (Admin Only)
# -------------------
@login_required
def edit_operator(request, row_index):
    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    df = pd.read_excel(EXCEL_PATH)

    if request.method == "POST":
        df.loc[row_index, 'NAME'] = request.POST.get('name')
        df.loc[row_index, 'SHIFT'] = request.POST.get('shift')
        df.loc[row_index, 'ST-10'] = request.POST.get('st10')
        df.loc[row_index, 'ST-15'] = request.POST.get('st15')
        df.loc[row_index, 'ST-20'] = request.POST.get('st20')
        df.loc[row_index, 'ST-25'] = request.POST.get('st25')
        df.loc[row_index, 'ST-30'] = request.POST.get('st30')
        df.loc[row_index, 'ST-40'] = request.POST.get('st40')
        df.loc[row_index, 'REMARK'] = request.POST.get('remark')

        df.to_excel(EXCEL_PATH, index=False)
        return redirect('dashboard')

    row = df.loc[row_index].to_dict()
    return render(request, 'edit_operator.html', {'row': row})


# -------------------
# Logout
# -------------------
@login_required
def admin_logout(request):
    logout(request)
    return redirect('dashboard')


# -------------------
# Download Excel (Admin Only)
# -------------------
@login_required
def download_operator_excel(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")
    return FileResponse(open(EXCEL_PATH, 'rb'),
                        as_attachment=True,
                        filename='operator_data.xlsx')
