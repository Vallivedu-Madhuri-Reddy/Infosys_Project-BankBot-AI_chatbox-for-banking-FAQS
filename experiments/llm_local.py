def grok_answer(user_query: str) -> str:
    """
    Local fallback LLM replacement
    NEVER fails
    """
    q = user_query.lower()

    if "data science" in q:
        return (
            "📊 Data Science is the field of analyzing data using "
            "statistics, programming, and machine learning to "
            "extract insights and support decision-making."
        )

    if "deep learning" in q:
        return (
            "🧠 Deep Learning is a subset of Machine Learning that "
            "uses multi-layer neural networks to learn complex "
            "patterns from large datasets."
        )

    return (
        "🤖 I can help with:\n"
        "• Balance enquiry\n"
        "• Money transfer\n"
        "• ATM location\n"
        "• Loan details\n"
        "• Card blocking\n"
        "• Basic tech questions"
    )
