from dotenv import load_dotenv
import google.genai as genai
import json
import os

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY_1'))

res = client.models.generate_content(
    model='gemini-2.5-flash-lite',
    contents='Hello'
)

print(f'Text: {res.text}')
# Text: Hello! How can I help you today?

print(f'Candidates: {res.candidates}')
# Candidates: [Candidate(
#   content=Content(
#     parts=[
#       Part(
#         text='Hello! How can I help you today?'
#       ),
#     ],
#     role='model'
#   ),
#   finish_reason=<FinishReason.STOP: 'STOP'>,
#   index=0
# )]

print(f'Candidate Content 0: {res.candidates[0].content}')
# Candidate Content 0: parts=[Part(
#   text='Hello! How can I help you today?'
# )] role='model'

print(f'Usage data: {res.usage_metadata}')
# Usage data: cache_tokens_details=None cached_content_token_count=None candidates_token_count=9 candidates_tokens_details=None prompt_token_count=2 prompt_tokens_details=[ModalityTokenCount(
#   modality=<MediaModality.TEXT: 'TEXT'>,
#   token_count=2
# )] thoughts_token_count=26 tool_use_prompt_token_count=None tool_use_prompt_tokens_details=None total_token_count=37 traffic_type=None

print(f'JSON: {json.dumps(res.model_dump(), indent=2)}')
# JSON: {
#   "sdk_http_response": {
#     "headers": {
#       "x-gemini-service-tier": "standard",
#       "content-type": "application/json; charset=UTF-8",
#       "vary": "Origin, X-Origin, Referer",
#       "content-encoding": "gzip",
#       "date": "Sun, 26 Apr 2026 06:06:50 GMT",
#       "server": "scaffolding on HTTPServer2",
#       "x-xss-protection": "0",
#       "x-frame-options": "SAMEORIGIN",
#       "x-content-type-options": "nosniff",
#       "server-timing": "gfet4t7; dur=1105",
#       "alt-svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",
#       "transfer-encoding": "chunked"
#     },
#     "body": null
#   },
#   "candidates": [
#     {
#       "content": {
#         "parts": [
#           {
#             "media_resolution": null,
#             "code_execution_result": null,
#             "executable_code": null,
#             "file_data": null,
#             "function_call": null,
#             "function_response": null,
#             "inline_data": null,
#             "text": "Hello! How can I help you today?",
#             "thought": null,
#             "thought_signature": null,
#             "video_metadata": null,
#             "tool_call": null,
#             "tool_response": null,
#             "part_metadata": null
#           }
#         ],
#         "role": "model"
#       },
#       "citation_metadata": null,
#       "finish_message": null,
#       "token_count": null,
#       "finish_reason": "STOP",
#       "grounding_metadata": null,
#       "avg_logprobs": null,
#       "index": 0,
#       "logprobs_result": null,
#       "safety_ratings": null,
#       "url_context_metadata": null
#     }
#   ],
#   "create_time": null,
#   "model_version": "gemini-2.5-flash-lite",
#   "prompt_feedback": null,
#   "response_id": "eavtabmJHZDKjuMPlomokAs",
#   "usage_metadata": {
#     "cache_tokens_details": null,
#     "cached_content_token_count": null,
#     "candidates_token_count": 9,
#     "candidates_tokens_details": null,
#     "prompt_token_count": 2,
#     "prompt_tokens_details": [
#       {
#         "modality": "TEXT",
#         "token_count": 2
#       }
#     ],
#     "thoughts_token_count": 41,
#     "tool_use_prompt_token_count": null,
#     "tool_use_prompt_tokens_details": null,
#     "total_token_count": 52,
#     "traffic_type": null
#   },
#   "model_status": null,
#   "automatic_function_calling_history": [],
#   "parsed": null
# }

clean = {
    "text": res.text,
    "tokens": res.usage_metadata.total_token_count,
    "model": res.model_version
}

print(f'Clean format: {json.dumps(clean, indent=2)}')
# Clean format: {
#   "text": "Hello there! How can I help you today?",
#   "tokens": 34,
#   "model": "gemini-2.5-flash-lite"
# }
