import requests

def main():
    flume_url = "http://flume:12345"

    print("Enter your text (type 'exit' to quit):")
    while True:
        user_input = input()
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        try:
            response = requests.post(flume_url, data=user_input)
            if response.status_code == 200:
                print("Data sent to Flume successfully.")
            else:
                print(f"Failed to send data to Flume. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending data to Flume: {e}")

if __name__ == "__main__":
    main()
