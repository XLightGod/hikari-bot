from fastapi import APIRouter, Request
import json

router = APIRouter()

@router.api_route("/tome", methods=["GET", "POST"])
async def tome_handler(request: Request):
    # 1) query 参数（GET 最常见）
    query = dict(request.query_params)

    # 2) headers（有些 forwarder 会带设备信息之类）
    headers = dict(request.headers)

    # 3) body（POST 时可能有）
    raw_body_bytes = await request.body()
    raw_body = raw_body_bytes.decode("utf-8", "ignore")

    # 4) 尝试解析 JSON（如果它是 application/json）
    json_body = None
    if raw_body:
        try:
            json_body = json.loads(raw_body)
        except Exception:
            json_body = None

    # 打印到日志（你看 journalctl / 控制台就能看到）
    print("\n===== /tome INCOMING =====")
    print("method:", request.method)
    print("url:", str(request.url))
    print("query:", query)
    print("content-type:", headers.get("content-type"))
    print("raw_body:", raw_body)
    print("json_body:", json_body)
    print("==========================\n")

    # 返回给 forwarder（让它别以为失败一直重试）
    return {
        "ok": True,
        "method": request.method,
        "query": query,
        "content_type": headers.get("content-type"),
        "raw_body": raw_body,
        "json_body": json_body,
    }