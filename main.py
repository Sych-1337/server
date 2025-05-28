from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
import httpx
from keitaro import get_offer_url
from config import APP_CONFIG
from analytics import store_postback, load_analytics
from jinja2 import Template

app = FastAPI()

@app.get("/kb")
async def get_offer_legacy(request: Request, user_id: str, campaign: str = "kotlinTest"):
    # Legacy endpoint for current production app
    client_ip = request.headers.get("x-forwarded-for", request.client.host)
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Mobile)",
        "X-Forwarded-For": client_ip
    }

    keitaro_url = "https://firtsoneballs.xyz/XD2gBKJv"
    try:
        async with httpx.AsyncClient(follow_redirects=False) as client:
            response = await client.get(
                keitaro_url,
                params={"sub_id": user_id, "campaign": campaign},
                headers=headers
            )
            if "location" in response.headers:
                return {"status": "ok", "url": response.headers["location"]}
            else:
                return {"status": "game"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/{app_name}/kb")
async def get_offer(
    app_name: str,
    request: Request,
    user_id: str,
    campaign: str,
    ua: str = "Mozilla/5.0 (Linux; Android 11; Mobile)"
):
    client_ip = request.headers.get("x-forwarded-for", request.client.host)
    headers = {
        "User-Agent": ua,
        "X-Forwarded-For": client_ip
    }

    app_conf = APP_CONFIG.get(app_name)
    if not app_conf:
        print(f"[ERROR] Unknown app: {app_name}")
        return {"status": "game"}

    keitaro_url = app_conf.get("keitaro_url")
    if not keitaro_url:
        print(f"[ERROR] No keitaro_url for: {app_name}")
        return {"status": "game"}

    try:
        async with httpx.AsyncClient(follow_redirects=False) as client:
            response = await client.get(
                keitaro_url,
                params={"sub_id": user_id, "campaign": campaign},
                headers=headers
            )

        print(f"\n[KEITARO] → GET {keitaro_url}?sub_id={user_id}&campaign={campaign}")
        print("[STATUS]", response.status_code)
        print("[HEADERS]", dict(response.headers))
        print("[BODY]", response.text[:500])

        offer_url = response.headers.get("location")  # <- безопасный способ
        if offer_url:
            return {"status": "ok", "url": offer_url}
        else:
            return {"status": "game"}

    except Exception as e:
        print("[ERROR] Exception while contacting Keitaro:", e)
        return {"status": "error", "message": str(e)}


@app.get("/postback")
async def postback_handler(request: Request):
    params = dict(request.query_params)
    app_name = params.get("app")
    if not app_name:
        return {"status": "error", "message": "Missing 'app'"}
    store_postback(app_name, params)
    return {"status": "received", "app": app_name}

@app.get("/analytics/{app_name}")
async def get_analytics(app_name: str):
    data = load_analytics()
    if app_name not in data:
        return {"status": "error", "message": "No data for app"}
    return {"status": "ok", "data": data[app_name]}

@app.get("/analytics/dashboard", response_class=HTMLResponse)
async def analytics_dashboard():
    data = load_analytics()
    
    # Собираем уникальные ключи (заголовки таблицы)
    headers = set()
    for records in data.values():
        for rec in records:
            headers.update(rec.keys())
    headers = sorted(list(headers))

    # HTML-шаблон
    html_template = """
    <html>
        <head>
            <title>📊 Full Analytics Dashboard</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f7f9fa;
                }
                h1 {
                    margin-bottom: 20px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    table-layout: fixed;
                }
                th, td {
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: left;
                    font-size: 14px;
                    word-wrap: break-word;
                }
                th {
                    background-color: #eaeaea;
                }
                tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
                .app-name {
                    font-weight: bold;
                    color: #333;
                    background-color: #d6eaff;
                }
            </style>
        </head>
        <body>
            <h1>📊 Analytics Overview</h1>
            <table>
                <tr>
                    <th>App</th>
                    {% for h in headers %}
                        <th>{{ h }}</th>
                    {% endfor %}
                </tr>
                {% for app, entries in all_data.items() %}
                    {% for entry in entries %}
                        <tr>
                            <td class="app-name">{{ app }}</td>
                            {% for h in headers %}
                                <td>{{ entry.get(h, "") }}</td>
                            {% endfor %}
                        </tr>
                    {% endfor %}
                {% endfor %}
            </table>
        </body>
    </html>
    """

    html = Template(html_template).render(all_data=data, headers=headers)
    return HTMLResponse(content=html)
