class ErrorCode:
    """
    Centralized Error Code Catalog for HireMind AI.
    """

    # 1000 Series: File & Parsing Errors
    HM1001 = ("HM1001", "Resume text parsing failed. Ensure file is unencrypted and readable.")
    HM1002 = ("HM1002", "File size exceeds the maximum allowed upload limit.")
    HM1003 = ("HM1003", "Unsupported file extension or MIME type.")

    # 2000 Series: Auth & Security Errors
    HM2001 = ("HM2001", "Authentication failed. Invalid email/mobile or password.")
    HM2002 = ("HM2002", "Invalid, expired, or previously used password reset token.")
    HM2003 = ("HM2003", "Access token expired or malformed.")
    HM2004 = ("HM2004", "Rate limit exceeded. Please wait before retrying.")

    # 3000 Series: AI Engine & Vector Errors
    HM3001 = ("HM3001", "Centralized AI Evaluation Engine execution error.")
    HM3002 = ("HM3002", "FAISS Vector Store index retrieval failure.")
    HM3003 = ("HM3003", "RAG Prompt Builder or Answer Validator failure.")

    @classmethod
    def format_error(cls, error_tuple, custom_detail: str = None, request_id: str = "req-unknown") -> dict:
        code, default_msg = error_tuple
        return {"code": code, "message": custom_detail or default_msg, "request_id": request_id}
