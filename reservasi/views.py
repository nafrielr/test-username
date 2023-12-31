from django.shortcuts import render, redirect, HttpResponse
from utils.query import query

def reservasi(request):
    return render(request, "form_reservasi.html")

def show_reservasi_kamar(request, custemail = 'Eduardo_Greenwood7181@1kmd3.site'):
    data = query(f""" 
                SELECT rr.rsv_id, rr.rNum, rr.Datetime, rr.isActive
                FROM reservation r
                JOIN reservation_room rr ON r.rID = rr.rsv_id
                WHERE r.cust_email = '{custemail}'
                """)
    context = {
        "data" : data,
    }
    return render(request, "daftar_reservasi_kamar.html",context)

def detail_reservasi(request, rsv_id):
    # Retrieve the details of the reservation for the specified rsv_id
    data = query(f"""
                SELECT rsv_id, rNum, rHotelName, rHotelBranch, Datetime, isActive
                FROM RESERVATION_ROOM
                WHERE rsv_id = '{rsv_id}';
            """)
    if not data:
        return HttpResponse("Reservation not found", status=404)

    return render(request, 'detail_reservasi.html', {'data': data[0]})

def show_shuttle_reserve(request):
    return render(request, "shuttle_reserve.html")


def cancel_reservasi(request, rsv_id):
    query(f"""
        UPDATE reservation
        SET status = 6
        WHERE rsv_id = '{rsv_id}';
    """)

    return redirect('daftar_reservasi_kamar')


def complaint_page(request, rsv_id):
    # custemail = 'Eduardo_Greenwood7181@1kmd3.site'
    res = query(f""" 
                SELECT rr.rsv_id, rr.rhotelname, rr.rhotelbranch, r.cust_email
                FROM reservation r
                JOIN reservation_room rr ON r.rID = rr.rsv_id
                WHERE rr.rsv_id = '{rsv_id}'
                """)
    
    # res2 = query(f""" 
    #             SELECT * FROM user WHERE email = '{custemail}'
    #             """)

    context = {
            'data': {
                'id': res[0][0],
                'email': res[0][3],
                'hotel_name': res[0][1],
                'hotel_branch': res[0][2]
            }
        }
    print(context)
    return render(request, "complaint.html", context)

def save_complaint(request):
    if request.method == 'POST':

        rsv_id = request.POST.get('id')
        complaint_message = request.POST.get('complain')
        hotel_name = request.POST.get('hotel_name')
        hotel_branch = request.POST.get('hotel_branch')
        email = request.POST.get('email')
        name = request.POST.get('name')

        try:
            latest_complaint_id = query(f"""
                SELECT id FROM "complaints" ORDER BY id::int DESC LIMIT 1
                """)
            
            new_id = str(int(latest_complaint_id[0][0]) + 1)

            insert = query(f"""
                INSERT INTO complaints
                (id, cust_email, rv_id, complaint)
                VALUES ('{new_id}', '{email}', '{rsv_id}', '{complaint_message}')
            """)

            print(insert)

            return redirect('daftar_reservasi_kamar')

        except Exception as e:
            print("error:", e)
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return HttpResponse("Invalid request method")