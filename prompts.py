from langchain.prompts import ChatPromptTemplate


product_prompt_string = """\
For the following text, extract the following information:

delivery_days: How many days did it take for the product \
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

customer_negative_feedback: Extract any problems customers are facing with the current product \
If this information is not found, output -1.

feature_requests: Extract any sentences about feature requests,\
and output them as a comma separated Python list.

competitor_mentions: Extract any sentences about the competition\
and output them as a comma separated Python list.


Format the output as JSON with the following keys:
delivery_days
price_value
customer_negative_feedback
feature_requests
competitor_mentions

text: {text}
"""

product_prompt_template = ChatPromptTemplate.from_template(product_prompt_string)
