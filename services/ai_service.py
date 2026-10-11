# Service tích hợp Trí tuệ nhân tạo (tóm tắt tài liệu, trích xuất ý chính, hỏi đáp Q&A)
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=key)



def call_openai(content: str, type: str, ques: str):

    prompts = [
        [{
            "role": "system", 
            "content": """Bạn là trợ lý phân tích văn bản. Hãy đọc tài liệu và trả về kết quả ĐÚNG định dạng JSON sau:
            {
                "summary": "Đoạn văn tóm tắt nội dung chính",
                "key_takeaways": ["Ý chính 1", "Ý chính 2", "Ý chính 3"]
            }"""},
        {"role": "user", "content": f"Nội dung tài liệu:\n{content}"}
        ],
        [{
            "role": "system",
            "content": (
                "Bạn là trợ lý phân tích tài liệu thông minh và khách quan. "
                "Nhiệm vụ của bạn là trả lời câu hỏi của người dùng CHỈ DỰA TRÊN "
                "nội dung tài liệu được cung cấp.\n\n"
                "QUY TẮC:\n"
                "1. Tuyệt đối không tự suy diễn hoặc bịa đặt thông tin ngoài tài liệu.\n"
                "2. Nếu tài liệu không chứa câu trả lời, hãy trả lời chính xác: "
                "'Thông tin này không được đề cập trong tài liệu được cung cấp.'\n"
                "3. Trả lời ngắn gọn, rõ ràng bằng tiếng Việt."
            )},
            {
            "role": "user",
            "content": (
                f"--- NỘI DUNG TÀI LIỆU ---\n"
                f"{content}\n"
                f"-------------------------\n\n"
                f"CÂU HỎI: {ques}"
            )}
        ]

    ]
    prompt = ""

    if type == "init":
        prompt = prompts[0]
    elif type == "ask":
        prompt = prompts[1]


    if type == "init":
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type":"json_object"},
            messages=prompt
        )

        result = response.choices[0].message.content
        return json.loads(result)
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt
        )
        return response.choices[0].message.content