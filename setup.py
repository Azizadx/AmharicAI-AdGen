import setuptools


__version__ = "0.0.1"

REPO_NAME = "AmharicAI-AdGen"
AUTHOR_USER_NAME = "azizadx"
SRC_REPO = "AmharicAI-AdGen"
AUTHOR_EMAIL = "craft@azizadx.me"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="The project centers on an Amharic RAG pipeline, leveraging robust AI for text manipulation. It aims to craft compelling Amharic text ads by analyzing campaign data, incorporating brand specifics, product details, and Telegram channel content history. ",
    # long_description='Redash LLM Chatbot: AI-powered Analytics &amp; Insights Unlock the power of your Redash dashboards and databases with natural language queries and automated insights.',
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "data_ingest"},
    packages=setuptools.find_packages(where="data_ingest")
)