import sys
from faqChatBot import FaqChatBot


def run():
    inputs = {
        "user_query": "How does Matrix work in the calculator?",
    }
    FaqChatBot().faqChatBotCrew().kickoff(inputs=inputs)


if __name__ == "__main__":

    try:

        print("********************************************")
        print("Crew is running.....")
        print("Crew is fetching the source...")
        print("********************************************")

        run()

    except Exception as err:
        sys.exit(f"Sorry the crew cannot run, it it encountered: {err}")
    