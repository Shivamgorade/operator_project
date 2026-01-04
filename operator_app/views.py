import os
import pandas as pd
from django.shortcuts import render, redirect
from django.http import FileResponse


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE_DIR, 'data', 'operator_data.xlsx')


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


def dashboard(request):
    df = pd.read_excel(EXCEL_PATH)

    # ✅ TOTAL MANPOWER = total entries in Excel (DO NOT FILTER)
    total_manpower = len(df)

    # -------------------------
    # SEARCH LOGIC
    # -------------------------
    search_query = request.GET.get('search', '').strip()

    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df['EMP ID'].astype(str).str.contains(search_query, case=False, na=False) |
            filtered_df['NAME'].astype(str).str.contains(search_query, case=False, na=False)
        ]

    # -------------------------
    # ADD SR NO (AFTER SEARCH)
    # -------------------------
    filtered_df.insert(0, 'SR_NO', range(1, len(filtered_df) + 1))

    # -------------------------
    # RENAME COLUMNS FOR TEMPLATE
    # -------------------------
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
        'search_query': search_query
    })
def download_operator_excel(request):
    return FileResponse(
        open(EXCEL_PATH, 'rb'),
        as_attachment=True,
        filename='operator_data.xlsx'
    )
