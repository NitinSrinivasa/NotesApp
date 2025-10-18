import requests

BASE_URL = "http://127.0.0.1:8000"

def get_user_id_by_username(username):
    response = requests.get(f"{BASE_URL}/users/by-username/{username}")
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print("❌ User not found.")
        return None

def get_notes_for_user(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}/notes/")
    if response.status_code == 200:
        notes = response.json()
        print(notes)
        if not notes:
            print("No notes found.")
        for note in notes:
            print(f"\n📝 {note['title']}\n{note['content']}")
    else:
        print("❌ Failed to fetch notes.")

def main():
    username = input("Enter username: ").strip()
    user_id = get_user_id_by_username(username)
    if user_id:
        get_notes_for_user(user_id)

if __name__ == "__main__":
    main()
