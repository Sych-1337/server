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
async def get_offer(app_name: str, request: Request, user_id: str, campaign: str):
    url = await get_offer_url(user_id, campaign, app_name)
    if url:
        return {"status": "ok", "url": url}
    else:
        return {"status": "game"}


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

@app.get("/analytics/{app_name}/view", response_class=HTMLResponse)
async def view_analytics(app_name: str):
    data = load_analytics()
    records = data.get(app_name, [])

    if not records:
        return f"<h2>No analytics for app: {app_name}</h2>"

    headers = list(records[0].keys())

    html_template = """
    <html>
        <head>
            <title>Analytics for {{ app_name }}</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ccc;
                    padding: 6px 12px;
                    font-size: 14px;
                }
                th {
                    background: #f5f5f5;
                }
                body {
                    font-family: sans-serif;
                    padding: 20px;
                }
            </style>
        </head>
        <body>
            <h2>Analytics for {{ app_name }}</h2>
            <table>
                <tr>
                    {% for h in headers %}
                        <th>{{ h }}</th>
                    {% endfor %}
                </tr>
                {% for row in records %}
                    <tr>
                        {% for h in headers %}
                            <td>{{ row.get(h, "") }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    """
    html = Template(html_template).render(app_name=app_name, records=records, headers=headers)
    return HTMLResponse(content=html)
