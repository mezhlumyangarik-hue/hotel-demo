from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Սենյակների տվյալները
ROOMS_DATA = [
    {
        "id": "1",
        "name": "Royal Suite",
        "price": 80000,
        "description": "Շքեղ երկտեղանոց սենյակ՝ ջակուզիով և Երևանի համայնապատկերով։",
        "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800",
        "amenities_list": ["Ջակուզի", "Անվճար Wi-Fi", "Մինի բար", "King Size Մահճակալ"]
    },
    {
        "id": "2",
        "name": "Family Comfort",
        "price": 55000,
        "description": "Ընդարձակ սենյակ նախատեսված ընտանեկան հանգստի համար։",
        "image_url": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800",
        "amenities_list": ["Խոհանոց", "Պատշգամբ", "TV", "Անվճար Wi-Fi"]
    }
]

# Ամրագրումների պահոց
BOOKINGS = []

@app.route('/')
def index():
    return render_template('index.html', rooms=ROOMS_DATA)

# ԱԴՄԻՆԻ ԼՈԳԻՆ և ՇՔԵՂ ՎԱՀԱՆԱԿ
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            # Պատրաստում ենք աղյուսակի տողերը
            bookings_html = "".join([
                f"""
                <tr>
                    <td data-label="ID">#{b['id']}</td>
                    <td data-label="Հյուր"><i class="fa-solid fa-user" style="color: #38bdf8; margin-right: 8px;"></i>{b['guest_name']}</td>
                    <td data-label="Հեռախոս"><a href="tel:{b['phone']}" style="color: #94a3b8; text-decoration: none;"><i class="fa-solid fa-phone" style="color: #10b981; margin-right: 8px;"></i>{b['phone']}</a></td>
                    <td data-label="Սենյակ"><span class="room-badge">{b['room_name']}</span></td>
                    <td data-label="Մուտք"><i class="fa-regular fa-calendar-check" style="margin-right: 6px;"></i>{b['check_in']}</td>
                    <td data-label="Ելք"><i class="fa-regular fa-calendar-xmark" style="margin-right: 6px;"></i>{b['check_out']}</td>
                    <td data-label="Ժամ"><i class="fa-regular fa-clock" style="color: #fbbf24; margin-right: 6px;"></i>{b['time']}</td>
                </tr>
                """ for b in BOOKINGS
            ])

            return f'''
            <!DOCTYPE html>
            <html lang="hy">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Ադմին Վահանակ | Royal Ararat</title>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
                <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap" rel="stylesheet">
                <style>
                    :root {{
                        --bg-deep: #070a13;
                        --bg-card: #0f172a;
                        --cyan-glow: #38bdf8;
                        --text-light: #f8fafc;
                        --text-gray: #94a3b8;
                    }}
                    * {{
                        margin: 0; padding: 0; box-sizing: border-box;
                        font-family: 'Montserrat', sans-serif;
                    }}
                    body {{
                        background-color: var(--bg-deep);
                        color: var(--text-light);
                        padding: 40px 20px;
                        min-height: 100vh;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        animation: fadeIn 0.6s ease-out;
                    }}
                    header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 40px;
                        flex-wrap: wrap;
                        gap: 20px;
                    }}
                    h1 {{
                        font-size: 1.8rem;
                        font-weight: 800;
                        letter-spacing: 1px;
                        color: var(--text-light);
                    }}
                    h1 span {{
                        color: var(--cyan-glow);
                        text-shadow: 0 0 15px var(--cyan-glow);
                    }}
                    .logout-btn {{
                        background: rgba(239, 68, 68, 0.1);
                        border: 1px solid #ef4444;
                        color: #ef4444;
                        padding: 12px 24px;
                        text-decoration: none;
                        border-radius: 50px;
                        font-weight: bold;
                        font-size: 0.9rem;
                        transition: 0.3s;
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                    }}
                    .logout-btn:hover {{
                        background: #ef4444;
                        color: white;
                        box-shadow: 0 0 15px rgba(239, 68, 68, 0.4);
                    }}
                    .table-wrapper {{
                        background: var(--bg-card);
                        border: 1px solid rgba(56, 189, 248, 0.15);
                        border-radius: 20px;
                        overflow: hidden;
                        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    th, td {{
                        padding: 18px 24px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #111827;
                        color: var(--cyan-glow);
                        font-weight: 800;
                        text-transform: uppercase;
                        font-size: 0.8rem;
                        letter-spacing: 1.5px;
                        border-bottom: 1px solid rgba(56, 189, 248, 0.15);
                    }}
                    td {{
                        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
                        font-size: 0.95rem;
                        color: #e2e8f0;
                    }}
                    tr:hover td {{
                        background: rgba(56, 189, 248, 0.02);
                    }}
                    .room-badge {{
                        background: rgba(56, 189, 248, 0.1);
                        border: 1px solid var(--cyan-glow);
                        color: var(--cyan-glow);
                        padding: 6px 12px;
                        border-radius: 20px;
                        font-size: 0.8rem;
                        font-weight: bold;
                    }}
                    .no-data {{
                        text-align: center;
                        padding: 60px;
                        color: var(--text-gray);
                        font-style: italic;
                    }}
                    .no-data i {{
                        font-size: 3rem;
                        margin-bottom: 15px;
                        color: rgba(255,255,255,0.05);
                    }}
                    @media (max-width: 900px) {{
                        table, thead, tbody, th, td, tr {{
                            display: block;
                        }}
                        thead tr {{
                            position: absolute;
                            top: -9999px;
                            left: -9999px;
                        }}
                        tr {{
                            border: 1px solid rgba(56, 189, 248, 0.15);
                            border-radius: 15px;
                            margin-bottom: 20px;
                            padding: 10px;
                            background: rgba(15, 23, 42, 0.6);
                        }}
                        td {{
                            border: none;
                            position: relative;
                            padding-left: 50%;
                            text-align: right;
                            font-size: 0.9rem;
                        }}
                        td:before {{
                            position: absolute;
                            top: 50%;
                            left: 20px;
                            transform: translateY(-50%);
                            content: attr(data-label);
                            font-weight: bold;
                            color: var(--cyan-glow);
                            text-transform: uppercase;
                            font-size: 0.75rem;
                            letter-spacing: 1px;
                        }}
                    }}
                    @keyframes fadeIn {{
                        from {{ opacity: 0; transform: translateY(20px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <header>
                        <h1>ROYAL <span>ARARAT</span> — Ադմին Վահանակ</h1>
                        <a href="/login" class="logout-btn"><i class="fa-solid fa-right-from-bracket"></i> Դուրս Գալ</a>
                    </header>
                    
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Հյուր</th>
                                    <th>Հեռախոս</th>
                                    <th>Սենյակ</th>
                                    <th>Մուտքի Ամսաթիվ</th>
                                    <th>Ելքի Ամսաթիվ</th>
                                    <th>Ժամ</th>
                                </tr>
                            </thead>
                            <tbody>
                                {bookings_html if BOOKINGS else '<tr><td colspan="7" class="no-data"><i class="fa-solid fa-folder-open d-block"></i><br>Ամրագրումներ դեռ չկան։</td></tr>'}
                            </tbody>
                        </table>
                    </div>
                </div>
            </body>
            </html>
            '''
        else:
            error_message = "Սխալ Օգտանուն կամ Գաղտնաբառ:"

    return f'''
        <!DOCTYPE html>
        <html lang="hy">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin Login | Royal Ararat</title>
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap" rel="stylesheet">
            <style>
                body {{
                    background: #070a13;
                    color: white;
                    font-family: 'Montserrat', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    padding: 20px;
                }}
                .login-card {{
                    background: #0f172a;
                    padding: 40px;
                    border-radius: 24px;
                    border: 1px solid rgba(56, 189, 248, 0.2);
                    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
                    width: 100%;
                    max-width: 400px;
                }}
                h2 {{
                    color: #38bdf8;
                    text-align: center;
                    margin: 0 0 8px 0;
                    font-weight: 800;
                    letter-spacing: 1px;
                }}
                p.subtitle {{
                    text-align: center;
                    color: #94a3b8;
                    font-size: 0.85rem;
                    margin-bottom: 30px;
                }}
                form {{
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                }}
                input {{
                    padding: 14px 18px;
                    background: #070a13;
                    border: 1px solid rgba(255,255,255,0.08);
                    color: white;
                    border-radius: 12px;
                    outline: none;
                    font-size: 0.95rem;
                    transition: 0.3s;
                }}
                input:focus {{
                    border-color: #38bdf8;
                    box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
                }}
                button {{
                    padding: 15px;
                    background: linear-gradient(135deg, #0ea5e9, #38bdf8);
                    border: none;
                    color: #070a13;
                    font-weight: 800;
                    border-radius: 12px;
                    cursor: pointer;
                    transition: 0.3s;
                    letter-spacing: 1px;
                }}
                button:hover {{
                    box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
                    transform: translateY(-2px);
                }}
                .error {{
                    color: #ef4444;
                    text-align: center;
                    font-size: 0.85rem;
                    margin: 0;
                    background: rgba(239, 68, 68, 0.1);
                    padding: 10px;
                    border-radius: 8px;
                    border: 1px solid rgba(239, 68, 68, 0.2);
                }}
            </style>
        </head>
        <body>
            <div class="login-card">
                <h2>Ադմին Պորտալ</h2>
                <p class="subtitle">Մուտք գործեք համակարգը կառավարելու համար</p>
                <form method="POST">
                    {f'<p class="error">{error_message}</p>' if error_message else ''}
                    <input type="text" name="username" placeholder="Օգտանուն" required autocomplete="off">
                    <input type="password" name="password" placeholder="Գաղտնաբառ" required>
                    <button type="submit">ՄՈՒՏՔ ԳՈՐԾԵԼ</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/book-room', methods=['POST'])
def book_room():
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        guest_name = data.get('guest_name')
        phone = data.get('phone')
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        time = data.get('time')

        room = next((r for r in ROOMS_DATA if r["id"] == room_id), None)
        room_name = room["name"] if room else "Անհայտ Սենյակ"

        new_booking = {
            "id": len(BOOKINGS) + 1,
            "room_id": room_id,
            "room_name": room_name,
            "guest_name": guest_name,
            "phone": phone,
            "check_in": check_in,
            "check_out": check_out,
            "time": time
        }

        BOOKINGS.append(new_booking)
        return jsonify({"status": "success", "room_name": room_name})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)